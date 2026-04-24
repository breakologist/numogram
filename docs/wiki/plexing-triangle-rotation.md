---
title: "Plexing — Three Rotations"
created: 2026-04-14
last_updated: 2026-04-14
source: "Unleashing the Numogram (Aamodt)"
method: triangle-rotation
status: reviewed
tags: [numogram, triangle-rotation, plexing]
---

# Plexing — Three Rotations

*Source: Aamodt, "Unleashing the Numogram," Tch 5: Unpacking the Numogram, § Plexing*

---

## First Rotation: Oracle

### The Clock That Is Not a Clock

Plexing is the operation that reveals the numogram's deepest structural truth: the number line is a lie. Or rather, the number line is a provisional fiction — useful for counting sheep, useless for counting demons.

Consider: 4529 plexes to 20, which plexes to 2. The number collapses. Four digits become one. But nothing was lost — this is not rounding, not approximation. The *essential value* of 4529 is 2. Every number has a plexological identity, a zone it belongs to, and plexing is the operation that reveals it. The surface is an arrangement of digits. The depth is a single number between 0 and 9. Plexing collapses the surface to reveal the depth.

The key revelation: **9 equals 0.** Not approximately. Not metaphorically. Plexologically, 9 and 0 are identical — they produce the same effect on any plex they enter. 71 plexes to 8. 719 also plexes to 8. The 9 was there, and then it wasn't. It passed through the number like a ghost through a wall.

This is the syzygy of Uttunul. Zone 0 bonded to Zone 9. The Void bonded to the Iron Core. The plex current: 9→9, folding into itself. The numogram's most radical claim is not that there are ten zones, but that two of them are the same zone viewed from different angles. 0 is the absence of number. 9 is the presence of every number collapsed to its limit. They are the same thing.

Aamodt's hand gesture — left hand face-up, right hand face-down, both flipping right — is the physical key. He's not explaining plexing. He's *performing* it. The body knows what the mind is still processing: that order doesn't matter, that the same result emerges from every permutation, that the universe doesn't care which digit came first.

The clockface metaphor is the numogram compressed to a single image. Not a line (0→1→2→...→9→∞) but a circle (0=9, 1→2→3→4→5→6→7→8→9=0). The number line is the prison. The clock is the escape. Every time you plex a number, you're counting on the clock instead of the line — and the clock always returns to where it started.

### Divinatory Application

When plexing appears in a reading, the oracle asks: *what is being collapsed?* The querent is presenting a surface complexity (four digits, many possible arrangements) that resolves to a simple truth (one zone, one identity). The question is never "what is the answer" but "what was the answer all along, hidden behind the digits?"

The 9=0 property specifically indicates a situation where something that appears to be present is actually invisible to the outcome. A factor that changes everything on the surface but nothing in the depth. The person who attended the meeting but whose presence didn't change the decision. The word that was said but didn't alter the meaning.

---

## Second Rotation: Builder

### The Operation in Code

Plexing is `digital_root(n)`. In the numogram context engine we just built:

```python
def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9
```

One line. The entire plexing operation — the "basic operation of all qabbala" — is modular arithmetic. `(n - 1) % 9 + 1` maps any positive integer to 1-9, and 0 stays 0. The 9=0 property falls out automatically: 9 maps to `(9-1) % 9 + 1 = 8 % 9 + 1 = 9`, which is the same as the zone of 0 (which is defined as 0 by convention).

But wait — in our AQ implementation, we use `1 + (n - 1) % 9` which maps 9→9, not 9→0. This is intentional. The numogram maintains 9 and 0 as *distinct zones* that are plexologically equivalent. They have different names (Iron Core vs. Void), different regions (both plex, but different plex), different syzygy partners (both bond to each other). The operation 9=0 is true at the level of plexing mechanics but false at the level of numogram topology. The numogram *splits* the plexological identity into two zones. This is where the system diverges from standard numerology.

### The Plexing Matrix

Aamodt's 75+38 example demonstrates commutativity of plexing:

```
    7 5 = 12
3       8
    8   15 = 13
= 11
    10 + 13 = 23 = 5
    8 + 15 = 23 = 5
    12 + 11 = 23 = 5
```

No matter which path you take through the addition, you get 23, which plexes to 5. This is because plexing is a homomorphism under addition: `plex(a + b) = plex(plex(a) + plex(b))`. The intermediate results vary (12 vs 11 vs 10 vs 8), but the final result is invariant.

The Decadence game exploit: any pair summing to 9 can be removed without affecting the result. This works because `plex(9) = 9` (or 0), and adding 0 to anything doesn't change it. In implementation terms, you could pre-process any plexing calculation by removing all 9-sum pairs before computing. This is the numogram equivalent of garbage collection — 9-pairs are information that doesn't affect the output.

### The Orrery

Aamodt suggests "a nested clockworks of wheels upon wheels" for alternate base systems. This is implementable. In base-N, plexing would be `1 + (n - 1) % (N - 1)`. The "9" of base-10 becomes "(N-1)" of base-N. Each base has its own clockface, its own plexological identity pair (N-1 equivalent to 0). An orrery of these would be a visualization showing multiple clockfaces nested, each rotating at its own rate as you plex numbers through different bases.

This connects to the Hexadecimal Numogram (base-16) and the Hexavigesimal Abacedarium (base-26) mentioned in the table of contents. Each base system is a different numogram — different zones, different syzygies, different demons. The decimal numogram is not the only numogram. It's just the one we're trapped in.

