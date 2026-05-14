"""CSI → Audio Transducer.

Bridges RuView WiFi CSI (Channel State Information) data into the numogram
audio pipeline. Takes per-subcarrier amplitude/phase data from ESP32 nodes
and produces audio spectrograms, WAV output, and MIR feature seeds for
mod-writer composition.

Three output paths:
  A) CSI spectrogram → ISTFT synthesis → WAV (room-as-instrument)
  B) CSI temporal spectrum → MIR features → AQ seed → mod-writer
  C) Vital-sign bands → LFO/modulation parameters (breathing/heartbeat)
"""

from __future__ import annotations

import json
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import scipy.fft
import scipy.signal

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CSIFrame:
    """Single CSI measurement from one ESP32 node."""
    timestamp_s: float
    rssi: float
    amplitude: np.ndarray  # shape: (n_antennas, n_subcarriers)
    phase: Optional[np.ndarray] = None  # same shape
    node_id: int = 1
    metadata: dict = field(default_factory=dict)

    @property
    def n_antennas(self) -> int:
        return self.amplitude.shape[0] if self.amplitude.ndim == 2 else 1

    @property
    def n_subcarriers(self) -> int:
        return self.amplitude.shape[-1]

    def mean_amplitude(self) -> np.ndarray:
        """Average across antennas → (n_subcarriers,)."""
        if self.amplitude.ndim == 1:
            return self.amplitude
        return self.amplitude.mean(axis=0)


@dataclass
class TransducerOutput:
    """Result of CSI→audio conversion."""
    # Path A: synthesised audio
    wav_samples: Optional[np.ndarray] = None
    sample_rate: int = 0
    # Path B: spectrogram for MIR pipeline
    spectrogram: Optional[np.ndarray] = None  # (freq_bins, time_frames)
    spec_freq_axis: Optional[np.ndarray] = None
    spec_time_axis: Optional[np.ndarray] = None
    # Path C: vital-sign derived modulation
    breathing_hz: float = 0.0       # dominant breathing frequency
    heartbeat_hz: float = 0.0       # dominant heart frequency
    breathing_band_power: float = 0.0
    heartbeat_band_power: float = 0.0
    motion_energy: float = 0.0
    presence_score: float = 0.0
    # MIR summary features
    centroid: float = 0.0           # spectral centroid of CSI spectrum
    rolloff: float = 0.0            # spectral rolloff
    flatness: float = 0.0           # spectral flatness
    mfcc: Optional[np.ndarray] = None
    seed_score: dict = field(default_factory=dict)

# ---------------------------------------------------------------------------
# CSI Frame parsers
# ---------------------------------------------------------------------------

def parse_json_frames(data: dict) -> List[CSIFrame]:
    """Parse the sample_csi_data.json format from RuView."""
    frames = []
    for f in data.get("frames", []):
        raw_amp = f["amplitude"]  # list of lists (antenna × subcarrier)
        if isinstance(raw_amp[0], list):
            amplitude = np.array(raw_amp, dtype=np.float64)
        else:
            amplitude = np.array([raw_amp], dtype=np.float64)
        phase = None
        if "phase" in f:
            raw_phase = f["phase"]
            if isinstance(raw_phase[0], list):
                phase = np.array(raw_phase, dtype=np.float64)
            else:
                phase = np.array([raw_phase], dtype=np.float64)
        frames.append(CSIFrame(
            timestamp_s=f.get("timestamp_s", 0.0),
            rssi=f.get("rssi", -80.0),
            amplitude=amplitude,
            phase=phase,
            node_id=f.get("node_id", 1),
            metadata=f,
        ))
    return frames


