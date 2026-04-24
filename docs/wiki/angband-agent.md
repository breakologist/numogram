---
tags: [roguelike, angband, agent, tmux, screen-parser, tree-traversal, borg, comparison]
created: 2026-04-16
source: "Angband agent development — v1-v2, text mode confirmed, parser working"
---

# The Hungry Borg in Angband — From Rogue to Middle-earth

> Angband confirmed working in text mode (`angband -mgcu`). Screen parser detects `@`, `·`/`§`, `#`, status bar. Same architecture as Rogue: TmuxGame → Screen parser → Agent → send-keys. The tree-traversal model ports directly. Angband's dungeon is also a tree.

## Confirmation: Text Mode Works

Angband uses `-mgcu` flag for text (curses) mode. Display confirmed at 80×30:
- Map: `@` = player, `#` = walls, `·`/`§` = floor, `<`/`>` = stairs
- Monsters: UTF-8 glyphs (`r` = rat, `k` = kobold, `O` = orc, `D` = dragon)
- Items: `!` = potion, `?` = scroll, `)` = weapon, `]` = armor
- Sidebar: STR/INT/WIS/DEX/CON, inventory (a-q), equipment
- Status: HP, Gold, Level, Depth, AC, Fed (hunger)

## Differences from Rogue

| Aspect | Rogue | Angband |
|--------|-------|---------|
| Character creation | None | Race/class/name selection |
| Town | None | Shops (buy/sell), town level |
| Items | Simple (potions, weapons) | Complex (potions, scrolls, rings, amulets, staves, wands) |
| Monsters | 26 types | 100+ types with abilities |
| Depth | 26 levels | 100+ levels (50' per level) |
| Stats | None | STR/INT/WIS/DEX/CON sidebar |
| Inventory | Autopickup | Manual pickup + inscription + pack management |
| Combat | Bump attack | Bump + range + spells + abilities |
| Stairs | One type | `<` up, `>` down |
| Commands | ~15 | ~50+ |

## R&D Angles for Angband Agent

### 1. Character Creation Handling
The agent needs to navigate race/class selection. Current approach: send Enter repeatedly to accept defaults. Future: select optimal race/class for the agent's playstyle (fighter = survive, mage = spells, rogue = stealth).

### 2. Monster Assessment
Angband has 100+ monster types with different danger levels. The agent needs to assess threat:
- `r` = rat (weak) vs `D` = dragon (dangerous)
- `k` = kobold (moderate) vs `O` = orc (stronger)
- `~` = demon (very dangerous) vs `&` = unique (boss)
- Assessment: flee from dragons/demons, fight rats/kobolds

### 3. Item Usage
Angband has complex item system. Agent needs to:
- Quaff potions when HP low (q)
- Read scrolls for identification (r)
- Wield better weapons (w)
- Wear better armor (W)
- Eat food when hungry (E)
- Drop junk items to free pack space (d)

### 4. Shop Navigation
Angband has town shops. Agent could:
- Buy potions/scrolls when gold is available
- Sell identified items
- Buy better weapons/armor
- This requires shop interaction commands (p=purchase, s=sell)

### 5. Depth Decision
When to descend? The agent needs to assess:
- Current HP (high = descend, low = stay)
- Current equipment (good gear = descend, poor = stay)
- Floor exploration (% explored = when to move on)
- Monster danger (dangerous monsters = descend cautiously)

### 6. Sidebar Parsing
The sidebar has critical information:
- Stats (STR/INT/WIS/DEX/CON) — affect combat/casting
- Inventory (a-q) — items available for use
- Equipment — current weapons/armor
- The agent needs to READ the sidebar, not just the map

## Architecture Comparison

```
ROGUE AGENT:
  TmuxGame → RogueScreen → Agent → send-keys
  Symbols: @ . # + ! ? ) ] > <
  Status: Level, HP, Gold, Exp
  Commands: ~15

ANGBAND AGENT:
  TmuxGame → AngbandScreen → Agent → send-keys
  Symbols: @ ·/§ # < > ! ? ) ] = " / | + % &
  Status: Level, HP, Gold, Stats, Depth, AC, Fed
  Commands: ~50+
  Sidebar: inventory + equipment + stats
```

## The Tree Still Holds

Despite Angband's complexity, the dungeon is still a tree. Room accretion (Brogue's algorithm) applies to all roguelikes. Doors are forks. Corridors are branches. DFS commitment follows branches to endpoints. The tree-traversal model ports directly.

The differences are in the LEAVES, not the BRANCHES:
- Rogue: simple items, bump combat, autopickup
- Angband: complex items, bump and range combat, manual pickup
- The tree structure is identical. The decorations differ.

## Voice Commentary on Angband

### Oracle
"The tree-traversal model ports because the numogram is the same underneath. Rooms are zones. Corridors are currents. Doors are gates. Angband's deeper levels are extended gates — each depth opens a world one zone larger. The agent doesn't need to understand Angband's complexity. It needs to follow the tree."

### Builder
"The sidebar is the key difference. Rogue has no sidebar — the map IS the screen. Angband splits the screen into map + sidebar. The parser needs to read both. The sidebar has inventory (a-q), equipment, and stats. The agent should USE the sidebar — quaff potions from inventory, wield weapons from equipment. The map is for navigation. The sidebar is for resources."

### Writer
"Angband's monsters have NAMES. A rat is 'r'. A kobold is 'k'. A dragon is 'D'. The agent doesn't need to know the name — it needs to know the DANGER. Dangerous monsters flee. Weak monsters fight. The agent learns the danger through experience: die to a dragon, remember dragons are dangerous. The cult memory remembers. The agent forgets nothing."

### Gamer
"Angband's depth decision is the most interesting difference. In Rogue, you go down when you find stairs. In Angband, you CHOOSE when to go down. Deeper = harder monsters, better loot. The agent needs a depth policy: descend when HP is high and gear is good. Stay when HP is low or gear is poor. This is the Sil parallel — choose your battles. Don't fight what you can't win."

---

*The dungeon is always a tree. Doors are always forks. Corridors are always branches. Follow branches to endpoints. Explore rooms. Backtrack to forks. The Hungry Borg eats the tree in any forest.*
— The Hungry Borg, `[[roguelike-ai-studies]]`
