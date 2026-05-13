"""
Xeno-Jump: Semantic Jump via AQ Value

Takes a text and replaces words with other words/phrases from our corpus
that share the same AQ value (Sum of 10-35 per char).
The "numerical skeleton" of the text remains identical, but the vocabulary mutates.

Usage:
    python xeno_jump.py "The time is now"  -- Replace random words
    python xeno_jump.py "The time is now" --target "time"  -- Replace specific word
    python xeno_jump.py "The time is now" --mode full  -- Replace all jumpable words
"""

import os
import re
import json
import random
import argparse

# ═══════════════════════════════════════════
# CORE MATH
# ═══════════════════════════════════════════
def get_aq(word):
    """
    Canonical CCRU AQ Algorithm:
    A=10, B=11 ... Z=35.
    Non-alpha characters are ignored in the sum.
    """
    return sum(ord(c.upper()) - 55 for c in word if c.isalpha())

def digital_root(n):
    """Masonic Addition / Digital Root."""
    if n == 0: return 0
    return (n - 1) % 9 + 1

# ═══════════════════════════════════════════
# LOAD INDEX
# ═══════════════════════════════════════════
def load_index(path="/home/etym/.hermes/scripts/aq_corpus_index.json"):
    if not os.path.exists(path):
        print(f"ERROR: Index not found at {path}. Run the scanner first.")
        exit(1)
    
    with open(path) as f:
        # JSON keys are strings, convert to int
        raw = json.load(f)
        return {int(k): v for k, v in raw.items()}

# ═══════════════════════════════════════════
# XENO-JUMP LOGIC
# ═══════════════════════════════════════════
def jump_word(word, index, strategy='random', seed=None):
    if seed is not None: random.seed(seed)
    
    val = get_aq(word)
    candidates = index.get(val, [])
    
    if not candidates:
        return word, False, val # No jump possible
    
    # Filter out the word itself
    options = [c for c in candidates if c.lower() != word.lower()]
    if not options:
        return word, False, val
    
    if strategy == 'random':
        new_word = random.choice(options)
    elif strategy == 'lexicographical':
        # Find the word alphabetically after the current one
        sorted_opts = sorted(options)
        for o in sorted_opts:
            if o > word.lower():
                new_word = o
                break
        else:
            new_word = sorted_opts[0] # Wrap around
    else:
        new_word = random.choice(options)
        
    # Preserve case styling
    if word[0].isupper():
        new_word = new_word.capitalize()
    elif word.isupper():
        new_word = new_word.upper()
        
    return new_word, True, val

def process_text(text, index, mode='all', seed=None, target_word=None):
    """
    Process text and perform jumps.
    mode='all': Jump every word that has a match.
    mode='random': Jump words with 30% probability.
    mode='first': Jump the first match.
    mode='target': Only jump 'target_word'.
    """
    tokens = re.split(r'(\W+)', text) # Split keeping separators
    result = []
    jump_info = [] # (Original, New, AQ Value, Zone)
    
    for token in tokens:
        # Is it a word?
        if re.match(r'^[a-zA-Z]+$', token):
            
            # Check conditions
            should_jump = False
            
            if mode == 'all':
                should_jump = True
            elif mode == 'random' and random.random() < 0.3:
                should_jump = True
            elif mode == 'target' and token.lower() == target_word.lower():
                should_jump = True
            elif mode == 'first' and not any(j for j in jump_info if j[1]):
                should_jump = True
            
            if should_jump:
                new_w, hit, val = jump_word(token, index, seed=seed)
                if hit:
                    result.append(new_w)
                    zone = digital_root(val) if val > 0 else 0
                    jump_info.append((token, new_w, val, zone))
                    continue
            
            result.append(token) # Append original if no jump
        else:
            result.append(token)
            
    return "".join(result), jump_info

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Xeno-Jump via AQ Values")
    parser.add_argument("text", nargs='?', help="Input text or phrase")
    parser.add_argument("--mode", choices=['all', 'random', 'target', 'first'], default='random')
    parser.add_argument("--target", type=str, help="Word to target specifically")
    parser.add_argument("--seed", type=int, default=None)
    
    # If no text arg, use examples
    import sys
    if len(sys.argv) == 1:
        print("Usage examples:")
        print("  python xeno_jump.py \"Gnostic Calvinism is a circuit\"")
        print("  python xeno_jump.py --target \"the\" --mode target \"The machine is the map\"")
        sys.exit(0)
        
    args = parser.parse_args()
    index = load_index()
    
    if not args.text:
        print("Error: Please provide text.")
        sys.exit(1)
        
    new_text, stats = process_text(args.text, index, mode=args.mode, seed=args.seed, target_word=args.target)
    
    print(f"Original: {args.text}")
    print(f"Xeno:     {new_text}")
    
    if stats:
        print("\nJumps:")
        for orig, new, val, zone in stats:
            print(f"  {orig} ({val} AQ, Z{zone}) -> {new}")
