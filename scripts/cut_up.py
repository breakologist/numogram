"""
Zone-Weighted Cut-Up Generator with Xenotation

Generates cut-up text where the cut ratio, fragmentation style, and
vocabulary substitution are determined by the target numogram zone.
Xenotation (nullotation → tic notation → prime factorization) is applied
as a zone-specific textual decomposition for outer zones (0, 3, 6, 9).
"""

import os, re, random, math, json

# ═══════════════════════════════════════════
# CORPUS
# ═══════════════════════════════════════════
def load_corpus():
    corpus = {}
    targets = {
        'ccru': "/home/etym/numogram/docs/numogram-source.txt",
        'djynxx': "/home/etym/.hermes/obsidian/hermetic/wiki/demon-djynxx.md",
        'paramita': "/home/etym/.hermes/obsidian/hermetic/wiki/paramita.md",
        'iching': "/home/etym/.hermes/obsidian/hermetic/wiki/i-ching-connections.md",
        'xenotation': "/home/etym/.hermes/obsidian/hermetic/wiki/xenotation-triangle-rotation.md",
        'quotes': "/home/etym/.config/conky/numogram-quotes.txt",
    }
    for name, path in targets.items():
        if os.path.exists(path):
            corpus[name] = _clean(open(path).read())
    
    journal_dir = "/home/etym/.hermes/obsidian/hermetic/wiki/autonomous-journal"
    journals = []
    for f in sorted(os.listdir(journal_dir)):
        if f.startswith('session-') and f.endswith('.md'):
            journals.append(_clean(open(os.path.join(journal_dir, f)).read()))
    corpus['journals'] = '\n\n'.join(journals)
    return corpus

def _clean(text):
    text = re.sub(r'^---[\s\S]*?---\n', '', text)
    text = re.sub(r'^#{1,6}\s*.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\|.*\|', '', text)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def get_fragment(corpus, source=None):
    if source and source in corpus:
        return corpus[source]
    return corpus[random.choice(list(corpus.keys()))]

# ═══════════════════════════════════════════
# FRAGMENTER
# ═══════════════════════════════════════════
def fragment(text, mode="sentence"):
    text = re.sub(r'\s+', ' ', text).strip()
    if mode == "word":
        return text.split()
    elif mode == "phrase":
        return [p.strip() for p in re.split(r'(?<=[,;:\u2014\u2013-])\s+', text) if p.strip()]
    elif mode == "mid-sentence":
        parts = re.split(r'(?<=[ ,])', text)
        return parts[::2]
    elif mode == "clause":
        return [s.strip() for s in re.split(r'(?<=[.!?])\s*', text) if len(s.strip()) > 10]
    elif mode == "term":
        return re.findall(r'\b[A-Z][a-zA-Z]{3,}\b|\b[a-z]{4,}\b', text)
    elif mode == "sentence":
        return [s.strip() for s in re.split(r'(?<=[.!?:])\s+', text) if len(s.strip()) > 10]
    elif mode == "paragraph":
        return [p.strip() for p in text.split('\n\n') if p.strip()]
    return text.split()

def cut(fragments, ratio=0.50):
    keep = max(1, int(len(fragments) * (1.0 - ratio)))
    random.shuffle(fragments)
    return fragments[:keep]

# ═══════════════════════════════════════════
# XENOTATION — three stages per Aamodt
# ═══════════════════════════════════════════
XENO = {
    "zero":"∅","void":"∅","one":"1","two":"2","three":"3",
    "four":"4","five":"5","six":"6","seven":"7","eight":"8",
    "nine":"9","and":"&","time":"T","gate":"G","zone":"Z",
    "current":"C","syzygy":"\u223F","demon":"\u0394","plex":"\u2119",
    "warp":"\u03A8","surge":"\u2191","sink":"\u2193","cycle":"\u221E",
    "loop":"\u21BB","mesh":"\u229E","net-span":"||",
    "hexagram":"\u2630","trigram":"\u2637",
    "paramita":"\u03C0","energy":"\u039E","kundalini":"\u3030","dharma":"\u2638",
    "digital root":"DR","digital":"DR","value":"AQ",
}