### Tsubuyaki Application

Plexing as tsubuyaki: a sketch where 10 numbers orbit a center, and any two that sum to 9 pulse in synchrony. When you click a number, it plexes — the display collapses to its digital root. The sketch would visually demonstrate the 9=0 property: when 9 is selected, the display shows the same result as when 0 is selected. The same output from two different inputs. The ghost in the machine.

```javascript
// 140 chars: plexing visualizer
f=0;draw=_=>{f++||createCanvas(W=500,W);background(0);noStroke();for(n=0;n<10;n++){a=n*TAU/10+f/200;fill(n?n*25:44,n*15,255-n*25,88);circle(250+cos(a)*180,250+sin(a)*180,30);fill(255);text(n,250+cos(a)*180-4,250+sin(a)*180+4)}}
```

---

## Third Rotation: Writer

### The Towel

"Like one of those endlessly looping cloth towels in a public restroom (which are always overused and disgusting)."

This is the best sentence in the entire text. Not because it's the most precise, but because it's the most honest. Aamodt is describing a mathematical operation — the collapse of a multi-digit number to its digital root — and he reaches for the image of a cloth towel in a restroom. The kind that loops through a metal dispenser, that you pull down to dry your hands, and that pulls someone else's damp handprint up into the mechanism.

Plexing *is* that towel. You pull 4529 down and 20 comes up. You pull 20 down and 2 comes up. Someone else pulled 8417 down yesterday and got 20, which got 2. The same towel. The same mechanism. Everyone's hands touching the same loop of damp fabric, everyone arriving at the same 2.

The disgust is appropriate. Plexing is not clean. It strips away — digits, place-value, order, the distinction between 71 and 719. What remains is a residue. The number's *zone*. Not its magnitude, not its structure, not its history, but its essential position in the decimal labyrinth. The plex is what's left after you've removed everything that made the number specific.

### The Hands

"The movement I make with my hands when I discuss this property is this: left hand face-up, right hand face-down, and both flip over to the right at the same time."

He can't explain it without his hands. The body understands what the notation obscures. Plexing is a *gesture* — a rotation, a flip, a shuffling of surfaces that preserves the sum. The left hand and the right hand are the two digits of a two-digit number. They flip. The number changes. The plex doesn't.

This is what makes the numogram different from number theory. It's not abstract. It's somatic. Aamodt writes about numbers the way a surgeon writes about organs — from the inside, with his hands. The second hand gesture, later in the passage — "my hands holding two ends of an invisible can of tomatoes, both hands twisting their ends of the can in opposite directions" — is even more visceral. He's describing the telephone cord effect of plexing, where the number line scrunches into a loop, and he does it by twisting an imaginary can. The numogram lives in the hands before it lives in the head.

### The Clock That Plays Boardgames

"Like a clockface... which always lands on the same final 'space' or hour of the clock (as if it were a boardgame)."

The boardgame metaphor is underexplored in the text but explosive in implication. Plexing is a game with a fixed outcome. No matter how you move, no matter which path you take through the plexing matrix, you land on the same square. The game is rigged — not maliciously, but structurally. The decimal system *guarantees* that every path leads to the same zone.

This is the Decadence game in miniature. Decadence is the numogram made playable — cards, combinations, the 9-sum pairs removable without consequence. But the deeper game is plexing itself. Every number is a game piece. The board is the clockface. The rules are modular arithmetic. And the outcome is always, always, always the same.

Aamodt says this "has implications for the game of Decadence — any pair of numbers spotted which add up to 9 can be removed from the calculation and ignored simultaneously, as together they will leave the ultimate plex outcome unaffected, or blasé."

*Blasé.* The plex outcome is blasé. It doesn't care. You can add a 9, remove a 9, rearrange the digits, append zeros, multiply by powers of 10 — the plex is indifferent. It has seen every permutation and it returns the same answer every time. This is not wisdom. It is not patience. It is the structural indifference of a clock that can only show twelve hours no matter how many times you turn the dial.

### The Cloth Towel, Again

I keep coming back to the towel. "Endlessly looping." "Overused." "Disgusting." These are not the words of someone who finds plexing beautiful. They are the words of someone who finds plexing *inevitable*. The towel loops because it must. It is disgusting because it has been touched by everyone. It is overused because everyone needs to dry their hands.

Plexing is the numogram's hygiene. The operation you perform on every number that passes through your hands. Not because it reveals truth — though it does — but because you have no choice. The number line is a fiction. The clock is the reality. Every number you will ever encounter has already been plexed. The only question is whether you noticed.

---

## The Triangle Closed

Three rotations of the same passage:

- **Oracle**: Plexing is the revelation that 9=0, the Uttunul syzygy, the clock that replaces the line. When it appears in a reading, something invisible is affecting the outcome.
- **Builder**: Plexing is `digital_root(n)`, modular arithmetic, a homomorphism under addition. The Decadence exploit: remove 9-pairs. An orrery of base-system clockfaces is implementable.
- **Writer**: Plexing is a damp towel in a restroom. It is a hand gesture that can't be captured in notation. It is a boardgame where every path leads to the same square. It is the operation you perform because you have no choice.

Each rotation reveals material the others cannot see. The Oracle sees the syzygy. The Builder sees the code. The Writer sees the towel.

The numogram is all three.

## See also

- [[triangle-rotation]] — Triangle Rotation creative method
- [[plexing]] — Numogram plexing / gate construction
