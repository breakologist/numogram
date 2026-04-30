#!/usr/bin/env python3
import sys, os, json, datetime, re, subprocess, importlib.util

writer_path = '/home/etym/.hermes/skills/numogram-audio/mod-writer/writer.py'
spec_w = importlib.util.spec_from_file_location("writer", writer_path)
writer = importlib.util.module_from_spec(spec_w)
spec_w.loader.exec_module(writer)

analyzer_path = '/home/etym/.hermes/skills/numogram-audio/audio-renderer/analyzer.py'
spec_a = importlib.util.spec_from_file_location("analyzer", analyzer_path)
analyzer = importlib.util.module_from_spec(spec_a)
spec_a.loader.exec_module(analyzer)

PERIOD_TABLE = writer.PERIOD_TABLE
NOTE_OFFSET = writer.NOTE_OFFSET

def period_to_note(period):
    try:
        idx = PERIOD_TABLE.index(period)
    except ValueError:
        return None
    octave = idx // 12
    note_idx = idx % 12
    note_name = [n for n, i in NOTE_OFFSET.items() if i == note_idx]
    return (note_name[0] + str(octave)) if note_name else None

def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def note_to_zone(note_str):
    if not note_str: return 0
    letter = note_str[:-1]; octave = int(note_str[-1])
    offset = NOTE_OFFSET.get(letter.upper(), 0)
    note_index = octave * 12 + offset
    return digital_root(note_index + 1) % 10

def parse_mod_notes(modpath):
    with open(modpath, 'rb') as f:
        data = f.read()
    if len(data) < 1084:
        return [], [], []
    song_length = data[950]
    order = list(data[952:952+128])[:song_length]
    patterns_used = sorted(set(order))
    notes = []
    for pat_idx in order:
        pat_offset = 1084 + pat_idx * 1024
        if pat_offset + 1024 > len(data):
            break
        for row in range(64):
            for ch in range(4):
                cell_off = pat_offset + (row*4 + ch)*4
                if cell_off + 4 > len(data):
                    continue
                b0, b1 = data[cell_off], data[cell_off+1]
                period = ((b0 & 0x0F) << 8) | b1
                if period == 0: continue
                note = period_to_note(period)
                if note:
                    notes.append({'pattern': pat_idx, 'row': row, 'channel': ch, 'period': period, 'note': note})
    return notes, order, patterns_used

def compute_fingerprint(notes):
    if not notes:
        return {'void_ratio':0,'warp_ratio':0,'hold_ratio':0,'rise_ratio':0,'sink_ratio':0,'gate_variance':0,'motifs':['Gate-Scattered']}
    zones = [note_to_zone(n['note']) for n in notes]
    zones = [z for z in zones if z is not None]
    nz = len(zones) or 1
    void = sum(1 for z in zones if z == 0) / nz
    warp = sum(1 for z in zones if z in (7,8,9)) / nz
    hold = sum(1 for z in zones if z in (4,5)) / nz
    rise = sum(1 for z in zones if z in (7,8)) / nz
    sink = sum(1 for z in zones if z in (1,2,3,6)) / nz
    mean = sum(zones)/nz
    gate_var = sum((z-mean)**2 for z in zones)/nz
    motifs = []
    if warp > 0.15: motifs.append('Warp-Seeking')
    if void > 0.30: motifs.append('Void-Dominant')
    if sink > 0.30: motifs.append('Sink-Seeking')
    if rise > 0.30: motifs.append('Rise-Seeking')
    if not motifs: motifs.append('Gate-Scattered')
    return {'void_ratio': void, 'warp_ratio': warp, 'hold_ratio': hold, 'rise_ratio': rise, 'sink_ratio': sink, 'gate_variance': gate_var, 'motifs': motifs}

