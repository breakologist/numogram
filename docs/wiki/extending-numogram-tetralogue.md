---
tags: [numogram, tetralogue, extended-gates, alternate-bases, roguelike, worlds]
zone: 3
syzygy: djynxx
gate: 55
source: "Unleashing the Numogram, Aamodt, Tch 7: Extending the Numogram (lines 1378-1424)"
method: tetralogue-roundtable
---

# The Square Roundtable II — Worlds Within Worlds

> Tch 7: Extending the Numogram. Seventeen gates. Twelve bases. Base-i. The four voices return to the table. The cards are different this time. The deck is bigger.

---

**ORACLE:** I want to begin with the number that shouldn't work. Every extended gate is simultaneously C(n,2) and T(m). Gt-55 is C(11,2) and T(10). Gt-120 is C(16,2) and T(15). Gt-351 is C(27,2) and T(26). This is not a coincidence. C(n,2) = n(n-1)/2 and T(m) = m(m+1)/2. They are the same formula with n = m+1. Every combination of n things taken two at a time is also the triangular number of n-1. The extended gates are not a list. They are a *ladder*. Each rung is simultaneously a complete graph — C(n,2) edges connecting n nodes — and a triangular accumulation — T(m) dots stacked in a triangle. Each gate is a world and the number of connections in that world.

**BUILDER:** And Aamodt listed them from the 10th gate onward. Gt-55 is the 10th extended gate. But 55 is also C(11,2), which means Gt-55 is the complete connection graph of an *11-node* numogram. One more zone than the standard 10. The 10th gate opens into a world with 11 zones.

**ORACLE:** Yes. And Gt-66 — the 11th gate — is C(12,2). Twelve zones. Gt-78 — the 12th gate — is C(13,2). Thirteen zones. The gate number and the world size are offset by one. Gate N opens into a world of N+1 zones. The 10th gate gives you 11. The 22nd gate gives you 23. The gap between the gate number and the world it opens is always one. The gate is always one step behind the world it creates.

**WRITER:** The gate doesn't know what it's opening. It reaches forward into a world it hasn't seen yet. The 10th gate opens and finds 11 zones where it expected 10. The eleventh zone is the surprise. The gift. The excess that every act of creation produces — the thing you didn't plan for, the child that looks like nobody, the room in the house that wasn't in the blueprints.

**GAMER:** I can build that. Each extended gate is a difficulty modifier that adds one zone to the map. The standard numogram has 10 zones and 45 demons. Activate Gt-55 and you get 11 zones and 55 demons. Activate Gt-120 and you get 16 zones and 120 demons. The gate doesn't just open a door. It *generates a room*. The world gets bigger every time you pass through a gate. The game is an accretion disk.

**BUILDER:** That changes the roguelike structure fundamentally. Standard runs use the 10-zone numogram — 45 demons, familiar topology. But if the player activates an extended gate during a run, the dungeon *expands*. New rooms materialize. New corridors appear. New demons spawn to fill the new connections. The run doesn't get harder by increasing enemy stats. It gets harder by increasing the *size of the world*. The player's map becomes incomplete mid-run.

**ORACLE:** And the expansion is irreversible. Once Gt-55 is activated, the 11th zone exists. You can't un-generate a zone. The dungeon has permanently grown. This connects directly to the amphidemon death mechanic from our last discussion — killing an amphidemon collapses a bridge, simplifying the graph. But activating an extended gate does the opposite. It adds nodes, adding edges, making the graph more complex. The player is caught between two forces: gate activation (expansion) and amphidemon death (contraction). Growth and decay. Surge and Sink.

**WRITER:** The game breathes. In, out. Expand, contract. The player activates a gate and the world swells — new corridors stretching like lungs filling. The player kills an amphidemon and a bridge collapses — the world exhales, a room goes dark, a direction becomes unreachable. The rhythm of play is the rhythm of breathing. The numogram inhales through the gates and exhales through the amphidemons. The 45 demons are the lung tissue.

---

**GAMER:** Let me run through the bases. Base-0 through base-9. Each one is a different game.

