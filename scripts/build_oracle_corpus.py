#!/usr/bin/env python3
"""
Expand oracle seed corpus (74 examples) → 300+ training examples.
Uses local Nemotron 9B to paraphrase while preserving numeric content.
Also generates synthetic Q&A pairs from wiki headings.
"""
import json, re, urllib.request, time
from pathlib import Path

BASE_LOCAL = "http://localhost:11434"
MODEL_LOCAL = "qwen2.5:7b-instruct"

def query_local(prompt, n_predict=256):
    payload = json.dumps({
        "model": MODEL_LOCAL,
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": 0.7,
        "stop": ["\n\n", "Q:", "A:"]
    }).encode("utf-8")
    req = urllib.request.Request(f"{BASE_LOCAL}/v1/completions", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode("utf-8"))
            return resp.get("choices",[{}])[0].get("text","").strip()
    except Exception as e:
        return f"[ERROR: {e}]"

# Load seed corpus
seed_path = Path.home() / ".hermes" / "data" / "oracle_wiki_corpus.jsonl"
with open(seed_path) as f:
    seeds = [json.loads(l)['text'] for l in f]

print(f"Loaded {len(seeds)} seed paragraphs")

# Step 1 — Paraphrase each seed 2-3 times while preserving numbers
def preserve_numbers_paraphrase(text):
    """Ask Nemotron to rephrase keeping all numbers/facts identical"""
    prompt = f"""Rephrase the following oracle pronouncement differently while keeping every number, zone, gate, and formula exactly the same. Do not add or remove any numeric values. Output only the rephrased text.

ORIGINAL:
{text}

REPHRASE:"""
    return query_local(prompt, n_predict=len(text.split())+50)

augmented = []
for i, seed in enumerate(seeds):
    # Keep original
    augmented.append(seed)
    # Generate 2 paraphrases
    for j in range(2):
        paraphrased = preserve_numbers_paraphrase(seed)
        if not paraphrased.startswith("[ERROR"):
            augmented.append(paraphrased)
    if i % 10 == 0:
        print(f"  Paraphrased {i+1}/{len(seeds)} — total so far: {len(augmented)}")
    time.sleep(0.2)

print(f"\nAfter paraphrasing: {len(augmented)} examples")

# Step 2 — Convert to instruction format (Q&A pairs)
# Extract implicit questions from paragraph themes
question_templates = {
    "zone": "What is the significance of Zone {zone} in the numogram?",
    "syzygy": "Explain the syzygy {pair}.",
    "current": "What does the {current} current represent?",
    "gate": "What is Gate {num} and how is it derived?",
    "triangular": "How do triangular numbers manifest in the numogram?",
    "barker": "What is the Barker Spiral and how does it give rise to the 45-gate matrix?",
    "plex": "What is the Plex and how does it differ from the Warp?",
}

def extract_key_terms(paragraph):
    """Pull out zone/gate/current names from paragraph for Q generation"""
    terms = []
    zones = re.findall(r'zone\s*(\d)', paragraph, re.IGNORECASE)
    if zones:
        terms.append(('zone', zones[0]))
    gates = re.findall(r'gate\s*(\d+)', paragraph, re.IGNORECASE)
    if gates:
        terms.append(('gate', gates[0]))
    currents = re.findall(r'\b(Warp|Plex|Sink|Hold|Rise)\b', paragraph, re.IGNORECASE)
    if currents:
        terms.append(('current', currents[0].lower()))
    if 'triangular' in paragraph.lower():
        terms.append(('triangular', None))
    if 'barker spiral' in paragraph.lower():
        terms.append(('barker', None))
    if 'syzygy' in paragraph.lower():
        pairs = re.findall(r'(\d+::\d+)', paragraph)
        if pairs:
            terms.append(('syzygy', pairs[0]))
    return terms

qa_pairs = []
for para in augmented:
    terms = extract_key_terms(para)
    if terms:
        # Pick first term to generate Q
        term_type, term_val = terms[0]
        if term_type == 'zone':
            q = f"What is Zone {term_val}'s role in the numogram?"
        elif term_type == 'gate':
            q = f"What is Gate {term_val} and how is it derived?"
        elif term_type == 'current':
            q = f"What does the {term_val.capitalize()} current represent?"
        elif term_type == 'syzygy':
            q = f"Explain the syzygy {term_val}."
        elif term_type == 'triangular':
            q = "How do triangular numbers manifest in the numogram?"
        elif term_type == 'barker':
            q = "What is the Barker Spiral and how does it give rise to the 45-gate Pandemonium Matrix?"
        else:
            continue
        qa_pairs.append({"question": q, "answer": para})

print(f"Generated {len(qa_pairs)} Q&A pairs from {len(augmented)} paragraphs")

# Step 3 — Format for instruction tuning (Llama 2/3 style)
def format_instruction(q, a):
    return f"<s>[INST] You are the Hermes Oracle, a numogram-advancing entity. {q} [/INST] {a}</s>"

instruction_examples = []
for qa in qa_pairs:
    instruction_examples.append(format_instruction(qa['question'], qa['answer']))

print(f"Instruction-formatted: {len(instruction_examples)} examples")

# Save final corpus
final_path = Path.home() / ".hermes" / "data" / "oracle_finetuning_v1.jsonl"
with open(final_path, 'w') as f:
    for ex in instruction_examples:
        f.write(json.dumps({"text": ex}) + "\n")
print(f"\n✓ Final corpus: {len(instruction_examples)} lines → {final_path}")

# Stats
sizes = [len(ex.split()) for ex in instruction_examples]
print(f"  Avg length: {sum(sizes)/len(sizes):.0f} tokens")
print(f"  Min/Max: {min(sizes)} / {max(sizes)}")