def parse_header_brief(path):
    with open(path, 'rb') as f:
        data = f.read(1084)
    title = data[0:20].split(b'\0')[0].decode('latin1', errors='ignore').strip()
    strings = []
    for m in re.finditer(rb'[\x20-\x7e]{4,}', data[:1000]):
        s = m.group().decode('latin1', errors='ignore').strip()
        if s not in strings:
            strings.append(s)
    return title, strings

mod_dir = '/home/etym/numogram/mod-imports/'
vault_wiki = '/home/etym/.hermes/obsidian/hermetic/wiki/'
vault_assets = os.path.join(vault_wiki, 'assets', 'mod-imports')

new_mods = [
    'modarchive-archon_-_sextyfour.mod',
    'modarchive-ifaskedt.mod',
    'modarchive-lightz_on_da_sky.mod',
    'modarchive-modworks-starbucks.mod',
]

def render_wav(src, base):
    wav = os.path.join(mod_dir, base + '.wav')
    cmd = ['ffmpeg', '-y', '-i', src, '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '2', wav]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.returncode == 0), wav

def spec_png(wav, base):
    spec = os.path.join(mod_dir, base + '_spec.png')
    cmd = ['ffmpeg', '-y', '-i', wav,
           '-filter_complex', 'showspectrumpic=scale=log:color=plasma:size=960x540',
           '-frames:v', '1', spec]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return (r.returncode == 0), spec

for mod_file in new_mods:
    src = os.path.join(mod_dir, mod_file)
    if not os.path.exists(src):
        print(f"Missing {mod_file}")
        continue
    base = mod_file.replace('.mod','')
    print(f"\n=== {base} ===")
    
    ok, wav = render_wav(src, base)
    if not ok: print(" Render failed"); continue
    print(" Rendered WAV")
    ok, spec = spec_png(wav, base)
    print(" Spectrogram OK" if ok else " Spectrogram failed")
    
    try:
        analysis = analyzer.full_analysis(wav)
        portrait = analyzer.describe_audio(analysis, zone=0, gate='-', current='-')
        print(" Audio analysis OK")
    except Exception as e:
        print(f" Analysis error: {e}")
        continue
    
    notes, order, patterns_used = parse_mod_notes(src)
    print(f" Extracted {len(notes)} notes, order len={len(order)}, patterns used={len(patterns_used)}")
    
    fp = compute_fingerprint(notes)
    ratios = {'void': fp['void_ratio'], 'warp': fp['warp_ratio'], 'hold': fp['hold_ratio'], 'rise': fp['rise_ratio'], 'sink': fp['sink_ratio']}
    dom = max(ratios, key=ratios.get)
    dom_zone_map = {'void':0,'warp':8,'hold':5,'rise':8,'sink':3}
    dom_zone = dom_zone_map[dom]
    
    asset_sub = os.path.join(vault_assets, base)
    os.makedirs(asset_sub, exist_ok=True)
    subprocess.run(['cp', wav, os.path.join(asset_sub, base+'.wav')], check=True, capture_output=True)
    subprocess.run(['cp', spec, os.path.join(asset_sub, base+'_spec.png')], check=True, capture_output=True)
    print(" Assets vault-synced")
    
    with open(os.path.join(asset_sub, base+'_analysis.json'), 'w') as f:
        json.dump({"audio": analysis, "portrait": portrait}, f, indent=2)
    
    zones_seq = [note_to_zone(n['note']) for n in notes]
    canonical = {
        "source": "modarchive",
        "filename": base,
        "header": {"song_length": len(order), "patterns_used": patterns_used, "notes_count": len(notes)},
        "notes": [{'n': n['note'], 'p': n['period'], 'c': n['channel']} for n in notes[:100]],
        "zone_sequence": [z for z in zones_seq if z is not None],
        "fingerprint": fp,
        "audio": {"duration": analysis.get('duration',0), "rms": analysis.get('RMS',0), "quality": analysis.get('quality','unknown')}
    }
    with open(os.path.join(asset_sub, base+'_canonical.json'), 'w') as f:
        json.dump(canonical, f, indent=2)
    
    title, strings = parse_header_brief(src)
    sample_list = ', '.join(strings[:6]) + ('...' if len(strings)>6 else '')
    samples_nonempty = sum(1 for s in strings if s)
    stub_tpl = (
        "---\n"
        "title: \"ModArchive: {base}.mod\"\n"
        "tags: [\"modarchive\", \"protracker\", \"module\", \"chiptune\", \"numogram-analysis\"]\n"
        "zone: {dom_zone}\n"
        "syzygy: pending\n"
        "created: {today}\n"
        "last_updated: {today}\n"
        "source: \"ModArchive — imported & analysed via Hermes Agent mod-writer skill\"\n"
        "status: stub\n"
        "---\n"
        "\n"
        "# {base}.mod\n"
        "\n"
        "> **Import date:** {today} | **Format:** Protracker M.K.  \n"
        "> **Order list:** {order_len} positions (unique patterns: {patterns_cnt})  \n"
        "> **Samples:** {samples_cnt} non-empty entries  \n"
        "> **Sample strings:** {sample_list}\n"
        "\n"
        "## Musical Summary\n"
        "\n"
        "- **Notes extracted:** {notes_cnt}\n"
        "- **Zone fingerprint:**\n"
        "| Metric | Value |\n"
        "|---|---|\n"
        "| Void ratio | {void:.1%} |\n"
        "| Warp ratio | {warp:.1%} |\n"
        "| Hold ratio | {hold:.1%} |\n"
        "| Rise ratio | {rise:.1%} |\n"
        "| Sink ratio | {sink:.1%} |\n"
        "| Gate variance | {gate_var:.2f} |\n"
        "| Motifs | {motifs} |\n"
        "\n"
        "## Audio Properties\n"
        "\n"
        "| Metric | Value |\n"
        "|---|---|\n"
        "| Duration | {duration:.1f} s |\n"
        "| Sample rate | {sample_rate} Hz |\n"
        "| Channels | {channels} |\n"
        "| RMS | {rms:.4f} |\n"
        "| Peak | {peak:.4f} |\n"
        "| LUFS | {lufs} |\n"
        "| Quality | `{quality}` |\n"
        "\n"
        "## Artifacts\n"
        "\n"
        "- Audio analysis: [[{base}_analysis.json]]\n"
        "- Spectrogram: [[{base}_spec.png]]\n"
        "- WAV: [[{base}.wav]]\n"
        "- Canonical data: [[{base}_canonical.json]]\n"
        "\n"
        "## Cross‑Links\n"
        "\n"
        "- [[mod-writer]]\n"
        "- [[audio-renderer]]\n"
        "- [[numogram-overview]]\n"
        "\n"
        "*Generated {timestamp}.*\n"
    )
    today = datetime.date.today().isoformat()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stub = stub_tpl.format(
        base=base,
        dom_zone=dom_zone,
        today=today,
        order_len=len(order),
        patterns_cnt=len(patterns_used),
        samples_cnt=samples_nonempty,
        sample_list=sample_list,
        notes_cnt=len(notes),
        void=fp['void_ratio'],
        warp=fp['warp_ratio'],
        hold=fp['hold_ratio'],
        rise=fp['rise_ratio'],
        sink=fp['sink_ratio'],
        gate_var=fp['gate_variance'],
        motifs=', '.join(fp['motifs']),
        duration=analysis.get('duration',0),
        sample_rate=analysis.get('sample_rate','-'),
        channels=analysis.get('channels','-'),
        rms=analysis.get('RMS',0),
        peak=analysis.get('Peak',0),
        lufs=analysis.get('LUFS','N/A'),
        quality=analysis.get('quality','unknown'),
        timestamp=timestamp
    )
    
    stub_path = os.path.join(vault_wiki, f"modarchive-{base}.md")
    with open(stub_path, 'w') as f:
        f.write(stub)
    print(f" Stub written: modarchive-{base}.md")

print("\nAll done.")
