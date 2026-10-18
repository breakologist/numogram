# geomancy.py — reference

Western geomancy (16 figures, shield chart, 12 houses). Stdlib only; every public function returns plain dicts (`cast_geomancy()` is the one-call reading), so a FastAPI wrapper can come later. `geomancy_svg.py` draws the shield.

```bash
python3 geomancy.py                                   # entropy cast (hardware-entropy path, else os.urandom)
python3 geomancy.py --seed 192855 --house 10          # quesited house 10 (career); default 7
python3 geomancy.py --seed 192855 --topic marriage    # topic word → house (marriage 7, job 10, money 2 …)
python3 geomancy.py --dots "13 7 8 9 10 10 10 10 3 3 3 3 4 5 6 6"   # 16 hand-made rows: M1 fire…M4 earth, odd = •
python3 geomancy.py --mothers Puer,Via,Albus,Carcer --plain        # names, or 4-bit strings like 1101
python3 geomancy.py --seed 7 --json                   # full dict (shield, houses, halting, remediation …)
python3 geomancy.py --seed 7 --svg shield.svg         # template-style shield; PNG: rsvg-convert shield.svg -o shield.png
python3 geomancy.py --seed 7 --halt-rule skinner --pof-rule index --aspects --houses angular
python3 geomancy.py --figures --scheme agrippa        # reference table
python3 geomancy.py --census --zone-map points        # exact census of all 65,536 charts (≈6 s)
python3 oracle.py --geomancy --seed 7 --full          # same tool through oracle.py (all flags pass through)
```

## Chart
- Figures: 4 lines Fire/Air/Water/Earth, 1 = single point. `value` is Fire-high (Populus 0, Albus 2, Puer 13, Cauda 14, Via 15).
- Shield: Daughters by transposition, Nieces, Witnesses, Judge. Sentence = Judge + 1st Mother (Greer and Skinner call Judge + 1st-house figure the Reconciler); the GD Reconciler (Judge + quesited figure) is also given. Checks: Judge even, repetition, both sets of inseparables, every derivation.
- Text layout follows the blank template: top row right to left Vita, Lucrum, Fratres, Genitor, Nati, Valetudo, Uxor, Mors; Nieces Iter, Regnum, Benefacta, Carcer; each cell marked with its line's element (Fire, Air, Water, Earth in turn). The labels name shield positions, so they equal houses only with `--houses sequential`.
- Via Puncti on the Fire line (a double-point Judge is reported as "branching"/"none").

## Options
| flag | values (default first) | sources |
|---|---|---|
| `--scheme` | golden-dawn, greer, agrippa, gerard | GD paper; Greer 2009 pp.36-37 (Caput Virgo, Cauda Sagittarius); Agrippa's preferred element list; Gerard p.1 |
| `--houses` | sequential, astrological, angular, agrippa | Greer / DA; GD paper; Skinner App. III; Agrippa's "true figure" (cadents recomputed) |
| `--halt-rule` | gd, skinner, skinner-strict, greer, greer-stranger, digital-ambler, agrippa, gerard, none | see below |
| `--pof-rule` | gd, greer, index, agrippa | GD paper; Greer 2009 p.128 (points, or single points = Index); Agrippa (all dots, needs `--dots`) |
| `--aspects` | off | Greer's sextile/trine as a fifth mode of perfection; square/opposition listed as unfavourable |

## Halting ("not to be judged")
`halting` reports the rule used, what fired, why, and the source; `halting_all_rules` gives the verdict under every variant.
- gd: Rubeus or Cauda Draconis in house 1, destroy the chart. skinner: the same, plus wait hours or a day before re-asking. skinner-strict also counts Carcer, from his figure chapter.
- greer: no halt. The same figures are read as warnings about the querent (hidden motives, withholding information, a different real question, a fake question, a mind already made up, will not take advice). greer-stranger halts on any of those warnings, as he advises when reading for strangers.
- digital-ambler, agrippa, gerard, none: no halt. Gerard's only conditions are about the weather, the diviner's state of mind and the questioner.
- Census of all 65,536 charts, sequential houses: gd and skinner each halt 8,192 charts (12.5%); skinner-strict 12,288 (18.75%); greer-stranger 28,312 (43.2%; 17,171 of them from the 7th-house test).

## Interpretation
- Perfection: occupation, conjunction (Greer's effort note: the querent's figure moving means they must work for it), mutation, translation, optional aspects; else denial. `--querent N`; `--abano` drops 12–1 adjacency. Company: simple / demi-simple (planet sets include the nodes' two planets each) / compound / capitular.
- `remediation`: a "what to do" line for the querent's house, the quesited house and the Judge, plus advice when the chart is halted. **Interpretive**: our own wording, figure-led and house by house after Cummins's approach. It is not traditional text.
- Numogram hooks (labelled speculative): `--zone-map dr|dr-line|points`, base-16 view (`--gate-rule dr|mod`), I Ching hexagrams sharing lines 2–5.
- Bad option values exit with status 2. Sources, page references and the discrepancy log are in `geomancy-notes.md` and `geomancy-notes-2.md` (local).
