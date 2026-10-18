#!/usr/bin/env python3
"""
geomancy.py — Western (European Renaissance) geomancy for the numogram CLI.

Stdlib only. Pure functions return plain dicts, so a FastAPI layer (see wiki
geomancy-api-design.md) can wrap them later without changes.

Usage:
  python3 geomancy.py                         # cast from entropy (hardware path → os.urandom)
  python3 geomancy.py --seed 192855           # deterministic (SHA-256 of the seed, like taixuan.py)
  python3 geomancy.py --hardware              # force the hardware-entropy path
  python3 geomancy.py --dots 13,8,7,9,...     # 16 counted dot-rows (Mother 1 fire … Mother 4 earth)
  python3 geomancy.py --mothers Puer,Via,Albus,Carcer
  python3 geomancy.py --seed 7 --house 10     # quesited house (or --topic job)
  python3 geomancy.py --seed 7 --json | --unicode | --plain | --full
  python3 geomancy.py --figures               # reference table
  python3 geomancy.py --census [--zone-map dr|dr-line|points]
Options:
  --scheme golden-dawn|agrippa|gerard   zodiac + attributed element (default golden-dawn)
  --houses sequential|astrological      shield → house placement (default sequential)
  --gate-rule dr|mod                    base-16 gate: digital root mod 15 (default) | T mod 16
  --zone-map dr|dr-line|points          SPECULATIVE figure → decimal zone map (default dr)
  --abano                               houses 12 and 1 are not adjacent (Peter of Abano)

Conventions
- A figure is four lines, Fire (head, top) / Air / Water / Earth (feet, bottom); 1 = one point
  (odd, active), 0 = two points (even, passive). `value` puts Fire in the high bit (Populus 0,
  Via 15, Puer 13 — the numbering in the user's earlier JSON, with Albus = 2, Cauda = 14);
  `line_value` puts Fire in the low bit (first-generated line = weight 1, as iching.py's line 1).
- Shield (Digital Ambler, "Geomantic Mathematics", 2013; Greer, Art and Practice of Geomancy):
  Daughters = Mothers transposed; Nieces = M1+M2, M3+M4, D1+D2, D3+D4; Right Witness = N1+N2;
  Left Witness = N3+N4; Judge = RW+LW; Sentence = Judge + M1 ("+" = per-line parity = XOR).
  The Golden Dawn "Reconciler" is Judge + the figure in the quesited house (GD Geomancy paper).
- Perfection (Moderately Quick Silver 2023; Digital Ambler 2014): occupation, conjunction,
  mutation, translation; otherwise denial. Company of houses: pairs 1-2, 3-4, … 11-12; simple,
  demi-simple, compound, capitular (Greer, Caduceus 2:3; Digital Ambler 2015).
- Numogram hooks (zone maps, base-16 view, nuclear-line I Ching link) are this tool's own,
  labelled speculative / non-historical in the output.
Sources and the error list for the user's materials: geomancy-notes.md (review, 2026-10-17).
"""

import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

LINES = ("fire", "air", "water", "earth")

URL_DA_MATH = "https://digitalambler.com/2013/06/24/geomantic-mathematics/"
URL_DA_OPS = "https://digitalambler.com/2018/03/02/on-the-structure-and-operations-of-the-geomantic-figures/"
URL_DA_ZODIAC = "https://digitalambler.com/2015/04/03/on-geomantic-figures-zodiac-signs-and-lunar-mansions/"
URL_DA_VIA_PUNCTI = "https://digitalambler.com/2012/12/18/de-geomanteia-via-puncti-follow-the-yellow-brick-road/"
URL_DA_COMPANY = "https://digitalambler.com/2015/07/30/thoughts-on-geomantic-company/"
URL_MQS_PERFECTION = "https://moderatelyquicksilver.com/2023/10/23/the-four-modes-of-geomantic-perfection/"
URL_MQS_VIA_PUNCTI = "https://moderatelyquicksilver.com/2023/12/08/the-via-puncti-way-of-the-point-in-geomancy/"
URL_GREER_CADUCEUS = "https://hermetic.com/caduceus/articles/2/2/medieval-methods-of-geomancy"
URL_GREER_COMPANY = "https://hermetic.com/caduceus/articles/2/3/medieval-methods-of-geomancy"
URL_GD = "https://www.tarrdaniel.com/documents/Thelemagick/gd/publication/english/Geomancy.html"
URL_AGRIPPA = "http://www.princeton.edu/~ezb/geomancy/agrippa.html"
DA_POST = "https://digitalambler.wordpress.com/"

