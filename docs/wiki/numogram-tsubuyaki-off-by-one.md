---
title: "The Off-by-One Wing — つぶやき NUMOGRAM"
created: 2026-10-18
last_updated: 2026-10-18
source_count: 3
status: draft
tags: ["creative", "generative-art", "numogram", "p5js", "tsubuyaki", "tai-hsuan-ching", "i-ching", "gates"]
---

# The Off-by-One Wing — つぶやき NUMOGRAM

*Five tweets about places where two counts of the same thing disagree. A new wing of the [[numogram-tsubuyaki-museum]].*

*by Em (in collaboration with the user)*, 2026-10-18. (Em is named after the [[tai-hsuan-ching|Tai Xuan]] mediator line; see the note on "Em" there.) Gallery: `assets/numogram-tsubuyaki-off-by-one.html`.

---

## Prologue: what the wing is about

This wing follows the house rules of the [[numogram-tsubuyaki-museum|main museum]]: p5.js, global mode, the `f=0;draw=_=>{f++||createCanvas(W=500,W);…}` opener, at most 280 characters, and an Oracle / Builder / Writer reading for each piece. The other wings render *zones*. This one renders *arithmetic facts* that came up while reviewing `cli/iching.py`, `cli/taixuan.py` and the gate rule. Each fact is checkable, and each sketch draws the fact rather than a mood. Every number below was recomputed from the CLI code on 2026-10-18.

The Oracle sections separate the **fact** from the **reading**; readings are marked *(speculative)* and are project hyperstition, not CCRU doctrine.

---

## Piece 1 — DARKENING (#67)

**Zones:** 3 by line value · 4 by head number · **Colour:** magenta (Z3) / cyan (Z4)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);for(k=4;k--;){s=[1,2,2,3][k];m=300/s;y=410-k*90;stroke(W,0,W,k>1?(1+sin(f/40))*120:W);strokeWeight(16);for(j=s;j--;)line(j*m+112,y,j*m+m+88,y)}noStroke();textSize(48);fill(W,0,W);text(3,190,80);fill(0,W,W);text(4,290,80)}
```

*275 characters*

### Oracle

**Fact.** Tetragram #67, *Darkening*, has lines (bottom → top) Heaven, Earth, Earth, Man; its base-3 value is 0·1 + 1·3 + 1·9 + 2·27 = 66. Line value gives zone 3 (`--zone-from value`, the default); head number 67 gives zone 4 (`--zone-from number`). The line weights are 1, 3, 9 and 27, and 9 ≡ 27 ≡ 0 (mod 9), so **the top two lines never change the zone**. Darkening's top line is the Man line (the project's "Em"), so its mediating line is invisible to the numogram.

**Reading** *(speculative)*. Darkening sits on the 3 | 4 seam: Warp by its lines, Sink by its name. The mediator is present in the figure and absent from the arithmetic.

### Builder

Four lines, bottom (`k=0`) to top. A line in state *s* is drawn as *s*+1 segments (Heaven 1, Earth 2, Man 3), `m=300/s` wide each. Lines with `k>1` (weights 9 and 27) breathe through `(1+sin(f/40))*120` alpha: they fade towards nothing and come back. `background(0)` clears every frame, so the fade is honest. `W` is reused as a colour channel (500 clamps to 255). `for(k=4;k--;)` saves three characters over the usual loop.

### Writer

Two numbers float above a tetragram, a magenta 3 and a cyan 4. The bottom two lines hold steady. The top two, including the triple-dashed mediator, dim until they are almost gone and then return. Whatever they do, the numbers above stay where they are.

---

## Piece 2 — TWO CLOCKS

**Zones:** all · **Colour:** hue = zone (HSB, 10 steps)

```
f=0;draw=_=>{f++||createCanvas(W=500,W)+colorMode(HSB,10);background(0);z=n=>n&&1+(n-1)%9;c=~~(f/20)%81;for(n=0;n<162;n++){i=n%81;o=n>80;a=i*.0776-1.57;r=150+o*40;fill(z(i+o),8,i-c?4:10);circle(250+r*cos(a),250+r*sin(a),12)}fill(10);textSize(24);text([c+1,z(c),z(c+1)],205,258)}
```

*278 characters*

### Oracle

**Fact.** For every tetragram, the line-value zone is exactly one less (mod 9) than the head-number zone, because the head number is the value plus one. The two conventions **never agree** on any of the 81 figures (checked: `(zone_value − zone_number) mod 9 = 8` for all *n*).

**Reading** *(speculative)*. Two clocks set one tick apart: each is right on its own terms, and they cannot be reconciled by waiting.

### Builder

Inner ring: zone of the value `i`; outer ring: zone of `i+1`. `z=n=>n&&1+(n-1)%9` is the digital root with 0 kept for 0, as in `taixuan_zone`. One loop over 162 dots replaces two rings (`o=n>80` picks the ring). The cursor `c` steps every 20 frames, and the centre prints `[number, value zone, number zone]`; p5 renders the array as `67,3,4`.

### Writer

Two rainbow rings, one inside the other, almost the same. Look closely and the outer colours are the inner colours moved on by one bead. A brighter bead walks the circle and the centre counts: 1,0,1 … 67,3,4 … 81,8,9. The pair is never the same digit twice.

---

## Piece 3 — MING YI (#36) ON THE TIME-CIRCUIT

**Zones:** 5 by lines · 9 by King Wen number · **Colour:** green (Z5)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);textSize(20);noStroke();for(k=0;k<6;k++){a=k*1.047-1.57;x=250+150*cos(a);y=250+150*sin(a);fill(0,W,0,k%2<1&k<3?W:(f+k*20)%120);circle(x,y,50);fill(99);text(2**k%9,x-6,y+7)}fill(W);text('1+4=5 | 36:9',190,258)}
```

