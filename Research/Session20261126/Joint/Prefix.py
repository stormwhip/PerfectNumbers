"""Integer Euler prefix verification; sieve necessary conditions, no primality assumption for survivors."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Joint import *
@cache
def premium(s):return min((e-s-i)*4*lo(3)+max(lo(10**8),2*i*lo(10**11)-hi(A)) for i in range(e-s+1))
def prefix():
    # Root A ≡5 (mod 8) is nonsquare; each A prime ordinary when q∤A. Therefore their even hull / A >1e8.
    assert A%8==5 and all(pow(3,1163,k)!=1 or not prime64(k) for k in range(2327,10**8+1,2326))
    cutoff=2220*hi(10);best=cutoff;amin=None
    for s in range(1020,e+1):
        y=3**s
        def base(k):q=2*k*y-1;return lo(pe*A*q)+lo(2*q)-hi(3)+premium(s)
        if base(1)>=best:continue
        cap=10001;m=1
        while m<cap:
            q=2*m*y-1
            if m%3 and not any(m%t==0 for t in BAN) and not any(q%t==0 for t in small if t<2000) and pow(2,q-1,q)==1:break
            m+=2
        z=base(m)
        if z<best:best=z;amin=(s,m)
    return best,amin
if __name__=='__main__':print(prefix())
