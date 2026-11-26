"""High Euler exponent or Euler supplying zero (q^1, s=0) => upper bound on number of distinct A prime factors.
Uses prior general Teich pricing + new numeric premium for EVERY ordinary A prime.
"""
import sys
from pathlib import Path
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here));from ExceptionalCube import cases
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'Research/EulerOneSieve'));from TeichmullerBaseline import B, Profile
for p in sorted(set(p for p,e in cases)):
    prof=Profile(p,max(e for q,e in cases if q==p))
    for q,e in cases:
        if p!=q:continue
        u=prof.U(e);d=prof.D(e);k=0
        while p**(3*e)*10**(10*k)<=B*u*d:k+=1
        print(dict(p=p,e=e,U=u,D=d,ordinary_A_primes_max=k-1,all_A_primes_max_if_Euler_in_A=k))