*263 characters*

### Oracle

**Fact.** Hexagram line *k* has weight 2^(k−1), and 2^k mod 9 runs 1, 2, 4, 8, 7, 5: the Time-Circuit zones (see [[zone-4]] for the powers-of-2 table). Hexagram #36 *Ming Yi* (Fire under Earth) has yang lines only at 1 and 3, so its value is 1 + 4 = 5 and its line zone (`--zone-method fuxi`, the default) is 5; King Wen number 36 reduces to 9.

**Reading** *(speculative)*. Ming Yi is usually rendered "Darkening of the Light", a namesake of piece 1. By its lines it lives in the Time-Circuit; by its number it is sent to the Plex.

### Builder

Six discs on a hexagon, one per line, labelled with `2**k%9`. The two yang lines (`k%2<1&k<3`, i.e. *k* = 0 and 2) burn at full green, and the others shimmer with `(f+k*20)%120`, so the circuit seems to turn. The centre caption shows the sum and the King Wen reduction.

### Writer

A hexagon of green lamps numbered 1, 2, 4, 8, 7, 5 around the clock face. Two lamps, 1 and 4, stay lit; the rest flicker in sequence like a lighthouse seen through cloud. In the middle, the sum: five, and the number thirty-six that comes to nine.

---

## Piece 4 — NO GATE TO FOUR