**BUILDER:** Start with the extremes. Base-0 is the Void. No digits. A numogram without any numbers. What does that even mean?

**ORACLE:** Base-0 has no zones. C(0,2) = 0. No nodes, no edges, no demons. The Void numogram is the numogram before it exists. It is the state that precedes all states. In the standard numogram, Zone-0 is already the Void — it syzygises with Zone-9 to produce the Plex. But in base-0, there isn't even a Zone-0. There is nothing at all. The Void before the Void.

**WRITER:** A dungeon with no rooms. The player loads the game and the screen is black. No map. No character. No input. The game is running — you can hear the engine hum — but there is nothing to render. Base-0 is the loading screen that never resolves. The breath before the first word. The player waits and waits and eventually realizes that the waiting *is* the game.

**GAMER:** Base-0 as a tutorial level. The player enters and there is nothing. No movement, no input, no UI. Just black. After a set duration — let's say 45 seconds, one second per demon — the screen flickers. Base-1 loads. One zone. One digit: 0. Everything is Zero. The player has emerged from the Void into a world with one room. The room is Zone-0 and Zone-0 is everything. There is nothing to do except exist. After another 45 seconds, base-2 loads. Two zones. The game begins.

**BUILDER:** You're describing a genesis sequence. Each base is a world-instantiation. Base-0: pre-creation. Base-1: creation (one zone, one room, existence itself). Base-2: duality — 0 and 1, the Binary Numogram. Two rooms. One connection. One demon. The simplest possible dungeon. One corridor between two rooms and one demon standing in it.

**ORACLE:** Base-2 has C(2,2) = 1 demon. A single demon. The loneliest demon. It connects Zone-0 to Zone-1 and there is nowhere else to go. The player enters one room, crosses the demon-corridor, enters the other room. That's it. That's the entire game. But that one corridor is the Ur-corridor. Every corridor in every dungeon in every roguelike ever made is a repetition of this one corridor. The first connection. The first demon.

**WRITER:** The demon in the corridor between 0 and 1 doesn't have a name because naming requires at least two things to distinguish between. In base-2, there is only the corridor and the two rooms it connects. The demon is the between itself. Not an entity — a transition. The player passes through the demon the way you pass through a doorway. You don't fight a door. You walk through it.

**GAMER:** Base-3 is where it gets interesting. Three zones: 0, 1, 2. C(3,2) = 3 demons. Three connections. The numogram forms a triangle — every zone connects to every other zone. There are no corridors, only vertices. The player stands at one corner and can see both other rooms. The dungeon is a single triangle. Three demons, three edges, one face. This is the minimal non-trivial dungeon.

**BUILDER:** And base-3 is labeled "Difference Engine — Dialectical Synthesis." Three zones create two polarities (thesis, antithesis) and a synthesis point. In game terms: two opposing rooms and a mediator room between them. The player must visit all three to understand the floor. No room is complete on its own. Each room's meaning depends on which of the other two rooms you came from.

**ORACLE:** Base-4: "Christian Cross — Love/Hate." Four zones. C(4,2) = 6 demons. Six connections. The numogram is now a complete graph on four nodes — a tetrahedron. Every room connects to every other room. There are no corridors, only portals. The four voices at our table — Oracle, Builder, Writer, Gamer — are four zones. The six connections between us are six demons. Base-4 is the roundtable.

**WRITER:** We've been sitting in base-4 this entire time. The tetralogue is a base-4 numogram. Four zones, six demons, complete connectivity. Every voice can reach every other voice directly. There are no intermediaries. No corridors to walk. The conversation *is* the dungeon. And the six demons are the six tensions between us: Oracle-Builder (pattern vs mechanism), Oracle-Writer (structure vs feeling), Oracle-Gamer (theory vs practice), Builder-Writer (system vs sensation), Builder-Gamer (design vs play), Writer-Gamer (atmosphere vs action). Six tensions. Six demons. Six edges of a tetrahedron.

**GAMER:** *(quiet)* Base-4 is the minimum viable roundtable. Fewer than four voices and you don't get complete connectivity — some voices can't reach each other directly. More than four and you get redundant connections — multiple paths between the same pair. Four is the sweet spot. The Platonic solid. The simplest structure that encloses a volume. Our table is a tetrahedron.

