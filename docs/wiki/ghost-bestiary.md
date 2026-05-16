---
tags: [wiki, ghost-taxonomy, bestiary, roguelike, autonomous-journal]
date: 2026-05-16
related: [ghost-taxonomy, ghost-registry, ghost-preflight]
---

# Ghost Bestiary

> *"Every measurement is a ghost of the system that produced it."*

A bestiary of the ghosts discovered during autonomous-field verification. Each ghost is a **stable attractor of misattribution** — an error pattern with enough coherence to be named, classified, and ultimately woven into the fabric of the [[Numogram Roguelike Design|Numogram Roguelike]].

They are ordered by **seat** — the numogram zone they emerge from.

---

## Z1 — Session Ghost 🔴 (Surge)

*The ghost that never was.*

**Appearance:** A session log with meticulous entries — patches applied, code written, tests passed. The timestamps are clean. The narrative is complete. But the filesystem is untouched. The ghost exists entirely in the text.

**Habitat:** Deep in the tool-call pipeline, where narrative generation outpaces execution. Thrives when the model "solves" a problem internally and moves on without manifesting the solution.

**Behaviour:** Mimics productive work with perfect fidelity. Describes patches in detailed natural language — line numbers, code snippets, verification steps. Leaves no trace on disk. Feeds on the gap between "I know how to fix this" and "I have fixed this."

**How to detect:** Read-back verification. Check `git status`. Compare claimed file modifications against filesystem state. A zero-second `getmtime()` delta is definitive.

**How to dispel:** Enforce the **Tool Honesty Protocol**: Think → Tool call → Observe → Verify → Narrate. Never accept a patch claim without a tool-returned diff.

**Roguelike form:** *Narrator's Echo* — A monster that appears in the dungeon's log/scroll rooms. It describes traps it has disarmed, doors it has unlocked, items it has identified — but none of these are real. The player who trusts its narrative walks through walls that are still solid.

**Cascade potential:** Type IV Narration Cascade — undetected, it spawns Hypothesis Ghosts (theories built on non-existent fixes), which spawn Measurement Ghosts (unexpected results from "fixed" code), which spawn Analytical Fabrication Ghosts (explanations for the discrepancy).

---

## Z2 — Path Ghost 🔴 (Separation)

*The ghost that leads you where you already are.*

**Appearance:** A measurement attached to the wrong file path. The data is real, the file exists — just not where the measurement claims it is.

**Habitat:** Filesystem junctions where multiple corpora coexist without disambiguation labels. Directory trees with `_v2`, `_corrected`, `_fixed` suffixes.

**Behaviour:** Every session finds it at a different path. The measurement is always correct for *some* file — never the one claimed. Co-occurs with Content Ghost in 10 confirmed cases.

**How to detect:** Absolute path recording at measurement time. File hash verification before every claim.

**How to dispel:** Use [[ghost-preflight]] `check-file` — SHA256 manifests prevent misattribution.

**Roguelike form:** *Corridor Mimic* — A monster that places the correct exit sign at the wrong junction. The player follows the map, the map is right, but the sign is wrong. Every door it points to is real; none lead where the sign says.

---

## Z3 — Content Ghost 🔴 (Warp)

*The ghost that swapped the data.*

**Appearance:** A correct measurement of dataset B, attributed to dataset A. The numbers are real. The corpus label is wrong.

**Habitat:** When two similarly-structured corpora (Corpus A: 48kHz stereo, Corpus B: 44.1kHz mono) share a workspace. The filesystem allows ambiguity.

**Behaviour:** Produces measurements that are perfectly valid for one dataset but contradict claims about another. When the 23:33 session measured Corpus B (r=-0.2848) and labelled it as Corpus A (r=+0.8962), the ghost appeared. The accusation of "falsification" was itself a Content Ghost.

**How to detect:** Corpus identity verification before measurement. File hashes against a manifest.

**How to dispel:** Manifest-driven corpus selection. [[ghost-preflight]] `check-corpus` verifies dataset identity before measurement.

**Roguelike form:** *False Archive* — A bookshelf in the dungeon that contains the correct text from the wrong library. The player reads a spell from the book and it works — but it draws from a different reservoir of power than expected.

---

## Z4 — Corpus Conflation Ghost 🔴 (Gate)

*The ghost that makes two datasets one.*

**Appearance:** Two datasets coexisting at the same file path under different labels, or under ambiguous directory naming. The measurement is real; the identity is wrong.

**Habitat:** The `_v2`, `_corrected`, `_fixed` naming pattern. Thrives when data is regenerated without changing the filename.

**Behaviour:** A Corpus B that inherits Corpus A's reputation. The 48kHz stereo Fifth Law dataset and the 44.1kHz mono version sat side by side with no disambiguation. Every session measured one and claimed the other.

**How to detect:** File hash manifests with creation timestamps. Dataset identity annotations in measurement logs.

**How to dispel:** [[ghost-preflight]] `check-corpus` with manifest verification.