EXTRA_XENO = {
    "becomes":"\u2192","transforms":"\u2297","flows":"\u223F","enters":"\u2295","exits":"\u2296",
    "the":"\u2202","of":"\u2218","is":"\u2261","not":"\u00AC","all":"\u2200","from":"\u27F6",
    "into":"\u27F9","through":"\u27F7","between":"\u27E1","within":"\u27E8\u27E9",
}

def prime_factors(n):
    if n <= 1: return []
    factors = []; d = 2
    while d * d <= n:
        while n % d == 0: factors.append(d); n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

def prime_order(p):
    n, count = 2, 0
    while n <= p:
        if all(n % d != 0 for d in range(2, int(math.sqrt(n))+1)):
            count += 1
            if n == p: return count
        n += 1
    return 1

def tic_notation(n):
    if n <= 1: return "\u00B7"
    factors = prime_factors(n)
    shapes = {2: ":", 3: "(:)", 5: "((:))", 7: "(::)" }
    parts = []
    for f in factors:
        if f in shapes:
            parts.append(shapes[f])
        else:
            idx = prime_order(f)
            parts.append('(' * (idx - 1) + ':' + ')' * (idx - 1))
    return "".join(parts)

def nullotate(text):
    tics = re.findall(r'[\(\):]+', text)
    if not tics:
        wc = len(text.split())
        depth = max(1, min(wc % 5 + 1, 5))
        return '(' * depth + ')' * depth
    result = ""
    for t in tics:
        inner = t.replace(':', '()')
        result += inner
    return result if result else "()"

def xenotate(text, mode="sparse"):
    r = text
    for term, sym in XENO.items():
        r = re.sub(r'\b' + term + r'\b', sym, r, flags=re.IGNORECASE)
    if mode in ("verb", "heavy", "total"):
        for t, s in EXTRA_XENO.items():
            r = r.replace(t, s)
    if mode == "total":
        words = r.split()
        new = []
        for w in words:
            new.append(w)
            if random.random() < 0.25:
                d = random.randint(1, 4)
                new.append('(' * d + ')' * d)
        r = ' '.join(new)
    return r

