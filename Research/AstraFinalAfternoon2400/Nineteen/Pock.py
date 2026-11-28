"""Build/read elementary Pocklington certificate chains (discovery requires sympy)."""
from functools import cache
from math import gcd,prod

@cache
def attempt(n):
    from sympy import factorint,isprime
    if n<2**64:return {} if isprime(n) else None
    ps=factorint(n-1,limit=25000); used={}; ys=[]
    for q,e in sorted(ps.items(),reverse=True):
        if not isprime(q):continue
        sub=attempt(q)
        if sub is None:continue
        for g in range(2,40):
            if pow(g,n-1,n)==1 and gcd(pow(g,(n-1)//q,n)-1,n)==1:
                used.update(sub);ys.append((q,e,g));break
        if prod(q**e for q,e,g in ys)**2>n:
            used[str(n)]=ys;return used
    return None

def verify(n,book,prime64,used=None):
    @cache
    def prime(q):
        if q<2**64:return prime64(q)
        w=book[str(q)]
        if used is not None:used.add(str(q))
        assert len(w)==len({a for a,b,c in w})
        F=prod(p**e for p,e,g in w)
        assert q>2 and F*F>q and (q-1)%F==0
        for p,e,g in w:
            assert 2<=p<q and e>=1 and 1<g<q and prime(p)
            assert pow(g,q-1,q)==1 and gcd(pow(g,(q-1)//p,q)-1,q)==1
        return True
    return prime(n)

if __name__=='__main__':
    import sys,json
    for n in map(int,sys.argv[1:]):
        print(n,json.dumps(attempt(n)),flush=True)
