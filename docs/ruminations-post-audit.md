# Tag Density & Cluster Reflection

**Created:** 2026-04-25 (post-audit rumination)  
**Context:** After completing the wiki health audit, some macro-patterns became visible that weren't obvious during file-by-file work.

---

## Observations

### 1. Tag Sprawl Despite Normalization

Even after reducing from 259→197 canonical tags, the distribution is **Pareto-heavy with a long tail**:

| Tag frequency | Count of tags |
|---------------|---------------|
| ≥10 pages | 8 tags (numogram, roguelike, tetralogue, i-ching, pandemonium, demon, triangle-rotation, creative) |
| 3–9 pages | ~30 tags |
| ≤2 pages | ~159 tags (≈81% of tag set) |

**Implication:** ~80% of our tag vocabulary only appears on one or two pages. Some are legitimate specialized terms (`abyssal-crawler`, `hungry-borg`), but others might be scope-creep or over-categorization.

**Candidates for consolidation:**
- `game`, `game-design`, `game-analysis`, `gameplan` → likely merge into `game-design`
- `visualization`, `svg`, `infographic` → could collapse to `visualization`
- `theory`, `methodology`, `structural`, `structural-rules` → possibly `theory` umbrella

**Counterpoint:** The wiki is partly a **personal knowledge base**, not a public taxonomy. Over-tagging may be a feature, not a bug — it aids associative recall.

---

### 2. Tetralogue Cluster — Monologues in Parallel

The `tetralogue` cluster contains **24 pages** (the largest single tag cluster). Yet internal cross-linking is sparse:

- Each tetralogue page averages <1 outbound link to *other* tetralogue pages
- They cite external pages heavily (`numogram`, `triangle-rotation`, `cult-garden` etc.) but not each other
- The four voices (Oracle/Builder/Writer/Gamer) appear to operate in **separate namespaces**

This may be **by design** — the tetralogue format presents four independent takes on a topic, not a conversation. However, the absence of a "see also" section linking the other three voices on each page reduces navigability.

**Opportunity:** Add a standard navbox at the bottom of each tetralogue:
```
[[tetralogue-<topic>-oracle]] | [[tetralogue-<topic>-builder]] | [[tetralogue-<topic>-writer]] | [[tetralogue-<topic>-gamer]]
```
This would create a proper tetralogue *dialogue* rather than four standalone essays.

---

### 3. Stub-to-Hub Ratio

17 stub pages were created to fill structural gaps. They're **intentional red links** — placeholders for future content. Their value is as **index anchors**, not as readable pages yet.

Risk: If left too long, they become permanent dead ends.  
Mitigation: The `POST-AUDIT-ROADMAP.md` tracks them as Batch B. Consider a **stub TTL** (e.g., 90 days) after which either content is written or the stub is merged into a broader page.

---

### 4. Sync Protocol — Manual but Safe

Current sync: vault → repo via `rsync` after manual commit. This is **correctly conservative** — it respects the vault as source of truth and avoids automated pushes that could overwrite work.

Potential improvement: A `Makefile` or `justfile` target like:
```
make sync
  git -C ~/.hermes/obsidian/hermetic add wiki/
  git -C ~/.hermes/obsidian/hermetic commit -m "sync: $(date)"
  rsync -av ~/.hermes/obsidian/hermetic/wiki/ ~/numogram/docs/wiki/
  git -C ~/numogram add docs/wiki/ && git commit -m "sync from vault $(date)" && git push
```
But the user's preference is "methodical, not automated" — so this stays a **recipe, not a robot**.

---

## Actionable Notes

1. **Tag consolidation campaign** — only *after* content expansion stabilizes. Pick one cluster (e.g., `game-*` tags) and merge with redirects.
2. **Tetralogue navbox** — low-effort, high-connectivity win. Could be a skill: `tetralogue-add-navbox`.
3. **Stub TTL policy** — set a checkpoint (e.g., next major audit in Q3) to either fill or fold stubs.
4. **Sync recipe** — document the current `rsync` + dual-commit workflow in `hermes.md` or a `SYNC-RECIPE.md`.

---

**Mood:** The wiki is now a **well-arched structure** with room to grow into. It's not overgrown; it's *underplanted*. The next phase is **content densification**, not structural repair.
