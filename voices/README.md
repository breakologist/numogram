# numogram-voices

Physical modelling synthesis of quasiphonic particles.

## formant_voice.py
Generates WAV files for each zone's quasiphonic sound:
- Zone 0: eiaoung (silent whisper)
- Zone 1: gl (gulp)
- Zone 2: dt (stutter)
- ... Zone 9: tn (grunt)

Requires `numpy` and `scipy`.

Run to regenerate all 10 zone samples:
```bash
python voices/formant_voice.py
```
