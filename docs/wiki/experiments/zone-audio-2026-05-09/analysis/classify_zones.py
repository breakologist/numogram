
#!/usr/bin/env python3
import subprocess
import json
import os

# Classify all generated WAV files
wav_dir = "/home/etym/.hermes/obsidian/hermetic/wiki/experiments/zone-audio-2026-05-09/wavs"
mod_dir = "/home/etym/.hermes/obsidian/hermetic/wiki/experiments/zone-audio-2026-05-09/mods"

# Find all WAV files
wav_files = [f for f in os.listdir(wav_dir) if f.endswith('.wav')]

print("Classifying generated audio files...")
results = []

for wav_file in wav_files:
    wav_path = os.path.join(wav_dir, wav_file)
    mod_path = os.path.join(mod_dir, wav_file.replace('.wav', '.mod'))
    
    # Run classification
    cmd = [
        "/home/etym/.hermes/hermes-agent/venv/bin/mod-writer",
        "--classify", wav_path,
        "--classify-format", "json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            classification = json.loads(result.stdout)
            results.append({
                "file": wav_file,
                "mod": os.path.basename(mod_path),
                "classification": classification
            })
            print(f"✓ Classified {wav_file}: {classification}")
        else:
            print(f"✗ Classification failed for {wav_file}: {result.stderr[:200]}")
    except Exception as e:
        print(f"✗ Error classifying {wav_file}: {e}")

# Save results
output_file = "/home/etym/.hermes/obsidian/hermetic/wiki/experiments/zone-audio-2026-05-09/classification_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"
Results saved to {output_file}")
