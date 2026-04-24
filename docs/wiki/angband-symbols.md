---
title: "Angband Map Symbols & Commands Reference"
created: 2026-04-24
tags: ["angband", "reference", "roguelike"]
status: active
---


# Angband Map Symbols & Commands Reference

> Source: Angband 4.2.5 gamedata/terrain.txt, gamedata/monster_base.txt, docs/dungeon.rst
> Verified against `/usr/share/angband/angband/gamedata/`

## Terrain Features

| Symbol | Name                 | Code        | Notes                                                                   |
| ------ | -------------------- | ----------- | ----------------------------------------------------------------------- |
| `#`    | Granite wall         | GRANITE     | Impassable. Can be tunneled with digger/pickaxe.                        |
| `#`    | Permanent wall       | PERM        | Impassable. Cannot be tunneled. Color: Blue-slate.                      |
| `#`    | Lava                 | LAVA        | Damaging terrain. Color: Red.                                           |
| `.`    | Open floor           | FLOOR       | Passable. Color: White.                                                 |
| `+`    | Closed door          | CLOSED      | Must be opened (`o` + direction) or searched (`s`). Color: Light umber. |
| `'`    | Open door            | OPEN        | Passable. Color: Light umber.                                           |
| `'`    | Broken door          | BROKEN      | Passable. Color: Umber.                                                 |
| `<`    | Up staircase         | LESS        | Return to previous level or town.                                       |
| `>`    | Down staircase       | MORE        | Descend to next dungeon level.                                          |
| `:`    | Rubble               | RUBBLE      | Impassable. Can be tunneled. Color: White.                              |
| `:`    | Passable rubble      | PASS_RUBBLE | Slow to walk through. Color: Umber.                                     |
| `%`    | Magma vein           | MAGMA       | Impassable. Diggable (difficulty 2). Color: Dark gray.                  |
| `%`    | Quartz vein          | QUARTZ      | Impassable. Diggable (difficulty 3). Color: Gray.                       |
| `*`    | Magma with treasure  | MAGMA_K     | Diggable. Contains gold/gems. Color: Orange.                            |
| `*`    | Quartz with treasure | QUARTZ_K    | Diggable. Contains gold/gems. Color: Yellow.                            |
| `$`    | Gold/treasure        | (item)      | May be on floor OR embedded in wall (adjacency heuristic).              |
| `?`    | Unknown/unseen       | NONE        | Not yet explored or out of line-of-sight.                               |

### Town Stores

| Symbol | Store |
|--------|-------|
| `1` | General Store |
| `2` | Armoury |
| `3` | Weapon Smiths |
| `4` | Bookseller |
| `5` | Alchemy Shop |
| `6` | Magic Shop |
| `7` | Black Market |
| `8` | Home |

## Objects

| Symbol | Category | Color |
|--------|----------|-------|
| `!` | Potion | Light blue |
| `?` | Scroll | White |
| `~` | Lamp/lantern | varies |
| `)` | Weapon | White |
| `[` | Hard armor | Slate |
| `]` | Soft armor | Slate |
| `(` | Shield | Light umber |
| `\` | Hafted weapon | White |
| `|` | Polearm | White |
| `=` | Ring | Red |
| `"` | Amulet | Orange |
| `_` | Staff | Light umber |
| `-` | Wand | Green |
| `~` | Rod | Light purple |
| `!` | Potion | Light blue |
| `?` | Scroll | White |
| `,` | Mushroom/food | Light umber |
| `/` | Digger | Slate |

## Monsters