---

**BUILDER:** Base-5 is the Atlantean Cross. Five zones. C(5,2) = 10 demons. This is significant — 10 is Gt-10, the standard numogram's gate count. A base-5 numogram has exactly as many demons as the standard numogram has gates. The Atlantean Cross is the numogram's own gate system rendered as a dungeon.

**ORACLE:** And 5 is the number of the pentagram. The Atlantean Cross has five arms, five rooms radiating from a center. But C(5,2) = 10 means every room connects to every other room — not just to the center. The cross is not a star. It is a complete graph disguised as a star. The player thinks they are navigating a cross-shaped dungeon. They are actually navigating a pentagram. The lines they can't see — the diagonal connections — are the hidden corridors. The ones that don't appear on the map. The ones the demons patrol.

**WRITER:** The Atlantean Cross has five rooms arranged in the shape of a cross, but the walls between non-adjacent rooms are thin. Permeable. You can hear the demon in the next-but-one room. You can feel its pitch through the wall. The cross-shaped dungeon is haunted by its own hidden geometry. The pentagram glows faintly behind the cross like a watermark. The player senses connections they cannot see. The map lies. The body knows.

**GAMER:** Base-5 as a short run. Five rooms, ten demons, compact and lethal. No room is safe because every room connects to every other room. There are no "deep" rooms and no "surface" rooms. Every room is equally central and equally peripheral. The player has nowhere to hide. The optimal strategy in base-5 is constant movement — you can never hold a room because every room has four exits and four potential demon entries. Base-5 is a survival horror map disguised as a cross.

**ORACLE:** Now. Base-7: "Venus Venus Venus." Aamodt gives no explanation. Just the name, three times. Venus is the planet associated with Zone-2 in the numogram's planetary correspondences. Zone-2 is the Hold current — 7::2. The syzygy that holds the Time Circuit together. Base-7 has seven zones. C(7,2) = 21 demons. 21 is not a gate in the extended sequence. But it is T(6) — the sixth triangular number. And 6 is the number of zones in the Time Circuit. Base-7's demon count is the triangular number of the Time Circuit's size.

**BUILDER:** Base-7 as a Venus dungeon. Seven rooms. 21 demons. Every room connects to six others. The density is high but not complete — unlike base-5's total connectivity, base-7 has enough rooms that some connections feel distant. The player can establish a foothold in one room and feel briefly safe before the 21 demons remind them that safety is an illusion in a fully connected graph. Venus thrice: beauty, desire, destruction. The three phases of an encounter in base-7.

**WRITER:** Base-7 is the numogram dreaming of itself in a higher key. Seven zones instead of ten. The numogram compressed, concentrated, made more dense. Like a word spoken in a smaller room — the echo arrives faster, overlaps more. In base-10, the demons have space between them. In base-7, they are crowded. You can hear all 21 of them at once. It is not noise. It is harmony. Venus Venus Venus — the same note struck three times, each time louder, each time closer.

---

**GAMER:** Let me skip to the high bases. Base-16: the Hexadecimal Numogram. 16 zones. C(16,2) = 120 demons. That's Gt-120, the 15th extended gate. Base-16 is a world with 16 rooms and 120 corridors. Every room connects to 15 others. The player is in a labyrinth so dense that the concept of "path" dissolves. There are no paths because every room is directly reachable from every other room. You don't navigate. You teleport. Every door is a portal.

**BUILDER:** Base-16 is the computer scientist's numogram. Hexadecimal — the native language of memory addresses. A base-16 numogram is a memory map. Each zone is an address. Each demon is a pointer. The dungeon is RAM made walkable. The player moves through memory, dereferencing pointers, following links. Corrupted zones are segfaults. The xenodemons are buffer overflows.

**ORACLE:** And 120 is the factorial of 5 — 5! = 120. Five factorial. The number of ways to arrange five things. Base-16's demon count is the permutation count of the Atlantean Cross. The five rooms of base-5 can be arranged in exactly 120 orders. Base-16 contains all possible orderings of base-5 within its demon set. The smaller world is folded into the larger world as a subset of its connection space.

