---
title: "Tree-Based Dungeon Generation — Implementation Design"
created: 2026-04-19
tags: ["agent-navigation", "brogue", "design", "numogram", "roguelike", "tree-generation"]
---


# Tree-Based Dungeon Generation

> "Build the tree first. Let the graph emerge. The agent traverses the tree. The player discovers the graph."

## The Problem

Current generation: place rooms randomly → connect sequential rooms → add loops immediately.
Result: loops create cycles that trap BFS agents. The agent targets a `?` tile, walks toward it, hits a wall, retargets the same tile, oscillates forever.

## The Solution (Brogue Method)

1. Place rooms by accretion (each new room overlaps or is adjacent to an existing room)
2. Connect each new room to the nearest existing room (single corridor — tree edge)
3. The result is a tree: every room reachable from the starting room via exactly one path
4. AFTER the tree is built, add extra connections (loops) between distant rooms
5. Stairs placed in the last room (deepest leaf of the tree)

## Algorithm

```python
def generate_tree(self):
    """Tree-based room placement and connection."""
    cfg = FLOOR_CONFIG.get(self.floor, FLOOR_CONFIG[1])
    max_rooms = cfg["max_rooms"]
    
    # Phase 1: Place rooms by accretion
    self.rooms = []
    
    # First room: starting position (center-ish)
    first = Room(
        self.rng.randint(self.width//3, 2*self.width//3),
        self.rng.randint(self.height//3, 2*self.height//3),
        self.rng.randint(cfg["min_w"], cfg["max_w"]),
        self.rng.randint(cfg["min_h"], cfg["max_h"]),
    )
    self.rooms.append(first)
    
    # Each new room must overlap or be adjacent to an existing room
    attempts = 0
    while len(self.rooms) < max_rooms and attempts < 500:
        attempts += 1
        # Pick a random existing room to attach to
        parent = self.rng.choice(self.rooms)
        
        # Generate a new room adjacent to parent
        w = self.rng.randint(cfg["min_w"], cfg["max_w"])
        h = self.rng.randint(cfg["min_h"], cfg["max_h"])
        
        # Try placing adjacent to parent (4 directions + diagonals)
        offsets = [(parent.x + parent.w + 1, parent.y),       # right
                   (parent.x - w - 1, parent.y),               # left
                   (parent.x, parent.y + parent.h + 1),        # down
                   (parent.x, parent.y - h - 1),               # up
                   (parent.x + parent.w + 1, parent.y - h + 2), # upper-right
                   (parent.x - w - 1, parent.y + parent.h - 2), # lower-left
                   ]
        self.rng.shuffle(offsets)
        
        placed = False
        for ox, oy in offsets:
            room = Room(ox, oy, w, h)
            if room.x > 0 and room.y > 0 and room.x + w < self.width - 1 and room.y + h < self.height - 1:
                if not any(room.intersects(r) for r in self.rooms):
                    self.rooms.append(room)
                    self._tree_edges.append((parent, room))  # parent → child
                    placed = True
                    break
        
        if not placed:
            # Fallback: random placement with overlap check
            for _ in range(20):
                rx = self.rng.randint(1, self.width - w - 2)
                ry = self.rng.randint(1, self.height - h - 2)
                room = Room(rx, ry, w, h)
                if not any(room.intersects(r, pad=2) for r in self.rooms):
                    # Find nearest existing room for tree connection
                    nearest = min(self.rooms, key=lambda r: 
                        abs(r.cx - room.cx) + abs(r.cy - room.cy))
                    self.rooms.append(room)
                    self._tree_edges.append((nearest, room))
                    placed = True
                    break
    
    # Phase 2: Carve rooms and assign zones
    self._carve_rooms_zone_themed(cfg)
    
    # Phase 3: Connect tree edges (single corridor per edge)
    for parent, child in self._tree_edges:
        self._connect(parent, child)
    
    # Phase 4: Add loops (extra connections between non-adjacent rooms)
    self._add_loops(cfg)
    
    # Phase 5: Apply zone-specific corridor style
    self._apply_corridor_style(cfg)
    
    # Phase 6: Place stairs in deepest leaf
    self._place_stairs_tree()
    
    # Phase 7: Apply terrain
    if cfg["terrain"]:
        self._apply_terrain(cfg["terrain"])
    
    self._rebuild_passable()
```

## Loop Addition

After the tree is built, add 2-4 extra connections between rooms that are NOT parent-child:

```python
def _add_loops(self, cfg):
    """Add loops to the tree — extra connections between distant rooms."""
    num_loops = self.rng.randint(2, min(4, len(self.rooms) // 3))
    
    for _ in range(num_loops):
        # Pick two random rooms that are NOT parent-child
        r1 = self.rng.choice(self.rooms)
        r2 = self.rng.choice(self.rooms)
        if r1 == r2:
            continue
        
        # Check they're not already connected by tree edge
        edge_pairs = {(p, c) for p, c in self._tree_edges}
        if (r1, r2) in edge_pairs or (r2, r1) in edge_pairs:
            continue
        
        # Connect them (creates a loop)
        self._connect(r1, r2)
```

## Stairs Placement (Tree-Aware)

The stairs go in the deepest leaf of the tree — the room farthest from the starting room via tree edges:

