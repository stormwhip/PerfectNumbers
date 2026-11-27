"""Replay every child including all simultaneous precio-supplier terminals."""
from pathlib import Path
from functools import cache
from math import prod
from collections import Counter
import json,gzip,sys
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H));from Prefix import proves,C,B
from PivotCheck import exact_leaf

def verify(name,expect):
 D=json.loads(gzip.decompress((H/name).read_bytes()));assert __debug__ and D['p']==11 and D['e']==396 and D['pivot']==2383 and set(map(int,D['cases']))==set(expect)
 seen=set();count=Counter()
 @cache
 def prime(z):
    n=z
    if n>=2**64:
        for row in D['ecpp'][str(z)]:assert row[0]==n;n=C.pc.level(*row)
        seen.add(str(z))
    assert C.pc.prime64(n);return True
 def live(P):
    st=C.State(P);return not st.conflict and st.base<=B and prod(C.sigma(z,h) for z,h in P)<=2*st.X
 def walk(P,node):
    assert live(P);kind=node['type'];count[kind]+=1
    if kind=='dual':assert set(node)=={'type'} and proves(P);return
    st=C.State(P)
    if kind=='forest':
        k,o,h=node['roots'],node['owners'],node['head'];C.validate_forest(st,k,o,h,prime);assert min(exact_leaf(P,k,o,h),C.Forest(st,k,o,h).lower()[0])>B;return
    assert kind=='split';q=node['q'];assert prime(q) and q not in st.rows and q not in st.bad and st.D%q==0;c=C.valuation(st.D,q);h=c;allowed=set();scale=st.base//q**c
    while scale*q**h<=B:
        nxt=P+[(q,h)]
        if st.possible(q,h,c) and live(nxt):allowed.add(str(h));walk(nxt,node['cases'][str(h)])
        h+=1
    assert allowed==set(node['cases'])
 assert prime(2383) and C.valuation(C.sigma(11,396),2383)==1
 for f,tr in D['cases'].items():walk([(11,396),(2383,int(f))],tr)
 assert seen==set(D['ecpp']);print('PASS',sorted(expect),dict(count),'certs',len(seen),flush=True)
if __name__=='__main__':verify('HybridFour.json.gz',[96,106,126,138])
