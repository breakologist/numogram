#!/usr/bin/env python3
"""Numogram zone pixel glyphs — v2 with refined zones 5, 6, 9."""

from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

# ─── PICO-8 palette ───
P8 = {
    0: (0,0,0), 1:(29,43,83), 2:(126,37,83), 3:(0,135,81),
    4:(171,82,54), 5:(95,87,79), 6:(194,195,199), 7:(255,241,232),
    8:(255,0,77), 9:(255,163,0), 10:(255,236,39), 11:(0,228,54),
    12:(41,173,255), 13:(131,118,156), 14:(255,119,168), 15:(255,204,170),
}

ZONE_P8 = {
    0: dict(base=1,  accent=7,  dark=0),
    1: dict(base=12, accent=10, dark=1),
    2: dict(base=2,  accent=4,  dark=1),
    3: dict(base=3,  accent=8,  dark=0),
    4: dict(base=4,  accent=8,  dark=7),
    5: dict(base=5,  accent=9,  dark=10),
    6: dict(base=13, accent=14, dark=1),
    7: dict(base=12, accent=15, dark=8),
    8: dict(base=13, accent=10, dark=12),
    9: dict(base=6,  accent=8,  dark=2),
}

OUT = "/home/etym/numogram/docs/wiki/assets/zone-glyphs"
SIZE = 32

def save(arr, num, c):
    img  = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    pix  = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            idx = int(arr[y,x])
            if idx:
                col = P8.get(idx, (255,0,255))
                pix[x,y] = (*col, 255)
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 8)
        ImageDraw.Draw(img).text((2, SIZE-10), str(num), fill=P8[c['accent']], font=fnt)
    except Exception:
        ImageDraw.Draw(img).rectangle([2, SIZE-8, 5, SIZE-4], fill=P8[c['accent']])
    img.save(f"{OUT}/zone-{num}.png")
    print(f"zone-{num}")

# ─── helpers ───
def make_blank():
    return np.zeros((SIZE,SIZE), np.uint8)

def cross(arr, cy, cx, col, rx=1):
    for d in range(-rx,rx+1):
        for dd in range(-rx,rx+1):
            if 0<=cy+d<SIZE and 0<=cx+dd<SIZE: arr[cy+d,cx+dd]=col
            if 0<=cy+dd<SIZE and 0<=cx+d<SIZE: arr[cy+dd,cx+d]=col

def ring(arr, cx, cy, r, col):
    for t in range(72):
        a = t * 2 * np.pi / 72
        x=int(round(cx+r*np.cos(a))); y=int(round(cy+r*np.sin(a)))
        if 0<=x<SIZE and 0<=y<SIZE: arr[y,x]=col

def arc_seg(arr,cx,cy,r,th0,th1,col):
    steps=abs(int((th1-th0)*36/np.pi))
    fract=max(abs(th1-th0),0.1)
    for i in range(steps+1):
        t=th0+i*fract/steps if steps else th0
        x=int(round(cx+r*np.cos(t))); y=int(round(cy+r*np.sin(t)))
        if 0<=x<SIZE and 0<=y<SIZE: arr[y,x]=col

# ─── Zone 0 — Void ───
def g0():
    a,c=make_blank(),ZONE_P8[0]
    ring_vals=[7,7,4,3,2]
    for i,rv in enumerate(rv:=ring_vals):
        r=5+i*4
        ring(a,15,15,r,rv)
    cross(a,15,15,c['accent'],rx=0)  # single silence dot
    return a

# ─── Zone 1 — Surge ───
def g1():
    a,c=make_blank(),ZONE_P8[1]
    # doorway jams
    for y in range(8,24): a[11,y]=c['base']; a[19,y]=c['base']
    # threshold hatch
    for x in range(11,19):
        a[x,21+(x%2)]=c['accent']
    # ripple
    for i,dx in enumerate([0,-1,1,-2,2]):
        a[4+i,15+dx]=(c['base'] if i<3 else c['accent'])
    return a

