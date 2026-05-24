---
title: "Planchette JSON Format"
tags: [json, planchette, oracle, pipeline, gate-loop]
created: 2026-05-24
last_updated: 2026-05-24
category: reference
---

# Planchette JSON Format

`oracle.py --seed N --planchette --json` emits a single-line JSON object
on stdout.  No reading text mixed in.  Consumed directly by
`planchette-svg.py --stdin` or any downstream process.

## Schema

```jsonc
{
  "zone": 7,            // decimal zone (1-9, 0 for Void)
  "name": "dt",         // zone particle / phoneme
  "region": "Separation",
  "particle": "dt",
  "polarity": "+",      // "+" Process / becoming  ·  "−" Substance / foundational
  "current": 5,         // current value (Hold)
  "gate": 3,            // final plex-reduced gate (0-9)
  // ── gate-loop metadata (added v1.2.3-dev) ─────────────────────
  "gate_raw": 21,       // triangular sum before plex reduction: sum(1..zone)
  "gate_loops": 1,      // number of while-iterations needed to reach single digit
                        //  0 = direct (<10), 1 = single-plex, 2 = only Z7
  "gate_history": [3],  // ordered list of intermediate gate values during reduction
                        //  e.g. [10,1] for Z7 (28→10→1, two iterations)
  // ── standard fields ───────────────────────────────────────────
  "syzygy": "7::2",     // syzygy pair string
  "reading": "The Warp consumes itself and grows larger..."  // zone reading
}
```

## Gate-loop Matrix

| Zone | gate_raw | gate | gate_loops | gate_history |
|------|----------|------|------------|-------------|
| Z0 | 0 | 0 | 0 | [] |
| Z1 | 1 | 1 | 0 | [] |
| Z2 | 3 | 3 | 0 | [] |
| Z3 | 6 | 6 | 0 | [] |
| Z4 | 10 | 1 | 1 | [1] |
| Z5 | 15 | 6 | 1 | [6] |
| Z6 | 21 | 3 | 1 | [3] |
| **Z7** | **28** | **1** | **2** | **[10, 1]** |
| Z8 | 36 | 9 | 1 | [9] |
| Z9 | 45 | 9 | 1 | [9] |

Z7 is the only multi-loop zone: `T7 = 28 → 2+8=10 → 1+0=1` (two iterations).
All other triggers require exactly one plex reduction.

## Usage

```bash
# Pipe directly to planchette-svg.py
oracle.py --seed 7 --planchette --json | python3 planchette-svg.py --stdin

# Extract gate loop metadata with jq
oracle.py --seed 7 --planchette --json | jq '.gate_loops, .gate_history'

# Zone gate-loop scan
for z in $(seq 0 9); do
  d=$(oracle.py --seed $z --planchette --json 2>/dev/null | head -1)
  echo "Z$z loops=$(echo $d | jq '.gate_loops') raw=$(echo $d | jq '.gate_raw')"
done
```

## Notes

- `gate_raw` always equals the *n*-th triangular number `T_z = z(z+1)/2`.
- For Z0, `gate_raw == 0` (explicitly handled; no zero-inclusive DR ambiguity).
- `--json` alone (`--json` without `--planchette`) prints the reading normally;
  combine as `--planchette --json` for JSON output.
- Prevents JSON from muddling up the reading: `--planchette` and `--json` flags both
  need to set for this flag to be true.

