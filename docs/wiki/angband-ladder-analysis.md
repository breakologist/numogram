---
title: "Angband Ladder Analysis — Human Play Data"
created: 2026-04-24
tags: ["analysis", "angband", "ladder", "roguelike"]
status: active
---


# Angband Ladder Analysis — Human Play Data

*Scraped from angband.live/ladder on 2026-04-17*
*6,735 character dumps available for base Angband variant*

## Source
- [Angband Live Ladder](https://angband.live/ladder/)
- Players upload character dumps on death or win
- Contains: equipment, stats, kills, death cause, turn count
- No turn-by-turn recording — Angband has no demo/replay feature

## Early Deaths (L1-15) — What Humans Carry

### L1-3 Deaths (avg 3 items equipped)
- **100% carry**: Wooden Torch
- **67% carry**: Dagger or Rapier (weapon)
- **67% carry**: Soft Leather Armour (body)
- **33% carry**: Leather Sandals (feet)
- Death causes: poison, soldiers, trap doors

**Agent implication**: The agent starts with torch + dagger + soft leather. At L1-3, just wielding the starting weapon and wearing starting armor is enough. The real killer is environment (traps, poison) not gear.

### L4-8 Deaths (avg 6 items equipped)
- **100%**: Wooden Torch, body armor
- **50%**: Sling (ranged), Dagger, Robe, Sandals, Gauntlets, Cloak, Ring, Amulet
- Death causes: Kobold archer, eastern dwarf

**Agent implication**: By L4-8, players have filled most slots. **Cloak** appears — the agent should prioritize cloaks (`[` in Angband). Sling is common — ranged combat matters. Ring of Protection and Amulet of Resist Acid are early survivability items.

### L9-15 Deaths (avg 7.1 items equipped)
- **86%**: Body armor, light source
- **71%**: Shield, boots
- **57%**: Ranged weapon, helm, gauntlets, **cloak**, weapon
- **29%**: Amulet, ring
- Common items: Set of Gauntlets (3), Iron Shod Boots (3), Leather Shield, Metal Cap, Ring of Slow Digestion, **Cloak**
- Death causes: Grishnákh, blacklock mage, stegocentipede, starvation

**Agent implication**: By L9-15, all 12 slots should be filled. **Cloak is 57% equipped** — it's a free AC slot the agent currently ignores. **Shield** is 71% — the agent should look for shields too. **Starvation** is a real killer — the agent needs to eat (currently doesn't).

## Mid-Level Deaths (L16-30) — avg 12 items
- Ring of Damage, Cloak of Aman, Light Crossbow of Accuracy, Dagger of Peron, Ring of See Invisible
- All slots filled, getting picky about bonuses

## High-Level Deaths (L31+) — avg 12 items
- Ring of Speed (+13), Shield of Thorin, Amulet of Trickery, Leather Shield of Preservation
- Most "deaths" are Ripe Old Age = winners who kept playing until death

## Top Race/Class Combos (from 500 ladder entries)

| Race/Class | Count | Notes |
|---|---|---|
| High-Elf Rogue | 25 | Most popular winner |
| Human Warrior | 20 | Simple, fights well |
| Half-Troll Warrior | 19 | Tank, low INT |
| High-Elf Warrior | 19 | Fast + fights |
| Gnome Mage | 18 | Spellcaster |
| Hobbit Ranger | 17 | Stealthy ranged |
| High-Elf Mage | 16 | Glass cannon |
| Gnome Rogue | 15 | Balanced |
| Hobbit Mage | 14 | Stealth mage |
| Dwarf Priest | 14 | Healer |

**Rogues dominate the ladder** — stealth + disarming is the winning strategy for humans. Our agent is a Warrior, which is right for automated play (fight > stealth when you can't plan).

## Equipment Slot Priority (for agent code)

Based on ladder data, the priority for equipping items found on the ground:

1. **Weapon** (`w`) — every character has one. Wield immediately.
2. **Body armor** (`W`) — 86-100% at all levels. Wear first armor found.
3. **Torch** — 100% carry rate. Replace when low.
4. **Cloak** — 57% by L9-15. The agent currently doesn't prioritize this. **Add to equip logic.**
5. **Shield** — 71% by L9-15. Free AC.
6. **Boots** — 71% by L9-15.
7. **Gauntlets** — 57% by L9-15.
8. **Helm** — 57% by L9-15.
9. **Ranged weapon** — 57% by L9-15. Sling is the early-game ranged weapon.
10. **Ring/Amulet** — 29% by L9-15, near-universal by mid-game.

## Death Causes (Early Game)

From recent ladder deaths:
- **Town**: dogs, drunks, Grip, Fang — lethal at L1-2
- **Dungeon L1-5**: Kobolds (archers are worst), rats, bats, centipedes
- **Dungeon L5-15**: Orcs (Grishnákh), mages, stegocentipedes, traps
- **Starvation**: real threat if agent doesn't eat

## Key Findings for Agent

1. **Cloaks are a free slot** — the agent should pick up and wear cloaks
2. **Shield + Boots + Gauntlets** fill fast — the agent should equip these when found
3. **Ranged weapons** matter by mid-game — but L1 agent should focus on melee
4. **Starvation kills** — the agent needs to eat (send `E` command)
5. **Rogues win more** — but Warriors are simpler for automated play
6. **All 12 slots filled by L9** — the agent should be fully equipped by then

## What the Agent Currently Does vs What Humans Do

| Behavior | Agent | Humans (L9-15) |
|---|---|---|
| Weapon | Equips on pickup ✓ | 100% |
| Body armor | Equips on pickup ✓ | 86% |
| Torch | Starts with one ✓ | 100% |
| Cloak | **Not tracked** ✗ | 57% |
| Shield | **Not tracked** ✗ | 71% |
| Boots | **Not tracked** ✗ | 71% |
| Gauntlets | **Not tracked** ✗ | 57% |
| Helm | **Not tracked** ✗ | 57% |
| Ranged | **Not tracked** ✗ | 57% |
| Rings | **Not tracked** ✗ | 29% |
| Amulets | **Not tracked** ✗ | 29% |
| Eating | **Never eats** ✗ | 100% |

## Related
- [[angband-symbols]] — terrain/monster/item symbols reference
- [[angband-agent]] — agent techniques and pitfalls
- [[brogue-design-principles]] — roguelike design principles

## Data Files
- `~/.hermes/angband_ladder_listings.json` — 500 ladder entries
- `~/.hermes/angband_ladder_dumps.json` — 30 detailed dumps with equipment
- `~/.hermes/angband_early_deaths.json` — 12 early death dumps with slot analysis
- `~/numogame/scrape_angband_ladder.py` — scraper script
