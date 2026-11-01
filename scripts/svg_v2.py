"""Generate v2 SVGs (Em, 1 Nov 2026) from repo data (lumpenspace/ccru@7c38ad9: positions.ts P_LABYRINTH,
currents.ts, gates.ts, zones.ts centauri) and ccru.net (Pandemonium Matrix; zone pages)."""
import math, os
OUT=os.path.join(os.path.dirname(__file__),'..','docs','wiki','assets')
BG='#0f172a'; FG='#e2e8f0'; MUT='#64748b'
REG={0:'plex',9:'plex',3:'warp',6:'warp'}; RC={'plex':'#a855f7','warp':'#e879f9','torque':'#22d3ee'}
reg=lambda z:REG.get(z,'torque')
HEAD=lambda w,h,t,sub:f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<style>text{{font-family:'JetBrains Mono','DejaVu Sans Mono',monospace}}</style>
<defs>{''.join(f'<marker id="m{n}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L10 4L0 8z" fill="{c}"/></marker>' for n,c in [('c','#22d3ee'),('w','#e879f9'),('p','#a855f7'),('g','#4ade80'),('a','#fbbf24')])}</defs>
<rect width="{w}" height="{h}" fill="{BG}"/>
<text x="30" y="40" fill="{FG}" font-size="18" font-weight="700">{t}</text>
<text x="30" y="60" fill="{MUT}" font-size="10">{sub}</text>'''
def tri(x1,y1,x2,y2,r1,r2,off=0):
    d=math.hypot(x2-x1,y2-y1);ux,uy=(x2-x1)/d,(y2-y1)/d;nx,ny=-uy*off,ux*off
    return x1+ux*r1+nx,y1+uy*r1+ny,x2-ux*r2+nx,y2-uy*r2+ny

def base10():
    P={6:(305,60),3:(495,60),2:(400,220),5:(200,335),7:(600,335),4:(200,540),8:(600,540),1:(400,655),9:(305,815),0:(495,815)}
    P={k:(x+60,y+90) for k,(x,y) in P.items()}; R=30
    s=[HEAD(980,1060,'THE DECIMAL NUMOGRAM — v2','Zones, syzygies (9-sum), currents and gates · layout: repo P_LABYRINTH · data: repo currents.ts / gates.ts, ccru.net Pandemonium')]
    for a,b in [(0,9),(1,8),(2,7),(3,6),(4,5)]:
        (x1,y1),(x2,y2)=P[a],P[b]; s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#475569" stroke-width="1" stroke-dasharray="3 4"/>')
        s.append(f'<text x="{(x1+x2)/2+6:.0f}" y="{(y1+y2)/2-6:.0f}" fill="#475569" font-size="9">{max(a,b)}::{min(a,b)}</text>')
    gates=[('Gt-03',2,3),('Gt-06',3,6),('Gt-10',4,1),('Gt-15',5,6),('Gt-21',6,3),('Gt-28',7,1),('Gt-36',8,9)]
    for n,a,b in gates:
        (x1,y1),(x2,y2)=P[a],P[b]; off=-14 if (a,b) in [(6,3)] else 14 if (a,b)==(3,6) else 0
        X1,Y1,X2,Y2=tri(x1,y1,x2,y2,R+4,R+6,off)
        s.append(f'<path d="M{X1:.0f} {Y1:.0f}L{X2:.0f} {Y2:.0f}" stroke="#4ade80" stroke-width="1.2" stroke-dasharray="2 3" fill="none" marker-end="url(#mg)"/>')
        ly={(3,6):-22,(6,3):26}.get((a,b),12); s.append(f'<text x="{(X1+X2)/2+5:.0f}" y="{(Y1+Y2)/2+ly:.0f}" fill="#4ade80" font-size="9" text-anchor="middle">{n}</text>')
    for n,z,dx in [('Gt-01',1,-40),('Gt-45',9,0),('Gt-00',0,0)]:
        x,y=P[z]; x+=dx; s.append(f'<path d="M{x-12} {y+R-2} C{x-30} {y+R+40} {x+30} {y+R+40} {x+12} {y+R}" stroke="#4ade80" stroke-width="1.2" stroke-dasharray="2 3" fill="none" marker-end="url(#mg)"/><text x="{x}" y="{y+R+46}" fill="#4ade80" font-size="9" text-anchor="middle">{n}</text>')
    for n,a,b,m in [('SURGE 8−1=7',8,7,'c'),('HOLD 7−2=5',2,5,'c'),('SINK 5−4=1',4,1,'c'),('WARP 6−3=3',6,3,'w')]:
        (x1,y1),(x2,y2)=P[a],P[b]; X1,Y1,X2,Y2=tri(x1,y1,x2,y2,R+4,R+6,0 if m=='c' else 0)
        if m=='w': Y1+=0; s.append(f'<path d="M{X1:.0f} {Y1-18:.0f}Q{(X1+X2)/2:.0f} {Y1-60:.0f} {X2:.0f} {Y2-18:.0f}" stroke="#e879f9" stroke-width="2.4" fill="none" marker-end="url(#mw)"/><text x="{(X1+X2)/2:.0f}" y="{Y1-52:.0f}" fill="#e879f9" font-size="10" font-weight="700" text-anchor="middle">{n}</text>'); continue
        s.append(f'<path d="M{X1:.0f} {Y1:.0f}L{X2:.0f} {Y2:.0f}" stroke="#22d3ee" stroke-width="2.4" fill="none" marker-end="url(#mc)"/>')
        s.append(f'<text x="{(X1+X2)/2:.0f}" y="{(Y1+Y2)/2-8:.0f}" fill="#22d3ee" font-size="10" font-weight="700" text-anchor="middle">{n}</text>')
    x,y=P[9]; s.append(f'<path d="M{x-R+2} {y-10} C{x-R-50} {y-40} {x-R-50} {y+30} {x-R} {y+8}" stroke="#a855f7" stroke-width="2.4" fill="none" marker-end="url(#mp)"/><text x="{x-R-30}" y="{y-36}" fill="#a855f7" font-size="10" font-weight="700" text-anchor="middle">PLEX 9−0=9</text>')
    for z,(x,y) in P.items():
        c=RC[reg(z)]; s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="#0b1220" stroke="{c}" stroke-width="2"/><text x="{x}" y="{y+7}" fill="{c}" font-size="20" font-weight="700" text-anchor="middle">{z}</text>')
    lx=760; L=[('#22d3ee','TORQUE / TIME-CIRCUIT 1 2 4 5 7 8'),('#e879f9','WARP 3 6'),('#a855f7','PLEX 0 9')]
    s.append(f'<rect x="{lx-14}" y="90" width="230" height="250" rx="6" fill="#0b1220" stroke="#1e293b"/>')
    for i,(c,t) in enumerate(L): s.append(f'<circle cx="{lx}" cy="{112+i*20}" r="6" fill="none" stroke="{c}" stroke-width="2"/><text x="{lx+14}" y="{116+i*20}" fill="{FG}" font-size="9">{t}</text>')
    rows=[('#22d3ee','solid','current (difference → tractor zone)'),('#4ade80','2 3','gate / channel (cumulation)'),('#475569','3 4','syzygy (9-sum twins)')]
    for i,(c,d,t) in enumerate(rows): s.append(f'<line x1="{lx-6}" y1="{186+i*20}" x2="{lx+10}" y2="{186+i*20}" stroke="{c}" stroke-width="2" {"" if d=="solid" else f"stroke-dasharray=\"{d}\""}/><text x="{lx+14}" y="{190+i*20}" fill="{FG}" font-size="9">{t}</text>')
    for i,t in enumerate(['Doubling cycle (2ⁿ digital roots):','1→2→4→8→7→5→1','Carriers: Katak 5::4 · Djynxx 6::3','Oddubb 7::2 · Mur Mur 8::1','Uttunul 9::0']):
        s.append(f'<text x="{lx-6}" y="{258+i*15}" fill="{MUT}" font-size="9">{t}</text>')
    s.append(f'<text x="30" y="1045" fill="{MUT}" font-size="9">Sources: ccru.net/digithype/pandemonium.htm; zone pages; repo lumpenspace/ccru@7c38ad9. Generated by scripts/svg_v2.py (Em, 1 Nov 2026).</text></svg>')
    open(os.path.join(OUT,'numogram-base10-v2.svg'),'w').write('\n'.join(s))

def cross():
    W,H=900,900; cx,cy=450,420
    pyl=[('I · CENTRE','Anamnesis','Memories &amp; Dreams',1,8,(cx,cy)),('II · RIGHT','Genesis','Creative Influences',7,2,(cx+270,cy)),
         ('III · LEFT','Apocalypse','Destructive Influences',5,4,(cx-270,cy)),('IV · CROWN','Fortune','Far Future',3,6,(cx,cy-250)),('V · ROOT','Foundation','Deep Past',9,0,(cx,cy+250))]
    s=[HEAD(W,H,'ATLANTEAN CROSS — v2','Five Pylons of the Decadology spread; Centauri Subdecadence maps each to a syzygy (light/active side · dark/passive side)')]
    for *_,(x,y) in pyl[1:]: s.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#334155" stroke-width="2"/>')
    for name,asp,gloss,lt,dk,(x,y) in pyl:
        c=RC[reg(lt)]; s.append(f'<circle cx="{x}" cy="{y}" r="78" fill="#0b1220" stroke="{c}" stroke-width="2"/>')
        s.append(f'<text x="{x}" y="{y-38}" fill="{c}" font-size="12" font-weight="700" text-anchor="middle">{name}</text>')
        s.append(f'<text x="{x}" y="{y-20}" fill="{FG}" font-size="11" text-anchor="middle">{asp}</text>')
        s.append(f'<text x="{x}" y="{y-5}" fill="{MUT}" font-size="9" text-anchor="middle">{gloss}</text>')
        s.append(f'<text x="{x}" y="{y+22}" fill="{FG}" font-size="18" font-weight="700" text-anchor="middle">{lt} <tspan fill="{MUT}" font-size="12">::</tspan> <tspan fill="#94a3b8">{dk}</tspan></text>')
        s.append(f'<text x="{x}" y="{y+42}" fill="{MUT}" font-size="8" text-anchor="middle">light {lt} · dark {dk}</text>')
    notes=['Rules [ccru.net Matrix]: Subdecadence = 40 cards (A–9 + four Queens = 0); pairs sum to 9.',
           'Each pair scores its difference; unpaired Set-1 cards score minus face value.',
           'An Aeon lasts until the first negative result; negative totals call demons by mesh number.',
           'Pylon ↔ zone mapping: repo zones.ts "centauri" field (from ccru.net zone pages).']
    for i,t in enumerate(notes): s.append(f'<text x="30" y="{835+i*15}" fill="{MUT}" font-size="9">{t}</text>')
    s.append('</svg>'); open(os.path.join(OUT,'subdecadence-atlantean-cross-v2.svg'),'w').write('\n'.join(s))

def subway():
    W,H=900,600
    st={1:(160,170),2:(320,170),4:(480,170),8:(640,170),7:(640,330),5:(480,330),3:(240,460),6:(400,460),9:(640,460),0:(800,460)}
    s=[HEAD(W,H,'NUMOGRAM TRANSIT MAP — v2','Stations = zones · Torque line runs the doubling cycle 1→2→4→8→7→5→1 · coloured spurs = currents')]
    order=[1,2,4,8,7,5]
    pts=' '.join(f'{st[z][0]},{st[z][1]}' for z in order)+f' {st[5][0]},{st[5][1]} 160,330 {st[1][0]},{st[1][1]}'
    s.append(f'<polyline points="{pts}" fill="none" stroke="#fbbf24" stroke-width="7" stroke-linejoin="round" opacity="0.85"/>')
    s.append(f'<text x="150" y="350" fill="#fbbf24" font-size="9">5 → 1 (cycle closes)</text>')
    def cur(a,b,c,lab,dx=0,dy=0,m='c'):
        (x1,y1),(x2,y2)=st[a],st[b]; X1,Y1,X2,Y2=tri(x1+dx,y1+dy,x2+dx,y2+dy,22,26)
        s.append(f'<path d="M{X1:.0f} {Y1:.0f}L{X2:.0f} {Y2:.0f}" stroke="{c}" stroke-width="3" fill="none" marker-end="url(#m{m})"/><text x="{(X1+X2)/2+8:.0f}" y="{(Y1+Y2)/2-6:.0f}" fill="{c}" font-size="10" font-weight="700">{lab}</text>')
    cur(8,7,'#22d3ee','SURGE 8→7',dx=26); cur(2,5,'#22d3ee','HOLD 2→5'); cur(4,1,'#22d3ee','SINK 4→1',dy=-34); cur(6,3,'#e879f9','WARP 6→3',m='w',dy=18)
    x,y=st[9]; s.append(f'<path d="M{x+14} {y+18} C{x+50} {y+70} {x-50} {y+70} {x-14} {y+20}" stroke="#a855f7" stroke-width="3" fill="none" marker-end="url(#mp)"/><text x="{x}" y="{y+76}" fill="#a855f7" font-size="10" font-weight="700" text-anchor="middle">PLEX 9→9</text>')
    for z,(x,y) in st.items():
        c=RC[reg(z)] if reg(z)!='torque' else '#fbbf24'
        s.append(f'<circle cx="{x}" cy="{y}" r="18" fill="{BG}" stroke="{c}" stroke-width="4"/><text x="{x}" y="{y+6}" fill="{FG}" font-size="15" font-weight="700" text-anchor="middle">{z}</text>')
    s.append(f'<text x="30" y="570" fill="{MUT}" font-size="9">Syzygies (interchanges): 1::8 Mur Mur · 2::7 Oddubb · 4::5 Katak · 3::6 Djynxx · 0::9 Uttunul. Currents: repo currents.ts; ccru.net Matrix.</text>')
    s.append(f'<text x="30" y="585" fill="{MUT}" font-size="9">Generated by scripts/svg_v2.py (Em, 1 Nov 2026).</text></svg>')
    open(os.path.join(OUT,'circular-flow-subway-v2.svg'),'w').write('\n'.join(s))
base10(); cross(); subway()
