"""Fallback arithmetic terminal for exact (11,16), t^25, s^16."""
from pathlib import Path
from functools import cache
from math import gcd,prod
from fractions import Fraction
import sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'FinalNight2400/Ten')]
from Coverage import sigma,prime64,val,B,require
from Weighted import lifts
P=11;T=50544702849929377;S=239337374873;BAN=(7,19)
ROWS=[(P,16),(T,25),(S,16)]
WEIGHT=106
FACTORS=(107,279599737)


def certify():
    require(all(prime64(q) for q in (P,T,S,*FACTORS)) and S-1==8*prod(FACTORS),'scope or order factorization')
    require(sigma(P,16)==T and sigma(T,25)%S==0 and T%4==1,'exact prefix')
    c=16-sum(val(sigma(q,h),S) for q,h in ROWS);require(c==15,'remaining S demand')
    X=prod(q**h for q,h in ROWS);D=prod(sigma(q,h)//(1+h%2) for q,h in ROWS)
    while (d:=gcd(D,P*T*S))>1:D//=d
    require(X*D<=B,'whole prefix already over size')
    # High Euler absent because exact t^25 occupies the slot. At most 5100 in index;
    # all positive S outputs have order 107 and exact base depth. No LTE shift.
    require(3**5100>B and (S-1)%107==0 and FACTORS[1]>5101 and S>5101,'not full order domain')
    U={}
    for j,rs in enumerate(lifts(S,107,c),1):
        m=S**j;R=m**WEIGHT
        for r in rs:
            if not r%2 or r in (1,P,T,S,*BAN) or r**WEIGHT>=R:continue
            if any(r%q==0 and q!=r for q in (3,5,7,11,13,17,19,23,29,31,37,41,43,47)):continue
            if pow(r,107,m*S)==1 or pow(2,r-1,r)!=1:continue
            if X*D*(r**106//gcd(r**106,D))>B:continue
            U[r]=max(U.get(r,Fraction(1)),Fraction(R,r**106))
    F=prod(U.values(),start=Fraction(1));lower=Fraction(X*S**(WEIGHT*c),1)/F
    require(lower>B,'S price too weak')
    print('PASS t^25, s^16 fallback terminal; exceptions',len(U),flush=True)

if __name__=='__main__':certify()
