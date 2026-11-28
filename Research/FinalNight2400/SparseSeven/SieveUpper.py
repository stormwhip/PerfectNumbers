"""Small-prime/Fermat witnesses sharpen q lower endpoints in primitive-order proof."""
from pathlib import Path
from math import gcd,isqrt
from functools import cache
import sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import PrimitiveSupport as V
small=[n for n in range(2,5001) if all(n%i for i in range(2,isqrt(n)+1))];old=V.minQ
@cache
def new(s,h):
    Y=7**s;k=h+1;u=pow(Y,-1,k);u+=k*((1-u)%2)
    for i in range(8000):
        q=2*u*Y-1
        if gcd(u,133)==1 and all(q%z for z in small) and pow(2,q-1,q)==1:break
        u+=2*k
    return 2*u*Y-1

def run():
    out={}
    for s in range(676,682):
        # Further sieve only the handful of exact exponents permitted by PrimitiveSupport.
        V.minQ=old;possible=V.possibilities(s);hs={h for h,c in possible};lookup={h:new(s,h) for h in hs}
        V.minQ=lambda i,h:lookup[h] if i==s and h in lookup else old(i,h);out[s]=[]
        for h,c in V.possibilities(s):
            cap=V.root((V.B//(V.X*V.A))**h*3**(h-c)//(2**(h-c)),2*h-c);Y=7**s;M=(cap+1)//(2*Y);Q=lookup[h];
            if M<20000:
                m=(Q+1)//(2*Y);ok=False
                while m<=M:
                    q=2*m*Y-1
                    if gcd(m,133)==1 and all(q%z for z in small) and pow(2,q-1,q)==1:ok=True;break
                    m+=2*(h+1)
                if not ok:continue
            out[s].append((h,c))
        print('sieved label',s,sorted(out[s]),flush=True)
    return out
def final():
    out=run();assert not out[681] and out[680]==[(4,2)]
    Y=7**680;h,c=4,2;M=(V.root((V.B//(V.X*V.A))**h*3**(h-c)//(2**(h-c)),2*h-c)+1)//(2*Y);assert M==14720
    feasible=[]
    for m in range(1,M+1,2):
        q=2*m*Y-1
        if q%5==1 and gcd(m,133)==1 and all(q%z for z in small) and pow(2,q-1,q)==1:
            feasible.append(m);g=pow(2,(q-1)//5,q);assert g not in (0,1) and pow(g,5,q)==1
            maxz=isqrt(V.B//(V.X*V.A*q));assert min(pow(g,j,q) for j in range(1,5))>maxz
    assert feasible==[2511,11751]
    print('PASS all canonical 7^906 must have s<=679 (factorization unrestricted).')
if __name__=='__main__':assert __debug__;final()
