"""E3b lower bound with joint price 81, b=0; pure integer logic. Optional python-flint for pow."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from Internal import *
from Next import primes,BAN
SPEED='--fast' in sys.argv
if SPEED:
    sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'));from flint import fmpz

def power(a,h,q):return int(pow(fmpz(a),h,fmpz(q))) if SPEED else pow(a,h,q)

def order_elim(q):
    # r<q handled by gcd(A,z) on every nontrivial order-d residue.
    # ord_q(r)=1 yields r≡1 mod q so no r in (1,q). For r>=q prove separately.
    assert R**200>10**2400
    seen={1}
    for f in range(2,200,2):
        d=gcd(f+1,q-1)
        if d in seen:continue
        for a in range(2,64):
            g=power(a,(q-1)//d,q);z=g;xs=[1];prod=1
            while z!=1 and len(xs)<d:xs.append(z);prod=prod*z%A;z=z*g%q
            if len(xs)==d and z==1:break
        else:return False
        if gcd(prod,A)!=1:return False
        seen.add(d)
    return True

def verify(t):
    caprows=caps(t);n=0
    for s,l in caprows:
        y=3**s;assert 2*y-1>50000
        ss=bytearray(b'\1')*(l+1);ss[::2]=bytes(l//2+1)
        for p in (*BAN,3):ss[::p]=bytes(l//p+1)
        for p in primes:
            k=pow(2*y,-1,p)
            if k<=l:ss[k::p]=bytes((l-k)//p+1)
        for m in range(1,l+1,2):
            if not ss[m]:continue
            q=2*m*y-1
            if power(2,q-1,q)!=1:continue
            # If r>=q, r^2>A so c=1. Thus H>=A*q as well as r^f*R^(2i)>=q²R^(2i).
            assert q*q>A and q>50000
            assert min(PE*q*81**(E-s-i)*max(A*q,q*q*R**(2*i)) for i in range(E-s+1))>10**t,(s,m,'large-r')
            assert order_elim(q),(s,m);n+=1
    print(dict(e=E,target=t,prefix=sum(l for _,l in caprows),order_exclusions=n),flush=True)
if __name__=='__main__':verify(int(sys.argv[1]))
