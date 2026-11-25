"""Search/replay 1108 globally with exact FLINT modular powers and all-s base. No logs or LP.
Reuse pure-stdlib Next.py for logic, replace modular exponentiation only if --fast. cwd arbitrary.
"""
import sys
from pathlib import Path
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here));from Next import *
if '--fast' in sys.argv:
    sys.path.insert(0,str(here/'vendor'));from flint import fmpz
    def modpow(a,h,q):return int(pow(fmpz(a),h,fmpz(q)))
else:modpow=pow

def order_test(q,cap):
    if cap>=q*q:return False
    # If a positive r with r^f<=cap exists, its lower bound r>=3 gives f<bit_length(cap).
    seen={1};maxf=cap.bit_length()
    for f in range(2,maxf,2):
        d=gcd(f+1,q-1)
        if d in seen:continue
        for a in range(2,64):
            g=modpow(a,(q-1)//d,q);z=g;xs=[1]
            while z!=1 and len(xs)<d:xs.append(z);z=z*g%q
            if len(xs)==d and z==1:break
        else:return False
        # Avoid full huge power in normal cases: integer floor-log2 bound.
        z=min(xs[1:]);
        if (z.bit_length()-1)*f<cap.bit_length() and z**f<=cap:return False
        seen.add(d)
    return True

def verify(target,ss=None):
    e=1108;P=3**e;A=(3*P-1)//2;R=10175119360001;assert R==1+2*(e+1)*32768*140000 and isqrt(A)**2!=A
    assert P*43**(2*(e-2))>10**2400
    t=0
    while R**(2*(t+1))<=A*R:t+=1
    threshold=10**target;cases=0;total=0;maxq=0
    for s in (ss if ss is not None else range(1,e+1)):
        u=e-s;extra=min(81**(u-i)*max(A*R,R**(2*i)) for i in {min(t,u),min(t+1,u)})
        y=3**s;l=(1+isqrt(3*threshold//(2*P*extra)))//(2*y)
        if not l:continue
        assert 2*y-1>50000
        if '--cost' in sys.argv:total+=l;maxq=max(maxq,l);continue
        sieve=bytearray(b'\1')*(l+1);sieve[::2]=bytes(l//2+1)
        for p in (*BAN,3):sieve[::p]=bytes(l//p+1)
        for p in primes:
            k=pow(2*y,-1,p)
            if k<=l:sieve[k::p]=bytes((l-k)//p+1)
        for m in range(1,l+1,2):
            if not sieve[m]:continue
            q=2*m*y-1
            if modpow(2,q-1,q)!=1:continue
            assert (2*q)**3*P*q*extra>27*81*threshold
            cap=threshold//(P*q*extra);assert order_test(q,cap),(e,s,m);cases+=1
        total+=l;print(s,l,cases,flush=True)
    print(dict(e=e,target=target,prefix=total,cases=cases,maxprefix=countmax if (countmax:=maxq) else None),flush=True)
if __name__=='__main__':verify(int(sys.argv[1]))
