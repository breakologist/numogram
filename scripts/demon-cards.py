#!/usr/bin/env python3
"""
demon-cards.py — Generate 45 Pandemonium demon tarot-card SVGs from pandemonium-matrix-45-demons.json.

Usage:
    python3 demon-cards.py                        # all 45
    python3 demon-cards.py --zone 5               # zone-5 only
    python3 demon-cards.py --current 1            # current-1 only
    python3 demon-cards.py --carrier              # five carrier demons
    python3 demon-cards.py --demo                  # one per zone (9 total)
    python3 demon-cards.py --mesh 14               # single demon by index
    python3 demon-cards.py --mesh "3::6"            # single demon by netspan

Requires: pandemonium-matrix-45-demons.json in raw/ or ~/numogram/data/
Optional:  ~/numogram/docs/wiki/assets/zone-glyphs/zone-{0-9}.png embedded in cards.
"""

from pathlib import Path
import argparse, json, sys, math, base64

try:
    from numogram_geometry import midpoint
except ImportError:
    def midpoint(p0, p1):
        return ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2)

ZONE_DATA = {
    0:{"particle":"eiaoung","name":"Void",      "color":"#991b1b"},
    1:{"particle":"gl",     "name":"Surge",     "color":"#d97706"},
    2:{"particle":"dt",     "name":"Separation","color":"#ef4444"},
    3:{"particle":"zx",     "name":"Release",   "color":"#16a34a"},
    4:{"particle":"skr",    "name":"Gate",      "color":"#ca8a04"},
    5:{"particle":"ktt",    "name":"Hinge",     "color":"#e11d48"},
    6:{"particle":"tch",    "name":"Traction",  "color":"#2563eb"},
    7:{"particle":"pb",     "name":"Breath",    "color":"#0891b2"},
    8:{"particle":"mnm",    "name":"Lull",      "color":"#c084fc"},
    9:{"particle":"tn",     "name":"Plex",      "color":"#7c3aed"},
}
CURRENT_COLOR = {
    1:"#fc8181",2:"#fbbf24",3:"#a3e635",4:"#38bdf8",
    5:"#a78bfa",6:"#fb923c",7:"#2dd4bf",8:"#9ca3af",9:"#f97316"
}
CARRIER_PAIRS = {frozenset({0,9}),frozenset({1,8}),
                 frozenset({2,7}),frozenset({3,6}),frozenset({4,5})}

def is_carrier(netspan):
    za,zb = parse_ns(netspan)
    return frozenset({za,zb}) in CARRIER_PAIRS

def current_from(za, zb): return abs(za - zb)
def gate_tri(zone): return zone*(zone-1)//2 if zone > 0 else 0

def parse_ns(raw):
    if "::" in raw: a,b = raw.split("::")
    elif "->" in raw: a,b = raw.split("->")
    else: a,b = raw[0], raw[-1]
    return int(a), int(b)

def demon_slug(d):
    raw = d["name"].split("(")[0].strip()
    return "".join(c if c.isalnum() else "-" for c in raw).strip("-").lower()[:32]

def load_demons():
    c = [Path.home()/".hermes/obsidian/hermetic/raw/pandemonium-matrix-45-demons.json"]
    for p in c:
        if p.exists():
            raw = json.loads(p.read_text())
            return {str(k):v for k,v in raw.items()}, p
    sys.exit("ERROR: pandemonium-matrix-45-demons.json not found.")

def rrect(x, y, w, h, rx=10):
    return (f'M {x+rx} {y}'
            f' L {x+w-rx} {y} Q {x+w} {y} {x+w} {y+rx}'
            f' L {x+w} {y+h-rx} Q {x+w} {y+h} {x+w-rx} {y+h}'
            f' L {x+rx} {y+h} Q {x} {y+h} {x} {y+h-rx}'
            f' L {x} {y+rx} Q {x} {y} {x+rx} {y} Z')

