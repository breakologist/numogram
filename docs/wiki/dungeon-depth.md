---
title: "Dungeon Depth — Zone-Themed Floor Generation"
created: 2026-04-19
last_updated: 2026-04-19
tags: ["design", "dungeon", "numogram", "roguelike", "zone-theme"]
---


# Zone-Themed Floor Generation

Each floor focuses on one zone's character. Rooms still get zone assignments via `i % 10`, but the floor-level parameters shape the entire experience.

## Floor Table

| Floor | Zone | Name | Rooms | Room Size | Terrain | Corridor | LOS | Special |
|-------|------|------|-------|-----------|---------|----------|-----|---------|
| 1 | 0 | The Void | 6-8 | Small (3-5 × 2-4) | Dense | Short dead-ends | 4 | Safe start, no demons |
| 2 | 1 | The Threshold | 10-12 | Medium (4-8 × 3-5) | Clear | Long straight | 8 | First encounters |
| 3 | 2 | The Fracture | 8-10 | Forked (split rooms) | Split paths | Branching | 6 | Trap rooms |
| 4 | 3 | The Warp | 10-14 | Irregular (random) | Water (~) | Spiraling | 5 | Amphidemons |
| 5 | 4 | The Ruin | 8-10 | Wide (6-10 × 4-6) | Ice (*) | Crumbling | 7 | **Cryptolith here** |
| 6 | 5 | The Core | 12-14 | Dense (3-5 × 3-5) | Dense grid | Dense | 6 | Machinery, traps |
| 7 | 6 | The Lattice | 10-12 | Medium | Static (~) | Echo corridors | 9 | Amphidemons |
| 8 | 7 | The Sump | 8-10 | Narrow (3-4 × 2-3) | Blood pools | Tight turns | 5 | High demon density |
| 9 | 8 | The Garden | 10-14 | Open (6-8 × 5-7) | Growth (%) | Branching | 7 | Xenodemons |
| 10 | 9 | Cthelll | 4-6 | Dense void | Minimal | Direct | 3 | Uttunul boss |

## Implementation

Each parameter maps to an existing DungeonMap attribute or a new one:

```python
FLOOR_CONFIG = {
    1: {"zone": 0, "max_rooms": 7,  "min_w": 3, "max_w": 5, "min_h": 2, "max_h": 4,
        "terrain": None, "corridor_style": "short", "los_bonus": 0, "no_demons": True},
    2: {"zone": 1, "max_rooms": 11, "min_w": 4, "max_w": 8, "min_h": 3, "max_h": 5,
        "terrain": None, "corridor_style": "long", "los_bonus": 2, "no_demons": False},
    3: {"zone": 2, "max_rooms": 9,  "min_w": 4, "max_w": 7, "min_h": 3, "max_h": 5,
        "terrain": None, "corridor_style": "branch", "los_bonus": 0, "no_demons": False},
    4: {"zone": 3, "max_rooms": 12, "min_w": 3, "max_w": 9, "min_h": 2, "max_h": 6,
        "terrain": "~", "corridor_style": "spiral", "los_bonus": -1, "no_demons": False},
    5: {"zone": 4, "max_rooms": 9,  "min_w": 6, "max_w": 10, "min_h": 4, "max_h": 6,
        "terrain": "*", "corridor_style": "wide", "los_bonus": 1, "no_demons": False},
    6: {"zone": 5, "max_rooms": 13, "min_w": 3, "max_w": 5, "min_h": 3, "max_h": 5,
        "terrain": None, "corridor_style": "grid", "los_bonus": 0, "no_demons": False},
    7: {"zone": 6, "max_rooms": 11, "min_w": 4, "max_w": 8, "min_h": 3, "max_h": 5,
        "terrain": "~", "corridor_style": "echo", "los_bonus": 3, "no_demons": False},
    8: {"zone": 7, "max_rooms": 9,  "min_w": 3, "max_w": 4, "min_h": 2, "max_h": 3,
        "terrain": "~", "corridor_style": "tight", "los_bonus": -1, "no_demons": False},
    9: {"zone": 8, "max_rooms": 12, "min_w": 6, "max_w": 8, "min_h": 5, "max_h": 7,
        "terrain": "%", "corridor_style": "branch", "los_bonus": 1, "no_demons": False},
    10: {"zone": 9, "max_rooms": 5,  "min_w": 4, "max_w": 8, "min_h": 3, "max_h": 5,
         "terrain": None, "corridor_style": "direct", "los_bonus": -3, "no_demons": False},
}
```

## Room Zone Assignment (Updated)

Instead of `zone = i % 10` (all zones mixed), use floor_zone as primary with occasional syzygy neighbors:

```python
primary_zone = FLOOR_CONFIG[floor]["zone"]
syzygy_zone = 9 - primary_zone  # syzygy partner

for i, room in enumerate(self.rooms):
    if i == 0:
        zone = primary_zone  # First room always primary
    elif i == len(self.rooms) - 1:
        zone = syzygy_zone  # Last room (stairs) is syzygy partner
    elif self.rng.random() < 0.7:
        zone = primary_zone  # 70% primary zone
    else:
        zone = syzygy_zone  # 30% syzygy partner
```

## Corridor Styles

| Style | Description | Implementation |
|-------|-------------|----------------|
| short | Dead-end corridors, tight | `_connect` uses shortest path only |
| long | Extended straight corridors | `_connect` adds extra horizontal/vertical segments |
| branch | Forking corridors | `_add_syzygy_corridors` always active |
| spiral | Curving corridors | Extra connections create loops |
| wide | Double-width corridors | `_widen_currents` always active |
| grid | Regular grid connections | Extra cross-corridors |
| echo | Parallel corridors | Mirror connections between rooms |
| tight | Minimal connections | Only adjacent rooms connect |
| direct | Straight to the point | One main corridor from start to stairs |

## Terrain Placement

After rooms are carved, fill interior tiles with terrain based on floor config:

```python
def _apply_terrain(self, terrain_char):
    """Fill room interiors with terrain character."""
    if not terrain_char:
        return
    for room in self.rooms:
        for y in range(room.y + 1, room.y + room.h - 1):
            for x in range(room.x + 1, room.x + room.w - 1):
                if self.rng.random() < 0.3:  # 30% terrain coverage
                    self.tiles[y][x] = terrain_char
```

## LOS Bonus

Each floor's LOS bonus modifies the zone-tied LOS radius:

```python
# In update_visible:
base_radius = self.ZONE_LOS_RADIUS.get(zone, 6) + floor_config["los_bonus"]
```

## No-Demon Floors

Floor 1 (The Void) should have no demon spawns. The `no_demons` flag in FLOOR_CONFIG prevents `should_spawn()` from returning True on that floor.

---

## What's Already Working

- Floor parameter passes to DungeonMap ✓
- Stairs placed in last room ✓
- Floor transition regenerates with new seed ✓
- Floor number in HUD ✓
- Stair rendering in curses ✓
- Floor zone calculation: `(floor - 1) % 10` ✓

## What Needs Building

1. FLOOR_CONFIG dict — zone-specific generation parameters
2. Modified `generate()` — uses floor config for room count, sizes
3. Room zone assignment — primary zone + syzygy neighbors
4. Terrain placement — fill rooms with zone-appropriate terrain
5. Corridor styles — different connection patterns per zone
6. LOS bonus — floor-specific vision radius
7. No-demon flag — Floor 1 has no spawns
8. Cryptolith placement — Floor 5 (The Ruin)

## See also

- [[tree-dungeon-generation]] — Tree dungeon generation
- [[roguelike-brogue]] — Brogue design principles