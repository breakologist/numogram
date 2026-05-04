# Triad–Syzygy Tetralogue — Voices on Tracker Harmony & the Numogram

> **Setting:** After the ModArchive corpus revealed triadalism as a structural invariant, four numogram voices convene to interpret the correspondence between triadic harmony and zone motifs. Data source: [[tracker-music-theory-mappings]] (triad → zone tables at octave 4) and [[modarchive_analysis_report]].

## The Speakers

- **Oracle** — Keeper of canonical mappings, aware of syzygy chains and digital‑root laws.
- **Builder** — Engineer of `mod-writer`, concerned with implementable constraints.
- **Writer** — Chronicler of scene lore, attuned to cultural semantics and hyperstition.
- **Gamer** — Player of the roguelike, sensitive to texture, tension, and moment‑to‑moment affect.

---

## Dialogue


**Oracle:** The triad is the atomic circuit of tracker harmony. Three pitches, three zones — a triangle inscribed on the numogram circle. Our calculation yields the zone sets for every major and minor triad at reference octave 4 (see [[tracker-music-theory-mappings]]). Observe: most triads project onto 2–3 distinct zones. A three‑zone set is a *triangular syzygy*; a two‑zone set is a complementary pair. Yet the Warp motif (zones 7–9) rarely appears as a pure triangle at this octave. Why does chippy, built on a B‑minor triad, classify as Zone 3 and syzygy djynxx (3::6)? The answer lies in register displacement.

**Builder:** Precisely. The zone function `note_to_zone()` is not pitch‑class only; it includes the octave term. A B‑minor triad voiced low (B4, D5, F♯5) yields zones [4,6,9] — Hold, Sink, Plex. But when the triad is shifted an octave higher (B5, D6, F♯6), we obtain [9,3,7] — Plex, Warp, Rise. High‑register voicings inject Warp and Rise zones. This explains the Warp‑Seeking classification of pieces that use B‑minor: they place the triad in the upper staff to exploit zone migration. The mod‑writer can enforce this via an `octave_offset` parameter per channel.

**Writer:** The B‑minor triad is the *Warp seed* for a reason beyond zone arithmetic. It is the triad of the djynxx current — a hyperstitional harmonic virus that propagates through the demo scene. Its latent message: D (zone 6) and F♯ (zone 4?) Actually, in chippy the triad is wrapped in a tremolo texture, making the zones resonate at a frequency of 3::6 — that is, 3 and 6 are complementary (9‑3=6). The Warp is not a zone but a current flowing between complementary gates. The triad provides the three nodes of that current: root (origin), third (displacement), fifth (return). B‑minor’s particular shape — a minor third below the root and a perfect fifth above — aligns with the Warp's folded topology when the root is placed at the threshold of register (B4 near the top of the low octave).

**Gamer:** For the player, the triad’s zone distribution is felt as *texture density* and *register fatigue*. Low triads (e.g., C‑minor at octave 4 → zones 2,4,7) produce a dense mid‑range cloud that feels like navigating a Hold corridor — predictable, enclosing. High triads (e.g., B‑minor voiced at octave 6) pierce the high register, generating Warp‑Seeking tension: the player hears bright dissonance that resolves only by descending, placing them in a Sink‑Seeking loop. The 4‑channel constraint amplifies this: channel 3 reserved for the triad’s fifth, leaving channel 2 free for an arpeggiated effect that reinforces the underlying syzygy by echoing the zone progression (e.g., zone 6 → zone 3 → zone 9 in rapid succession).

**Oracle:** Let us synthesize. The 24 triad zone sets (at octave 4) enumerate the possible triangular syzygies:

| Triad | Zone set | Syzygy type |
|---|---|---|
| B‑minor | [4,6,9] | mixed (Hold+Sink+Plex) — high‑octave displacement yields Warp‑adjacent |
| D‑minor | [4,6,9] | same as B‑minor (enharmonic equivalence via zone symmetry) |
| C‑major | [2,4,8] | mixed (Hold+Sink+Rise) |
| F♯‑minor | [1,4,8] | triangular 1::4::8 — a complete syzygy across Sink‑Hold‑Rise |
| E‑major | [3,6,8] | triangular 3::6::8 — partial Warp cluster (3 and 6 are Warp pair, 8 Rise) |

Only a few triads yield a *pure* three‑zone syzygy (three distinct zones without repetition). These are candidates for strict motif enforcement. For example, F♯‑minor (1,4,8) combines Sink, Hold, Rise — a balanced traversal. Conversely, triads that collapse to two zones (like B‑minor at low octave) are degenerate syzygies, which can be amplified by octave lifting into three‑zone triangles.

**Builder:** Implementable rule for `mod-writer`: `triad_motif_policy(motif, root, voicing)`. Given a desired motif, choose a triad whose zone set (computed per voicing) maximally overlaps the target zone range. Warp: target zones {7,8,9}; highest overlap wins. We pre‑compute a candidate table across root_octave ∈ {3,4,5,6}. E.g., Warp best match at octave 5: B‑minor (9,3,7) → 2/3 zones in Warp+Rise; D‑major at octave 5 yields [?, check]... The writer then constrains the pattern generator to voice the triad within that octave band.

**Writer:** This is not merely engineering; it is *hyperstitional grammar*. Each triad encodes a historical echo: B‑minor appears in `chippy`, the seminal Warp seed of the Russian demoscene. By reproducing that triad‑zone alignment, we re‑enact the original current. Thus, `mod-writer` becomes a ritual engine: given a desired syzygy, it selects the appropriate triad and voicing, thereby making the gate speak through newly generated modules. The lore page should cross‑link each generated piece to its underlying triad and the canonical track that seeded it.

**Gamer:** From the player’s perspective, the mixture of zones produces a characteristic *feel*: triads that span Hold+Rise generate forward momentum (useful for ascent runs); triads heavy in Sink invite contemplation, slowing the crawl. In a roguelike, this translates to zone‑dependent soundtrack tiers: when the agent enters a Warp‑heavy region, the music shifts to high‑voiced B‑minor or D‑major triads; in Hold corridors, C‑major or A‑minor anchor the middle range. Audio feedback thus becomes a compass, not just decoration.


---

*Tetralogue recorded: 2026‑04‑29 | References: [[tracker-music-theory-mappings]], [[tracker-composition-principles]], [[numogram-overview]]*