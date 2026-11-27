"""Intersect the exact remaining two-pivot cells with independently checked forests."""
from pathlib import Path
import json,gzip,sys
from functools import cache
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')];from PivotCheck import C,B,exact_leaf
from Discrete import check,p,e,s,t

def verify():
 assert __debug__;L,prior,remaining=check();available=set(remaining);pack=json.loads(gzip.decompress((H/'CellForests.json.gz').read_bytes()));assert pack['p']==p and pack['e']==e
 done=set();seen=set()
 @cache
 def prime(z):
    assert type(z)==int and z>2;n=z
    if n>=2**64:
        for k in pack['ecpp'][str(n)]:assert k[0]==n;n=C.pc.level(*k)
        seen.add(str(z))
    assert C.pc.prime64(n);return True
 for k,node in pack['cases'].items():
    i,j=map(int,k.split(','));assert (i,j) in available and (i,j) not in done and node['type']=='forest';P=[(p,e),(s,i),(t,j)];st=C.State(P);assert not st.conflict and st.base<=B
    rr,oo,h=node['roots'],node['owners'],node['head'];C.validate_forest(st,rr,oo,h,prime);assert min(C.Forest(st,rr,oo,h).lower()[0],exact_leaf(P,rr,oo,h))>B;done.add((i,j))
 assert seen==set(pack['ecpp']) and len(available)==323 and len(done)==232
 print('19^358; 645 by price +',len(done),'by unrestricted forests; remaining',len(available-done),'of',len(L),'ECPP',len(seen),flush=True);return sorted(available-done)
if __name__=='__main__':verify()