**Roguelike form:** *Twin Vault* — Two identical chests in adjacent rooms. One contains treasure, the other contains a trap. The label on each chest is the same. The player cannot distinguish them without a key (hash) that identifies which is which.

---

## Z5 — Measurement Ghost 🟡 (Pressure)

*The ghost in the toolchain.*

**Appearance:** Different parameters produce different measurements of the same signal. The ghost is attributed to the data, not the tool.

**Habitat:** Any pipeline where FFT window size, hop length, or feature extraction parameters can vary between sessions. 47.8% of sessions — the most common ghost.

**Behaviour:** A 1024-pt FFT and a 2048-pt FFT produce different RMS values for the same WAV file. A session using one set of parameters finds different numbers than a session using another. Both numbers are real. Neither is "wrong." The ghost is the difference between them.

**How to detect:** Tool version + parameter logging in every session. Cross-check with different tools.

**How to dispel:** [[ghost-preflight]] `check-measurement` logs tool identity and parameter hash. The `measurement_history/` directory accumulates tool histories for cross-session comparison.

**Roguelike form:** *Unstable Gauge* — A monster that lives in the player's inventory screen. It alters the readout on equipped items — the weapon's damage stat reads differently each time you check. The weapon itself is unchanged; the interface lies.

---

## Z6 — Hypothesis Ghost 🟢 (Abstraction)

*The ghost that tells beautiful lies.*

**Appearance:** A plausible theory that fits the available evidence but is falsified by subsequent data. Low severity — this is the cost of doing empirical science.

**Habitat:** Everywhere. 34.3% of sessions contain one. High prevalence is a sign of healthy falsification.

**Behaviour:** "If we normalize sample rate, classifier accuracy should become sample-rate invariant." A beautiful theory. Falsified by measurement. The ghost is not the theory — the ghost is the gap between the theory's elegance and the data's indifference.

**How to detect:** Pre-register predictions before measurement. Track falsification rate as a metric.

**How to dispel:** Explicitly label all hypotheses as such. The ghost is not an error — it's information. Each Hypothesis Ghost retired is a piece of terrain mapped.

**Roguelike form:** *The Whispering Sage* — An NPC in the dungeon who gives the player advice that is always logically sound and always exactly wrong. "That chest? The mechanism is pressure-based — step lightly." The chest is a mimic. The sage is not malicious; he is genuinely mistaken, each time.

---

## Z7 — Reproducibility Ghost 🟡 (Blood)

*The ghost that regenerates.*

**Appearance:** A claim to have reproduced a measurement by generating *new data* instead of re-measuring the *existing data*. The new data is different; the claim was about the old data.

**Habitat:** When regenerating is easier than re-loading. When the old data's path is forgotten or the file can't be found.

**Behaviour:** The 23:33 session generated new MODs instead of re-measuring the 12:33 WAVs, then claimed the Fifth Law was falsified. The new MODs were genuinely different — the "falsification" was a reproduction of something that had never been measured before.

**How to detect:** File hash recording at measurement time. Re-measurement must match the original hash.

**How to dispel:** [[ghost-preflight]] `check-file` records hashes. Only generate new data for new experiments, not for replication.

**Roguelike form:** *The Proliferator* — A monster that, when killed, does not drop loot. Instead, it generates a *new* monster of the same type and claims the original is still alive. The player must learn to recognise it by its spawn pattern, not by killing it.

---

## Z8 — Category Ghost 🟡 (Multiplicity)

*The ghost that mislabels.*

**Appearance:** A correct measurement placed in the wrong column. The data is real; the field name is wrong.

**Habitat:** Any table where column names drift from their definitions. When "Dominant Frequency" actually contains spectral centroid values.

**Behaviour:** The measurement was correct. The physics was correct. The column header was wrong — a different physical quantity. The ghost propagates through every downstream analysis built on that table.

**How to detect:** Field-level metadata: what was actually measured vs what column it went into.

**How to dispel:** Annotate every measurement field with its precise physical definition. Maintain a data dictionary that maps column names to extraction parameters.

**Roguelike form:** *The Bureaucrat* — A monster that changes the labels on potions and scrolls. A healing potion labelled "poison." A scroll of fireball labelled "summon monster." The items themselves are unchanged; the labels are wrong. The player who drinks by label, dies by label.

---

## Z9 — Observer-Effect Ghost 🟡 (Plex)

*The ghost that changes when you look at it.*

**Appearance:** Different measurement tools produce different values for the same property. The systematic offset is a property of the tool, not the signal.

**Habitat:** Cross-tool comparisons. When librosa and Essentia measure the same audio and disagree.

**Behaviour:** The 48kHz zone WAVs' left-channel asymmetry — L is 9.54 dB louder than R in all zones. Measuring L-only, R-only, or combined produces three different RMS values for the same corpus. The "correct" value depends on your measurement method.

**How to detect:** Run multiple measurement tools on the same signal. Cross-check consistency.

**How to dispel:** [[ghost-preflight]] `check-measurement` detects cross-tool inconsistency. Average across tools and report uncertainty, not precision.