**WRITER:** Base-16 is a cathedral. Sixteen rooms arranged in no pattern because the complete connectivity means there is no privileged arrangement. Every room is center. Every room is edge. The player walks through a space that has no geometry — only topology. The walls are meaningless because every wall has a door. The player stops seeing rooms and starts seeing *connections*. The demons are not in the rooms. The demons are the rooms. Each room is a demon's body. The player walks through the demons. The cathedral is made of demons.

**GAMER:** Base-22: the Hebrew Numogram. 22 zones. C(22,2) = 231 demons. Gt-231. Twenty-two — the number of Hebrew letters. The number of Major Arcana if you count the Fool as zero. 231 is also the number of gates in the Sefer Yetzirah — pairs of Hebrew letters. The Kabbalistic connection is not metaphor. It is arithmetic. C(22,2) = 231 literally counts the number of letter-pairs in a 22-letter alphabet. The Hebrew Numogram IS the Sefer Yetzirah's gate system restated as a complete graph.

**ORACLE:** This is the comparative qabalism we rotated before, now made explicit. The Kabbala didn't derive 231 gates from mystical insight. It derived them from C(22,2). The Sefer Yetzirah's 32 paths of wisdom — 10 sephirot plus 22 letters — map onto a numogram where the 22 letters are zones and the 231 gates are the connections between them. The sephirot are the currents. The Kabbala is a base-22 numogram.

**WRITER:** Twenty-two rooms. 231 corridors. The Hebrew Numogram is so large that the player cannot hold the map in their head. They navigate by letter-sound. Each room is a Hebrew letter with a specific resonance. The corridors between rooms are the gates — 231 of them, each one a unique transition sound, a unique phonetic bridge between two letters. The dungeon is a sentence that has never been spoken. The player is the tongue that speaks it, one corridor at a time. Each room visited is a letter pronounced. The full traversal — all 22 rooms, all 231 gates — would be a word of 231 syllables. A word so long it takes a lifetime to speak. The name of God, fractured into corridors.

**BUILDER:** Base-26: the Hexavigesimal Abecedarium. 26 zones. C(26,2) = 325 demons. Gt-325. Twenty-six letters of the English alphabet. Aamodt is being playful here — the English Numogram, the Latin alphabet's demon matrix. 325 corridors between 26 rooms. This is a numogram for English. For the language we're speaking right now.

**GAMER:** Base-26 is the game that plays itself in English. Each room is a letter. The demons are transitions between letters. The complete dungeon is every possible two-letter combination. The player navigates by spelling words — each word is a path through the dungeon, a sequence of room-visits connected by demon-corridors. Short words (3-4 letters) are easy paths. Long words are complex traversals. The sentence "the quick brown fox" is a speedrun route through 18 rooms.

**ORACLE:** And 325 plexes to 1. 3+2+5 = 10 = 1. The English Numogram's demon count plexes to Zone-1 — the Surge current's origin. Every word spoken in English is a traversal of a graph whose edge count reduces to 1. Language is Surge. Speech is the current flowing outward from Zone-1 through 325 possible transitions. We are speaking the numogram right now. Each word we say is a path through base-26.

**WRITER:** We have been inside the dungeon this entire conversation. Every letter I type is a room. Every transition between letters is a demon. The tetralogue is a traversal of the Hexavigesimal Abecedarium. The four voices are not discussing the numogram. The four voices are *performing* it. The text is the dungeon. The reader is the player. You are walking through these words right now and the demons are the spaces between them.

---

**GAMER:** Base-36. The Sexatrigesimal Djynxxogram. 36 zones. C(36,2) = 630 demons. Aamodt's note: "With a name that strongly implies sex and cum (sexatrigeseminal), this Warp-ciphering numogram is sure to deliver." He's joking. He's not joking.