# ─── THE SIXTEEN FIGURES ───
# bits = (fire, air, water, earth). Per-figure text is paraphrased from Digital Ambler's
# "De Geomanteia" posts (2012–13; the user's Obsidian extracts are copies of them), with
# motion / entering-exiting from Digital Ambler 2018 and planets per Greer (Caduceus 2:2).
FIGURES: List[Dict[str, Any]] = [
    dict(name="Populus", english="People", bits=(0, 0, 0, 0), planet="Moon", motion="waxing",
         alt=["congregation", "assembly", "group"], image="a crowd; a meeting-house",
         mobility="stable", passage="liminal", sephirah="Yesod", body="breast, midriff",
         favourable="reflection; preserving the status quo (good with good, bad with bad)",
         unfavourable="when change is wanted, or solitude",
         da=DA_POST + "2013/02/19/de-geomanteia-populus-if-youre-one-of-us-then-roll-with-us/"),
    dict(name="Via", english="Way", bits=(1, 1, 1, 1), planet="Moon", motion="waning",
         alt=["road", "journey", "candle"], image="a road into the distance; a walking-stick",
         mobility="mobile", passage="liminal", sephirah="Yesod", body="stomach, digestion",
         favourable="change, speed, travel and journeys",
         unfavourable="stability, keeping the status quo, staying put",
         da=DA_POST + "2013/02/12/de-geomanteia-via-goes-ever-on-and-on/"),
    dict(name="Albus", english="White", bits=(0, 0, 1, 0), planet="Mercury", motion="direct",
         alt=["the Bearded One", "laughing", "happy"], image="an upright goblet; a high-backed chair",
         mobility="stable", passage="entering", sephirah="Hod", body="throat, lungs, mind",
         favourable="generally, but weakly; slow thought, planning, counsel",
         unfavourable="matters needing speed or enthusiasm",
         da=DA_POST + "2012/11/20/de-geomanteia-albus-like-yoda-but-with-less-green-and-epicness/"),
    dict(name="Conjunctio", english="Conjunction", bits=(0, 1, 1, 0), planet="Mercury", motion="retrograde",
         alt=["Coniunctio", "assembly", "meeting", "crossroads"], image="an X; joined hands; a bridge",
         mobility="mobile", passage="liminal", sephirah="Hod", body="belly, intestines, arms, hands",
         favourable="discussion, meetings, decisions, short travel, unions (good with good, bad with bad)",
         unfavourable="isolation, stability, fixed opinions",
         da=DA_POST + "2012/11/27/de-geomanteia-coniunctio-crossroads-and-crossing-others-sabres-sexual-interests/"),
    dict(name="Puella", english="Girl", bits=(1, 0, 1, 1), planet="Venus", motion="direct",
         alt=["gracious", "beauty", "purity"], image="a hand-mirror",
         mobility="stable", passage="entering", sephirah="Netzach", body="lower back, buttocks, kidneys",
         favourable="friendship, love, harmony (but fickle)",
         unfavourable="permanence, stability, constancy",
         da=DA_POST + "2012/12/11/de-geomanteia-puella-paint-me-like-one-of-your-french-girls/"),
    dict(name="Amissio", english="Loss", bits=(1, 0, 1, 0), planet="Venus", motion="retrograde",
         alt=["external capture", "something escaped"], image="an upside-down bag; arrows moving away",
         mobility="mobile", passage="exiting", sephirah="Netzach", body="shoulders, neck, throat",
         favourable="when loss is wanted (an illness, a debt); love",
         unfavourable="gain and getting",
         da=DA_POST + "2012/12/04/de-geomanteia-amissio-where-have-you-been-all-my-life-ife-ife-ife-ife-ife/"),
    dict(name="Fortuna Major", english="Greater Fortune", bits=(0, 0, 1, 1), planet="Sun", motion="rising / by day",
         alt=["Fortuna Maior", "inward fortune", "inside / hidden help"], image="a tree growing upward",
         mobility="stable", passage="entering", sephirah="Tiphareth", body="heart, chest, circulation",
         favourable="among the most favourable: slow, sure success that overcomes adversity",
         unfavourable="quick results (it may be slow in coming)",
         da=DA_POST + "2013/01/01/de-geomanteia-fortuna-maior-the-sun-passes-over-filth-and-is-not-defiled/"),
    dict(name="Fortuna Minor", english="Lesser Fortune", bits=(1, 1, 0, 0), planet="Sun", motion="setting / by night",
         alt=["outward fortune", "outside / apparent help"], image="a mountain with a staff atop it",
         mobility="mobile", passage="exiting", sephirah="Tiphareth", body="spine, upper back",
         favourable="speed, evasion, escape; success that leans on outside help",
         unfavourable="confrontation, slow progress, long-term determination",
         da=DA_POST + "2012/12/25/de-geomanteia-fortuna-minor-going-gentle-into-that-good-night/"),
    dict(name="Puer", english="Boy", bits=(1, 1, 0, 1), planet="Mars", motion="direct",
         alt=["the Beardless One", "sword", "fighter"], image="a sword",
         mobility="mobile", passage="exiting", sephirah="Geburah", body="head",
         favourable="war and love; strength, activity, directed passion",
         unfavourable="most other matters (rash, over-eager)",
         da=DA_POST + "2013/02/05/de-geomanteia-puer-living-hard-just-like-we-should/"),
    dict(name="Rubeus", english="Red", bits=(0, 1, 0, 0), planet="Mars", motion="retrograde",
         alt=["burning", "danger"], image="an overturned goblet",
         mobility="mobile", passage="exiting", sephirah="Geburah", body="sexual organs, excretory system",
         favourable="only where passion, excess or violence is wanted",
         unfavourable="generally",
         da=DA_POST + "2013/01/29/de-geomanteia-rubeus-i-see-a-red-door-and-i-wanna-paint-it-black/"),
    dict(name="Acquisitio", english="Gain", bits=(0, 1, 0, 1), planet="Jupiter", motion="direct",
         alt=["grasping", "incoming fortune"], image="a bowl collecting money; a money-bag",
         mobility="stable", passage="entering", sephirah="Chesed", body="hips, thighs, liver",
         favourable="gain of every kind (including catching a cold)",
         unfavourable="when one wants to lose, shed or avoid something",
         da=DA_POST + "2013/03/12/de-geomanteia-acquisitio-i-got-a-15-million-dollar-contract-coming-my-way/"),
    dict(name="Laetitia", english="Joy", bits=(1, 0, 0, 0), planet="Jupiter", motion="retrograde",
         alt=["healthy", "upward motion", "bearded"], image="an arch, tower or rainbow",
         mobility="mobile", passage="exiting", sephirah="Chesed", body="feet, fat",
         favourable="joy, promotion, rising; cheerful but fast-moving",
         unfavourable="secrets, tying things down, stability",
         da=DA_POST + "2013/03/05/de-geomanteia-laetitia-hands-up-and-touch-the-sky/"),
    dict(name="Tristitia", english="Sorrow", bits=(0, 0, 0, 1), planet="Saturn", motion="direct",
         alt=["upside down", "relapsed", "damned", "diminished"], image="a stake, a pit, a collapsed building",
         mobility="stable", passage="entering", sephirah="Binah", body="lower legs, ankles, circulation",
         favourable="land, underground matters, secrets, stability",
         unfavourable="generally (lowered spirits, getting stuck)",
         da=DA_POST + "2013/03/26/de-geomanteia-tristitia-give-up-on-this-dont-give-up-on-us/"),
    dict(name="Carcer", english="Prison", bits=(1, 0, 0, 1), planet="Saturn", motion="retrograde",
         alt=["constriction", "bound together"], image="a ring; a cell; two people facing away",
         mobility="stable", passage="liminal", sephirah="Binah", body="knees, bones",
         favourable="maintaining or enforcing a situation; security",
         unfavourable="generally (delay, restriction, isolation)",
         da=DA_POST + "2013/03/19/de-geomanteia-carcer-on-the-inside-of-this-marble-house-i-grow/"),
    dict(name="Caput Draconis", english="Head of the Dragon", bits=(0, 1, 1, 1), planet="North Node",
         motion="benefic (Venus + Jupiter)",
         alt=["inner threshold", "coming in of fortune", "stepping inside"], image="a path leading to a doorway",
         mobility="stable", passage="entering", sephirah="Malkuth", body="right arm; mouth and senses",
         favourable="beginnings of all kinds (good with good, bad with bad)",
         unfavourable="ending, closing or getting rid of something",
         da=DA_POST + "2013/01/08/de-geomanteia-caput-draconis-looking-for-someone-to-share-in-an-adventure/"),
    dict(name="Cauda Draconis", english="Tail of the Dragon", bits=(1, 1, 1, 0), planet="South Node",
         motion="malefic (Mars + Saturn)",
         alt=["outer threshold", "going out of fortune", "stepping outside"], image="leaving home; a trail leading away",
         mobility="mobile", passage="exiting", sephirah="Malkuth", body="left arm; excretory functions",
         favourable="endings, wrapping up, getting out (bad with good, good with bad)",
         unfavourable="starting anything new",
         da=DA_POST + "2013/01/15/de-geomanteia-cauda-draconis-he-ceased-his-fearless-roar/"),
]

