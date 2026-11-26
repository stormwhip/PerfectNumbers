"""Conditional secondary 3-adic budget across canonical roots, no ledger credit.
If 3^h||N and the Euler component supplies no 3, every remaining unit costs at least K/D after accounting for p^e exactly once. Recompute first impossible even h; no implication for smaller h or Euler supplying 3.
"""
from pathlib import Path
from fractions import Fraction
from math import isqrt
import json
R=Path(__file__).resolve().parents[1];ORDER=(19,7,11,31,13,3,5,17);B=10**2400;T=10000;K=T*T

def discount(bad):
    D=Fraction(1)
    for t in range(7,T,6):
        if t in bad or any(t%j==0 for j in range(2,isqrt(t)+1)):continue
        k=1;best=Fraction(1)
        while True:
            h=3**k-1;u=Fraction(K**k,t**h)
            if u<=1:break
            if any(pow(t,h+1,z*(t-1))==1 for z in bad):break
            best=max(best,u);k+=1
        D*=best
    return D

def run():
    # Bind the frozen original 244, so updating the published frontier never invalidates a conditional result.
    d=json.loads((R/'Midday/Delta.json').read_bytes());pairs={(s['root'],e) for s in d['remaining_shards'] for e in s['remaining_actuals']};assert len(pairs)==244;out=[]
    for p in ORDER:
        if p in (3,5,17):continue
        D=discount(ORDER[:ORDER.index(p)])
        for _,e in sorted(k for k in pairs if k[0]==p):
            v=(p**(e+1)-1)//(p-1);b=0
            while v%3==0:b+=1;v//=3
            if b==0:continue
            h=b+b%2
            while p**e*3**h*K**(h-b)*D.denominator<=B*D.numerator:h+=2
            assert h%2==0 and p**e*3**h*K**(h-b)*D.denominator>B*D.numerator
            out.append((p,e,b,h))
    return out
if __name__=='__main__':
    if not __debug__:raise SystemExit('assertions required')
    print(json.dumps({'scope':'secondary root-3 required; Euler supplies zero to 3','rows_p_e_primary_supply_first_impossible_v3':run(),'new_full_actuals':[]}))
