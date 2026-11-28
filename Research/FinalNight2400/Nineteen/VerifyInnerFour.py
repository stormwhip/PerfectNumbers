"""Fully eliminate h28 23773^4; use direct exact stock price at fixed-Euler prefix."""
from pathlib import Path
from math import prod
from functools import cache
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path[:0]=[str(P.parents[1]/'Session20261126'),str(P.parents[1]/'FinalSprint')];from PivotCheck import C,B,exact_leaf;import JointValuation as J

def main():
    assert __debug__;baseQ=json.loads(gzip.decompress((P/'Packet28Inner.json.gz').read_bytes()));Q=baseQ['Q'];D=json.loads(gzip.decompress((P/'Packet28Four.json.gz').read_bytes()));seen=set();stats=[0,0,0]
    @cache
    def prime(z):
        n=z
        if n>=2**64:
            seen.add(str(z))
            for row in D['ecpp'][str(z)]:assert n==row[0];n=C.pc.level(*row)
        assert C.pc.prime64(n);return True
    base=[(19,282),(1735317810514627,10),(8383027,28),(Q,2),(23773,4)];assert all(prime(z) for z,h in base)
    def live(s):return not s.conflict and s.base<=B and prod(C.sigma(z,h) for z,h in s.rows.items())<=2*s.X
    def walk(rows,n):
        s=C.State(rows);assert live(s)
        if n['type']=='transfer':
            # Direct theorem replay; no mathematical transfer needed by this verifier.
            assert rows==base+[(319414207966840061,4),(491,2),(6529,1)];J.excludes(rows,(),[0,2,3]);stats[2]+=1;return
        if n['type']=='forest':
            a,b,h=n['roots'],n['owners'],n['head'];C.validate_forest(s,a,b,h,prime);assert C.Forest(s,a,b,h).lower()[0]>B and exact_leaf(rows,a,b,h)>B;stats[1]+=1;return
        assert n['type']=='split';q=n['q'];assert prime(q) and q not in s.rows and s.D%q==0;c=C.valuation(s.D,q);k=c;seenK=set()
        while s.base//q**c*q**k<=B:
            if s.possible(q,k,c):
                r=rows+[(q,k)]
                if live(C.State(r)):seenK.add(str(k));walk(r,n['cases'][str(k)])
            k+=1
        assert seenK==set(n['cases']);stats[0]+=1
    walk(base,D['nodes']);assert stats==[3,58,1] and seen==set(D['ecpp']);print('PASS r28 23773^4; 3 full splits,58 strict forests,1 exact 3-target price')
if __name__=='__main__':main()
