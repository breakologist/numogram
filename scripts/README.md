# Text Recombination & Xeno-Jump Scripts

Numogram-native text transformation pipeline.

## Core Scripts

| Script | Purpose |
|--------|---------|
| `xeno_jump.py` | AQ checksum-preserving vocabulary mutation |
| `cut_up.py` | Zone-weighted fragmentation engine (10 profiles, 7 modes) |
| `seed_transforms.py` | 4-method permutation engine (Fixed Chain, Truncated, Syzygy, Phrase Jump) |
| `run_recursive_jumps.py` | Multi-method recursive generator (7 output files) |
| `oracle_text_seed.py` | Oracle → xeno-jump → cut-up pipeline |

## Corpus

| File | Size | Description |
|------|------|-------------|
| `aq_corpus_enriched.json` | ~1.1MB | 89K+ entries, 535 AQ buckets. Sources: CCRU texts, autonomous journals, oracle.py, numogame code, cult-garden lore |

## Usage

```bash
# Basic xeno-jump
python3 xeno_jump.py "Seed phrase" --mode all

# Cut-up with zone profile
python3 cut_up.py all

# Recursive jumps (multi-output)
python3 run_recursive_jumps.py

# Oracle-seeded pipeline
python3 oracle_text_seed.py --seed 666
```

## Architecture

The pipeline treats the numogram AQ system as a checksum trapdoor:
1. Calculate AQ checksum of source text
2. Replace each word with a synonym from the same AQ bucket
3. Repeat recursively — the numerical skeleton holds, vocabulary drifts to glossolalia
4. Pass jumped text through the cut-up engine for zone-profiled fragmentation
