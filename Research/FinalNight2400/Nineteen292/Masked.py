"""Replay every child including all simultaneous precio-supplier terminals."""
from pathlib import Path
from functools import cache
from math import prod
from collections import Counter
import json,gzip,sys
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H));from Price import prefix
sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B
from PivotCheck import exact_leaf

def verify(name,expect):
 D=json.loads(gzip.decompress((H/name).read_bytes()));assert __debug__ and D['p']==19 and D['e']==292 and D['pivot']==10018843 and set(map(int,D['cases']))==set(expect)
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
    if kind in ('ab','masked'):
        st=C.State(P);k=node['roots'];assert set(k).isdisjoint(st.rows) and len(k)==len(set(k)) and all(prime(y) and st.D%y==0 for y in k)
        extras=[]
        for y in k:
            v=C.valuation(st.D,y);extras.append((y,v+(v%2 if st.fixed_euler or y%4==3 else 0)))
        an=prod(C.sigma(y,h) for y,h in P+extras);ad=prod(y**h for y,h in P+extras)
        if kind=='ab':assert an>2*ad;return
        bad=node['bad'];assert len(bad)==len(set(bad)) and not set(bad)&(set(k)|set(st.rows))
        for y in bad:
            assert prime(y);h=2 if st.fixed_euler or y%4==3 else 1;assert an*C.sigma(y,h)>2*ad*y**h
        st=C.State(P,absent=bad);o,n=node['owners'],node['head'];C.validate_forest(st,k,o,n,prime)
        sys.path.insert(0,str(H.parents[1]/'Night2400/A'));from MaskedForest import exact_absence_bound
        assert min(C.Forest(st,k,o,n).lower()[0],exact_absence_bound(P,k,o,n,st.bad,B))>B;return
    st=C.State(P)
    if kind=='forest':
        k,o,h=node['roots'],node['owners'],node['head'];C.validate_forest(st,k,o,h,prime);assert min(exact_leaf(P,k,o,h),C.Forest(st,k,o,h).lower()[0])>B;return
    assert kind=='split';q=node['q'];assert prime(q) and q not in st.rows and q not in st.bad and st.D%q==0;c=C.valuation(st.D,q);h=c;allowed=set();scale=st.base//q**c
    while scale*q**h<=B:
        nxt=P+[(q,h)]
        if st.possible(q,h,c) and live(nxt):allowed.add(str(h));walk(nxt,node['cases'][str(h)])
        h+=1
    assert allowed==set(node['cases'])
 assert prime(10018843) and C.valuation(C.sigma(19,292),10018843)==1
 for f,tr in D['cases'].items():walk([(19,292),(10018843,int(f))],tr)
 assert seen==set(D['ecpp']);print('PASS',sorted(expect),dict(count),'certs',len(seen),flush=True)
if __name__=='__main__':
    verify('First26.json.gz',[26]);verify('First28.json.gz',[28])
