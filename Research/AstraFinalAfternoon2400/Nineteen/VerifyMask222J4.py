"""Exact complete j=4 terminal at the last f=2/g=22 second prefix of root 222."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,val,sig,need,T,R
sys.path.insert(0,str(RESEARCH/'Night2400/A'))
from MaskedForest import exact_absence_bound
from functools import cache
from fractions import Fraction
from math import prod,gcd

Q=2032322226061
P=((19,222),(T,2),(R,22),(Q,4))
BANS=(7,11)

def main():
    need(__debug__,'no Python optimization')
    z=readz(HERE/'Mask222J4.json.gz'); need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P and tuple(z['mask'])==BANS,'sealed scope')
    a=RESEARCH/'FinalNight2400/Root222'; w=readz(a/'ThirdForests.json.gz')['cases']['2:22']
    d,tail=domain(P[:3],Q)
    need(w['q']==Q and w['left']==[1,2,4,18,28] and set(d)==set(w['left'])|set(map(int,w['children'])) and 4 in d and tail==z['raw_tail'],'exact frozen third window')
    n=z['ecpp'];seen=set()
    @cache
    def prime(p):
        q=p
        if p>=2**64:
            a=n[str(p)];need(bool(a),'missing prime chain');seen.add(str(p))
            for x in a:need(x[0]==q,'wrong subject');q=C.pc.level(*x)
        return C.pc.prime64(q)
    X,D=exact(P);K,O,H=z['forest'];need(all(prime(q)for q in (*dict(P),*K,*BANS)) and len(K)==len(set(K)),'certified exact/compelled labels')
    need(all(D%q==0 and q not in dict(P) for q in K) and not set(K)&set(BANS) and not set(dict(P))&set(BANS),'distinct compulsory roots')
    I=Fraction(prod(sig(q,e)for q,e in P),X);lo=[]
    for q in K:
        a=val(D,q);h=a+(a%2 if q%4!=1 else 0)
        I*=Fraction(sig(q,h),q**h);lo.append([q,h])
    need(lo==z['minimum_abundance_exponents'],'minimum exponent receipt')
    # Permit multiple independent Euler positions while calculating I; a true
    # N obeys each individual minimum, so this only weakens the lower bound.
    for p in BANS:
        e=1 if p%4==1 else 2
        need(I*Fraction(sig(p,e),p**e)>2,'unproved local absence')
    s=C.State(P,absent=BANS);need(not s.conflict and s.bad==BANS,'locally justified mask')
    C.validate_forest(s,K,O,H,prime)
    v=C.Forest(s,K,O,H).lower()[0];u=exact_absence_bound(P,K,O,H,BANS,B)
    need(min(v,u)>B and [floor10(v),floor10(u)]==z['floor10'] and set(n)==seen,'masked integer terminal')
    print('PASS root222 f=2,g=22,j=4; local absences 7 and 11; strict floors',z['floor10'],'prime chains',len(seen),'raw tail',tail)

if __name__=='__main__':main()
