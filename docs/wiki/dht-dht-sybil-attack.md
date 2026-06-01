---
title: BitTorrent DHT — Coordinated Sybil Attack Analysis
created: 2026-06-01
tags:
  - security
  - P2P
  - DHT
  - Sybil-attack
  - distributed-systems
  - numogram
status: annotation
source: raw/dht.md (84 lines)
---

# BitTorrent DHT — Coordinated Sybil Attack Analysis

**Source:** `raw/dht.md` — attributed r/torrents post with authorial voice, operational detail, academic references, and explicit attribution chain. Content is a primary-source report; claims should be cross-checked against the cited papers and IP records.

**Caveat:** Raw text contains slurs and casual profanity. The technical content is substantive and worth extracting regardless of the framing language.

---

## Attack Summary

Coordinated Sybil attack on the **Mainline DHT** (Mainline BitTorrent DHT, UDP 6881) lasting ≥5 months at time of writing. Multiple attacker groups performing complementary roles:

1. **Nearest-node spoofers** — fake peers with IDs *very close* to the victim's node ID, clustered in the same bucket. They are reported as next-step routers for victim requests, giving the attacker visibility into all DHT lookups.
2. **Hash-targeted infiltrators** — nodes that dynamically generate IDs matching recently-requested torrent hashes, blending into legitimate query results. Confirmed via Tixati DHT Event Log: same IP addresses cycling through IDs correlated with victim query history.
3. **Empty-bucket polluters** — populate buckets with non-existent node addresses in response to legitimate queries, forcing clients to exhaust retries and abandon searches.

**Endgame observed:** Attackers have escalated from passive observation to active disruption — returning long lists of fake nodes to make clients "give up the search after many futile tries."

**Targeted null-routing:** Specific content categories are null-routed (no peers returned):
- Nyaa and RuTracker hashes (treated as "pirated")
- Ubuntu official torrents (likely re-uploaded to a tracking site)
- Pornolab hashes are *not* null-routed — "Like, you need to pay us more?"

---

## Technical Indicators

### Observable Anomalies in Tixati
- **Node Table**: 20-21 buckets should be full; attacker presence appears as many *empty* buckets followed by sudden clusters of nodes with near-identical IDs to your own.
- **Port clustering**: attackers mostly use **6881** for DHT — port alone is not a useful signal because IDs are already the real fingerprint.
- **ID proximity**: IDs sharing the first 4+ bytes with your node ID are statistically almost impossible at random. These are generated, not random.
- **DHT Event Log (detailed mode)**: same IP addresses replying with new IDs correlated to recent queries.

### Client-Side Mitigations
- **Tixati v3 protocol**: uses blind hashes (`hash(hash)`); public DHT only sees the outer hash, real content owners can still connect.
- **BiglyBT / Azureus / Vuze**: separate DHT network with IDs partially tied to IPv4 subnets, making flooding harder.
- **Blunt-force countermeasure**: seed 50+ random non-existing hashes across the full DHT ID space via browser console:
  ```
  crypto.getRandomValues(new Uint8Array(20)).toHex();
  ```
  This floods your buckets with legitimate-looking unknown requests, reducing attacker density. Ineffective if attacker decides to block *all* DHT activity.

### Academic References Cited
1. `doi.org/10.1145/1883612.1883615` — Sybil attack foundations (2000s, original formulation)
2. `doi.org/10.1109/NTMS.2011.5721044`
3. `doi.org/10.1109/P2P.2013.6688697` — DHT-specific attack taxonomy
4. `arXiv:1412.0103` — DHT size estimation (Sohl et al.) — contains proposal for more secure DHT implementation
5. `eli.sohl.com/2020/06/05/dht-size-estimation.html` — same author, details on using regular searches to measure irregularities

---

## Attribution

**IP range:** `31.200.249.0/24` (active ≥1 year)

**WHOIS:** Teleport Rus LLC — contact: **Andrey Klimenko**, also head of **PiratePay**

**Entity chain:**

| Entity | What it does |
|--------|-------------|
| PiratePay | Anti-piracy; pivoted from ISP-local P2P optimization → DPI/censorship push; funded by Microsoft + Skolkovo; demo'd to Putin |
| Teleport Media | "Bittorrent Video CDN" — Russian version mentions Olympic-scale traffic; no confirmed international licensing clients |
| Zillion Data | Big-data hourly gathering of global bittorrent statistics |
| Nodr App | "We pay crypto for using your network" — botnet-in-a-suit |
| AS216158 | BGP-visible network; increased global connectivity Jan 2026; doing China business |