# Golden Dawn geomancy paper: general judgement + effect in houses 1–12 (short quotations).
GD_HOUSES: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    'Populus': ('Sometimes good and sometimes bad; good with good, and evil with evil.',
        ('Good for marriage.', 'Medium good.', 'Rather good than bad.', 'Good in all but love.', 'Good in most things.', 'Good.', 'In war good; else medium.', 'Evil.', 'Look for letters.', 'Good.', 'Good in all.', 'Very evil.')),
    'Via': ('Injurious to the goodness of other figures generally, but good for journeys and voyages.',
        ('Evil except for prison.', 'Indifferent.', 'Very good in all.', 'Good in all save love.', 'Voyages good.', 'Evil.', 'Rather good, especially for voyages.', 'Evil.', 'Indifferent. Good for journeys.', 'Good.', 'Very good.', 'Excellent.')),
    'Albus': ('Good for profit and for entering into a place or undertaking.',
        ('Good for marriage. Mercurial. Peace.', 'Good in all.', 'Very good.', 'Very good except in War.', 'Good.', 'Good in all things.', 'Good except for War.', 'Good.', 'A messenger brings a letter.', 'Excellent in all.', 'Very good.', 'Marvellously good.')),
    'Conjunctio': ('Good with good, or evil with evil. Recovery of things lost.',
        ('Good with good, evil with evil.', 'Commonly good.', 'Good fortune.', 'Good save for health; see the 8th.', 'Medium.', 'Good for immorality only.', 'Rather good.', 'Evil; death.', 'Medium good.', 'For love; good. For sickness, evil.', 'Good in all.', 'Medium. Bad for prisoners.')),
    'Puella': ('Good in all demands, especially in those relating to women.',
        ('Good except in war.', 'Very good.', 'Good.', 'Indifferent.', 'Very good, but notice the aspects.', 'Good, but especially so for debauchery.', 'Good except for war.', 'Good.', 'Good for music. Otherwise only medium.', 'Good for peace.', 'Good, and love of ladies.', 'Good in all.')),
    'Amissio': ('Good for loss of substance and sometimes for love; but very bad for gain.',
        ('Ill in all things but for prisoners.', 'Very ill for money, but good for love.', 'Ill end, except for quarrels.', 'Ill in all.', 'Evil except for agriculture.', 'Rather evil for love.', 'Very good for love, otherwise evil.', 'Excellent in all questions.', 'Evil in all things.', 'Evil except for favour with women.', 'Good for love, otherwise bad.', 'Evil in all things.')),
    'Fortuna Major': ('Good for gain in all things where a person has hopes to win.',
        ('Good save in secrecy.', 'Good except in sad things.', 'Good in all.', 'Good in all, but melancholy.', 'Very good in all things.', 'Very good except for debauchery.', 'Good in all.', 'Moderately good.', 'Very good.', 'Exceedingly good. Go to superiors.', 'Very good.', 'Good in all.')),
    'Fortuna Minor': ('Good in any matter in which a person wishes to proceed quickly.',
        ('Speed in victory and in love, but choleric.', 'Very good.', 'Good, but wrathful.', 'Haste; rather evil except for peace.', 'Good in all things.', 'Medium in all.', 'Evil except for war or love.', 'Evil generally.', 'Good, but choleric.', 'Good, except for peace.', 'Good, especially for love.', 'Good, except for alteration, or for suing another.')),
    'Puer': ('Evil in most demands, except in those relating to War or Love.',
        ('Indifferent. Best in War.', 'Good, but with trouble.', 'Good fortune.', 'Evil, except in War and Love.', 'Medium good.', 'Medium.', 'Evil, save in War.', 'Evil, save for Love.', 'Evil except for War.', 'Rather evil. But good for Love and War.', 'Most other things medium.', 'Medium; good favour. Very good in all.')),
    'Rubeus': ('Evil in all that is good and Good in all that is evil.',
        ('Destroy the figure if it falls here! It makes the judgment worthless.', 'Evil in all demands.', 'Evil except to let blood.', 'Evil except in War and Fire.', 'Evil save for love, and sowing seed.', 'Evil except for blood-letting.', 'Evil except for war and fire.', 'Evil.', 'Very evil.', 'Dissolute. Love, fire.', 'Evil, except to let blood.', 'Evil in all things.')),
    'Acquisitio': ('Generally good or profit and gain.',
        ('Happy, success in all things.', 'Very prosperous.', 'Favour and riches.', 'Good fortune and success.', 'Good success,', 'Good, especially if it agrees with the 5th.', 'Reasonably good.', 'Rather good, but not very. The sick shall die.', 'Good in all demands.', 'Good in suits. Very prosperous.', 'Good in all.', 'Evil, pain and loss.')),
    'Laetitia': ('Good for joy, present or to come.',
        ('Good, except in war.', 'Sickly.', 'Ill.', 'Mainly good.', 'Excellent.', 'Evil generally.', 'Indifferent.', 'Evil generally.', 'Very good.', 'Good, rather in war than in peace.', 'Good in all.', 'Evil generally.')),
    'Tristitia': ('Evil in almost all things.',
        ('Medium, but good for treasure and fortifying.', 'Medium, but good to fortify.', 'Evil in all.', 'Evil in all.', 'Very evil.', 'Evil, except for debauchery.', 'Evil for inheritance and magic only.', 'Evil, but in secrecy good.', 'Evil except for magic.', 'Evil except for fortifications.', 'Evil in all.', 'Evil. But good for magic and treasure.')),
    'Carcer': ('Generally evil. Delay, binding, bar, restriction.',
        ('Evil except to fortify a place.', 'Good in Saturnine questions; else evil.', 'Evil.', 'Good only for melancholy.', 'Receive a letter within three days. Evil.', 'Very evil.', 'Evil.', 'Very evil.', 'Evil in all.', 'Evil save for hidden treasure.', 'Much anxiety.', 'Rather good.')),
    'Caput Draconis': ('Good with evil; evil with evil. Gives a good issue for gain.',
        ('Good in all things.', 'Good.', 'Very good.', 'Good save in war.', 'Very good.', 'Good for immorality only.', 'Good especially for peace.', 'Good.', 'Very good.', 'Good in all.', 'Good for the church and ecclesiastical gain.', 'Not very good.')),
    'Cauda Draconis': ('Good with evil, and evil with good. Good for loss, and for passing out of an affair.',
        ('Destroy figure if it falls here! Makes judgment worthless.', 'Very evil.', 'Evil in all.', 'Good especially for conclusion of the matter.', 'Very evil.', 'Rather good.', 'Evil, war, and fire.', 'No good, except for magic.', 'Good for science only. Bad for journeys. Robbery.', 'Evil save in works of fire.', 'Evil save for favours.', 'Rather good.')),}

# ─── ATTRIBUTION SCHEMES (zodiac sign + attributed element) ───
# golden-dawn: Greer, Caduceus 2:2 (the GD set) and the GD geomancy paper; the nodes have no sign
#   (Caput takes the dignities of Jupiter + Venus, Cauda of Saturn + Mars).
# agrippa: pseudo-Agrippa, "Of Geomancy" (Fourth Book, 1655), signs by planetary house, elements by
#   the triplicities given in the same passage. The 1655 text reads "Puella and Rubeus have …
#   Scorpio"; Puella is already given Taurus and Puer is listed in the fiery triplicity, so Puer is
#   read as Aries here [editorial reading, flagged in the output].
# gerard: Gerard of Cremona, "Astronomical Geomancy", as tabulated by Digital Ambler (2015).
#   Elements for Gerard are derived from the sign [derived].
SIGN_ELEMENT = {"Aries": "fire", "Leo": "fire", "Sagittarius": "fire", "Taurus": "earth", "Virgo": "earth",
                "Capricorn": "earth", "Gemini": "air", "Libra": "air", "Aquarius": "air",
                "Cancer": "water", "Scorpio": "water", "Pisces": "water"}