# ═══════════════════════════════════════════
# RECOMBINER
# ═══════════════════════════════════════════
def recombine(frags, style="echo"):
    if style == "echo":
        out = []
        for f in frags:
            out.append(f); out.append(f + "\u2014")
        return out
    elif style == "splice":
        out = []
        for i in range(0, len(frags)-1, 2):
            if i+1 < len(frags):
                a, b = frags[i], frags[i+1]
                mid = len(a)//2
                sp = mid
                for j in range(mid, len(a)):
                    if a[j] in ',; ':
                        sp = j; break
                out.append(a[:sp] + b[sp:])
            else:
                out.append(frags[i])
        return out
    elif style == "bridge":
        return [' / '.join(frags[i:i+2]) for i in range(0, len(frags), 2)]
    elif style == "palindrome":
        front = frags[:len(frags)//2]
        back = frags[len(frags)//2:]
        return front + back[::-1]
    elif style == "duplicate":
        out = []
        for f in frags:
            out.append(f); out.append(f)
        return out
    return frags

# ═══════════════════════════════════════════
# ZONE PROFILES
# ═══════════════════════════════════════════
ZONES = {
    0: {"name":"Void",        "cut":0.90, "mode":"word",       "xen":True, "xmode":"heavy",  "sep":"\n",    "rec":False,   "prefix":"\u00B7 "},
    1: {"name":"Surge",       "cut":0.50, "mode":"phrase",     "xen":False,"xmode":None,     "sep":" ",     "rec":True,    "rs":"echo"},
    2: {"name":"Separation",  "cut":0.60, "mode":"clause",     "xen":False,"xmode":None,     "sep":" / ","rec":True,    "rs":"bridge"},
    3: {"name":"Warp",        "cut":0.40, "mode":"mid-sentence","xen":True, "xmode":"verb",   "sep":" \u2192 ","rec":True,    "rs":"splice"},
    4: {"name":"Gate",        "cut":0.55, "mode":"sentence",   "xen":False,"xmode":None,     "sep":"",      "rec":False,   "prefix":""},
    5: {"name":"Pressure",    "cut":0.35, "mode":"paragraph",  "xen":False,"xmode":None,     "sep":"\n\n",  "rec":False,   "prefix":""},
    6: {"name":"Abstraction", "cut":0.45, "mode":"term",       "xen":True, "xmode":"heavy",  "sep":" :: ","rec":False,   "prefix":""},
    7: {"name":"Blood",       "cut":0.50, "mode":"phrase",     "xen":False,"xmode":None,     "sep":" ","rec":False,   "prefix":""},
    8: {"name":"Multiplicity","cut":0.20, "mode":"keep",       "xen":False,"xmode":None,     "sep":"\n",    "rec":True,    "rs":"duplicate"},
    9: {"name":"Plex",        "cut":0.10, "mode":"recursive",  "xen":True, "xmode":"total",  "sep":" ",     "rec":True,    "rs":"palindrome"},
}

# ═══════════════════════════════════════════
# GENERATORS
# ═══════════════════════════════════════════
def generate(corpus, zone, source=None, length=40, seed=None):
    if seed is not None: random.seed(seed)
    z = ZONES[zone]
    text = get_fragment(corpus, source)
    frags = fragment(text, z["mode"])
    frags = cut(frags, z["cut"])
    if z.get("rec"):
        frags = recombine(frags, z.get("rs", "echo"))
    if z["xen"]:
        frags = [xenotate(f, z.get("xmode", "sparse")) for f in frags]
    prefix = z.get("prefix", "")
    frags = [prefix + f for f in frags]
    frags = frags[:length]
    return z["sep"].join(frags)

def generate_multi(corpus, zones=None, length=30, seed=None, sources=None):
    if zones is None: zones = list(range(10))
    parts = []
    for z in zones:
        zname = ZONES[z]["name"]
        text = generate(corpus, z, length=length, seed=seed)
        parts.append(f"\n--- ZONE {z} [{zname.upper()}]")
        parts.append(text)
    return '\n'.join(parts)

def nullotate_chain(corpus, zone, length=40, seed=None, iters=3):
    """
    Recursive void-folding chain (Zone 0 / Zone 9).
    Each iteration takes the previous output, nullotates it,
    and uses the nullotation as a seed prefix for the next cut.
    Produces: text → text+() → text+(()) → text+((())) ...
    """
    if seed is not None: random.seed(seed)
    z = ZONES[zone]
    text = get_fragment(corpus)
    frags = fragment(text, z["mode"])
    frags = cut(frags, z["cut"])
    if zone == 9:
        # Plex: nullotate every nth word
        output = " ".join(frags)
        for i in range(iters):
            output = nullotate(output) + " " + output
    else:
        # Zone 0 Void: insert void foldings between words
        output = " ".join(frags)
        for i in range(iters):
            depth = random.randint(1, i+2)
            output = output.replace(" ", " " + "("*depth + ")"*depth + " ", random.randint(3, 8))
    return output[:length*5]  # cap length

if __name__ == '__main__':
    import sys
    corpus = load_corpus()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        # Default: generate multi-zone
        result = generate_multi(corpus, seed=666, length=25)
        print(result)
        sys.exit(0)
    
    if cmd == "zone" and len(sys.argv) > 2:
        zone = int(sys.argv[2])
        source = sys.argv[3] if len(sys.argv) > 3 else None
        length = int(sys.argv[4]) if len(sys.argv) > 4 else 40
        seed = int(sys.argv[5]) if len(sys.argv) > 5 else 666
        print(generate(corpus, zone, source, length, seed))
    
    elif cmd == "all":
        print(generate_multi(corpus, seed=666, length=30))
    
    elif cmd == "test":
        print("\n=== XENOTATION TEST ===\n")
        for n in [36, 45, 78, 86, 174, 234]:
            pf = prime_factors(n)
            tic = tic_notation(n)
            null = nullotate(tic)
            print(f"  {n:3d} \u2192 {pf} \u2192 {tic:15s} \u2192 null: {null}")
        
        print("\n=== SAMPLE: ZONE 9 PLEX ===\n")
        result = generate(corpus, 9, seed=45, length=80)
        print(result)
        
        print("\n=== SAMPLE: ZONE 0 VOID ===\n")
        result = generate(corpus, 0, seed=0, length=60)
        print(result)
        
        print("\n=== SAMPLE: ZONE 3 WARP ===\n")
        result = generate(corpus, 3, seed=3, length=30)
        print(result)
    
    else:
        print(f"Usage: cut_up.py [zone <N> [source] [length] [seed] | all | test]")
