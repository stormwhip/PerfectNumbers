"""Partial no-factorization source audit with an exact test of every known factor.
Run with optional argument (repository checkout root). Never updates input.
"""
import hashlib,json,sys
from pathlib import Path
from math import gcd
from functools import cache
sys.path.insert(0,str(Path(__file__).resolve().parent))
from SourceSquare import dual

B=10**2400; e=1162; pe=3**e; A=(3*pe-1)//2; ban=(7,11,13,19,31)
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[3]
raw=(root/'Research/P3I00193Review/Candidate/P3E1162Complete.json').read_bytes().replace(b'\r\n',b'\n');cert=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='54652cb67d6f807170248c00eb0c9004a200cd7b9027a73e923b7ea1a46cb30b'
R=10**4;K,n,d=dual(R)
# Every Euler source has b=0, q>=Q, and r^f>2Q/3. Disjoint ordinary suppliers cost M(e-s).
S=next(s for s in range(1,e+1) if 2*pe*(2*3**s-1)**2*K**(e-s)*d<=3*B*n)
Y=3**S;Q=2*Y-1
assert S==1020

def prime64(p):
    if p<2 or p>2**64-1: return False
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        if p%a==0:return p==a
    n=p-1; h=0
    while not n%2:n//=2;h+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        x=pow(a,n,p)
        if a%p==0 or x in (1,p-1):continue
        for _ in range(h-1):
            x=x*x%p
            if x==p-1:break
        else:return False
    return True

@cache
def certified(r):
    if r<2**64:return prime64(r)
    P=1;used=set()
    for t,k,a in cert['primes'].get(str(r),[]):
        assert 2<=t<r and t not in used and certified(t) and 1<=k<=r.bit_length() and 1<a<r
        P*=t**k;used.add(t)
        assert (r-1)%P==0 and pow(a,r-1,r)==1 and gcd(pow(a,(r-1)//t,r)-1,r)==1
    return P*P>r

@cache
def phi(r,m):
    if m==1:return r-1
    x=r**m-1
    for j in range(1,m):
        if m%j==0:x//=phi(r,j)
    return x

@cache
def eligible(r):
    assert r>3 and r%2==1 and A%r and r<Q
    # This test needs NO primality assumption: if r were a source prime,
    # each checked necessary condition would hold.
    f=0;v=1;cap=B//(pe*A*Q)
    while v*r*r<=cap:
        f+=2;v*=r*r;m=f+1
        if m%3==0 or (v*r-1)//(r-1)<Q:continue
        if any(pow(r,m,t*(r-1))==1 for t in ban):continue
        # q = -1 mod Y and q=1 mod lcm(4,m)=4m.
        q0=1+4*m*((-2*pow(4*m,-1,Y))%Y)
        if q0<Q:q0+=4*m*Y*((Q-q0+4*m*Y-1)//(4*m*Y))
        if v*q0*pe*A>B:continue
        C=phi(r,m)
        if C<q0:continue
        # C=q*w, w=-C mod Y. Coefficients are exact.
        w=(-C)%Y or Y
        if w*q0<=C:return True
    return False

def rows():
    for i,l in enumerate(cert['cell10']+cert['cell11']):
        F=l['forest'];L=l['lp'];u=set(F['roots'] if F else []);p=set(L['P'] if L else [])
        if F:
            for v in F['edges'].values():u.update(v)
        strip=u|p|{2,3}; absent=set(ban)|set(l['absent_extra']); opts=[]
        if F:opts += [('forest',int(r),f) for r,cut in F['cut_even'].items() for f in range(2,cut,2)]
        opts += [('lp',r,f) for r in p for f in range(2,(40 if r<100 else 20 if r<400 else 10)+1,2)]
        for k,r,f in opts:
            x=(r**(f+1)-1)//(r-1)
            if any(x%t==0 for t in absent):continue
            for t in strip:
                while x%t==0:x//=t
            if x>1: yield i,k,r,f,x

if __name__=='__main__':
    assert __debug__
    blocks=list(rows());assert len(blocks)==34972
    unique={x for *_,x in blocks}; known={int(n) for n in cert['primes']}|{p for l in cert['cell10']+cert['cell11'] for p in ((l['lp'] or {}).get('P',[]) + (l['forest'] or {}).get('roots',[]))};known.update(range(5,50000,2));
    assert all(certified(int(r)) for r in cert['primes'])
    known=sorted(t for t in known if t>=5 and certified(t))
    # Algebraic splitting of the unstripped sigma via cyclotomic divisors is
    # valid without assuming any primitive-prime property of the row itself.
    for _,_,r,f,x in blocks:
        m=f+1
        for j in range(3,m+1,2):
            if m%j==0:
                z=gcd(phi(r,j),x)
                if 1<z<2**64 and prime64(z):known.append(z)
    known=sorted(set(known))
    reduced={};may=[];tested=set()
    for x in sorted(unique):
        assert gcd(A,x)==1 and x<Q
        y=x; stack=[]
        for t in known:
            if t>y:break
            if y%t==0:
                while y%t==0:y//=t
                stack.append(t)
        if y>1 and prime64(y):stack.append(y);y=1
        crit=[r for r in stack if eligible(r)];tested.update(stack);may.extend(crit)
        reduced[x]=not crit and y==1
    guaranteed=sum(reduced.values());count=sum(reduced[x] for *_,x in blocks)
    print(json.dumps(dict(status='CONDITIONAL_ONLY',baseline_s=S,source_input_sha256=hashlib.sha256(raw).hexdigest(),rows=len(blocks),distinct=len(unique),source_free_rows=count,source_free_distinct=guaranteed,unresolved_rows=len(blocks)-count,distinct_tested_bases=len(tested),sieve_survivors=sorted(set(may)),accepted_actuals=[]),indent=2))