**Narrative arc per raw text:** Investors originally tried to steer ISP torrent traffic to LAN peers (legitimate P2P optimization), then pivoted to anti-piracy via DPI+Sybil attacks, then to data gathering, then to a "video CDN" that may actually be pirate TV infrastructure layered on P2P. Author's read: Hollywood's enforcement arm outsourced to a provincial Russian company with both legal-copyright and surveillance infrastructure experience.

---

## Hash-Routing as a Structural Vulnerability

The fundamental issue is not "BitTorrent is insecure" — it's that **hash-based ID routing is adversarial by design under targeted Sybil pressure**:

- DHT lookup routes through **k nearest nodes** to the target hash
- Attacker only needs to control a fraction of those k nodes to intercept, observe, or deny
- The attack is **slow-burn**: start with observation, measure insertion success, then escalate to disruption
- ID synthesis is trivial when using port 6881 as a canary — the port is not concealed because IDs are already a red herring

This maps onto any hash-routed system where node identity is self-asserted rather than cryptographically bound to an address: PDHTs, Kademlia-based networks, content-addressed stores without proof-of-storage.

---

## Connection to Hermetic / Numogram Concerns

### Salt + Oil Framing
The DHT attack is a layered residual phenomenon that maps cleanly onto [[salt-and-oil-residual-memory]]:

- **Salt layer** — the persistent structural corruption: attacker-controlled buckets that *stay* polluted across days, near-identical IDs that crystallize in routing tables, the slowly-growing list of 450+ IPs. This is mineral persistence: once a bucket is filled with fake nodes, it takes deliberate flushes to clear.
- **Oil layer** — the dynamic infiltration: hash-targeted ID cycling, query-correlated responses, the escalation from observation to active disruption. This is the combustible, shape-shifting component.
- **Threshold** — the moment both layers are simultaneously active is when the attack moves from passive monitoring to search poisoning (the "give up after many futile tries" phase). Exactly the combined-layer state.

### Security Implications for the Project
Hermes Agent and its infrastructure (wiki sync, skill distribution, plugin network) depend on:
- **GitHub as a coordination point** — not DHT, but similar public-key trust model. The Blobby attack pattern (observe → measure → escalate) is observable in git-based coordination too.
- **Entropy sources** — [[numogram-entropy-source]] and hardware entropy digestion. If entropy is gathered from public network sources, it is vulnerable to the same observation-and-poisoning pattern. Self-hosted entropy should take the DHT lesson seriously.
- **Plugin/skill loading from repos** — analogous to DHT: you resolve a skill name to a source. If the resolver is poisoned or the source is replaced, you load adversarial code. The current architecture (explicit git URL + pin) is structurally safer than DHT.
- **MCP server discovery** — the MCP ecosystem uses a growing registry. The DHT lesson applies: registry poisoning is easier than attacking the server itself.

### Numogram Pattern
The attack's temporal structure maps onto a **syzygy chain**:
- Day 0 (observation) → Zone 0 register
- Day 1–4 (measurement and ID calibration) → current 0→1→2→3→4
- Day 5 (escalation to active disruption) → Zone 5 arrival
- Day 6–7 (null-routing, content filtering) → Zone 6→7

This matches the pattern seen in [[land-posts]] smooth-skid flatline: the attack's rhythm is composed of differential speeds, beginning imperceptibly.

---

## Cross-References

- [[salt-and-oil-residual-memory]] — salt/oil framework for residual attack layers
- [[numogram-entropy-source]] — hardware entropy; network-sourced entropy has same vulnerability shape
- [[land-posts]] — CCRU"smooth skids" / differential-speed rhythm of attacks
- [[zone-7]] — amphibian threshold; the attack's slow escalation mirrors Zone 7's "imperceptible advance"
- [[pandemonium-matrix]] — parallel to 45-demon taxonomy; fake node groups could be mapped as adversarial pandemonium entries
- FOOM / Transq training loops — relevant to the "observe → measure → escalate" cycle as a reinforcement pattern
- [[cables-gl]] — if DHT-style Sybil attacks ever target visual-programming coordination layers, the node graph is a natural attack surface

---

## Action Items

- [ ] Cross-check DOI references and confirm papers still accessible
- [ ] Verify AS216158 / 31.200.249.0/24 WHOIS data current as of 2026-06-01
- [ ] Map attacker IP patterns onto existing [[pandemonium-matrix]] entity slots
- [ ] Draft "Distributed Trust" section for main security page
- [ ] File under `raw/dht.md` as primary source; consider archival mirror
- [ ] Evaluate whether Hermes MCP registry introduces similar trust assumptions to DHT
- [ ] Add hash-blinding (analogous to Tixati v3 blind hashes) to entropy source design

---

*Raw source included unedited slurs that have been omitted from this synthesis. The technical content stands without them.*