def parse_adr018_buffer(buf: bytes) -> CSIFrame:
    """Parse a single ADR-018 binary UDP frame from the ESP32 firmware.

    Header (20 bytes):
        magic(4) node_id(1) n_ant(1) n_sc(2) freq_mhz(4) seq(4) rssi(1) noise(1) rsvd(2)
    Payload: n_ant × n_sc × 2 bytes (I8, Q8 per subcarrier)
    """
    if len(buf) < 24:
        raise ValueError(f"Frame too short: {len(buf)} bytes")
    magic = struct.unpack_from("<I", buf, 0)[0]
    if magic != 0xC5110001:
        raise ValueError(f"Bad ADR-018 magic: 0x{magic:08X}")
    node_id = buf[4]
    n_ant = buf[5]
    n_sc = struct.unpack_from("<H", buf, 6)[0]
    rssi = struct.unpack_from("<b", buf, 16)[0]
    payload = buf[20:]
    expected = n_ant * n_sc * 2
    if len(payload) < expected:
        raise ValueError(f"Payload short: {len(payload)} < {expected}")

    iq = np.frombuffer(payload, dtype=np.int8, count=expected)
    iq = iq.reshape(n_ant, n_sc, 2)
    amplitude = np.sqrt(iq[..., 0].astype(np.float64) ** 2 +
                        iq[..., 1].astype(np.float64) ** 2)
    phase = np.arctan2(iq[..., 1].astype(np.float64),
                       iq[..., 0].astype(np.float64))

    # Reconstruct timestamp from seq+noise (best available without wall clock)
    seq = struct.unpack_from("<I", buf, 12)[0]

    return CSIFrame(
        timestamp_s=seq / 100.0,  # approximate, depends on frame rate
        rssi=float(rssi),
        amplitude=amplitude,
        phase=phase,
        node_id=node_id,
    )


# ---------------------------------------------------------------------------
# Amplitude matrix builder
# ---------------------------------------------------------------------------

def build_amplitude_matrix(frames: List[CSIFrame]) -> np.ndarray:
    """Stack mean amplitudes into (n_frames, n_subcarriers) matrix."""
    return np.array([f.mean_amplitude() for f in frames], dtype=np.float64)


# ---------------------------------------------------------------------------
# Path A: Spectrogram synthesis (room-as-instrument)
# ---------------------------------------------------------------------------

