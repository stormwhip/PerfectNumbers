"""Rigorous cheap screen for all zero-premium A factors with moderate p-adic order: bound expansion in p^t explicitly.
All r|A satisfy 1 mod 2(e+1); explore cumulative multiplicative rep lattice via gcd for small allowable k; no primality needed.
"""
from pathlib import Path
import sys,math,json
cases=[(7,906),(7,738),(7,456),(13,612),(13,618)]
def run(p,e,mult):
    A=(p**(e+1)-1)//(p-1);D=2*(e+1);assert all((e+1)%j for j in range(2,math.isqrt(e+1)+1))
    r0=[a for a in range(2,p) if pow(a,3,p)==1];bad=[];N=0
    for t in range(1,e+1):
        m=p**t
        # Each prime of A of odd order 3 mod p and that level lies on these CRT progressions.
        for a,x in enumerate(r0):
            z=x+m*((1-x)*pow(m,-1,D)%D)
            if z<=mult*m:
                mn=min(mult*m,A);v=1
                for r in range(z,mn+1,D*m):
                    if r<2:continue
                    # strip non-exact level so the same prime not reported at lower t.
                    if pow(r,3,p*m)==1:continue
                    N+=1;v=v*r%A
                if math.gcd(v,A)>1:bad.append((t,math.gcd(v,A)))
        r0=[pow(x,p,m*p) for x in r0]
    print(dict(p=p,e=e,C=mult,progressions_tested=N,gcd_hits=bad),flush=True);assert not bad
if __name__=='__main__':
    for p,e in cases:run(p,e,int(sys.argv[1]) if len(sys.argv)>1 else 100000)