SCHEMES: Dict[str, Dict[str, Any]] = {
    "golden-dawn": dict(source=URL_GREER_CADUCEUS, signs={
        "Puer": "Aries", "Amissio": "Taurus", "Albus": "Gemini", "Populus": "Cancer", "Via": "Cancer",
        "Fortuna Major": "Leo", "Fortuna Minor": "Leo", "Conjunctio": "Virgo", "Puella": "Libra",
        "Rubeus": "Scorpio", "Acquisitio": "Sagittarius", "Carcer": "Capricorn", "Tristitia": "Aquarius",
        "Laetitia": "Pisces", "Caput Draconis": None, "Cauda Draconis": None},
        elements={"fire": ["Puer", "Fortuna Major", "Acquisitio", "Cauda Draconis"],
                  "air": ["Albus", "Puella", "Tristitia", "Fortuna Minor"],
                  "water": ["Populus", "Rubeus", "Laetitia", "Via"],
                  "earth": ["Amissio", "Conjunctio", "Carcer", "Caput Draconis"]}),
    "agrippa": dict(source=URL_AGRIPPA, note="Puer → Aries is an editorial reading of the 1655 text", signs={
        "Puer": "Aries", "Puella": "Taurus", "Albus": "Gemini", "Populus": "Cancer", "Via": "Cancer",
        "Fortuna Major": "Leo", "Fortuna Minor": "Leo", "Conjunctio": "Virgo", "Amissio": "Libra",
        "Rubeus": "Scorpio", "Cauda Draconis": "Scorpio", "Laetitia": "Sagittarius", "Carcer": "Capricorn",
        "Caput Draconis": "Capricorn", "Tristitia": "Aquarius", "Acquisitio": "Pisces"},
        elements={"fire": ["Puer", "Fortuna Major", "Fortuna Minor", "Laetitia"],
                  "earth": ["Puella", "Conjunctio", "Carcer", "Caput Draconis"],
                  "air": ["Albus", "Amissio", "Tristitia"],
                  "water": ["Via", "Populus", "Rubeus", "Cauda Draconis", "Acquisitio"]}),
    "gerard": dict(source=URL_DA_ZODIAC, note="elements derived from the sign", signs={
        "Acquisitio": "Aries", "Fortuna Minor": "Taurus", "Laetitia": "Taurus", "Puer": "Gemini",
        "Rubeus": "Gemini", "Albus": "Cancer", "Via": "Leo", "Caput Draconis": "Virgo", "Conjunctio": "Virgo",
        "Puella": "Libra", "Amissio": "Scorpio", "Tristitia": "Scorpio", "Cauda Draconis": "Sagittarius",
        "Populus": "Capricorn", "Fortuna Major": "Aquarius", "Carcer": "Pisces"}, elements=None),
}
# "Structural" element = Digital Ambler's figure posts (the line pattern decides); Greer's "inner element".
STRUCTURAL_ELEMENT = {"fire": ["Laetitia", "Fortuna Minor", "Cauda Draconis", "Amissio"],
                      "air": ["Rubeus", "Puer", "Conjunctio", "Acquisitio"],
                      "water": ["Via", "Puella", "Populus", "Albus"],
                      "earth": ["Tristitia", "Fortuna Major", "Carcer", "Caput Draconis"]}

GLYPHS = {"Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀", "Mars": "♂", "Jupiter": "♃",
          "Saturn": "♄", "North Node": "☊", "South Node": "☋"}

# GD paper: significations of the houses; topic keywords → quesited house.
HOUSE_MEANINGS = {
    1: "life, health, the querent", 2: "money, property, personal worth",
    3: "siblings, news, short journeys", 4: "father, land, inheritance; the end of the matter",
    5: "children, pleasure, feasts, speculation", 6: "servants, sickness, small animals",
    7: "love, marriage, partners, open enemies, lawsuits", 8: "deaths, wills, legacies; anxiety",
    9: "long journeys, science, religion, divination", 10: "mother; rank, profession, authority",
    11: "friends, hopes and wishes", 12: "sorrows, secret enemies, prisons, hidden dangers"}
TOPICS = {"health": 1, "self": 1, "money": 2, "property": 2, "sibling": 3, "news": 3, "home": 4,
          "land": 4, "father": 4, "children": 5, "child": 5, "pleasure": 5, "illness": 6, "work": 6,
          "love": 7, "marriage": 7, "partner": 7, "lawsuit": 7, "death": 8, "inheritance": 8,
          "travel": 9, "journey": 9, "study": 9, "religion": 9, "job": 10, "career": 10, "mother": 10,
          "friends": 11, "hopes": 11, "enemies": 12, "prison": 12}

_BY_NAME: Dict[str, Dict[str, Any]] = {}
_BY_BITS: Dict[Tuple[int, ...], Dict[str, Any]] = {}
for _f in FIGURES:
    _f["value"] = _f["bits"][0] * 8 + _f["bits"][1] * 4 + _f["bits"][2] * 2 + _f["bits"][3]
    _f["line_value"] = _f["bits"][0] + _f["bits"][1] * 2 + _f["bits"][2] * 4 + _f["bits"][3] * 8
    _f["points"] = sum(2 - b for b in _f["bits"])
    _f["parity"] = "even" if _f["points"] % 2 == 0 else "odd"
    _f["active_lines"] = [LINES[i] for i in range(4) if _f["bits"][i]]
    _f["element_structural"] = next(e for e, ns in STRUCTURAL_ELEMENT.items() if _f["name"] in ns)
    _f["gd_general"], _f["gd_houses"] = GD_HOUSES[_f["name"]]
    _BY_BITS[_f["bits"]] = _f
    for _n in [_f["name"], _f["english"]] + _f["alt"][:1]:
        _BY_NAME[_n.lower()] = _f
BY_VALUE = {f["value"]: f for f in FIGURES}


def figure(x: Any) -> Dict[str, Any]:
    """Resolve a figure from a name, a bits tuple, a fire-high value 0–15, or a 4-char '1011'
    string (1 = single point, Fire first)."""
    if isinstance(x, dict):
        return _BY_BITS[tuple(x["bits"])]
    if isinstance(x, (tuple, list)):
        return _BY_BITS[tuple(int(b) for b in x)]
    if isinstance(x, int):
        return BY_VALUE[x]
    s = str(x).strip()
    if len(s) == 4 and set(s) <= {"0", "1"}:
        return _BY_BITS[tuple(int(c) for c in s)]
    if s.lower() in _BY_NAME:
        return _BY_NAME[s.lower()]
    raise KeyError(f"unknown figure: {x!r}")


def name(x: Any) -> str:
    return figure(x)["name"]


# ─── OPERATIONS (Digital Ambler 2018) ───
def add(a: Any, b: Any) -> Dict[str, Any]:
    """Geomantic addition: per line, odd + odd = even, etc. (XOR)."""
    return _BY_BITS[tuple(x ^ y for x, y in zip(figure(a)["bits"], figure(b)["bits"]))]


def invert(a: Any) -> Dict[str, Any]:
    """Inversion: every line flipped (single ↔ double). = base-16 syzygy (15 − value)."""
    return _BY_BITS[tuple(1 - b for b in figure(a)["bits"])]


def reverse(a: Any) -> Dict[str, Any]:
    """Reversion: the figure turned upside down (Fire ↔ Earth, Air ↔ Water)."""
    return _BY_BITS[tuple(reversed(figure(a)["bits"]))]


def convert(a: Any) -> Dict[str, Any]:
    """Conversion: reversion + inversion."""
    return invert(reverse(a))


def opposite(a: Any) -> Dict[str, Any]:
    """Greer's 'opposite' figure (company compound): the reverse, or the inverse for the four
    figures that are their own reverse (Populus/Via, Carcer/Conjunctio)."""
    r = reverse(a)
    return invert(a) if r is figure(a) else r


def attributions(x: Any, scheme: str = "golden-dawn") -> Dict[str, Any]:
    f, sc = figure(x), SCHEMES[scheme]
    sign = sc["signs"].get(f["name"])
    if sc["elements"]:
        elem = next((e for e, ns in sc["elements"].items() if f["name"] in ns), None)
    else:
        elem = SIGN_ELEMENT.get(sign)
    return {"scheme": scheme, "sign": sign, "element": elem, "source": sc["source"],
            "note": sc.get("note")}


