"""
Zone-Weighted Cut-Up Generator with Xenotation

Generates cut-up text where the cut ratio, fragmentation style, and
vocabulary substitution are determined by the target numogram zone.
Xenotation (nullotation → tic notation → prime factorization) is applied
as a zone-specific textual decomposition for outer zones (0, 3, 6, 9).
"""

import os, re, random, math, json, zipfile

# ═══════════════════════════════════════════
# CORPUS SELECTION
# ═══════════════════════════════════════════
def _epub_text(path):
    """Extract readable text from an epub (zip of xhtml)."""
    texts = []
    try:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.endswith(('.xhtml', '.html', '.htm', '.txt')):
                    try:
                        t = z.read(name).decode('utf-8', errors='ignore')
                        t = re.sub(r'<[^>]+>', ' ', t)
                        t = t.replace('&amp;', '&').replace('&nbsp;', ' ')
                        t = re.sub(r'\s+', ' ', t).strip()
                        if len(t) > 100:
                            texts.append(t)
                    except: pass
    except: pass
    return '\n\n'.join(texts)

CORPUS_SOURCES = {
    'oracle': {
        'ccru': "/home/etym/.hermes/obsidian/hermetic/raw/Unleashing the Numogram.md",
        'grok_rotor': "/home/etym/.hermes/obsidian/hermetic/raw/Grok rotor.md",
        'grok_notes': "/home/etym/.hermes/obsidian/hermetic/raw/Grok notes on the Numogram.md",
        'grok_convo': "/home/etym/.hermes/obsidian/hermetic/raw/Grok convo.md",
        'grok_angband': "/home/etym/.hermes/obsidian/hermetic/raw/Grok Angband conversation.md",
        'land_numogram': "/home/etym/.hermes/obsidian/hermetic/raw/nick land numogram explained.txt",
        'land_time': "/home/etym/.hermes/obsidian/hermetic/raw/nick land time.txt",
        'unleashing': "/home/etym/.hermes/obsidian/hermetic/raw/Unleashing the Numogram.md",
        'declab': "/home/etym/.hermes/obsidian/hermetic/raw/ccru-net-declab-stripped-2026-04-28.txt",
        'occultures': "/home/etym/.hermes/obsidian/hermetic/raw/ccru-net-occultures-full-2026-04-28.txt",
        'djynxx': "/home/etym/.hermes/obsidian/hermetic/wiki/demon-djynxx.md",
        'paramita': "/home/etym/.hermes/obsidian/hermetic/wiki/paramita.md",
        'iching': "/home/etym/.hermes/obsidian/hermetic/wiki/i-ching-connections.md",
        'bentov': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Itzhak Bentov - Stalking The Wild Pendulum - On the Mechanics of Consciousness.epub"),
        'starships': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Star.Ships.epub"),
        'geosophia_i': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Geosophia-I.epub"),
        'geosophia_ii': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Geosophia-II.epub"),
        'time_sorcery': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Time Sorcery - Vexsys.epub"),
        'cryptolith': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/LAND -- Cryptolith.epub"),
        'xenosystems': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/XENOSYSTEMS_FRAGMENTS.epub"),
        # --- New sources: lexical & philosophical texture (added 2026-05-16) ---
        'devils_dictionary': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/Ambrose Bierce - The Devil's Dictionary.epub"),
        'buddhist_suttas': "/home/etym/.hermes/obsidian/hermetic/raw/Buddhist-Suttas.md",
        'diamond_sutra': "/home/etym/.hermes/obsidian/hermetic/raw/Diamond-Sutra.md",
        'lotus_sutra': "/home/etym/.hermes/obsidian/hermetic/raw/Lotus-Sutra.md",
        'mountains_water': "/home/etym/.hermes/obsidian/hermetic/raw/Mountains&Water-Sutra.md",
        'esoteric_alphabet': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/TheEsotericStructureOfTheAlphabet_AlvinBoydKuhn-TheEsotericStructureOfTheAlphabet.epub"),
        'troward_dore': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/T.Troward - Dore Lectures.epub"),
        'troward_creative': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/T.Troward - The Creative Process.epub"),
        'troward_edinburgh': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/T.Troward - The Edinburgh Lectures.epub"),
        'troward_hidden': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/T.Troward - The Hidden Power.epub"),
        'troward_law_word': ('epub', "/home/etym/.hermes/obsidian/hermetic/raw/T.Troward - The Law and the Word.epub"),
    },
    'xenon': {
        'gist_zones': "/home/etym/Documents/05-Research/gist",
        'kron_tensors': "/home/etym/.hermes/obsidian/hermetic/raw/Kron-TensorsForCircuits_djvu.txt",
        'tokyo_passport': "/home/etym/.hermes/obsidian/hermetic/raw/Tokyo Millennium Civilian Passport.txt",
    },
}

def load_corpus(name='oracle'):
    import zipfile
    corpus = {}
    targets = CORPUS_SOURCES.get(name, CORPUS_SOURCES['oracle'])
    
    for source_name, path in targets.items():
        if isinstance(path, tuple):
            # (format, actual_path)
            fmt, actual_path = path
            if fmt == 'epub':
                corpus[source_name] = _clean(_epub_text(actual_path))
        elif os.path.isdir(path):
            # Read all text files in directory
            for f in sorted(os.listdir(path)):
                fp = os.path.join(path, f)
                if os.path.isfile(fp) and f.endswith(('.txt', '.md')):
                    try:
                        text = _clean(open(fp, encoding='utf-8', errors='ignore').read())
                        if text:
                            corpus[f"{source_name}:{f}"] = text
                    except: pass
        elif os.path.exists(path):
            corpus[source_name] = _clean(open(path).read())
    
    # Journals always available for oracle
    if name in ('oracle', 'all'):
        journal_dir = "/home/etym/.hermes/obsidian/hermetic/wiki/autonomous-journal"
        if os.path.exists(journal_dir):
            journals = []
            for f in sorted(os.listdir(journal_dir)):
                if f.startswith('session-') and f.endswith('.md'):
                    journals.append(_clean(open(os.path.join(journal_dir, f)).read()))
            if journals:
                corpus['journals'] = '\n'.join(journals)
    
    # Filter empty entries
    corpus = {k: v for k, v in corpus.items() if v and len(v) > 20}
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
    
    # Check for --corpus flag
    corpus_name = 'oracle'
    args = sys.argv[1:]
    if '--corpus' in args:
        idx = args.index('--corpus')
        if idx + 1 < len(args):
            corpus_name = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    corpus = load_corpus(corpus_name)
    
    if len(sys.argv) > 1:
        cmd = args[0] if args else None
    else:
        # Default: generate multi-zone
        result = generate_multi(corpus, seed=666, length=25)
        print(result)
        sys.exit(0)
    
    if cmd == "zone" and len(args) > 1:
        zone = int(args[1])
        source = args[2] if len(args) > 2 else None
        length = int(args[3]) if len(args) > 3 else 40
        seed = int(args[4]) if len(args) > 4 else 666
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
