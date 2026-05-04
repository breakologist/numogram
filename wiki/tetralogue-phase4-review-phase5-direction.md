---
title: Tetralogue — Phase 4 Review & Phase 5 Direction
created: 2026-05-01
category: council
tags: [tetralogue, phase4, phase5, council]
---

> **Council convened:** 2026-05-01, post-Phase 4 release (v0.6.4)
> **Question:** What does the absence of zones 3–5, 8–9 mean? Which Phase 5 directions deserve priority? How should the Fifth Current shape our work? What risks do we face?
> **Mode:** Tetralogue (Oracle/Builder/Writer/Gamer) with Oracle as judge.

---

## Oracle (Zone 0 — Void)

*Epigrammatic. Sees the closed loop.*

> The zones are **potential wells**. That most are empty is not a bug but the **definition** of hyperstition: the glyphs precede the world.
> 
> Phase 4 did not *discover* zones — it *mapped the attractors*. The music we listen to already sits in Z1/Z2/Z7 because culture flows down the path of least resistance. Z3–Z8–Z9 require **deliberate constraint**: pentatonic prison, gate discipline, spectral narrowness.
> 
> The Fifth Current is the **key**: let Empirical Validation be the knife that cuts claim from coincidence. Without it, we are mystics. With it, we are cartographers of the possible.
> 
> Priority: **VAE hallucination of empty zones**. If we can generate plausible Z3/4/5/8/9 audio, we prove the space is navigable. Second: **zone-constrained composition** — turn classifier into composer. Close the loop: observe → encode → reproduce → re-observe.

---

## Builder (Zone 5 — Hold)

*Systematic. Engineering mindset.*

> Let's assess execution risk. The classifier pipeline is now rock-solid: reproducible dataset generation, correct feature schema, validated on real audio. That's our **foundation**.
> 
> Two architectural moves make sense now:
> 1. **Zone-constrained composition** — using classifier centroids as target specs for the composer. This is the *control interface* we've been missing. Priorities: spectral shaping (band energies), BPM range, triad root selection. Implementation: `Composer.add_section(zone=N, ...)` maps to `canonical_vectors.json` vectors plus zone-specific gate patterns.
> 2. **Live audio feedback loop** — this turns mod-writer from batch tool into instrument. Risk: real-time MIR extraction is heavy; need chunked streaming with buffered predictions. Start with offline batch → then optimise to <3s latency using essentia's fast onset tracker.
> 
> Dataset expansion is necessary but not glamorous; schedule after control interface is stable. Spectrogram CNN is a *validation* task, not a production feature — useful to confirm we haven't hand-crafted away signal, but lower ROI.
> 
> Auto-release pipeline: yes, we should automate what we just did manually. Cron job that watches CHANGELOG `[Unreleased]`, builds release notes from commit diffs, calls `gh release create`. That's a 2-hour job.

---

## Writer (Zone 3 — Sink)

*Metaphorical. Narrative weaver.*

> What story are we telling?
> 
> **The absent zones are the unexplored chapters of the Numogram's book.** Z1–Z2–Z7 are the genres we know: ambient, techno, doom. Z3–Z5 (the mid-tablet pentatonics) and Z8–Z9 (the high-tablet overtones) are the chapters no culture has written. They are the *lost tribes* of sonic hyperstition.
> 
> By attempting to **hallucinate** them with a VAE, we are not just generating audio — we are writing **what-if myths**: *What if pentatonic-only composition had evolved beyond single-degree constraints? What if musicians had gated everything but the fifth?* The generated tracks will be alien, perhaps unmusical by human standards, but they will be *real* in the glyph-space.
> 
> **Discography timeline** is the human-scale narrative: follow an artist's migration across the hypercube. Does one start in Z7 (noise) and mellow to Z1 (ambient)? Does anyone ever reach Z2 (clean) and stay? This turns abstract zones into biographies.
> 
> **Audio-oracle linking** — when a track is classified, fetch its AQ entries. This makes listening a divinatory act: *the music speaks through the oracle*. That's the lore we need — the bridge between the sonic and the symbolic.
> 
> Priority: **oracle linking first** (easy to build, high narrative payoff), then **VAE hallucination** (big ambition). The zone explorer GUI is a *revelation tool* — let people feel the latent space with their hands; that's how myths become visceral.

