"""Integer E3a base, all 1<=s<=e (no window). Given the factor-range cross-check NextRange.py.
The pricing is for ordinary primes other than r,A,q, after 81 per external supplier unit.
"""
from math import isqrt,gcd
from functools import cache
import sys
BAN=(7,11,13,19,31)
sieve=bytearray(b'\1')*50000
for p in range(2,isqrt(len(sieve)-1)+1):
    if sieve[p]:sieve[p*p::p]=bytes((len(sieve)-1-p*p)//p+1)
primes=[p for p in range(5,len(sieve),2) if sieve[p]]
def impossible(q,cap):
    if cap>=q*q:return False
    seen={1};maxf=cap.bit_length(); # since r>=3, f<bit_length(cap)
    for f in range(2,maxf,2):
        d=gcd(f+1,q-1)
        if d in seen:continue
        for a in range(2,64):
            g=pow(a,(q-1)//d,q);z=g;xs=[1]
            while z!=1 and len(xs)<d:xs.append(z);z=z*g%q
            if len(xs)==d and z==1:break
        else:return False
        if min(xs[1:])**f<=cap:return False
        seen.add(d)
    return True

def run(e,target):
    assert __debug__;assert all((e+1)%p for p in range(2,isqrt(e+1)+1))
    P=3**e;A=(3*P-1)//2;R=1+2*(e+1)*32768*140000;assert isqrt(A)**2!=A
    # For i above switch t, max term =R^(2i), grows faster than 81^i; below t, decreases. Two endpoints suffice.
    t=0
    while R**(2*(t+1))<=A*R:t+=1
    threshold=10**target;cases=[];total=0
    assert P*43**(2*(e-2))>10**2400 # excludes s<=2, including q<17, before any source discount
    for s in range(1,e+1):
        u=e-s;extra=min(81**(u-i)*max(A*R,R**(2*i)) for i in {min(t,u),min(t+1,u)})
        y=3**s;l=(1+isqrt(3*threshold//(2*P*extra)))//(2*y)
        if not l:continue
        ss=bytearray(b'\1')*(l+1);ss[::2]=bytes(l//2+1)
        for p in (*BAN,3):ss[::p]=bytes(l//p+1)
        for p in primes:
            k=pow(2*y,-1,p)
            if k<=l:
                if 2*y*k-1==p:k+=p
                if k<=l:ss[k::p]=bytes((l-k)//p+1)
        for m in range(1,l+1,2):
            if not ss[m]:continue
            q=2*m*y-1
            if pow(2,q-1,q)!=1:continue
            # For a counterexample to the *base* lower bound, r^f <= threshold/(P*q*extra).
            # This cap is much stronger than using N<=10^2400 when e is small.
            assert (2*q)**3*P*q*extra>27*81*threshold # if b>0 the normalized source exceeds target
            cap=threshold//(P*q*extra) # only b=0 remains
            assert impossible(q,cap),(e,s,m);cases.append((s,m))
        total+=l
    print(dict(e=e,R=R,target=target,prefix=total,cases=cases),flush=True)
if __name__=='__main__':
    for e,t in ((1108,2117),(970,1855),(990,1893),(856,1639)):run(e,t)