| Symbol | Category | Examples |
|--------|----------|----------|
| `a` | Ants | |
| `b` | Bats | |
| `c` | Canines | Dogs, wolves, hellhounds |
| `d` | Dragons | (lowercase = young, uppercase = mature) |
| `e` | Floating eyes | |
| `f` | Felines | Cats, cave bears |
| `g` | Golems | |
| `h` | Humanoids | |
| `i` | Icky things | |
| `j` | Jellies | |
| `k` | Kobolds | |
| `l` | Liches | (uppercase L) |
| `m` | Molds | |
| `n` | Nagas | |
| `o` | Orcs | |
| `p` | People/Humans | |
| `q` | Quadrupeds | |
| `r` | Rodents | |
| `s` | Snakes | |
| `t` | Townsfolk (in town) | |
| `u` | Minor demons | (lowercase u) |
| `v` | Vortices | |
| `w` | Worms/worm masses | |
| `x` | Skeletons | |
| `y` | Yeeks | |
| `z` | Zombies | |
| `A` | Ainur/Angels | |
| `B` | Birds | |
| `C` | Centipedes | |
| `D` | Ancient Dragons | (uppercase = adult/ancient) |
| `E` | Elementals | |
| `F` | Dragon flies | |
| `G` | Ghosts | |
| `H` | Hybrids | |
| `I` | Insects | |
| `J` | Snakes (large) | |
| `K` | Killer beetles | |
| `L` | Liches | |
| `M` | Mimics | |
| `N` | Major demons | |
| `O` | Ogres | |
| `P` | Giant humanoids | |
| `Q` | Quylthulgs | |
| `R` | Reptiles/Amphibians | |
| `S` | Spiders/Scorpions | |
| `T` | Trolls | |
| `U` | Major demons | |
| `V` | Vampires | |
| `W` | Wraiths | |
| `X` | Xorns | |
| `Y` | Yetis | |
| `Z` | Zephyr hounds | |
| `,` | Mushroom patches | |
| `@` | Player | |
| `&` | Unique demons | Morgoth's servants |
| `~` | Uniques (misc) | |

## Commands (Original Keyset)

### Movement
- `1-9` or numpad: Move in 8 directions
- `5` or `.`: Wait a turn

### Doors & Searching
- `o` + direction: Open a closed door or chest
- `s`: Search adjacent tiles for hidden doors/traps (searches ALL 8 directions, no direction key needed)
- `S`: Toggle continuous search mode
- `+` + direction: Alter (tunnel wall, disarm trap, bash door)

### Tunneling
- `T` + direction: Tunnel/mine walls
- `+` + direction: Also tunnels (Alter command)

### Stairs
- `<`: Go up stairs (when standing on `<`)
- `>`: Go down stairs (when standing on `>`)

### Items
- `g` or `,`: Pick up items
- `d`: Drop an item
- `i`: Show inventory
- `e`: Show equipment
- `w`: Wear/wield equipment
- `t`: Take off equipment

### Combat
- `f`: Fire missile weapon
- `v`: Throw an item

### Magic & Devices
- `a`: Aim a wand
- `u`: Use a staff
- `z`: Zap a rod
- `r`: Read a scroll
- `q`: Quaff a potion

### Other
- `R`: Rest
- `:`: Look at map
- `/`: Identify symbol on map
- `~`: Knowledge menu
- `?`: Help
- `Ctrl+X`: Save and quit

## Digging Difficulty Reference

| Difficulty | Terrain | Typical Turns (no pickaxe) |
|------------|---------|---------------------------|
| 1 | Rubble | ~5-10 |
| 2 | Magma vein | ~20-50 |
| 3 | Quartz vein | ~50-100 |
| 4 | Granite wall | ~100-500+ |
| 5 | Closed door | ~1-5 (bash) |

> **Key insight for agent:** Granite walls (#) have difficulty 4. Without a digger/pickaxe, tunneling them at DL1 takes hundreds of turns. Hidden doors are revealed by searching (`s`), not tunneling.

## Key Lessons for Angband Agent

1. **`s` searches ALL adjacent tiles** — no direction needed. This is how you find hidden doors.
2. **`+` + direction is Alter** — tunnels walls, disarms traps, bashes doors. NOT the same as searching.
3. **Closed doors (`+`)** can be opened with `o` + direction OR walked into (bump to open).
4. **Hidden doors look like walls (`#`)** until revealed by `s` (search).
5. **Town walls are permanent** — cannot be tunneled.
6. **Stairs (`<` `>`)** may be hidden in unrevealed terrain.

## See also

- [[angband-agent]] — Autonomous agent documentation
- [[angband-agent-display-notes]] — Screen parser notes