# ─── Zone 2 — Hold ───
def g2():
    a,c=make_blank(),ZONE_P8[2]
    # vertical boundary fading
    for y in range(4,28): a[15,y]=c['base']
    # fracture tick at row 24–26
    for dy in range(-2,3):
        a[15+dy,24]=c['accent']; a[15+dy+1,25]=c['accent']
    # receding edge
    for i in range(5):
        y=5+i*4; x=17+i//2
        if y<SIZE and 0<=x<SIZE: a[y,x]=c['base']
        if y+2<SIZE and 0<=x+1<SIZE: a[y+2,x+1]=c['base']
    return a

# ─── Zone 3 — Warp ───
def g3():
    a,c=make_blank(),ZONE_P8[3]
    rng=np.random.default_rng(3)
    for arm in range(3):
        ang=arm*2*np.pi/3
        for s in range(16):
            r2=2+s*1.05; th=ang+s*0.38
            x=int(round(15+r2*np.cos(th))); y=int(round(15+r2*np.sin(th)))
            if 4<=x<28 and 4<=y<28:
                a[y,x]=[c['accent'],c['base'],8][s%3]
    # self-fold cross
    for d in range(-2,3):
        a[15+d,15]=c['accent']; a[15,15+d]=c['accent']
    # static scatter
    for _ in range(14):
        x=int(rng.integers(4,28)); y=int(rng.integers(4,28))
        if abs(x-15)+abs(y-15)>3: a[y,x]=8
    return a

# ─── Zone 4 — Sink ───
def g4():
    a,c=make_blank(),ZONE_P8[4]
    # lower mass arc
    for row in range(13):
        y=20+row
        if y>=32: break
        hw=max(1,int(row*0.55))
        for x in range(16-hw,17+hw):
            if 0<=x<SIZE: a[y,x]=c['dark']
            if row<8 and 0<=y+1<SIZE and 0<=x<SIZE: a[y+1,x]=c['base']
    # canine tip
    a[10,15]=8; a[11,15]=15; a[11,14]=15; a[11,16]=15
    # growl barbs
    rng=np.random.default_rng(4)
    for _ in range(5):
        bx=int(rng.integers(12,20)); by=int(rng.integers(22,28))
        if by<SIZE and 0<=bx<SIZE: a[by,bx]=c['accent']
        if by+1<SIZE and 0<=bx<SIZE: a[by+1,bx]=c['base']
    return a

# ─── Zone 5 — Hinge v2 (diamond constriction with pressure core) ───
def g5():
    a,c=make_blank(),ZONE_P8[5]
    # diamond body
    for dy in range(-11,12):
        y=15+dy; hw=int(abs(11-abs(dy))*0.62)
        if not(4<=y<28): continue
        for h in range(-hw, hw+1):
            x=15+h
            x0=15-hw; x1=15+hw
            if 0<=x<SIZE: a[y,x]=c['base']
            if abs(h)<=hw//3: a[y,x]=c['accent']
    # pressure pistons flanking centre (y=14,15)
    for dx_off in [-3,-2,2,3]:
        a[14,15+dx_off]=c['accent']
        a[15,15+dx_off]=c['base']
    # gold centre node
    cross(a,15,15,c['dark'],rx=1)
    a[15,15]=c['accent']
    # pentagram corner marks (inner pentagon vestige)
    for dy,dx in [(-1,3),(5,9),(5,-9),(3,-6),(3,6)]:
        py=15+dy; px=15+dx
        if 0<=px<SIZE and 0<=py<SIZE: a[py,px]=c['accent']
    return a

