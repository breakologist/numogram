#!/usr/bin/env python3
"""Tic Xenotation (TX) and Nullotation (0X) encoder/decoder (Em, 1 Nov 2026).
TX (Hyperstition 003538, 2004): ':' = factor 2; '(x)' = the nth prime where n is the TX of x.
0X (Hyperstition 005109, 2005): substitute '()' for every TX ':' (so 2 = '()', 3 = '(())').
Mirrors lumpenspace/ccru@7c38ad9 app/lib/xenotation.ts. Run with no args for a self-check."""
import sys
P=[2]
def _grow(k=None,upto=None):
    c=P[-1]
    while (k and len(P)<k) or (upto and P[-1]<upto):
        c+=1
        if all(c%q for q in P if q*q<=c): P.append(c)
def prime(k): _grow(k=k); return P[k-1]
def primepi(p): _grow(upto=p); return P.index(p)+1
def factorint(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def tx(n):
    if n == 1: return ''
    out=''
    for p,e in sorted(factorint(n).items()):
        out += (':' if p==2 else '('+tx(int(primepi(p)))+')')*e
    return out
def nx(n): return tx(n).replace(':','()')
def dec(s):
    s=s.replace('()','\0') if ':' not in s else s  # 0X: '()' leaf -> factor 2
    i=0
    def prod(stop):
        nonlocal i; v=1
        while i<len(s):
            c=s[i]
            if c==')':
                if stop: return v
                raise ValueError(s)
            if c in ':\0': v*=2; i+=1; continue
            if c=='(':
                i+=1; inner=prod(True); i+=1; v*=prime(inner); continue
            raise ValueError(c)
        return v
    return prod(False)
if __name__=='__main__':
    if len(sys.argv)>1:
        for a in sys.argv[1:]: print(a, tx(int(a)) if a.isdigit() else dec(a))
    else:
        for n in range(2,10): print(n, tx(n), nx(n))
