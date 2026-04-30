# Validation and Inspection

The Mod-Writer provides three dry‑run flags to validate triad‑motif mappings and inspect generated grids without writing a `.mod` file.

## `--validate-motif MOTIF`
Builds the motif pattern in‑memory, extracts period values, maps them back to zones, and prints a JSON report comparing expected vs observed zone sets. Exits with code 0 on match, 1 otherwise.

```bash
mod-writer --validate-motif Sink --rows 16 --gate 0 --current A
```

Sample output:
```json
{
  "mode": "validate-motif",
  "motif": "Sink",
  "rows": 16,
  "gate": 0,
  "current": "A",
  "triangular": false,
  "expected_zones": [1,3,6],
  "observed_zones": [1,3,6],
  "match": true,
  "detail": { ... }
}
```

## `--validate-all`
Runs the above validation for **all** 24 canonical triads (12 roots × 2 qualities) defined in `data/canonical_vectors.json`. Summarises total/passed/failed and exits non‑zero if any mismatch.

```bash
mod-writer --validate-all --rows 16
```

## `--inspect-motif MOTIF`
Prints a full row‑by‑row table of note, octave, zone, period for each channel, or outputs JSON/CSV. Useful for debugging and understanding the internal grid.

```bash
# Table (default)
mod-writer --inspect-motif Pythagorean --rows 8 --gate 10 --current B

# JSON
mod-writer --inspect-motif Pythagorean --inspect-format json

# CSV
mod-writer --inspect-motif Ptolemaic --inspect-format csv > ptolemaic.csv
```

## Canonical vectors
The ground‑truth zone triples used by `--validate-all` are stored in `data/canonical_vectors.json`. Each entry contains:

```json
{ "root": "D", "quality": "minor", "octave": 3, "zones": [1,3,6] }
```

These vectors are generated exhaustively from the `period_for_note` table and the digital‑root formula. Maintaining their accuracy ensures that motif validation remains authoritative.