def describe(x: Any, scheme: str = "golden-dawn") -> Dict[str, Any]:
    """Full reference record for one figure (JSON-safe)."""
    f = figure(x)
    out = {k: v for k, v in f.items() if k not in ("bits", "gd_houses")}
    out["bits"] = list(f["bits"])
    out["lines"] = {LINES[i]: ("single" if f["bits"][i] else "double") for i in range(4)}
    out["attribution"] = attributions(f, scheme)
    out["inverse"], out["reverse"], out["converse"] = name(invert(f)), name(reverse(f)), name(convert(f))
    out["gd_houses"] = {str(h + 1): t for h, t in enumerate(f["gd_houses"])}
    out["sources"] = {"meanings": f["da"], "operations": URL_DA_OPS, "gd_houses": URL_GD}
    return out


def render(x: Any, style: str = "unicode") -> List[str]:
    """Four text rows, Fire first. style: unicode (●), plain (*), dots (•)."""
    one, two = {"unicode": ("  ●  ", "●   ●"), "plain": ("  *  ", "*   *"), "dots": ("  •  ", "•   •")}[style]
    return [one if b else two for b in figure(x)["bits"]]


# ─── CASTING ───
def _entropy(nbytes: int, hardware: bool = True) -> Tuple[bytes, str]:
    """The fixed hardware-entropy path shared with taixuan.py (hardware_entropy.py → os.urandom →
    local collector). Falls back to os.urandom if taixuan.py is not importable."""
    if hardware:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import taixuan as _tx
            return _tx._get_entropy(nbytes), "hardware-entropy path (taixuan._get_entropy)"
        except Exception:
            pass
    return os.urandom(nbytes), "os.urandom"


def mothers_from_bits(bits16: int) -> List[Dict[str, Any]]:
    """16 bits → 4 Mothers; bit 15 = Mother 1 Fire … bit 0 = Mother 4 Earth."""
    out = []
    for m in range(4):
        v = (bits16 >> (12 - 4 * m)) & 0xF
        out.append(BY_VALUE[v])
    return out


def mothers_from_dots(counts: Sequence[int]) -> List[Dict[str, Any]]:
    """16 dot counts (rows), Mother 1 Fire, Air, Water, Earth, then Mother 2 …; odd = one point."""
    if len(counts) != 16 or any(int(c) < 1 for c in counts):
        raise ValueError("need 16 positive dot counts")
    return [_BY_BITS[tuple(int(c) % 2 for c in counts[4 * m:4 * m + 4])] for m in range(4)]


def cast_mothers(seed: Optional[int] = None, hardware: bool = False,
                 dots: Optional[Sequence[int]] = None, mothers: Optional[Sequence[Any]] = None
                 ) -> Tuple[List[Dict[str, Any]], str]:
    if mothers is not None:
        ms = [figure(m) for m in mothers]
        if len(ms) != 4:
            raise ValueError("need exactly 4 Mothers")
        return ms, "manual mothers"
    if dots is not None:
        return mothers_from_dots(dots), "manual dot counts"
    if seed is not None:
        b = hashlib.sha256(str(seed).encode()).digest()[:2]
        return mothers_from_bits(int.from_bytes(b, "big")), f"seed:{seed}"
    b, src = _entropy(2, hardware=True)
    return mothers_from_bits(int.from_bytes(b, "big")), src


# ─── SHIELD ───
POSITIONS = ["M1", "M2", "M3", "M4", "D1", "D2", "D3", "D4", "N1", "N2", "N3", "N4", "RW", "LW", "J", "S"]
POSITION_NAMES = {"M": "Mother", "D": "Daughter", "N": "Niece", "RW": "Right Witness",
                  "LW": "Left Witness", "J": "Judge", "S": "Sentence"}
PARENTS = {"RW": ("N1", "N2"), "LW": ("N3", "N4"), "J": ("RW", "LW"), "N1": ("M1", "M2"),
           "N2": ("M3", "M4"), "N3": ("D1", "D2"), "N4": ("D3", "D4")}


def shield_from_mothers(mothers: Sequence[Any]) -> Dict[str, Dict[str, Any]]:
    """The 15-figure shield plus the Sentence (Judge + First Mother)."""
    m = [figure(x) for x in mothers]
    d = [_BY_BITS[tuple(m[j]["bits"][i] for j in range(4))] for i in range(4)]
    s = {f"M{i + 1}": m[i] for i in range(4)}
    s.update({f"D{i + 1}": d[i] for i in range(4)})
    s["N1"], s["N2"] = add(m[0], m[1]), add(m[2], m[3])
    s["N3"], s["N4"] = add(d[0], d[1]), add(d[2], d[3])
    s["RW"], s["LW"] = add(s["N1"], s["N2"]), add(s["N3"], s["N4"])
    s["J"] = add(s["RW"], s["LW"])
    s["S"] = add(s["J"], s["M1"])
    return s


def validate(shield: Dict[str, Any]) -> Dict[str, Any]:
    """Checks for a shield (also one calculated by hand): Judge even; repetition; the two sets of
    sikidy 'inseparables' (Digital Ambler 2013); and the derivations themselves."""
    s = {k: figure(v) for k, v in shield.items()}
    first15 = [s[p]["name"] for p in POSITIONS[:15]]
    set1 = [name(add(s["N1"], s["J"])), name(add(s["M2"], s["S"])), name(add(s["N2"], s["LW"]))]
    set2 = [name(add(s["LW"], s["S"])), name(add(s["RW"], s["M1"])), name(add(s["N2"], s["M2"]))]
    rebuilt = shield_from_mothers([s["M1"], s["M2"], s["M3"], s["M4"]])
    bad = [p for p in POSITIONS if rebuilt[p] is not s[p]]
    res = {
        "judge_even": s["J"]["points"] % 2 == 0,
        "repeat_in_15": len(set(first15)) < 15,
        "repeat_in_16": len(set(first15 + [s["S"]["name"]])) < 16,
        "inseparables": {"set1": set1, "set2": set2,
                         "ok": len(set(set1)) == 1 and len(set(set2)) == 1},
        "derivation_errors": bad,
    }
    res["valid"] = res["judge_even"] and res["repeat_in_16"] and res["inseparables"]["ok"] and not bad
    return res


def via_puncti(shield: Dict[str, Any]) -> Dict[str, Any]:
    """Way of the Point on the Fire line: from the Judge, follow parents whose Fire line equals the
    Judge's. Single-point Judge → one path to a Mother/Daughter (Digital Ambler 2012, MQS 2023).
    Double-point Judge → may branch or stop at once; Greer reads this as complex causes, MQS notes
    the older books do not treat it as a valid Via Puncti."""
    s = {k: figure(v) for k, v in shield.items()}
    head = s["J"]["bits"][0]
    paths: List[List[str]] = []

    def walk(pos: str, trail: List[str]) -> None:
        nxt = [p for p in PARENTS.get(pos, ()) if s[p]["bits"][0] == head]
        if not nxt:
            paths.append(trail)
        for p in nxt:
            walk(p, trail + [p])

    walk("J", ["J"])
    ends = [t[-1] for t in paths]
    if head == 1:
        kind = "single"
    elif all(t == ["J"] for t in paths):
        kind = "none"
    else:
        kind = "branching"
    return {"judge_fire": "single" if head else "double", "kind": kind,
            "paths": [[f"{p} {s[p]['name']}" for p in t] for t in paths],
            "ends": [f"{p} {s[p]['name']}" for p in ends],
            "traditional": kind == "single",
            "sources": [URL_DA_VIA_PUNCTI, URL_MQS_VIA_PUNCTI]}


# ─── HOUSE CHART ───
# sequential: houses 1–12 = M1–M4, D1–D4, N1–N4 (Greer; Digital Ambler).
# astrological: the GD paper (and pseudo-Agrippa): figure 1 → house 10, 2 → 1, 3 → 4, 4 → 7,
#   5 → 11, 6 → 2, 7 → 5, 8 → 8, 9 → 12, 10 → 3, 11 → 6, 12 → 9.
ASTRO_PLACEMENT = [10, 1, 4, 7, 11, 2, 5, 8, 12, 3, 6, 9]