def csi_to_spectrogram(
    amp_matrix: np.ndarray,
    sampling_rate: float,
    window_size: int = 128,
    hop_size: int = 64,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute a 2D spectrogram from the CSI amplitude time-series.

    Each subcarrier column gets an STFT (Doppler decomposition), producing
    a (freq_bins × time_frames) power spectrogram. This is structurally
    identical to an audio spectrogram — just with different frequency units.

    Returns (spectrogram, freq_axis_hz, time_axis_s).
    """
    n_frames, n_sc = amp_matrix.shape
    n_freq = window_size // 2 + 1

    window = scipy.signal.windows.hann(window_size)
    spec = np.zeros((n_freq, n_sc), dtype=np.float64)

    for sc in range(n_sc):
        signal = amp_matrix[:, sc].copy()
        # Remove DC (room baseline)
        signal -= signal.mean()
        # Apply window
        if len(signal) >= window_size:
            signal = signal[:window_size] * window
            fft_bins = scipy.fft.rfft(signal)
            power = np.abs(fft_bins) ** 2
            n_out = min(n_freq, len(power))
            spec[:n_out, sc] = power[:n_out]
        elif len(signal) >= 4:
            # Pad for short signals
            padded = np.zeros(window_size)
            padded[:len(signal)] = signal * window[:len(signal)]
            fft_bins = scipy.fft.rfft(padded)
            power = np.abs(fft_bins) ** 2
            spec[:n_freq, sc] = power[:n_freq]

    # Frequency and time axes
    freq_axis = scipy.fft.rfftfreq(window_size, d=1.0 / sampling_rate)
    # Each column = one subcarrier; "time" axis is subcarrier index scaled
    time_axis = np.arange(n_sc) * (1.0 / n_sc * 20e6 / sampling_rate)  # approximate

    # Normalise to [0, 1]
    max_val = spec.max()
    if max_val > 0:
        spec /= max_val

    return spec, freq_axis, time_axis


def spectrogram_to_audio(
    spec: np.ndarray,
    sample_rate: int = 44100,
    min_freq: float = 100.0,
    max_freq: float = 4000.0,
    synthesis_time: float = 10.0,
) -> np.ndarray:
    """Resynthesize a spectrogram into audio via sinusoidal additive synthesis.

    Each CSI subcarrier column becomes a frequency band. Amplitude in that
    band controls the gain of oscillators within the corresponding audio
    frequency range. Produces a wav-like signal you can hear.

    This IS the room-as-instrument transducer: the WiFi field's multipath
    profile becomes a spectral envelope, and people in the room become
    timbral modulators.
    """
    n_freq, n_sc = spec.shape
    n_samples = int(sample_rate * synthesis_time)
    audio = np.zeros(n_samples, dtype=np.float64)

    t = np.arange(n_samples) / sample_rate

    for sc_idx in range(n_sc):
        # Map subcarrier index to audio frequency (linear mapping)
        f_center = min_freq + (max_freq - min_freq) * sc_idx / n_sc
        f_band = (max_freq - min_freq) / n_sc  # bandwidth per subcarrier

        # Build amplitude envelope from the spectrogram column
        col = spec[:, sc_idx]
        col_energy = col.sum()  # total energy in this subcarrier's Doppler spectrum

        if col_energy < 0.001:
            continue  # silence for empty subcarriers

        # Gain proportional to Doppler energy
        gain = col_energy * 0.1

        # Carrier oscillators: fundamental + first 4 harmonics
        for harm in range(1, 5):
            h_gain = gain / (harm * harm)
            freq = f_center * harm
            if freq > sample_rate / 2:
                break
            audio += h_gain * np.sin(2 * np.pi * freq * t)

    # Normalise to [-0.95, 0.95]
    max_abs = np.abs(audio).max()
    if max_abs > 0:
        audio = audio / max_abs * 0.95

    return audio


# ---------------------------------------------------------------------------
# Path C: Vital sign band extraction
# ---------------------------------------------------------------------------

def extract_vital_bands(
    amp_matrix: np.ndarray,
    sampling_rate: float,
) -> dict:
    """Extract breathing and heartbeat frequency bands from CSI amplitude.

    Breathing: 0.1–0.5 Hz (6–30 BPM)
    Heart rate: 0.8–2.0 Hz (48–120 BPM)

    Returns dict with Hz frequencies, BPM, and band powers.
    """
    n_frames, n_sc = amp_matrix.shape
    if n_frames < 10:
        return {"breathing_hz": 0.0, "heartbeat_hz": 0.0,
                "breathing_bpm": 0.0, "heartbeat_bpm": 0.0,
                "breathing_band_power": 0.0, "heartbeat_band_power": 0.0,
                "motion_energy": 0.0, "presence_score": 0.0}

    # Average amplitude across subcarriers → single time series
    signal = amp_matrix.mean(axis=1)
    signal -= signal.mean()  # remove DC

    # FFT
    n = len(signal)
    fft_vals = scipy.fft.rfft(signal)
    freqs = scipy.fft.rfftfreq(n, d=1.0 / sampling_rate)
    psd = np.abs(fft_vals) ** 2
    psd /= psd.sum() + 1e-12  # normalise

    # Skip DC
    freqs = freqs[1:]
    psd = psd[1:]

    # Breathing band: 0.1–0.5 Hz
    breath_mask = (freqs >= 0.1) & (freqs <= 0.5)
    breath_power = psd[breath_mask].sum() if breath_mask.any() else 0.0

    # Heart rate band: 0.8–2.0 Hz
    heart_mask = (freqs >= 0.8) & (freqs <= 2.0)
    heart_power = psd[heart_mask].sum() if heart_mask.any() else 0.0

    # Peak frequencies
    breathing_hz = float(freqs[breath_mask][np.argmax(psd[breath_mask])]) if breath_power > 0 else 0.0
    heartbeat_hz = float(freqs[heart_mask][np.argmax(psd[heart_mask])]) if heart_power > 0 else 0.0

    # Motion energy: total variance
    motion_energy = float(np.var(signal))

    # Presence: fraction of energy in vital bands vs total
    total_vital = breath_power + heart_power
    presence_score = min(1.0, total_vital * 100)  # heuristic scale

    return {
        "breathing_hz": float(breathing_hz),
        "heartbeat_hz": float(heartbeat_hz),
        "breathing_bpm": float(breathing_hz * 60),
        "heartbeat_bpm": float(heartbeat_hz * 60),
        "breathing_band_power": float(breath_power),
        "heartbeat_band_power": float(heart_power),
        "motion_energy": motion_energy,
        "presence_score": float(presence_score),
    }


# ---------------------------------------------------------------------------
# Path B: MIR feature extraction from CSI spectrum
# ---------------------------------------------------------------------------

def csi_to_mir_features(
    spec: np.ndarray,
    vital_bands: dict,
) -> dict:
    """Extract MIR-like features from the CSI spectrogram.

    The CSI spectrum is structurally identical to an audio magnitude spectrum.
    These features can be fed directly into the mod-writer seed pipeline
    (audio-to-AQ classifier) or used as composition constraints.

    Returns dict with spectral centroid, rolloff, flatness, and MFCCs.
    """
    if spec.ndim != 2 or spec.shape[0] == 0:
        return {
            "centroid": 0.0, "rolloff": 0.0, "flatness": 0.0,
            "mfcc": None, "seed_score": {}
        }

    # Collapse: average spectrogram across Doppler dimension → (n_subcarriers,)
    spectrum = spec.mean(axis=0)
    spectrum = spectrum / (spectrum.max() + 1e-12)  # normalise
    n_bins = len(spectrum)

    if n_bins < 2:
        return {"centroid": 0.0, "rolloff": 0.0, "flatness": 0.0,
                "mfcc": None, "seed_score": {}}

    # Treat subcarrier index as pseudo-frequency axis (0 = subcarrier 0, etc.)
    freq_axis = np.arange(n_bins, dtype=np.float64)

    # Spectral centroid: weighted mean
    centroid = float(np.sum(freq_axis * spectrum) / (spectrum.sum() + 1e-12))

    # Spectral rolloff: frequency below which 85% of energy is contained
    cumsum = np.cumsum(spectrum)
    total = cumsum[-1]
    rolloff = float(np.searchsorted(cumsum, 0.85 * total)) if total > 0 else 0.0

    # Spectral flatness: geometric / arithmetic mean ratio
    log_spectrum = np.log(spectrum + 1e-12)
    geometric_mean = np.exp(float(np.mean(log_spectrum)))
    arithmetic_mean = float(np.mean(spectrum))
    flatness = geometric_mean / (arithmetic_mean + 1e-12)

    # MFCCs (13 coefficients) via DCT of log power spectrum
    n_mfcc = 13
    dct_matrix = np.zeros((n_mfcc, n_bins))
    for k in range(n_mfcc):
        dct_matrix[k] = np.cos(np.pi * (2 * np.arange(n_bins) + 1) * k / (2 * n_bins))
    log_spec = np.log(spectrum + 1e-12)
    mfcc = dct_matrix @ log_spec

    return {
        "centroid": centroid,
        "rolloff": rolloff,
        "flatness": float(flatness),
        "mfcc": mfcc,
        "seed_score": {
            "centroid_zone": int(centroid % 9) + 1,
            "flatness_log": float(np.log10(flatness + 1e-12)),
            "breathing_power": vital_bands.get("breathing_band_power", 0.0),
            "heartbeat_power": vital_bands.get("heartbeat_band_power", 0.0),
            "motion_energy": vital_bands.get("motion_energy", 0.0),
        },
    }


# ---------------------------------------------------------------------------
# Main transducer pipeline
# ---------------------------------------------------------------------------

def transduce(
    frames: List[CSIFrame],
    sample_rate: float = 100.0,
    audio_sr: int = 44100,
    synthesis_time: float = 10.0,
) -> TransducerOutput:
    """Run the full CSI→audio transduction pipeline.

    Args:
        frames: Parsed CSI frames
        sample_rate: CSI sampling rate (Hz), default 100 Hz from ESP32
        audio_sr: Audio sample rate for WAV synthesis
        synthesis_time: Duration of synthesised audio (seconds)

    Returns:
        TransducerOutput with all three paths
    """
    if not frames:
        return TransducerOutput()

    amp_matrix = build_amplitude_matrix(frames)

    # Path A: spectrogram + audio synthesis
    spec, freq_axis, time_axis = csi_to_spectrogram(
        amp_matrix, sample_rate, window_size=min(128, len(frames)),
    )
    wav_samples = spectrogram_to_audio(
        spec, sample_rate=audio_sr,
        synthesis_time=synthesis_time,
    )

    # Path C: vital sign extraction
    vitals = extract_vital_bands(amp_matrix, sample_rate)

    # Path B: MIR features for mod-writer seed
    mir = csi_to_mir_features(spec, vitals)

    out = TransducerOutput(
        wav_samples=wav_samples,
        sample_rate=audio_sr,
        spectrogram=spec,
        spec_freq_axis=freq_axis,
        spec_time_axis=time_axis,
        breathing_hz=vitals["breathing_hz"],
        heartbeat_hz=vitals["heartbeat_hz"],
        breathing_band_power=vitals["breathing_band_power"],
        heartbeat_band_power=vitals["heartbeat_band_power"],
        motion_energy=vitals["motion_energy"],
        presence_score=vitals["presence_score"],
        centroid=mir["centroid"],
        rolloff=mir["rolloff"],
        flatness=mir["flatness"],
        mfcc=mir["mfcc"],
        seed_score=mir["seed_score"],
    )
    return out


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """Run transducer on sample CSI JSON data and print results."""
    import argparse
    import time

    parser = argparse.ArgumentParser(description="CSI → Audio Transducer")
    parser.add_argument("--input", default=None,
                        help="Path to CSI JSON file (uses sample if omitted)")
    parser.add_argument("--output-wav", default=None,
                        help="Output WAV file path")
    parser.add_argument("--synthesis-time", type=float, default=10.0,
                        help="Duration of synthesised audio (seconds)")
    parser.add_argument("--n-frames", type=int, default=0,
                        help="Use only first N frames (0 = all)")
    args = parser.parse_args()

    # Load data
    if args.input:
        src = Path(args.input)
    else:
        # Try the RuView sample data
        src = Path(__file__).parent / "sample_csi_data.json"
        if not src.exists():
            src = Path("/home/etym/RuView/archive/v1/data/proof/sample_csi_data.json")

    print(f"[transducer] loading {src}")
    with open(src) as f:
        data = json.load(f)

    info = data.get("generator", "unknown")
    print(f"[transducer] source: {info}")
    print(f"[transducer] frames: {data.get('num_frames', 'N/A')}")
    print(f"[transducer] subcarriers: {data.get('num_subcarriers', 'N/A')}")
    print(f"[transducer] sampling_rate: {data.get('sampling_rate_hz', 'N/A')} Hz")
    print(f"[transducer] antennas: {data.get('num_antennas', 'N/A')}")

    frames = parse_json_frames(data)
    if args.n_frames > 0:
        frames = frames[:args.n_frames]
    print(f"[transducer] parsed {len(frames)} frames")

    sr = data.get("sampling_rate_hz", 100.0)
    t0 = time.time()
    out = transduce(frames, sample_rate=sr, synthesis_time=args.synthesis_time)
    elapsed = time.time() - t0
    print(f"[transducer] transduction complete in {elapsed:.3f}s")

    # Report
    print(f"\n{'=' * 50}")
    print(f"  Spectrogram shape: {out.spectrogram.shape if out.spectrogram is not None else 'None'}")
    print(f"  WAV samples: {len(out.wav_samples) if out.wav_samples is not None else 0} at {out.sample_rate} Hz")
    print(f"  Audio duration: {len(out.wav_samples) / out.sample_rate if out.wav_samples is not None else 0:.1f}s")
    print(f"\n  Vital Signs:")
    print(f"    Breathing: {out.breathing_hz:.4f} Hz ({out.breathing_hz * 60:.1f} BPM)")
    print(f"    Heartbeat: {out.heartbeat_hz:.4f} Hz ({out.heartbeat_hz * 60:.1f} BPM)")
    print(f"    Breathing power: {out.breathing_band_power:.6f}")
    print(f"    Heartbeat power: {out.heartbeat_band_power:.6f}")
    print(f"    Motion energy:   {out.motion_energy:.6f}")
    print(f"    Presence score:  {out.presence_score:.4f}")
    print(f"\n  MIR Features:")
    print(f"    Centroid: {out.centroid:.2f} (subcarrier index)")
    print(f"    Rolloff:  {out.rolloff:.2f} (85% energy)")
    print(f"    Flatness: {out.flatness:.4f}")
    if out.mfcc is not None:
        print(f"    MFCC[0:5]: {out.mfcc[:5]}")
    print(f"\n  mod-writer seed score:")
    print(f"    Centroid zone: {out.seed_score.get('centroid_zone', '?')}")

    # Save WAV
    if args.output_wav and out.wav_samples is not None:
        try:
            import wave as _wave
            wav_path = Path(args.output_wav)
            audio_bytes = (out.wav_samples * 32767).astype(np.int16).tobytes()
            with _wave.open(str(wav_path), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(out.sample_rate)
                wf.writeframes(audio_bytes)
            print(f"\n  WAV saved: {wav_path} ({wav_path.stat().st_size / 1024 / 1024:.2f} MB)")
        except Exception as e:
            print(f"\n  WAV save error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