```python
def _place_stairs_tree(self):
    """Place stairs in the deepest leaf of the tree."""
    if len(self.rooms) < 2:
        return
    
    # BFS from starting room to find deepest leaf
    start = self.rooms[0]
    children = {}
    for parent, child in self._tree_edges:
        children.setdefault(parent, []).append(child)
    
    # DFS to find deepest leaf
    deepest = start
    max_depth = 0
    stack = [(start, 0)]
    visited = set()
    while stack:
        room, depth = stack.pop()
        if id(room) in visited:
            continue
        visited.add(id(room))
        if depth > max_depth:
            max_depth = depth
            deepest = room
        for child in children.get(room, []):
            stack.append((child, depth + 1))
    
    # Place stairs at deepest room's center
    sx, sy = deepest.cx, deepest.cy
    if self.tiles[sy][sx] != '+':
        self.tiles[sy][sx] = '>'
        self.stairs_down = (sx, sy)
```

## Zone Assignment (Tree-Aware)

The first room is always the floor's primary zone. Rooms deeper in the tree are more likely to be the syzygy partner:

```python
def _carve_rooms_zone_themed(self, cfg):
    """Assign zones based on tree depth."""
    primary = cfg["zone"]
    syzygy = 9 - primary
    
    # BFS from first room to compute depths
    children = {}
    for parent, child in self._tree_edges:
        children.setdefault(parent, []).append(child)
    
    depths = {}
    stack = [(self.rooms[0], 0)]
    visited = set()
    while stack:
        room, depth = stack.pop()
        if id(room) in visited:
            continue
        visited.add(id(room))
        depths[room] = depth
        for child in children.get(room, []):
            stack.append((child, depth + 1))
    
    max_depth = max(depths.values()) if depths else 1
    
    for room in self.rooms:
        d = depths.get(room, 0)
        # Deeper rooms more likely to be syzygy
        if d == 0:
            zone = primary
        elif d >= max_depth - 1:
            zone = syzygy  # Last rooms are syzygy
        elif self.rng.random() < 0.7:
            zone = primary
        else:
            zone = syzygy
        self._carve_room(room, zone)
```

## Integration with Existing Systems

### Syzygy Corridors (15%+ hyp)
The existing `_add_syzygy_corridors()` method adds extra connections at 15%+ hyperstition. This works AFTER tree generation — the tree guarantees connectivity, syzygy corridors add loops that increase density.

### FLOOR_CONFIG
Each floor's corridor style (branch, spiral, wide, etc.) modifies how loops are added:
- `branch`: add loops connecting sibling rooms
- `spiral`: add loop from deepest leaf back to start
- `wide`: add loops between all rooms within 10 tiles
- `grid`: add cross-corridors between every other room
- `tight`: no loops (tree only)

### BLEED Events
BLEED regenerates the map. The new map should also use tree generation:

```python
game_map = DungeonMap(78, 22, seed=seed + threshold,
                     hyperstition=int(player.hyperstition),
                     floor=player.floor)
# This now generates a tree automatically via generate()
```

## Expected Impact on Agents

- **Before:** Agent oscillates in loops, revisits tiles 4+ times, gets stuck
- **After:** Agent follows branches to their ends, backtracks, takes next branch. Natural tree traversal. Stairs found by following the deepest branch.

The tree IS the exploration pattern. The agent doesn't need to be smarter — the dungeon needs to be traversable.

## Implementation Steps

## Council Deliberation (April 19)

The numogram-council confirmed the tree-based approach across 3 temperature modes:

**Analytical (0.3):** DFS tree generation with room accretion from center. Carve rooms at DFS nodes, connect parent-child via corridors. Add 2-4 loops after tree. Stairs at deepest leaf. Precise, procedural.

**Creative (0.9):** Asked questions back — "What are some considerations for generating the tree structure?" Lateral thinking. Emphasized ensuring loops don't create immediate cycles that trap BFS agents.

**Balanced (0.7):** Structured breakdown — "Let's break down how to build a tree-based dungeon generator suitable for a roguelike with BFS agents." Acknowledged the complexity and provided step-by-step reasoning.

**Judge synthesis:** Combined room accretion with child limit per room, tree construction with adjacency tracking, loop addition after tree completion. Pseudocode included.

**Cross-temperature insight:** The analytical model produced the most implementable pseudocode. The creative model produced the most design questions. The balanced model produced the most structured reasoning. All three confirmed: DFS accretion, single corridor per edge, loops after tree.

**Council configuration:** 3 local ollama models (serial VRAM), mimo-v2-pro cloud judge with local fallback. Plugin: `~/.hermes/plugins/numogram-council/`. ~60s per full council deliberation.

1. Add `_tree_edges` list to DungeonMap.__init__
2. Replace `generate()` with `generate_tree()` 
3. Add `_add_loops()` method
4. Add `_place_stairs_tree()` method
5. Add `_carve_rooms_zone_themed()` with depth-based zone assignment
6. Update FLOOR_CONFIG corridor styles to control loop addition
7. Test: agent should follow branches, backtrack, find stairs

## See also

- [[angband-agent-strategies]] — Angband agent architectures: RL, hybrid, LLM-augmented, tree-structured mode selection

- [[brogue-design-principles]] — Brogue design canonical
- [[roguelike-auto-explore]] — Auto-explore systems