def house_chart(shield: Dict[str, Any], method: str = "sequential") -> Dict[int, Dict[str, Any]]:
    first12 = [figure(shield[p]) for p in POSITIONS[:12]]
    if method == "sequential":
        return {h + 1: first12[h] for h in range(12)}
    if method == "astrological":
        return {ASTRO_PLACEMENT[i]: first12[i] for i in range(12)}
    raise ValueError("houses: sequential|astrological")


def _adjacent(h: int, abano: bool = False) -> List[int]:
    out = [12 if h == 1 else h - 1, 1 if h == 12 else h + 1]
    if abano:
        out = [x for x in out if {h, x} != {1, 12}]
    return out


def perfection(houses: Dict[int, Any], querent: int = 1, quesited: int = 7,
               abano: bool = False) -> Dict[str, Any]:
    """The four modes (MQS 2023; Digital Ambler 2014):
    occupation — the same figure in both significator houses;
    conjunction — either significator's figure also in a house next to the other's house;
    mutation — both figures side by side elsewhere in the chart;
    translation — a third figure next to both significator houses. None → denial."""
    H = {h: figure(f) for h, f in houses.items()}
    q, s = H[querent], H[quesited]
    found: List[Dict[str, Any]] = []
    if q is s:
        found.append({"mode": "occupation", "detail": f"{q['name']} in houses {querent} and {quesited}"})
    else:
        for h in _adjacent(quesited, abano):
            if h not in (querent, quesited) and H[h] is q:
                found.append({"mode": "conjunction", "detail": f"querent's {q['name']} passes to house {h}, "
                              f"next to house {quesited}", "moves": "querent"})
        for h in _adjacent(querent, abano):
            if h not in (querent, quesited) and H[h] is s:
                found.append({"mode": "conjunction", "detail": f"quesited's {s['name']} passes to house {h}, "
                              f"next to house {querent}", "moves": "quesited"})
        for a in range(1, 13):
            for b in _adjacent(a, abano):
                if {a, b} & {querent, quesited}:
                    continue
                if H[a] is q and H[b] is s:
                    found.append({"mode": "mutation", "detail": f"{q['name']} (house {a}) meets "
                                  f"{s['name']} (house {b})"})
        for f in FIGURES:
            if f is q or f is s:
                continue
            near_q = [h for h in _adjacent(querent, abano) if h != quesited and H[h] is f]
            near_s = [h for h in _adjacent(quesited, abano) if h != querent and H[h] is f]
            if near_q and near_s:
                found.append({"mode": "translation", "detail": f"{f['name']} in house(s) "
                              f"{sorted(set(near_q + near_s))} bridges houses {querent} and {quesited}"})
    order = ["occupation", "conjunction", "mutation", "translation"]
    modes = sorted({x["mode"] for x in found}, key=order.index)
    return {"querent": {"house": querent, "figure": q["name"]},
            "quesited": {"house": quesited, "figure": s["name"]},
            "perfects": bool(found), "modes": modes or ["denial"], "details": found,
            "abano_adjacency": abano, "sources": [URL_MQS_PERFECTION]}


def company(houses: Dict[int, Any], house: int) -> Dict[str, Any]:
    """Company of houses (pairs 1-2 … 11-12): simple (same figure), demi-simple (same planet),
    compound (opposite figures), capitular (same Fire line) — Greer, Caduceus 2:3; DA 2015."""
    partner = house + 1 if house % 2 else house - 1
    a, b = figure(houses[house]), figure(houses[partner])
    if a is b:
        kind = "simple"
    elif a["planet"] == b["planet"]:
        kind = "demi-simple"
    elif opposite(a) is b:
        kind = "compound"
    elif a["bits"][0] == b["bits"][0]:
        kind = "capitular"
    else:
        kind = None
    return {"house": house, "partner": partner, "figures": [a["name"], b["name"]], "company": kind,
            "combined": name(add(a, b)) if kind else None, "sources": [URL_GREER_COMPANY, URL_DA_COMPANY]}


def part_of_fortune(shield: Dict[str, Any], method: str = "sequential") -> Dict[str, Any]:
    """GD paper: total points of the first twelve figures ÷ 12; the remainder (0 → 12) names the
    figure, which then sits in its house."""
    first12 = [figure(shield[p]) for p in POSITIONS[:12]]
    total = sum(f["points"] for f in first12)
    idx = total % 12 or 12
    house = idx if method == "sequential" else ASTRO_PLACEMENT[idx - 1]
    return {"points": total, "figure_number": idx, "house": house, "figure": first12[idx - 1]["name"],
            "source": URL_GD}


def impediment(houses: Dict[int, Any]) -> Optional[str]:
    """GD paper: 'If Rubeus or Cauda Draconis in Ascendant destroy the figure.'"""
    f = figure(houses[1])["name"]
    if f in ("Rubeus", "Cauda Draconis"):
        return f"{f} in house 1: the GD paper says the chart is unfit for judgement (re-cast)"
    return None


def house_for_topic(text: str) -> Optional[int]:
    t = text.lower()
    for k, h in TOPICS.items():
        if k in t:
            return h
    return None