def build_card(d, glyph_dir, CW=360, CH=500):
    name   = d["name"]
    ns     = d["netspan"]
    dz     = d.get("type","")
    attrs_ = d.get("attrs","")
    za,zb  = parse_ns(ns)
    cur    = current_from(za,zb)
    zda    = ZONE_DATA[za];  zdb = ZONE_DATA[zb]
    car    = is_carrier(ns)
    cur_c  = CURRENT_COLOR.get(cur,"#94a3b8")
    gt     = gate_tri(min(za,zb))
    gt_z   = (gt%9) if (gt%9)!=0 else 9
    aq_sum = (64+za)+(64+zb)
    P=16; BAR_Y=62; BAR_H=36; BAR_BOT=BAR_Y+BAR_H
    lbx=P+58; rbx=CW-P-58
    SR=28; gly_y=BAR_BOT+82
    gl_a=P+SR+8;  gl_b=CW-P-SR-8
    MY=gly_y+SR+22; PY=MY+42; SY=PY+28
    mark = "★ " if car else ""
    L = []
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" '
             f'width="{CW}" height="{CH}" '
             f'role="img" aria-label="Demon {name} ({ns}) {dz}">')
    L.append("<defs>")
    L.append('<radialGradient id="dbg" cx="50%" cy="42%" r="62%">'
             '<stop offset="0%" stop-color="#1e293b"/>'
             '<stop offset="100%" stop-color="#0f172a"/></radialGradient>')
    for ci,cv in CURRENT_COLOR.items():
        L.append(f'<marker id="da-{ci}" markerWidth="8" markerHeight="5" '
                 f'refX="7" refY="2.5" orient="auto">'
                 f'<polygon points="0,0 8,2.5 0,5" fill="{cv}"/></marker>')
    L.append('<style>@keyframes med--zone-medallion{0%{opacity:.88;filter:hue-rotate(0deg)}50%{opacity:1;filter:hue-rotate(30deg)}}</style>')
    L.append("</defs>")
    L.append(f'<path d="{rrect(0,0,CW,CH,12)}" fill="url(#dbg)" '
             f'stroke="#1e293b" stroke-width="1.5"/>')
    L.append(f'<rect x="{P}" y="{BAR_Y}" width="58" height="{BAR_H}" '
             f'rx="7" fill="{zda["color"]}" opacity="0.92"/>')
    L.append(f'<rect x="{CW-P-58}" y="{BAR_Y}" width="58" height="{BAR_H}" '
             f'rx="7" fill="{zdb["color"]}" opacity="0.92"/>')
    L.append(f'<text x="{lbx}" y="{BAR_Y+11}" font-size="10" fill="white" '
             f'font-weight="bold">Z{za} — {zda["name"][:7]}</text>')
    L.append(f'<text x="{rbx}" y="{BAR_Y+19}" font-size="10" fill="white" '
             f'text-anchor="end" font-weight="bold">Z{zb} — {zdb["name"][:7]}</text>')
    L.append(f'<text x="{lbx}" y="{BAR_Y+24}" font-size="8" fill="#94a3b8">'
             f'[{zda["particle"]}]</text>')
    L.append(f'<text x="{rbx}" y="{BAR_Y+32}" font-size="8" fill="#94a3b8" '
             f'text-anchor="end">[{zdb["particle"]}]</text>')
    pred = f"★ {dz}" if car else dz
    L.append(f'<text x="{CW//2}" y="17" font-size="16" fill="#e2e8f0" '
             f'font-weight="bold">{mark}{name}</text>')
    L.append(f'<text x="{CW//2}" y="31" font-size="13" fill="#cbd5e1">{ns}</text>')
    L.append(f'<text x="{CW//2}" y="44" font-size="9" fill="#64748b">{pred}</text>')
    L.append(f'<text x="{CW//2}" y="57" font-size="9" fill="#94a3b8">{attrs_[:60]}</text>')
    p0=(lbx,BAR_BOT);  p1=(rbx,BAR_BOT)
    mx,my = midpoint(p0,p1)
    sgn   = -1 if cur%2==1 else +1
    ctrl  = (mx, my+sgn*28)
    for dy in [0,8]:
        body = f'M {p0[0]:.0f} {p0[1]+dy:.0f} Q {ctrl[0]:.0f} {ctrl[1]:.0f} {p1[0]:.0f} {p1[1]+dy:.0f}'
        L.append(f'<path d="{body}" stroke="{cur_c}" stroke-width="10" '
                 f'fill="none" stroke-opacity="0.10" '
                 f'marker-end="url(#da-{cur})"/>')
    body = f'M {p0[0]:.0f} {p0[1]:.0f} Q {ctrl[0]:.0f} {ctrl[1]:.0f} {p1[0]:.0f} {p1[1]:.0f}'
    L.append(f'<path d="{body}" stroke="{cur_c}" stroke-width="2.5" '
             f'fill="none" stroke-opacity="0.88" '
             f'marker-end="url(#da-{cur})"/>')
    lx = mx+(-12 if cur%2 else 12)
    ly = (ctrl[1]+my)/2 + (6 if cur%2==0 else -12)
    L.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="18" fill="{cur_c}" '
             f'font-weight="bold">{cur}</text>')
    for gx,gy,zn in [(gl_a,gly_y,za),(gl_b,gly_y,zb)]:
        zc = zda["color"] if zn==za else zdb["color"]
        L.append(f'<circle cx="{gx}" cy="{gy}" r="{SR+2}" '
                 f'fill="#162032" stroke="{zc}" stroke-width="2.5"/>')
        png = glyph_dir / f"zone-{zn}.png"
        if png.exists():
            b64 = base64.b64encode(png.read_bytes()).decode()
            L.append(f'<image x="{gx-SR-2}" y="{gy-SR-2}" '
                     f'width="{SR*2+4}" height="{SR*2+4}" '
                     f'style="animation:med--zone-medallion 2s ease-in-out infinite" xlink:href="data:image/png;base64,{b64}"/>')
        else:
            L.append(f'<text x="{gx}" y="{gy+6}" font-size="20" fill="{zc}" '
                     f'font-weight="bold" text-anchor="middle">{zn}</text>')
    L.append(f'<line x1="{lbx}" y1="{BAR_BOT}" '
             f'x2="{gl_a}" y2="{gly_y-SR}" '
             f'stroke="#334155" stroke-width="1" '
             f'stroke-dasharray="3 3" opacity="0.55"/>')
    L.append(f'<line x1="{rbx}" y1="{BAR_BOT}" '
             f'x2="{gl_b}" y2="{gly_y-SR}" '
             f'stroke="#334155" stroke-width="1" '
             f'stroke-dasharray="3 3" opacity="0.55"/>')
    L.append(f'<rect x="{P}" y="{MY}" width="{CW-2*P}" height="40" '
             f'rx="6" fill="#162032" stroke="#334155" stroke-width="1"/>')
    L.append(f'<text x="{CW//2}" y="{MY+14}" font-size="10" fill="#94a3b8">'
             f'  Z{za}={64+za}  ⊕  Z{zb}={64+zb}  ·  AQΣ={aq_sum}  DR={aq_sum%9 or 9}</text>')
    L.append(f'<text x="{CW//2}" y="{MY+28}" font-size="9" fill="#64748b">'
             f'Gate: Gt-{gt:03d} → Z{gt_z}   ·   Current: {cur}</text>')
    L.append(f'<text x="{CW//2}" y="{PY}" font-size="13" fill="#8899aacc" '
             f'opacity="0.8">Δ─────────Δ</text>')
    sv=za+zb; sdr=sv%9 if sv%9!=0 else 9
    L.append(f'<text x="{CW//2}" y="{SY}" font-size="9" fill="#64748b">'
             f'≡  {za}⊕{zb}  ≡  {sv}  ≡  {sdr}  ≡</text>')
    for cx,cy,lab in [(22,22,str(za)),(CW-22,22,str(zb)),
                       (22,CH-22,str(cur)),(CW-22,CH-22,str(abs(za-zb)))]:
        L.append(f'<text x="{cx}" y="{cy}" font-size="9" fill="#1e293b" '
                 f'opacity="0.55" text-anchor="middle" font-weight="bold">{lab}</text>')
    L.append("</svg>")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zone",    type=int, help="Only cards for zone (0-9)")
    ap.add_argument("--current", type=int, help="Only cards for current (1-9)")
    ap.add_argument("--carrier", action="store_true", help="Five carrier demons")
    ap.add_argument("--demo",   action="store_true", help="One per zone (9 total)")
    ap.add_argument("--mesh",   help="Single demon: netspan '3::6' or index '0-44'")
    ap.add_argument("-o","--out", default=".", help="Output directory")
    ap.add_argument("--glyphs", default="~/numogram/docs/wiki/assets/zone-glyphs",
                    help="zone-{N}.png directory")
    args = ap.parse_args()
    data, src = load_demons()
    entries = sorted(data.values(), key=lambda d: parse_ns(d["netspan"]))
    out_dir = Path(args.out);  gl_dir = Path(args.glyphs).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    def in_zone(d):
        za,zb = parse_ns(d["netspan"])
        return za==args.zone or zb==args.zone
    def in_current(d):
        za,zb = parse_ns(d["netspan"])
        return current_from(za,zb)==args.current
    pool = list(entries)
    if args.mesh:
        if "::" in args.mesh:
            pool = [v for v in entries if v["netspan"]==args.mesh]
        else:
            pool = [entries[int(args.mesh)]]
    elif args.carrier:
        pool = [d for d in entries if is_carrier(d["netspan"])]
    elif args.zone is not None:
        pool = [d for d in entries if in_zone(d)]
    elif args.current is not None:
        pool = [d for d in entries if in_current(d)]
    elif args.demo:
        seen=set(); demo=[]
        for d in entries:
            za = min(parse_ns(d["netspan"]))
            if za not in seen: seen.add(za); demo.append(d)
        pool = demo
    errs=0
    for d in pool:
        ns  = d["netspan"]
        key = next(k for k,v in data.items() if v is d)
        fn  = f"demon-{key}-{demon_slug(d)}.svg"
        try:
            (out_dir / fn).write_text(build_card(d, gl_dir))
            print(f"  ✓  {fn}")
        except Exception as e:
            print(f"  ✗  {fn}: {e}", file=sys.stderr); errs+=1
    print(f"\n{len(pool)} cards, {errs} errors → {out_dir}")

if __name__ == "__main__":
    main()
