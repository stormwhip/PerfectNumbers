"""Exact compulsory Q^2, and 35 complete tertiary branches inside (19,282;t^10;r^28)."""
from pathlib import Path
from math import prod
from functools import cache
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'Session20261126'));from PivotCheck import C,B,exact_leaf

def main():
    assert __debug__;K=json.loads(gzip.decompress((P/'Masked24.json.gz').read_bytes()));seen=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2;y=z
        if z>=2**64:
            seen.add(str(z))
            for row in K['ecpp'][str(z)]:assert y==row[0];y=C.pc.level(*row)
        assert C.pc.prime64(y);return True
    base=[(19,282),(1735317810514627,10)];assert all(prime(z) for z,h in base)
    assert all(C.State(base[:i]).D%base[i][0]==0 for i in (1,));seenNodes=[0,0]
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
        if node['type']=='masked':
            s=C.State(rows);a=node['roots'];bad=node['bad'];assert len(a)==len(set(a)) and all(z not in s.rows and s.D%z==0 and prime(z) for z in a)
            parts=rows[:]
            for z in a:
                h=C.valuation(s.D,z);parts.append((z,h+(h%2 if s.fixed_euler or z%4==3 else 0)))
            sn=prod(C.sigma(z,h) for z,h in parts);xd=prod(z**h for z,h in parts)
            assert len(set(bad))==len(bad) and all(prime(z) and z not in a and z not in s.rows for z in bad)
            for z in bad:
                k=2 if z%4==3 or s.fixed_euler else 1;assert sn*C.sigma(z,k)>2*xd*z**k
            u=C.State(rows,absent=bad);a,o,k=node['roots'],node['owners'],node['head'];C.validate_forest(u,a,o,k,prime)
            sys.path.insert(0,str(P.parents[1]/'Night2400/A'));from MaskedForest import exact_absence_bound
            assert C.Forest(u,a,o,k).lower()[0]>B and exact_absence_bound(rows,a,o,k,u.bad,B)>B;return
        if node['type']=='ab':
            s=C.State(rows);a=node['roots'];assert len(a)==len(set(a)) and all(z not in s.rows and s.D%z==0 and prime(z) for z in a)
            parts=rows[:]
            for z in a:
                h=C.valuation(s.D,z);h+=h%2 if s.fixed_euler or z%4==3 else 0;parts.append((z,h))
            assert prod(C.sigma(z,h) for z,h in parts)>2*prod(z**h for z,h in parts);return
        if node['type']=='split':
            ds,_=kids(rows,node['q']);assert set(ds)==set(node['cases']);seenNodes[0]+=1
            for k,R in ds.items():walk(R,node['cases'][k])
        else:
            assert node['type']=='forest';s=C.State(rows);a,b,h=node['roots'],node['owners'],node['head'];C.validate_forest(s,a,b,h,prime)
            assert C.Forest(s,a,b,h).lower()[0]>B and exact_leaf(rows,a,b,h)>B;seenNodes[1]+=1
    ds,tail=kids(base,8383027);assert set(K['nodes'])=={'24'} and set(K['nodes'])<=set(ds) and tail==202
    for h,node in K['nodes'].items():walk(ds[h],node)
    assert seen==set(K['ecpp']);print('PASS roots 19,282 t^10; r^24 exact exclusions',seenNodes,'chains',len(seen))
if __name__=='__main__':main()