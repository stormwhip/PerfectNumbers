"""Exact bounded Euler-one interior divisor windows for LCM-prefixed pricing.

The price inequality N >= V*q/m² gives a rigorous U=floor(B*m²/V).
q has Euler residue 2*m-1 modulo 4*m. If the source index e+1 is an
odd prime n absent from its remaining block, every prime divisor q of
that block has exact order n for the source prime, and q = 1 mod 2*n.
Recompute all windows; account for each using the cheaper complete integer
progression, or an individually checked lattice witness on the prime side.
"""
from math import gcd, isqrt
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path[:0]=[str(H/'C7'),str(H.parent/'NightMerge')]
from PrefixPrice import excludes
from LatticeLeaf import verify as lattice


class Interior:
    def __init__(self,witnesses):
        assert type(witnesses) is dict
        self.witnesses=witnesses;self.used=set();self.enum=0;self.empty=0;self.calls=0

    def __call__(self,j,p,e,block,m,lo,upper,levels):
        self.calls+=1
        mod=4*m;q0=lo;upper=min(block,upper);n=e+1
        if n>2 and n%2 and all(n%k for k in range(2,isqrt(n)+1)) and block%n:
            # If q divides p-1, then sigma(p^e) = n mod q; the sole q=n is absent.
            # Otherwise q divides p^n-1 and ord_q(p)=n. Since q is odd, 2*n|q-1.
            g=gcd(mod,2*n)
            if (1-lo)%g:
                self.empty+=1;return True
            h=2*n//g; q0=lo+mod*((1-lo)//g*pow(mod//g,-1,h)%h);mod*=h
        if q0>upper:
            self.empty+=1;return True
        # q is positive and q0 is the smallest positive representative, because lo is.
        assert 1<=q0<mod and gcd(q0,mod)==1
        lower_k=(block+upper-1)//upper;max_k=block//q0
        z=block*pow(q0,-1,mod)%mod;k0=lower_k+(z-lower_k)%mod
        if k0>max_k:
            self.empty+=1;return True
        # A real cofactor is in that progression, and yields a tighter q interval.
        lo_q=max(q0,(block+max_k-1)//max_k);lo_q+=(q0-lo_q)%mod
        hi_q=min(upper,block//k0)
        if lo_q>hi_q:
            self.empty+=1;return True
        cq=1+(hi_q-lo_q)//mod;ck=1+(max_k-k0)//mod
        if min(cq,ck)<=100000:
            self.enum+=min(cq,ck)
            vals=range(lo_q,hi_q+1,mod) if cq<ck else range(k0,max_k+1,mod)
            return all(block%value for value in vals)
        key=','.join(map(str,(j,*levels)))
        assert key not in self.used;self.used.add(key)
        row=self.witnesses[key]
        assert set(row)=={'side','w'}
        if row['side']=='prime':
            # q0 is coprime to mod, so removing block factors sharing mod is harmless.
            n0=block
            while (g:=gcd(n0,mod))>1:n0//=g
            return lattice(n0,1,q0,mod,lo_q,hi_q,row['w'])
        assert row['side']=='cofactor' and gcd(block,mod)==1
        return lattice(block,1,z,mod,k0,max_k,row['w'])


def check(P,banned,targets,witnesses):
    h=Interior(witnesses)
    receipt=excludes(P,banned,targets,interior=h)
    assert h.used==set(witnesses)
    return receipt, {'interior_checks':h.calls,'empty':h.empty,'direct_divisions':h.enum,'lattice':len(h.used)}