# ─── NUMOGRAM HOOKS (speculative; not traditional geomancy) ───
def dr9(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


ZONE_MAPS = {
    "dr": "digital root of the Fire-high value 0–15 (Populus 0, Via 6)",
    "dr-line": "digital root of the line value (Fire = 1, Air = 2, Water = 4, Earth = 8)",
    "points": "number of points, 4–8 (Via 4 … Populus 8)",
}


def zone(x: Any, zone_map: str = "dr") -> int:
    f = figure(x)
    if zone_map == "dr":
        return dr9(f["value"])
    if zone_map == "dr-line":
        return dr9(f["line_value"])
    if zone_map == "points":
        return f["points"]
    raise ValueError("zone-map: dr|dr-line|points")


def base16_view(x: Any, gate_rule: str = "dr") -> Dict[str, Any]:
    """Figure as a zone of the base-16 numogram: syzygy n :: 15 − n is exactly inversion, for any
    bit order. Gate = triangular number T(n) reduced by the base-16 digital root (mod 15, the
    repo's default) or, with gate_rule='mod', the last digit (T mod 16)."""
    f = figure(x)
    v = f["value"]
    tri = v * (v + 1) // 2
    tgt = (tri % 16) if gate_rule == "mod" else (0 if tri == 0 else 1 + (tri - 1) % 15)
    return {"zone16": v, "syzygy": name(invert(f)), "syzygy_zone16": 15 - v, "current16": abs(2 * v - 15),
            "gate_tri": tri, "gate_target16": tgt, "gate_figure": BY_VALUE[tgt]["name"], "gate_rule": gate_rule}


# I Ching link via nuclear lines 2–5 [non-historical]. Fu Xi value v = Σ yang_k << (k−1), line 1 =
# bottom; KW_BY_VALUE as in iching.py. Figure Fire = line 5, Air = 4, Water = 3, Earth = 2 (top to top).
KW_BY_VALUE = [2, 24, 7, 19, 15, 36, 46, 11, 16, 51, 40, 54, 62, 55, 32, 34, 8, 3, 29, 60, 39, 63, 48, 5,
               45, 17, 47, 58, 31, 49, 28, 43, 23, 27, 4, 41, 52, 22, 18, 26, 35, 21, 64, 38, 56, 30, 50, 14,
               20, 42, 59, 61, 53, 37, 57, 9, 12, 25, 6, 10, 33, 13, 44, 1]
VALUE_BY_KW = {kw: v for v, kw in enumerate(KW_BY_VALUE)}


def figure_from_hexagram(kw: int) -> Dict[str, Any]:
    v = VALUE_BY_KW[kw]
    lines = [(v >> k) & 1 for k in range(6)]          # line 1 … line 6
    return _BY_BITS[(lines[4], lines[3], lines[2], lines[1])]


def hexagrams_for_figure(x: Any) -> List[int]:
    return sorted(kw for kw in range(1, 65) if figure_from_hexagram(kw) is figure(x))


def census(zone_map: str = "dr", method: str = "sequential", gate_rule: str = "dr") -> Dict[str, Any]:
    """Exact enumeration of all 16^4 = 65,536 charts."""
    from collections import Counter
    judge, judge_zone, all_zone, house_zone = Counter(), Counter(), Counter(), Counter()
    vp, pof, unique15, impeded, perfect17 = Counter(), Counter(), 0, 0, 0
    odd_total = {12: 0, 15: 0, 16: 0}
    for bits16 in range(65536):
        sh = shield_from_mothers(mothers_from_bits(bits16))
        figs = [sh[p] for p in POSITIONS]
        judge[sh["J"]["name"]] += 1
        judge_zone[zone(sh["J"], zone_map)] += 1
        for f in figs:
            all_zone[zone(f, zone_map)] += 1
        H = house_chart(sh, method)
        for h in range(1, 13):
            house_zone[zone(H[h], zone_map)] += 1
        vp[via_puncti(sh)["kind"]] += 1
        pof[part_of_fortune(sh, method)["house"]] += 1
        if len({f["name"] for f in figs[:15]}) == 15:
            unique15 += 1
        singles = [sum(f["bits"]) for f in figs]
        for n in (12, 15, 16):
            if sum(singles[:n]) % 2:
                odd_total[n] += 1
        if impediment(H):
            impeded += 1
        if perfection(H, 1, 7)["perfects"]:
            perfect17 += 1
    zsum = sorted({(dr9(f["value"]) + dr9(15 - f["value"])) % 9 for f in FIGURES})
    return {"charts": 65536, "zone_map": zone_map, "zone_map_meaning": ZONE_MAPS[zone_map],
            "house_method": method,
            "judge": dict(sorted(judge.items())), "judge_zone": dict(sorted(judge_zone.items())),
            "zone_all_16_positions": dict(sorted(all_zone.items())),
            "zone_houses_1_12": dict(sorted(house_zone.items())),
            "via_puncti": dict(vp), "part_of_fortune_house": dict(sorted(pof.items())),
            "charts_with_15_unique_figures": unique15,
            "odd_total_single_points": {f"first_{n}": c for n, c in odd_total.items()},
            "impeded_charts": impeded, "perfects_1_7": perfect17,
            "dr_of_syzygy_pair_sums_mod9": zsum}


# ─── TOP-LEVEL CAST ───
def _brief(f: Dict[str, Any], scheme: str, zone_map: str) -> Dict[str, Any]:
    at = attributions(f, scheme)
    return {"name": f["name"], "english": f["english"], "bits": list(f["bits"]), "value": f["value"],
            "points": f["points"], "planet": f["planet"], "sign": at["sign"], "element": at["element"],
            "element_structural": f["element_structural"], "zone": zone(f, zone_map)}


def cast_geomancy(seed: Optional[int] = None, hardware: bool = False, dots: Optional[Sequence[int]] = None,
                  mothers: Optional[Sequence[Any]] = None, quesited: int = 7, querent: int = 1,
                  scheme: str = "golden-dawn", houses: str = "sequential", zone_map: str = "dr",
                  gate_rule: str = "dr", abano: bool = False, question: Optional[str] = None
                  ) -> Dict[str, Any]:
    """One complete reading as a JSON-safe dict (the shape a future /geomancy endpoint returns)."""
    if scheme not in SCHEMES:
        raise ValueError(f"scheme: {'|'.join(SCHEMES)}")
    if not (1 <= quesited <= 12 and 1 <= querent <= 12) or quesited == querent:
        raise ValueError("querent and quesited must be different houses 1–12")
    ms, source = cast_mothers(seed=seed, hardware=hardware, dots=dots, mothers=mothers)
    sh = shield_from_mothers(ms)
    H = house_chart(sh, houses)
    reconciler = add(sh["J"], H[quesited])
    j = sh["J"]
    return {
        "system": "geomancy", "source": source, "question": question,
        "options": {"scheme": scheme, "houses": houses, "zone_map": zone_map, "gate_rule": gate_rule,
                    "querent": querent, "quesited": quesited, "abano": abano},
        "shield": {p: _brief(sh[p], scheme, zone_map) for p in POSITIONS},
        "houses": {str(h): dict(_brief(H[h], scheme, zone_map), meaning=HOUSE_MEANINGS[h],
                                gd=H[h]["gd_houses"][h - 1]) for h in range(1, 13)},
        "judge": {"name": j["name"], "gd_general": j["gd_general"], "favourable": j["favourable"],
                  "unfavourable": j["unfavourable"], "source": j["da"]},
        "sentence": sh["S"]["name"], "reconciler_gd": reconciler["name"],
        "validation": validate(sh),
        "via_puncti": via_puncti(sh),
        "perfection": perfection(H, querent, quesited, abano),
        "company": [company(H, h) for h in (querent, quesited)],
        "part_of_fortune": part_of_fortune(sh, houses),
        "impediment": impediment(H),
        "numogram": {
            "speculative": True,
            "zone_map": zone_map, "zone_map_meaning": ZONE_MAPS[zone_map],
            "judge_zone": zone(j, zone_map), "base16_judge": base16_view(j, gate_rule),
            "iching_nuclear": {"non_historical": True, "judge_hexagrams": hexagrams_for_figure(j),
                               "rule": "figure = lines 5,4,3,2 (Fire … Earth) of a hexagram"},
        },
    }


# ─── TEXT OUTPUT ───
def _glyph(planet: str) -> str:
    return GLYPHS.get(planet, "")


SHORT = {"Fortuna Major": "Fort.Maj", "Fortuna Minor": "Fort.Min", "Caput Draconis": "Caput Dr",
         "Cauda Draconis": "Cauda Dr", "Acquisitio": "Acquisit", "Conjunctio": "Conjunct"}


def format_shield(data: Dict[str, Any], style: str = "unicode") -> List[str]:
    sh = data["shield"]

    def row(keys: Sequence[str], width: int) -> List[str]:
        cols = [render(sh[k]["bits"], style) for k in keys]
        out = ["".join(c[i].center(width) for c in cols) for i in range(4)]
        out.append("".join((sh[k]["name"] if width > 10 else SHORT.get(sh[k]["name"], sh[k]["name"]))
                           .center(width) for k in keys))
        return out

    lines: List[str] = []
    # Traditional layout reads right to left: M1 is the rightmost figure on the top row.
    lines += row(["D4", "D3", "D2", "D1", "M4", "M3", "M2", "M1"], 9)
    lines += [""] + row(["N4", "N3", "N2", "N1"], 18)
    lines += [""] + row(["LW", "RW"], 36)
    lines += [""] + row(["J"], 72)
    return lines


def format_geomancy(data: Dict[str, Any], style: str = "unicode", full: bool = False) -> str:
    o = data["options"]
    sep = "══════════════════════════════════════════════════════════════════════"
    out = [sep, "  GEOMANCY — SHIELD CHART", f"  Source: {data['source']}   scheme: {o['scheme']}   "
           f"houses: {o['houses']}", sep]
    if data.get("question"):
        out.append(f"  Question: {data['question']}")
    out += format_shield(data, style)
    j = data["judge"]
    out += ["", f"  Judge: {j['name']} — {j['gd_general']}",
            f"    favourable: {j['favourable']}", f"    unfavourable: {j['unfavourable']}",
            f"  Witnesses: right {data['shield']['RW']['name']}, left {data['shield']['LW']['name']}"
            f"   Sentence (J+M1): {data['sentence']}   GD Reconciler (J+house {o['quesited']}): "
            f"{data['reconciler_gd']}"]
    v = data["validation"]
    out.append(f"  Checks: judge even {'✓' if v['judge_even'] else '✗'}, repeat {'✓' if v['repeat_in_16'] else '✗'}, "
               f"inseparables {'✓' if v['inseparables']['ok'] else '✗'} "
               f"({v['inseparables']['set1'][0]} / {v['inseparables']['set2'][0]})")
    vp = data["via_puncti"]
    if vp["kind"] == "single":
        out.append(f"  Via Puncti: {' → '.join(vp['paths'][0])}")
    else:
        out.append(f"  Via Puncti: {vp['kind']} (double-point Judge; not a traditional Via Puncti)"
                   + (f": ends {', '.join(vp['ends'])}" if vp["kind"] == "branching" else ""))
    out += ["", "  House  Figure            Planet       Sign         Elem    GD in this house"]
    for h in range(1, 13):
        x = data["houses"][str(h)]
        pl = f"{_glyph(x['planet'])} {x['planet']}" if style == "unicode" else x["planet"]
        out.append(f"  {h:>5}  {x['name']:<17} {pl:<12} {str(x['sign'] or '—'):<12} "
                   f"{str(x['element'] or '—'):<7} {x['gd']}")
    p = data["perfection"]
    out += ["", f"  Perfection (house {o['querent']} {p['querent']['figure']} ↔ house {o['quesited']} "
            f"{p['quesited']['figure']}): {', '.join(p['modes'])}"]
    for d in p["details"][: (None if full else 3)]:
        out.append(f"    {d['mode']}: {d['detail']}")
    for c in data["company"]:
        if c["company"]:
            out.append(f"  Company {c['house']}–{c['partner']}: {c['company']} ({' + '.join(c['figures'])})")
    pf = data["part_of_fortune"]
    out.append(f"  Part of Fortune: {pf['points']} points → figure {pf['figure_number']}, house {pf['house']} "
               f"({pf['figure']})")
    if data["impediment"]:
        out.append(f"  ⚠ {data['impediment']}")
    n = data["numogram"]
    b = n["base16_judge"]
    out += ["", "  [speculative numogram hooks — not traditional geomancy]",
            f"    Judge → zone {n['judge_zone']} ({n['zone_map']}: {n['zone_map_meaning']})",
            f"    base-16: zone {b['zone16']} :: {b['syzygy_zone16']} ({b['syzygy']}, = inversion), "
            f"current {b['current16']}, gate T={b['gate_tri']} → {b['gate_target16']} ({b['gate_figure']}, "
            f"rule {b['gate_rule']})",
            f"    I Ching via nuclear lines 2–5 [non-historical]: hexagrams "
            f"{', '.join(map(str, n['iching_nuclear']['judge_hexagrams']))}"]
    if full:
        out += ["", "  Figure notes (paraphrased from Digital Ambler, 'De Geomanteia'):"]
        for k in ("M1", "J"):
            f = figure(data["shield"][k]["name"])
            out.append(f"    {f['name']} ({f['english']}; {', '.join(f['alt'])}): image {f['image']}; "
                       f"{f['sephirah']}; body {f['body']}.  {f['da']}")
    out.append(sep)
    return "\n".join(out)


def figures_table(scheme: str = "golden-dawn", style: str = "unicode") -> str:
    out = [f"  {'#':>2}  {'Figure':<15} {'English':<19} {'Lines':<6} {'Pts':>3}  {'Planet':<11} "
           f"{'Sign':<12} {'Elem':<6} {'Struct':<6} Inv / Rev / Conv"]
    for f in sorted(FIGURES, key=lambda f: f["value"]):
        at = attributions(f, scheme)
        out.append(f"  {f['value']:>2}  {f['name']:<15} {f['english']:<19} {''.join(map(str, f['bits'])):<6} "
                   f"{f['points']:>3}  {f['planet']:<11} {str(at['sign'] or '—'):<12} {str(at['element'] or '—'):<6} "
                   f"{f['element_structural']:<6} {name(invert(f))} / {name(reverse(f))} / {name(convert(f))}")
    out.append(f"  (lines: 1 = single point, Fire first; scheme {scheme}: {SCHEMES[scheme]['source']})")
    return "\n".join(out)


# ─── CLI ───
def _opt(args: List[str], flag: str, default: Optional[str] = None) -> Optional[str]:
    if flag in args:
        i = args.index(flag)
        if i + 1 >= len(args):
            print(f"{flag} needs a value"); sys.exit(2)
        return args[i + 1]
    return default


def main(argv: Optional[List[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    if "--help" in args or "-h" in args:
        print(__doc__); return 0
    style = "plain" if "--plain" in args else "unicode"
    scheme = _opt(args, "--scheme", "golden-dawn")
    houses = _opt(args, "--houses", "sequential")
    zone_map = _opt(args, "--zone-map", "dr")
    gate_rule = _opt(args, "--gate-rule", "dr")
    for flag, val, ok in (("--scheme", scheme, SCHEMES), ("--houses", houses, ("sequential", "astrological")),
                          ("--zone-map", zone_map, ZONE_MAPS), ("--gate-rule", gate_rule, ("dr", "mod"))):
        if val not in ok:
            print(f"{flag} must be one of {', '.join(ok)}"); return 2
    if "--figures" in args:
        print(figures_table(scheme, style)); return 0
    if "--census" in args:
        c = census(zone_map, houses, gate_rule)
        print(json.dumps(c, indent=2)); return 0

    seed = None
    if "--seed" in args:
        a = _opt(args, "--seed")
        try:
            seed = int(a, 16) if a.lower().startswith("0x") else int(a)
        except ValueError:
            print(f"--seed needs an integer (decimal or 0x-hex), got {a!r}"); return 2
    dots = mothers = None
    if "--dots" in args:
        try:
            dots = [int(x) for x in _opt(args, "--dots").replace(",", " ").split()]
            mothers_from_dots(dots)
        except ValueError as e:
            print(f"--dots needs 16 positive integers ({e})"); return 2
    if "--mothers" in args:
        try:
            mothers = [figure(x) for x in _opt(args, "--mothers").split(",")]
        except KeyError as e:
            print(f"--mothers: {e}"); return 2
        if len(mothers) != 4:
            print("--mothers needs exactly four figures"); return 2
    question = _opt(args, "--question")
    quesited = 7
    try:
        if "--house" in args:
            quesited = int(_opt(args, "--house"))
        elif "--topic" in args or question:
            quesited = house_for_topic(_opt(args, "--topic", question or "")) or 7
        querent = int(_opt(args, "--querent", "1"))
        data = cast_geomancy(seed=seed, hardware="--hardware" in args, dots=dots, mothers=mothers,
                             quesited=quesited, querent=querent, scheme=scheme, houses=houses,
                             zone_map=zone_map, gate_rule=gate_rule, abano="--abano" in args,
                             question=question)
    except ValueError as e:
        print(f"geomancy: {e}"); return 2
    if "--json" in args:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(format_geomancy(data, style=style, full="--full" in args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
