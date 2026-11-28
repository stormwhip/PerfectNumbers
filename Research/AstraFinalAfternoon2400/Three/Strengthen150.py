"""Complete Euler-one exterior/internal role split for p=398581, h=150.
The v3 Euler coordinate is partitioned without importing any frozen numeric cut.
"""
from TwoSided import *
from hashlib import sha256
from fractions import Fraction as F

def verify():
    assert __debug__
    k='6-2-150';rows=CASES[k];R,fixed,odd,X,S,D,spec=certificate(rows);p=rows[-1][0];z=1093
    V,E=price2(rows,p);F0=fixed[3]-vp(S,3)
    assert F0==5 and fixed[z]-vp(S,z)==1 and fixed[p]-vp(S,p)==149
    assert sig(3,6)==z and sig(z,2)==3*p and spec==[(p,151,D)] and V>B and not E
    counts={};states=[]
    for i in range(2):
      for j in range(150):
        m=z**i*p**j
        for a in range(6):
          q=lower_euler(m,a);M=m*3**a;qq=2*M-1;W=p**(2*j)
          if V*q>B*W or X*D*q>B:typ='basic'
          elif X*D*R*q>B and not inside_euler(qq,M,D):typ='parity'
          elif inside_euler(qq,M,D):typ='internal Euler possible'
          else:
            B1=2*X*D*R*q*q>3*B
            B2=4*V*X*D*q**4>9*B**2*W*D or (j>0 and X*D*q*q*p**j>B*max(p**151,q)*(p**(151-j)+4))
            typ='source' if (B1 and B2) else 'exterior Euler open'
          counts[typ]=counts.get(typ,0)+1;states.append((i,j,a,typ))
    digest=sha256(repr(states).encode()).hexdigest()
    assert counts=={'basic':545,'internal Euler possible':631,'exterior Euler open':390,'source':217,'parity':17}
    assert digest=='7918cc639dfd359b96d3f604e08b42d4a630492b2b78068b07f08318f6ac30ae'
    print('PASS complete 1800-window enumeration',counts,digest,flush=True)
    return states
if __name__=='__main__':verify()
