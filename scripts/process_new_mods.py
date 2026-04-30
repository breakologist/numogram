STUB_TEMPLATE = '---\ntitle: "ModArchive: {base}.mod"\ntags: ["modarchive", "protracker", "module", "chiptune", "numogram-analysis"]\nzone: 0\nsyzygy: pending\ncreated: {today}\nlast_updated: {today}\nsource: "ModArchive — imported & analysed via Hermes Agent mod-writer skill"\nstatus: stub\n---\n\n# {base}.mod\n\n> **Import date:** {today} | **Format:** Protracker M.K.  \n> **Sample strings:** {sample_list}\n\n## Musical & Audio Summary\n\n- **Duration:** {dur:.1f} s  \n- **Audio portrait:** {portrait}\n- **RMS:** {rms:.4f} | **Peak:** {peak:.4f}  \n- **LUFS:** {lufs} | **Quality:** `{quality}`\n\n## Artifacts\n\n- Audio analysis: [[{base}_analysis.json]]\n- Spectrogram: [[{base}_spec.png]]\n- WAV: [[{base}.wav]]\n\n## Cross‑Links\n\n- [[mod-writer]]\n- [[audio-renderer]]\n- [[numogram-overview]]\n\n*Generated {timestamp}.*\n'

#!/usr/bin/env python3
import sys, os, json, datetime, re, subprocess

skills_root = '/home/etym/.hermes/skills/'
sys.path.insert(0, skills_root)
sys.path.insert(0, os.path.join(skills_root, 'numogram-audio'))
sys.path.insert(0, os.path.join(skills_root, 'numogram-audio', 'audio-renderer'))

from audio_renderer.analyzer import full_analysis, describe_audio

mod_dir = '/home/etym/numogram/mod-imports/'
vault_wiki = '/home/etym/.hermes/obsidian/hermetic/wiki/'
vault_assets = os.path.join(vault_wiki, 'assets', 'mod-imports')
batch_summary_path = os.path.join(vault_assets, 'modarchive_batch_summary.json')

new_mods = [
    'modarchive-archon_-_sextyfour.mod',
    'modarchive-ifaskedt.mod',
    'modarchive-lightz_on_da_sky.mod',
    'modarchive-modworks-starbucks.mod',
]

def parse_header_brief(path):
    with open(path, 'rb') as f:
        data = f.read(1084)
    title = data[0:20].split(b'\\0')[0].decode('latin1', errors='ignore').strip()
    strings = []
    for m in re.finditer(rb'[\\x20-\\x7e]{4,}', data[:1000]):
        s = m.group().decode('latin1', errors='ignore').strip()
        if s not in strings:
            strings.append(s)
    return title, strings

def render_wav(modpath, wavpath):
    cmd = ['ffmpeg', '-y', '-i', modpath, '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '2', wavpath]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0

def spec_png(wavpath, pngpath):
    cmd = ['ffmpeg', '-y', '-i', wavpath,
           '-filter_complex', 'showspectrumpic=scale=log:color=plasma:size=960x540',
           '-frames:v', '1', pngpath]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0

if os.path.exists(batch_summary_path):
    with open(batch_summary_path) as f:
        batch = json.load(f)
else:
    batch = {"modules": [], "generated": datetime.datetime.now().isoformat()}

for mod_file in new_mods:
    src = os.path.join(mod_dir, mod_file)
    if not os.path.exists(src):
        print(f"Missing {mod_file}")
        continue
    base = mod_file.replace('.mod', '')
    print(f"\\n=== {base} ===")
    
    wav = os.path.join(mod_dir, base + ".wav")
    if not render_wav(src, wav):
        print("  Render failed; skipping")
        continue
    print("  Rendered WAV")
    
    spec = os.path.join(mod_dir, base + "_spec.png")
    if not spec_png(wav, spec):
        print("  Spectrogram failed")
    else:
        print("  Spectrogram OK")
    
    try:
        analysis = full_analysis(wav)
        portrait = describe_audio(analysis)
        print("  Audio analysis OK")
    except Exception as e:
        print(f"  Analysis error: {e}")
        continue
    
    asset_sub = os.path.join(vault_assets, base)
    os.makedirs(asset_sub, exist_ok=True)
    subprocess.run(['cp', wav, os.path.join(asset_sub, base + ".wav")], check=True, capture_output=True)
    subprocess.run(['cp', spec, os.path.join(asset_sub, base + "_spec.png")], check=True, capture_output=True)
    print("  Assets vault-synced")
    
    anal_json = os.path.join(asset_sub, base + "_analysis.json")
    with open(anal_json, 'w') as f:
        json.dump({"audio": analysis, "portrait": portrait}, f, indent=2)
    
    title, strings = parse_header_brief(src)
    dur = analysis.get('duration', 0)
    rms = analysis.get('RMS', 0)
    peak = analysis.get('Peak', 0)
    lufs = analysis.get('LUFS', 'N/A')
    quality = analysis.get('quality', 'unknown')
    
    sample_list = ', '.join(strings[:6])
    if len(strings) > 6:
        sample_list += '...'
    
    stub = STUB_TEMPLATE.format(
        base=base,
        today=datetime.date.today().isoformat(),
        sample_list=sample_list,
        dur=dur,
        portrait=portrait,
        rms=rms,
        peak=peak,
        lufs=lufs,
        quality=quality,
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    stub_path = os.path.join(vault_wiki, f"modarchive-{base}.md")
    with open(stub_path, 'w') as f:
        f.write(stub)
    print(f"  Stub written: modarchive-{base}.md")
    
    batch["modules"].append({
        "filename": base,
        "duration": dur,
        "rms": rms,
        "notes": 0,
        "zone_data": "pending parser",
        "portrait": portrait,
    })

with open(batch_summary_path, 'w') as f:
    json.dump(batch, f, indent=2)
print(f"\\n✓ Batch summary: {len(batch['modules'])} total modules")
