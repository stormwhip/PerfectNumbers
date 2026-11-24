"""Finite square-kernel sieve with exact integers. This is NOT an odd-perfect-number exclusion."""
from math import gcd,isqrt,prod
from time import perf_counter

CASES=((3,1162),(5,520),(3,1108),(19,676))
LIMIT=10**11

def primes(n):return [i for i in range(2,n+1) if all(i%j for j in range(2,isqrt(i)+1))]
def test(p,e,cap):
    h=e+1;A=(p**h-1)//(p-1)
    if h<=p or h not in primes(h) or A%h==0 or h%2!=1:raise ValueError('prime-order preconditions')
    # A=Phi_h(p), any prime r|A has ord_r(p)=h, hence r=1 mod 2h. Thus sf(A)=1 mod 2h.
    qs=[j for j in primes(250) if j>2 and gcd(A*2*h,j)==1];w=1;res=[0];remaining=[]
    def allowed(q):return {A*pow(j,-2,q)%q for j in range(1,q)}
    for q in qs[:6]:
        ok=allowed(q);res=[b+w*j for b in res for j in range(q) if (1+2*h*(b+w*j))%q in ok];w*=q
    tests=[(q,allowed(q)) for q in qs[6:]];mmax=(cap-1)//(2*h)
    for b in res:
        for i in range(b,mmax+1,w):
            k=1+2*h*i
            if all(k%q in al for q,al in tests) and A%k==0 and isqrt(A//k)**2==A//k:remaining.append(k)
    return remaining
if __name__=='__main__':
    start=perf_counter()
    for p,e in CASES:
        left=test(p,e,LIMIT)
        if left:raise ValueError((p,e,left))
        print(p,e,'squarefree kernel >',LIMIT,'(conditional size gain only)')
    print('seconds',round(perf_counter()-start,3))
