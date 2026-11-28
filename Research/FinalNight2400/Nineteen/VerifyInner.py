"""Exact compulsory Q^2, and 35 complete tertiary branches inside (19,282;t^10;r^28)."""
from pathlib import Path
from math import prod
from functools import cache
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'Session20261126'));from PivotCheck import C,B,exact_leaf

def main():
    assert __debug__;K=json.loads(gzip.decompress((P/'Packet28Inner.json.gz').read_bytes()));Q=K['Q'];seen=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2;y=z
        if z>=2**64:
            seen.add(str(z))
            for row in K['ecpp'][str(z)]:assert y==row[0];y=C.pc.level(*row)
        assert C.pc.prime64(y);return True
    base=[(19,282),(1735317810514627,10),(8383027,28)];assert all(prime(z) for z,h in base)
    assert all(C.State(base[:i]).D%base[i][0]==0 for i in (1,2));seenNodes=[0,0]
    def live(s):return not s.conflict and s.base<=B and prod(C.sigma(z,h) for z,h in s.rows.items())<=2*s.X
    def kids(rows,z):
        s=C.State(rows);assert live(s) and prime(z) and z not in s.rows and s.D%z==0
        c=C.valuation(s.D,z);k=c;out={}
        while s.base//z**c*z**k<=B:
            if s.possible(z,k,c):
                child=rows+[(z,k)]
                if live(C.State(child)):out[str(k)]=child
            k+=1
        return out,k
    def walk(rows,node):
        if node['type']=='split':
            ds,_=kids(rows,node['q']);assert set(ds)==set(node['cases']);seenNodes[0]+=1
            for k,R in ds.items():walk(R,node['cases'][k])
        else:
            assert node['type']=='forest';s=C.State(rows);a,b,h=node['roots'],node['owners'],node['head'];C.validate_forest(s,a,b,h,prime)
            assert C.Forest(s,a,b,h).lower()[0]>B and exact_leaf(rows,a,b,h)>B;seenNodes[1]+=1
    ds,tail=kids(base,Q);assert set(ds)=={'2'};ds2,tail2=kids(ds['2'],23773);assert len(ds2)==37 and set(ds2)-set(K['nodes'])=={'1','4'} and set(K['nodes'])<=set(ds2)
    for h,node in K['nodes'].items():walk(ds2[h],node)
    assert seen==set(K['ecpp']);print('PASS 282 r^28 fixes Q^2, 23773 residual {1,4}; excluded',len(K['nodes']),'tails',tail,tail2,'split/forest',seenNodes,'ECPP',len(seen),flush=True)
if __name__=='__main__':main()
