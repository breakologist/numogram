---
title: DHT Sybil Attack — Primary Source
created: 2026-06-01
last_updated: 2026-06-01
source_count: 1
status: primary
tags: ["dht", "sybil", "teleport", "piratepay", "i2p", "bittorrent", "residual-trace", "network"]
---

# DHT Sybil Attack — Primary Source

**Source file:** `raw/dht.md`  
**Type:** Investigative dump + I2P paste reference  
**Date of observations:** ~2025–2026  
**Network indicators:** `31.200.249.0/24`, `AS216158`, `Teleport Rus LLC`, PiratePay, Nodr App  
**I2P paste:** http://privatebin.i2p/?83a11cb45a33f8bb#5282MS75jyz2moPHWx1vA4NFLusE6RnUWx6jgaybG4v8 (mirror: https://paste.i2pd.xyz/)

## Observed Pattern

A sustained Sybil attack on the BitTorrent Mainline DHT, lasting approximately five months at time of writing. Attackers injected fake node IDs clustered around the victim's own ID prefix, plus IDs matched to recently searched torrent hashes, so poisoned peers appeared as next-hop routes in both bucket listings and search responses.

Key behaviors reported:
- **Bucket poisoning:** Empty/fake nodes in lower-distance buckets.
- **Hash-targeted impersonation:** Nodes switch IDs to match recently requested torrent infohashes.
- **Selective null-routing:** Nyaa and RuTracker hashes blocked; Pornolab not blocked.
- **Search exhaustion:** Long lists of fake non-existent nodes returned, causing clients to abandon search.
- **Port bias:** Most fake nodes use 6881.
- **Rotation:** New fake nodes added daily; old ones recycled.

## Actor Chain

| Entity | Role | Notes |
|--------|------|-------|
| PiratePay | Corporate predecessor | ISP-side P2P throttling/MITM → antipiracy pivot; Microsoft + Skolkovo funding |
| Teleport Rus LLC | WHOIS contact for `31.200.249.0/24` | Same people, different entity |
| Teleport Media | BitTorrent Video CDN | Promoted record Olympic viewership; unverified real-world usage |
| Nodr App | "We pay crypto for using your network" | Botnet-shaped architecture |
| Zillion Data | Big-data torrent hash surveillance | Possibly same data-collection lineage |

## Why It Matters Here

This is not merely a network forensics artifact. In the wiki's own terms:

- **Residual memory operates on the DHT.** The distributed hash table is a distributed recurrence pressure field: each node is a crystallization of exposure. Fake nodes are interference patterns, not absence.
- **The attack is a salt-layer corruption.** Real peers carry the honest grain; fake peers are the crystallized repetition of an opposing intent — the environment retains the *shape* of manipulation even after individual attacker nodes rotate.
- **Oil / delayed ignition:** The I2P paste is dormant exposure. The list of 450+ fake node IDs is not action; it is potential recursion waiting for a trigger (re-entry, analysis, rejoining).
- **Gates as Sybil boundaries.** A syzygy gate is a transition between basins; a DHT Sybil attack is a manufactured boundary between honest and poisoned routing basins. CBD from `foom.md` is exactly the tool for locating where a client's search trajectory flips from real to fake: the basin boundary at `q(θ) ≈ 0.5`.
- **The 31.200.249.0/24 block as anomaly field.** Continuous high-frequency probing regardless of content type implies an observational rather than content-selective motive — the attacker wants topology, not piracy enforcement. That makes this a Mesh-style telemetry operation, not a takedown.

## External References Cited in Source

- https://doi.org/10.1145/1883612.1883615 — foundational Sybil attack paper (2000s)
- https://doi.org/10.1109/NTMS.2011.5721044
- https://doi.org/10.1109/P2P.2013.6688697
- https://doi.org/10.48550/arXiv.1412.0103 — DHT size estimation / irregularities
- https://eli.sohl.com/2020/06/05/dht-size-estimation.html — practical measurement
- https://bgp.he.net/net/31.200.249.0/24
- https://bgp.he.net/net/31.200.249.0/24#_SearchTab
- https://bgp.he.net/AS216158
- https://www.abuseipdb.com/check-block/31.200.249.0/24
- Archived corporate profiles: russoft, cyberleninka, archive.fo, YouTube

## Cross-References

- [[salt-and-oil-residual-memory]] — salt = crystallized fake-node repetition; oil = dormant I2P paste awaiting re-activation
- [[FOOM-numogram-kernel-synthesis]] — Cronkle Bisection Descent as the analytical tool for locating poisoned basin boundaries
- [[strange-signals-tetralogue]] — Mesh-∞ as uninvited guest; DHT Sybil is the network analogue of an invasive current
- [[numogram-structure]] — attractors / basins as DHT bucket topology
- [[pandemonium-glossary]] — demons as motive force without purpose: fake nodes inherit this structure
- [[land-posts]] — "most beautiful heretical abomination" framework applied to protocol-level subversion