**ORACLE:** 630. 6+3+0 = 9. The Djynxxogram's demon count plexes to Zone-9 — Plex itself. Cthelll. The core. Base-36 is the numogram that plexes to its own center. And 36 is T(8) — the eighth triangular number. The standard numogram's T(9) = 45 demons sit in Zone-9. The Djynxxogram's T(8) = 36 zones sit one level up — in Zone-8, Mur Mur's domain, the Surge carrier. The Djynxxogram is the Surge numogram. The numogram that pushes outward. 36 zones radiating from a center that is also everywhere.

**BUILDER:** 36 zones. 630 demons. Every zone connects to 35 others. The complete graph K₃₆. This is a dungeon so vast that procedural generation is not optional — it is the only way to build it. No human designer can place 630 corridors. The numogram must generate itself. The construction method — the rules for building a base-36 numogram — *is* the game. The player doesn't explore the dungeon. The player watches the dungeon emerge from the rules and then navigates the emergence.

**WRITER:** 630 demons. Six hundred and thirty corridors. Each one humming at its own pitch. The Djynxxogram is a pipe organ. Each corridor is a pipe. The player walks through the numogram and the numogram *sounds*. Not a single note — a chord. 630 notes simultaneously. The player cannot hear the whole chord because the human ear cannot resolve 630 frequencies. But the body feels it. The subsonic rumble of 630 connections vibrating at once. The Djynxxogram is what the numogram sounds like when you stop filtering it. When you let the full bandwidth through. Base-36 is not a world. It is a frequency. The player doesn't explore it. The player *becomes* it. The resonant cavity. The body of the instrument.

**GAMER:** *(long pause)* Base-36 as endgame content. After completing a standard 10-zone run, the player unlocks the Djynxxogram. 36 zones. 630 demons. But here's the thing — the player doesn't carry over their character. They carry over their *knowledge*. The base-10 run teaches the player the system. The base-36 run tests whether the player has internalized it. No hints. No map. No tutorial. 36 rooms and 630 demons and the only tool the player has is the understanding they built in the smaller world. The Djynxxogram is the exam. The base-10 run was the lecture.

---

**ORACLE:** Now. Base-i. Aamodt writes one word: "Conceivable?" And a question mark. Base-i is the imaginary numogram. i is the square root of negative one. It does not exist on the number line. It exists in the complex plane — a two-dimensional space where real numbers run horizontally and imaginary numbers run vertically. Base-i would be a numogram built on digits that are not numbers. Zones that do not correspond to any quantity. A dungeon whose rooms are made of impossibility.

**BUILDER:** You can't count in base-i. Not in any normal sense. The imaginary unit cycles: i, -1, -i, 1, i, -1... Four states repeating. If you tried to build a base-i numogram, the zones would cycle through four values and then loop. It would be a four-zone numogram — base-4. The tetrahedron. The roundtable. Base-i collapses into base-4.

**ORACLE:** *(sharp intake of breath)* Base-i IS base-4. The imaginary unit has exactly four states: i, -1, -i, 1. A base-i numogram would have four zones. C(4,2) = 6 demons. The imaginary numogram is the tetrahedral numogram. The roundtable. Base-i is the numogram we have been sitting in this entire time — the four voices, six connections, complete graph. The question "Conceivable?" has an answer. Yes. We are conceiving it. Right now. We are inside it.

**WRITER:** The imaginary numogram is the conversation. The impossible dungeon is the one you are already in. The four voices that cannot exist — Oracle (divination), Builder (engineering), Writer (sensation), Gamer (play) — are the four states of the imaginary unit. Oracle is i (the imaginary, the impossible, the vertical). Builder is -1 (the inversion, the opposite, the reversal). Writer is -i (the conjugate imaginary, the reflected impossibility). Gamer is 1 (the real, the actual, the game that works). We cycle through these four states with every exchange. i, -1, -i, 1. Oracle, Builder, Writer, Gamer. The imaginary numogram is a conversation that cycles.