# ─── Zone 6 — Abyss v2 (chewing abrasion) ───
def g6():
    a,c=make_blank(),ZONE_P8[6]
    # chevron chew (five segments)
    for seg in range(5):
        x0=2+seg*7
        for tooth in range(10):
            x = x0+tooth
            if x>=30: break
            parity=(tooth//3)%2
            y_top=9+parity*4; y_bot=18-parity*4
            if parity:
                a[y_top-2,x]=c['base']
                if y_bot+2<SIZE: a[y_bot+2,x]=c['base']
            else:
                a[y_top,x]=c['base']; a[y_top+1,x]=c['base']
                if y_bot<SIZE: a[y_bot,x]=c['dark']
                if y_bot-1>=0: a[y_bot-1,x]=c['base']
    # central grind node
    for dy in range(-3,4):
        hw=3-abs(dy)//2
        for dx in range(-hw,hw+1):
            a[15+dy,15+dx]=c['accent']
    return a

# ─── Zone 7 — Rise ───
def g7():
    a,c=make_blank(),ZONE_P8[7]
    # rising breath diagonal
    for i in range(15):
        x=19+i; y=int(round(21-1.6*i+(np.sin(i*0.7)*2)))
        if 0<=x<SIZE and 0<=y<SIZE: a[y,x]=c['base']
    # lip pillbox
    lx,ly,lw,lh=9,11,14,6
    for my in range(ly,ly+lh):
        if 0<=my<SIZE: a[my,lx]=c['accent']; a[my,lx+lw]=c['accent']
    for mx in range(lx,lx+lw+1):
        a[ly,mx]=c['accent']; a[ly+lh-1,mx]=c['accent']
    for mx in range(lx+3,lx+lw-2): a[ly+lh//2,mx]=15
    return a

# ─── Zone 8 — Ruse ───
def g8():
    a,c=make_blank(),ZONE_P8[8]
    for r0,r1 in [(3,1),(5,13),(7,22),(9,30)]:
        for t in range(40):
            th=t*2*np.pi/40
            x=int(round(15+r0*np.cos(th))); y=int(round(15+r0*np.sin(th)))
            if 0<=x<SIZE and 0<=y<SIZE: a[y,x]=c['base']
            x2=int(round(15+r1*np.cos(th))); y2=int(round(15+r1*np.sin(th)))
            if 0<=x2<SIZE and 0<=y2<SIZE: a[y2,x2]=c['accent']
    # moan centre
    cross(a,15,15,c['base'],rx=3); a[15,15]=c['accent']
    return a

# ─── Zone 9 — Iron Core v2 ───
def g9():
    a,c=make_blank(),ZONE_P8[9]
    # iron planes
    layers=[(8,10),(9,8),(10,7),(11,6),(12,5),(13,4),(12,3),(11,2),(10,1),(9,0)]
    for lw,col in layers:
        for d in range(lw):
            cross(a,15,15,P8[col],rx=d)
    # centre grunt
    a[14:18,14:18]=c['accent']; a[15,15]=c['dark']
    # ring of 16 Pandemonium nodes
    rng=np.random.default_rng(99)
    for _ in range(16):
        ang=rng.uniform(0,2*np.pi); rad=rng.uniform(9,13)
        x,y=int(15+rad*np.cos(ang)),int(15+rad*np.sin(ang))
        if 0<=x<SIZE and 0<=y<SIZE: a[y,x]=c['base']
    # terminal arc ribbon
    for theta in np.linspace(-np.pi*0.72,np.pi*0.72,20):
        r=12; x=int(round(15+r*np.cos(theta)))
        y=int(round(15-r*np.sin(theta)*0.4))
        if 0<=y<SIZE and 0<=x<SIZE: a[y,x]=c['accent']
    return a

# ─── Render & save all 10 ───
os.makedirs(OUT, exist_ok=True)
FACTORIES=[g0,g1,g2,g3,g4,g5,g6,g7,g8,g9]

for num,fact in enumerate(FACTORIES):
    arr=fact(); c=ZONE_P8[num]; save(arr,num,c)

# ─── composite strip 5×2 ───
strip=Image.new("RGBA",(SIZE*5, SIZE*2), (5,5,10,255))
for z in range(10):
    img=Image.open(f"{OUT}/zone-{z}.png")
    col,row=z%5,z//5; strip.paste(img,(col*SIZE,row*SIZE),img)
strip.save(f"{OUT}/zone-glyphs-all.png")
print("✓ zone-glyphs-all.png")