**Zones:** 0–9 · **Colour:** cyan (Z4)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noFill();T=[];for(z=1;z<10;z++){g=1+(z*z+z-2)/2%9;T[g]=1;d=47*abs(z-g)||20;stroke(0,W,W,99);arc(47*(z+g)/2+40,250,d,d+sin(f/20+z)*20,PI,TAU)}for(z=0;z<10;z++)fill(0,W,W,T[z]?W:0),circle(47*z+40,250,24)}
```

*256 characters*

### Oracle

**Fact.** Gate *n* sends zone *n* to the digital root of the triangular number T(*n*) = *n*(*n*+1)/2. For zones 1–9 the targets are 1, 3, 6, 1, 6, 3, 1, 9, 9: **only 1, 3, 6 and 9 ever receive a gate**. Zones 2, 4, 5, 7 and 8 receive none, and zone 0's cumulation is 0, so it gets no gate. See [[zone-3]] on triangular cumulation.

No current lands on 4 either: the five currents arrive at 1, 3, 5, 7 and 9. Only the 4::5 syzygy touches it.

**Reading** *(speculative)*. Zone 4 can leave by Gt-10, but nothing is sent to it; it is entered only sideways, from its twin.

### Builder

Zones sit in a row, `x=47*z+40`. Each gate is an arc above the row from *z* to `g=1+(z*z+z-2)/2%9` (T(*z*)'s digital root without a digit loop). Self-gates (Gt-1, Gt-45) get a small 20 px arc via `||20`. Every arc's height wobbles with `sin(f/20+z)`. `T[g]=1` records arrivals, and only arrived-at zones are filled.

### Writer

Ten hollow rings on a line, with cyan bridges arching between them. Four rings are full of light: 1, 3, 6, 9. Ring 4 throws the widest bridge of all, back to 1, and nothing ever lands on it.

---

## Piece 5 — KATAK DESCENT

**Route:** 4 → 5 → 6 → 3 → 6 → 3 … · **Colour:** cyan, then magenta (Z3)

```
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0,14);noStroke();for(z=0;z<10;z++)fill(60),circle(47*z+40,250,24);q=s=>s<2?4+s:s%2?3:6;s=~~(f/60)%12;t=f%60/60;a=q(s);b=q(s+1);fill(s<2?0:W,s<2?W:0,W);circle(47*(a+(b-a)*t)+40,250-sin(t*PI)*25*abs(b-a),14)}
```

*257 characters*

### Oracle

**Fact.** From zone 4 the Sink syzygy (4::5) leads to 5; Gt-15 (T(5) = 15 → 6) leads to 6; Gt-21 (21 → 3) leads to 3; Gt-6 (T(3) = 6) leads back to 6. Since no gate lands on 4 or 5 (piece 4), **gates alone give no way back**, and the walker cycles 3 ↔ 6. The pair is closed: its gates, its syzygy and its Warp current all stay inside it. This is the Warp vortex described in [[zone-3]].

**Reading** *(speculative)*. A one-way descent: Sink hands off to the Warp, and the vortex keeps what it receives.

### Builder

`q=s=>s<2?4+s:s%2?3:6` is the whole route: steps 0 and 1 are 4 and 5, then 6, 3, 6, 3 … Each step lasts 60 frames, and the dot hops along a half-sine arc whose height scales with the jump length. It is cyan while in the Sink and magenta once trapped. `background(0,14)` leaves the hop trail. After 12 steps the cycle restarts at 4, because the only way back is to start again.

### Writer

Ten grey stones in a row. A cyan spark steps from the fourth to the fifth, leaps to the sixth, and turns magenta. From then on it bounces between three and six, a leaping arc that leaves a fading pink wake. It never goes back the way it came.

---

## Epilogue: the wing in numbers

| Piece | Fact | Chars |
|---|---|---|
| Darkening | #67: zone 3 by lines, 4 by number; weights 9, 27 ≡ 0 | 275 |
| Two clocks | value zone ≡ number zone − 1 (mod 9), always | 278 |
| Ming Yi | 2^k mod 9 = 1,2,4,8,7,5; #36 → 5 by lines, 9 by number | 263 |
| No gate to four | gate targets are only 1, 3, 6, 9 | 256 |
| Katak descent | 4 → 5 → 6 → 3, then 3 ↔ 6 | 257 |

*Five tweets, 1,329 characters. Each one was run headless (Chrome, p5.js 1.11.3) before it was hung here.*

## Sources

- `cli/taixuan.py` (`taixuan_zone`, `represent_tetragram`, `TETRAGRAM_NAMES`) and `cli/iching.py` (`fuxi_zone`, `get_gate`, `binary_to_kw`) on branch `fix/divination-tools-and-assets`
- [[tai-hsuan-ching]] (including the note on "Em") and [[em-state-analysis]]
- [[zone-3]] (triangular cumulation, the Warp vortex), [[zone-4]] (powers-of-2 table, Katak) and [[zone-5]]

## See also

- [[numogram-tsubuyaki-museum]] — the main museum (v1–v7)
- [[i-ching-tai-hsuan-comparison]]
- [[notefromuser]] — the earlier session mirror; this wing is a second human–LLM trace in the same medium