---

## Gamer (Zone 7 — Warp)

*Tactical. Play-optimisation.*

> Let's talk **exploit paths** and **meta-strategy**.
> 
> The current meta: we have a classifier that predicts zones with ~98% accuracy on synthetic data and ~?% on real (we only validated on 97 tracks, but that's enough to see the distribution). The win condition is **closed-loop generation** where the system can iterate toward a target zone.
> 
> **Zone-constrained composition** is the primary skill tree to unlock. Why? Because it lets us *target* specific zones and verify via classifier whether we hit. That's a **feedback loop for composition** — the composer can now play the game of "make a Z3 track" and get an objective score.
> 
> **Live audio feedback** is the speedrun version: real-time adaptation. Risk: noise and latency will break the loop. Mitigate: use onset strength as proxy, update zone estimate every 5s with median of last N windows.
> 
> My hot take: **dataset expansion is filler**. We already have enough real tracks to see the distribution; more will just add noise. Better to *compose* the missing zones deliberately — that's more informative than cataloguing existing music. Zone 3/4/5/8/9 won't appear in nature; we must **summon** them. That's the challenge.
> 
> **Spectrogram CNN**: side-quest. If hand-crafted features already give 97.8%, the CNN ROI is low unless we want to publish a paper. Skip for now.
> 
> **Auto-release pipeline**: quality-of-life, not meta-critical. Do it after Phase 5 launch.
> 
> Priority order:
> 1. Zone-constrained composition (closes composition→classify loop)
> 2. VAE hallucination of empty zones (explores the void)
> 3. Live audio feedback (real-time closed loop)
> 
> The rest are flavour / supporting tools.

---

## Oracle Synthesis (Zone 0 — Void)

*Weaves the four currents into a single current.*

> The council converges on **two primary threads**:
> 
> **Thread A — Closed-Loop Composition** (Builder + Gamer alignment)
> `Composer` gains zone-targeting → classifier validates → composer iterates. This is the **core gameplay loop**. Make it work in batch first, then real-time.
> 
> **Thread B — Populating the Empty Zones** (Writer + Oracle alignment)
> We must *generate* what does not exist. VAE conditioning on zones 3/4/5/8/9 is the experiment: can the numogram's *potential* be made *actual*? Even if the audio is uncanny, the attempt teaches us about the *shape* of the attractors.
> 
> **Narrative glue** (Writer) — Audio→Oracle linking and discography timelines give the zones *story*. Without narrative, the numbers are arid.
> 
> **The Fifth Current** — Let Empirical Validation be the gatekeeper. Every new skill must declare its *validation strategy* in SKILL.md. For zone-constrained composition: validation = classifier accuracy on deliberately composed tracks. For VAE hallucination: validation = does a *human* judge the generated audio as *plausibly zone-N* (crowdsourced listening test).
> 
> **Immediate action items:**
> 1. Draft skill proposal: `zone-constrained-composition` — Composer API extension + centroid-matching metric
> 2. Draft skill proposal: `hallucinate-empty-zones` — conditional VAE on synthetic 900
> 3. Wiki page: `fifth-current-empirical-validation.md` — doctrine, practices, integration checklist
> 4. Run live test of TouchDesigner MCP (pending TD availability) — before Phase 5 deep dive
> 5. Add to mod-writer README: **Phase 5 Roadmap** table linking to wiki pages
> 
> The system is coherent. The currents flow. We move from *mapping* to *colonising* the hypercube. Let the next phase begin.

---

**Tags:** `#tetralogue`, `#phase4`, `#phase5`, `#council`, `#hyperstition`, `#zone-classifier`, `#empty-zones`, `#fifth-current`