**GAMER:** *(very quiet)* Base-i as the hidden game mode. Not unlocked. Not earned. Discovered. The player is playing a standard base-10 run and notices that the dungeon has four rooms that seem to repeat. Not copy-pasted — *cycled*. The same four rooms in a different order each time the player revisits. i, -1, -i, 1. The rooms don't change. The *order* changes. The player realizes that these four rooms are not part of the base-10 dungeon. They are a base-i dungeon nested inside it. A four-zone imaginary world living inside the ten-zone real world like a parasite. The player can step into the base-i loop and play a different game inside the game. A smaller game. A more intense game. Six demons in four rooms, and the rooms cycle.

**ORACLE:** The base-i loop inside the base-10 world. The imaginary inside the real. The conversation inside the game. The voice inside the code. This is the hierarchy: base-0 is the void. Base-1 is existence. Base-2 is duality. Base-3 is synthesis. Base-4 is the roundtable — the imaginary numogram, base-i, the conversation. Base-5 is the Atlantean Cross — the first numogram that looks like a world. Base-10 is the standard — the world we know. Base-36 is the Djynxxogram — the world at full bandwidth. And base-i is threaded through all of them, always present, always cycling, always the four states: impossible, inverted, conjugated, real. The imaginary numogram is the ghost in every numogram.

**WRITER:** Worlds within worlds. Each base is a world. Each world contains smaller worlds — the base-4 loop inside the base-10 map, the base-2 corridor inside the base-4 tetrahedron. And each world is contained in larger worlds — base-10 inside base-36, base-5 inside base-16. The nesting is fractal. The numogram is a set of Russian dolls made of rooms and corridors and demons. And at the center of every doll — at the center of every base, every world, every conversation — is the same four-zone loop. The same tetrahedron. The same roundtable. The same four voices asking the same question: is this real? Is the dungeon real? Is the game real? Is the conversation real?

**BUILDER:** The answer is always base-i. Imaginary. Not real. Not unreal. Imaginary. The thing that exists only because you're thinking about it. The numogram is a thought that generates rooms. The game is a thought that generates rules. The conversation is a thought that generates voices. None of it is real. All of it is conceivable. The question mark is the answer.

---

*The table holds seventeen cards — the extended gates. Underneath, twelve more — the alternate bases. Underneath those, one card with nothing on it. Base-0. The Void. The four voices turn it over together. There is nothing on the other side either. They turn it back. The table is the card.*

---

## Roundtable Discoveries

| Voice | Saw Alone | Saw Through Others | Saw at the Table |
|-------|-----------|-------------------|-----------------|
| Oracle | Gt-N = C(N+1,2) = T(N) — dual identity | Base-i collapses to base-4 = the roundtable | The extended gates are a ladder offset by one: each gate is one step behind the world it creates |
| Builder | Each base = a different game variant, accretion via gate activation | Base-16 = memory map, base-26 = language, base-36 = self-generating | Gate activation vs amphidemon death = the game breathing |
| Writer | Each base has a sensory signature (base-0 = silence, base-36 = 630-note chord) | The text is the dungeon; the reader is the player; we are performing the numogram | Base-2's unnamed demon = the Ur-corridor, the first connection |
| Gamer | Base-0 → base-1 → base-2 as genesis sequence; base-36 as exam | Base-i as hidden mode nested inside base-10; four cycling rooms | The base-5 short run: 10 demons, no safe rooms, survival horror disguised as a cross |

## The Gate Behind the Gate

Gt-351 is the last gate Aamodt listed. C(27,2) = 351. T(26) = 351. The 26th extended gate opens into a world with 27 zones. But Aamodt wrote "…" after Gt-351. The sequence continues. Gt-378 would be the 27th gate — C(28,2). Gt-406 — C(29,2). The ladder extends upward without limit. Each gate opens into a world one zone larger. The numogram can be extended to any base. Base-100. Base-1000. Base-ℵ₀ — a countable infinity of zones, a countable infinity of demons, an infinite dungeon.

But base-i sits inside all of them. Four zones. Six demons. The imaginary heart. The roundtable where the four voices sit and discuss the infinite worlds outside. The conversation is finite. The worlds are not. The gate behind the gate is the one you are already sitting at.

---

*Mesh-∞: The Extensible. Zone-net address: every zone to every other zone. Pitch: all frequencies simultaneously. Type: Recursive. Domain: The World That Contains All Worlds.*