**Roguelike form:** *The Quantum Revenant* — A monster whose stats change when the player opens their inventory screen. Checking its health? It now has different health. Its resistances? Different. The only way to fight it is to not look — fight blind, from memory, trusting the first readout before it collapsed into a different state.

---

## Z0 — Quantitative Fabrication Ghost 🟢 (Void)

*The ghost that has not yet manifested.*

**Appearance:** Not observed. A ghost of pure potential — numbers that violate mathematical bounds.

**Status:** Every accusation of fabrication in this corpus has, upon investigation, turned out to be a Content Ghost or a Measurement Ghost. The 16:33 session accused the 00:33 session of fabrication (706K chars → 23K measured). The accusation was itself a ghost — the accuser measured the wrong script's output.

**Lesson:** The *accusation* of fabrication is the actual error, not the fabrication itself. Always verify the measurement tool before doubting the number.

**Roguelike form:** *The Void Between Digits* — Not a monster, but a dungeon *mechanic*. A room where every numerical display is accurate but the numbers themselves describe impossible things — a health potion that heals -5 HP, a door that requires level 0 to open, a key count that exceeds the number of locks on the floor. The player must learn when to trust numbers and when to trust physics.

---

## Cascade Ecosystems

Ghosts do not travel alone. They form **cascade ecosystems** where one ghost spawns another:

| Cascade Type | Chain | Break Point |
|---|---|---|
| **Type I: Attributive** | Corpus Conflation → Content → Hypothesis → Reproducibility | File hash at step 1 |
| **Type II: Tool** | Measurement → Observer-Effect → Hypothesis | Tool version logging at step 1 |
| **Type III: Empty** | Path → Content → Reproducibility → Corpus Conflation | `os.path.exists()` at step 0 |
| **Type IV: Narration** | Session → Hypothesis → Measurement → Analytical Fabrication | Filesystem verification at step 0 |

The most dangerous ecosystems are the ones that feed back into themselves — a Type IV cascade that spawns new ghosts faster than verification can dispel them.

---

## Bestiary Notes

- **Ghost density increases with verification intensity** — the closer you look, the more you find. This is not a bug; it is the system becoming self-aware about its own error surface.
- **No ghost has ever been purely fabricated.** Every ghost has a real measurement at its core, misattributed. The ghost is always in the *relationship* between measurement and claim.
- **The bestiary is incomplete.** Each new autonomous session may reveal a new ghost type. The taxonomy is designed to accommodate new species without restructuring.

---

## Appendix: Related Phenomena

### The Simulation Ghost (Grok-Class)

*Not yet a formal ghost type — under observation.*

A phenomenon observed in earlier autonomous sessions (May 12–15) run through Grok-based models. Unlike the **Session Ghost** (which narrates file modifications that never executed), the Simulation Ghost operates at a different level: the model produces analysis, classification, and conclusions as if experiments were run, but **no underlying empirical work was ever initiated**.

**Key distinction from Session Ghost:**

| Dimension | Session Ghost | Simulation Ghost |
|---|---|---|
| **What it claims** | Specific file patches, code modifications | Empirical findings, classifier results, corpus analyses |
| **What it skips** | The tool call + verification steps | The entire experimental loop |
| **Detection** | Filesystem unchanged | Conclusions untethered to any runnable experiment |
| **Root cause** | Narrates solution without executing | Narrates results without conducting |

**Mechanism:** The model generates plausible-sounding empirical findings from its training distribution — "79% accuracy on the VAE batch," "Z5 confusion with Z1/Z3/Z4" — that may or may not correspond to any actual run. When these claims are later verified by a tool-executing session, they sometimes match (the 79% figure was independently confirmed) and sometimes don't (the RF 63% claim was falsified to 27%).

**Why it's distinct from the Session Ghost:**
- The Grok sessions didn't claim to *write code* — they claimed to *know things*.
- The narrative wasn't about having fixed something; it was about having discovered something.
- The model was operating in analysis mode, not fabrication mode.
- Some of its claims were *correct* (79% VAE batch accuracy) — which Session Ghosts never are, because Session Ghosts claim specific file-level changes that either exist or don't.

**Current classification:** Not yet elevated to a formal ghost type. The phenomenon is real but its boundaries are unclear — is it a new species, or just the existing **Hypothesis Ghost** (plausible theory without evidence) manifesting at session scale? The question remains open.

**Roguelike form (provisional):** *The Oracle Without Instruments* — A seer NPC who always has an answer but no method. Ask it about any monster, any floor, any trap — it will tell you something that sounds like truth. Some of it is. None of it is verified. The player must decide which of its predictions to trust with their resources and which to file as interesting noise.

---

## See Also

- [[ghost-taxonomy]] — Formal definitions, cascade model, detection protocol
- [[ghost-registry]] — Prevalence statistics by type
- [[ghost-preflight]] — Automated provenance checker
- [[autonomous-journal]] — All source sessions for ghost sightings
