# Triangular Semantics

## Pattern length formula
When `--triangular` is enabled, the pattern row count is computed as the triangular number of the highest zone present in the composition:

```
length = T(max_zone) = max_zone × (max_zone + 1) // 2
```

Examples:
- zone 3 → T(3) = 6 rows
- zone 6 → T(6) = 21 rows
- zone 9 → T(9) = 45 rows

If no notes are placed, the default representative zone is 5 → T(5) = 15 rows.

## 64‑row cap
Protracker patterns are limited to 64 rows. Triangular lengths above 64 are capped:

```
length = min(T(max_zone), 64)
```

Thus zone 12 (T(12)=78) would be truncated to 64 rows.

## Syzygy topology link
The triangular length echoes the triangular syzygy geometry in the numogram: three vertices (zones) that sum to a triangular number form a syzygy cluster. By setting pattern length to the triangular of the maximum zone, the temporal structure mirrors the spatial topology of the zone triple itself, creating a direct correlation between the number of rows and the zone set of the motif.

## Implementation
In `ModComposer.build_patterns_from_grid(triangular=True)`:

```python
zones_present = [v['zone'] for v in self.zone_grid.values()]
rep_zone = max(zones_present) if zones_present else 5
tri_len = rep_zone * (rep_zone + 1) // 2
length = min(tri_len, 64)  # hard cap at 64 rows
```

All missing cells (rows/channels without explicit notes) are zero‑filled by `_fill_missing_cells`.
