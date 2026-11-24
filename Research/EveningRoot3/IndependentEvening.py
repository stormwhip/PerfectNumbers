"""Root-three audit, independent of FactorGap, SourceSplit and GapAbundance.
Python 3.10+, standard library only. No output files. Default: recompute the
certified FactorGap, SourceSplit and BothEuler exponent sets on the entire input.
--abundance also reproduces all abundance cells relative to the LiftDeep input;
--only 1290 1276 ... selects exponents. Unproved large integers are ignored.
"""
import argparse
from bisect import bisect_left
from collections import Counter
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import accumulate
import json
from math import gcd, isqrt, lcm, prod
from pathlib import Path

H = Path(__file__).resolve().parent
B, T, S = 10**2400, 100000, 10**8
BAN = {7, 11, 13, 19, 31}

def need(condition, why):
    if not condition:
        raise ValueError(why)

def load(p):
    return json.loads(p.read_text(encoding='utf8'))

def primes():
    flags = bytearray([1])*(T+1)
    for i in range(2, isqrt(T)+1):
        if flags[i]:
            flags[i*i::i] = bytes(len(range(i*i, T+1, i)))
    return tuple(i for i in range(2, T+1) if flags[i])

PS = primes()
SUP = [p for p in PS if p%3 == 1 and p not in BAN]

def ilog(x, b):
    # Find the last successful integral power by doubling and binary search.
    lo, hi = 0, 1
    while b**hi <= x:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        j = (hi+lo)//2
        if b**j <= x: lo = j
        else: hi = j
    return lo

def mr64(n):
    if n < 2 or n%2 == 0: return n == 2
    need(n < 2**64, 'non-deterministic MR range')
    d = n-1; v = (d & -d).bit_length()-1; d >>= v
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a % n == 0: continue
        x = pow(a, d, n)
        if x == 1: continue
        for _ in range(v):
            if x == n-1: break
            x = x*x%n
        else: return False
    return True

def elliptic_step(n, tr, co, a, xy):
    # Independent left-to-right Jacobian/mixed-affine multiplications. Prove
    # mP=O and co*P!=O for every prime dividing n, with m/co the next prime.
    m = n+1-tr
    need(n>3 and gcd(n,6)==1 and co>0 and m%co==0 and tr*tr<4*n,'invalid ECPP data')
    q = m//co
    need((isqrt(isqrt(n))+2)**2 < q < n, 'insufficient Hasse margin')
    x,y = (u%n for u in xy); b = (y*y-x**3-a*x)%n
    need(gcd(n,4*a**3+27*b*b)==1, 'singular curve')
    units = 1
    def mul(k):
        nonlocal units
        w = None
        for bit in bin(k)[2:]:
            if w is not None:
                X,Y,Z = w
                if Y==0: w=None
                else:
                    units = units*Y%n
                    yy=Y*Y%n; h=(3*X*X+a*pow(Z,4,n))%n; u=4*X*yy%n
                    nx=(h*h-2*u)%n
                    w=(nx,(h*(u-nx)-8*yy*yy)%n,2*Y*Z%n)
            if bit=='0': continue
            if w is None: w=x,y,1; continue
            X,Y,Z=w; zz=Z*Z%n; u=(x*zz-X)%n; v=(y*Z*zz-Y)%n
            if u==0:
                if v==0:
                    if Y==0: w=None; continue
                    units=units*Y%n; yy=Y*Y%n
                    h=(3*X*X+a*zz*zz)%n; kx=4*X*yy%n; nx=(h*h-2*kx)%n
                    w=(nx,(h*(kx-nx)-8*yy*yy)%n,2*Y*Z%n)
                else:
                    need((y*Z*zz+Y)%n==0, 'inconsistent inverse'); units=units*v%n; w=None
            else:
                units=units*u%n; uu=u*u%n; u3=u*uu%n; kx=X*uu%n; nx=(v*v-u3-2*kx)%n
                w=(nx,(v*(kx-nx)-Y*u3)%n,u*Z%n)
        return w
    coP=mul(co)
    need(coP is not None and gcd(coP[2],n)==1, 'zero cofactor point')
    need(mul(m) is None and gcd(units,n)==1, 'invalid elliptic scalar products')
    return q

@cache
def prime(n):
    if n<2**64: return mr64(n)
    cert=H/'ECPP'/(sha256(str(n).encode('ascii')).hexdigest()[:24]+'.json')
    if not cert.exists(): return False
    q=n
    for row in load(cert):
        need(q==row[0], 'ECPP chain mismatch')
        q=elliptic_step(*row)
    need(mr64(q), 'ECPP final prime'); return True

@cache
def legal(z, f):
    # Compute sigma(z^f) modulo every banned prime directly via the finite
    # geometric sum, distinguishing z==1 (mod b) from the invertible case.
    for b in BAN:
        if z%b==1:
            if (f+1)%b==0: return False
        elif pow(z,f+1,b)==1: return False
    return True

@cache
def blocks(e):
    need(e%2==0 and 2<=e and e+1<=T, 'invalid exponent')
    rel={}
    for d in range(1,e+2):
        if (e+1)%d==0:
            rel[d]=(3**d-1)//prod(v for j,v in rel.items() if d%j==0)
    del rel[1]
    need(prod(rel.values())==(3**(e+1)-1)//2,'bad cyclotomic decomposition')
    return rel

@cache
def residual_units(h,u):
    if u==1:return 0
    stride=lcm(3,2*h); first=1+((T-1)//stride+1)*stride; end=first+100000*stride
    # Composite hits can only relax this bound. Avoid unnecessary work when a
    # bound from the first candidate already equals that from the last.
    low=ilog(u,end*end)
    if ilog(u,first*first)==low:return low
    for z in range(first,end,stride):
        if u%(z*z)==0:return ilog(u,z*z)
    return low

def factor_small(A):
    nums={}; u=A
    for p in PS:
        while u%p==0:
            nums[p]=nums.get(p,0)+1; u//=p
    return nums,u

@cache
def ordinary():
    bases=[]
    for z in SUP:
        b=z
        while b<=T:
            bases.append(b*b); b=b**3
    return [1,*accumulate(sorted(bases), lambda a,b:a*b)]

@cache
def old_cells(e):
    pe=3**e; high=set(); one=set(); sep=set()
    for k,price in enumerate(ordinary()[:e+1]):
        s=e-k; y=3**s; q=max(2*y-1,5); size=pe*price
        if size*max(5**5,3**max(5*s-5,0))>B: high.add(s)
        if s and pe*8*q**4>=27*B:sep.add(s)
        if q*size>B or (s in sep and 2*size*q*q>=3*B):one.add(s)
    return high,one,sep

def minimum(z,c):
    m=c+(c%2)
    while not legal(z,m):m+=2
    return m

@cache
def low_prices(z,f):
    # Number of fully subsidized levels = floor(log_3(f+1)). For each next
    # nested threshold telescope the extra exponent beyond f; prices outside
    # the trial table get a common lower bound T+1.
    goal=3**(ilog(f+1,3)+1)-1; out=[]
    while legal(z,goal):
        delta=goal-f
        if delta>=17 or z**delta>T:break
        out.append(z**delta); f=goal; goal=3*(1+goal)-1
    return tuple(out)

def audit_factor(e,raw,accepted=False):
    need(e>=2 and e%2==0 and e+1<=T,'invalid root-three exponent')
    pe=3**e; P=3*pe; A=(P-1)//2; d,u=factor_small(A)
    if accepted:
        supplied=[int(s) for s in raw]
        need(len(set(supplied))==len(supplied),'duplicate accepted factor')
        for z in supplied:
            need(z>2 and (z>T or z in d),'bad listed small divisor')
    else:
        supplied={int(t[0]) for t in raw}
    for z in sorted(supplied):
        if z<=T:continue
        if not prime(z):
            need(not accepted, 'missing primality proof for accepted factor '+str(z));continue
        need(u%z==0,'prime witness does not divide A')
        while u%z==0: d[z]=d.get(z,0)+1;u//=z
    floor={r:minimum(r,c) for r,c in d.items()}; extras={r:r**(floor[r]-c) for r,c in d.items()}
    premium=prod(extras.values()); M=pe*A*premium
    # Distinct legal Euler prime in A or no Euler prime there. Bound worst
    # discount separately instead of treating any PRP as a prime.
    discount=max([1]+[r**max(0,floor[r]-d[r]-(1-d[r])%4) for r in d
                        if r%4==1 and all((r+1)%b for b in BAN)])
    if M>B*discount:return True,True,True
    high,proved,sep=old_cells(e)
    # If q lies among the compelled factors we do not require it to round to
    # an even exponent. The rate table will ignore the missing q-component
    # by minimizing over a superset of possible (non-Euler) suppliers.
    all_discount=max([1]+[extras[r] for r in d if r%4==1 and all((r+1)%b for b in BAN)])
    max_a=ilog(B,5)   # q^a<=N<=B and q>=5
    # A cell can be skipped in the uniform scan only if BOTH old branches closed.
    open_s=sorted(set(range(e+1))-(proved & high))
    knownfree=sum(ilog(m+1,3) for r,m in floor.items() if r%3==1)
    Gbig=knownfree+ilog(u,(T+1)**2)
    rates=sorted(x for z in SUP for x in low_prices(z,floor.get(z,0)))
    product=[1,*accumulate((rates+[T+1]*e)[:e],lambda a,b:a*b)]
    chunks=[(h,gcd(u,v)) for h,v in blocks(e).items()]
    need(prod(t for _,t in chunks)==u and all(gcd(t,v)==1 for i,(_,t) in enumerate(chunks) for _,v in chunks[:i]), 'overlapping unsieved cyclotomic blocks')
    Gsmall=knownfree+sum(residual_units(h,v) for h,v in chunks)
    bonus=(T+1)**sum(isqrt(v)**2!=v for h,v in chunks)
    factor=split=len(high)==e+1; both=True
    for s in open_s:
        y=3**s;q=max(5,2*y-1); k=e-s; m=M*q; rhs=B*max(P,q)*(P//y+4)
        C=product[max(0,k-Gsmall)]
        if M*C<=B*all_discount:
            # Internal Euler: (3/q)=1, q=1 mod 4 -> q=1 mod 3; LTE gives
            # Y | a+1 <= max_a+1. Above that cutoff Euler is definitely external.
            highq=max(5**5,3**max(0,5*s-5))
            if s not in high and (y<=max_a+1 or M*C*highq<=B): both=False
        if s in proved:continue
        if not s:
            factor=split=False
            if M*C<=B*all_discount:both=False
            continue
        if m>B:continue
        Cbig=product[max(0,k-Gbig)]
        if not (s in sep and m*q*y*Cbig>=rhs*max(extras.values(),default=1)):factor=False
        if m*bonus>B:continue
        cell=(s in sep and 2*m*q*C>=3*B and (u==1 or m*q*y*C>=rhs))
        if cell:
            for z in d:
                if m*q*y*C>=rhs*extras[z]:continue
                # Independent CRT formulation: if w in allowed range exists then
                # floor(sigma/Q) reaches the first positive -sigma mod Y.
                f=floor[z];limit=B//(m*C)
                for extra in range(0,ilog(max(1,limit),z)+1,2):
                    if z**extra>limit:break
                    n=f+extra+1
                    if n%3==0 or not legal(z,n-1):continue
                    sig=(z**n-1)//(z-1)
                    if sig//q>=(y-1-sig)%y+1:cell=False;break
                if not cell:break
        if not cell:
            split=False
            if m*C<=B and M*C<=B*all_discount:both=False
        if not (factor or split or both):break
    return factor,split,both

@cache
def benefit(r):
    # Rational atanh-series upper bound, evaluated by a single exact division.
    t=2*r-1; t2=t*t; bot=15*t**3*(t2-1); top=2*S*(15*t2*t2-10*t2-2)
    return (top+bot-1)//bot

LOG2=int(sum(Fraction(2*S,(2*i+1)*3**(2*i+1)) for i in range(10)))

@cache
def small_residual(r,cut):
    # Exponent >=64: b<=m/8 since 3^(floor(m/8))>=m+1. Compare the
    # entire tail to the finite minimum, including negative residual prices.
    bits=[]
    for f in range(2,64,2):
        if not legal(r,f): continue
        n=f+1; b=0
        while r%3==1 and n%3==0: b+=1;n//=3
        bits.append((r**f).bit_length()-1-b*cut)
    lb=64*(r.bit_length()-1)-(8*cut if r%3==1 else 0)
    need(bits and lb>=min(bits), 'small-prime exponent tail')
    return min(bits)

def abundance(e,orig):
    pe=3**e;P=pe*3;A=(P-1)//2; small,u=factor_small(A)
    chunks=[(h,gcd(u,v)) for h,v in blocks(e).items()];need(prod(n for _,n in chunks)==u,'shared blocks')
    G=sum(residual_units(h,n) for h,n in chunks)
    prem=sorted(r for r,c in small.items() if c%2 and r%3!=1); prem=prod(prem[:-1])
    ext=[r for r in PS if 3<r<=1000 and r not in BAN and r not in small]
    deficit=LOG2-benefit(3)-sum(benefit(r) for r in small)-ilog(u,T+1)*benefit(T+1)
    rest={i for a,b in orig for i in range(a,b+1)}
    for cut in (8,10,12,14,16):
        leftD=deficit; debt=0
        for r,c in small.items():
            if r%3!=1: continue
            f=c;j=1
            while True:
                n=max(f,3**j-1); paid=(r**(n-f)).bit_length()-1
                if paid>=cut:break
                debt+=cut-paid;f=n;j+=1
        tail=Fraction(18-cut,benefit(1001)); items=[]
        for r in ext:
            b=small_residual(r,cut); h=benefit(r)
            if b<0:debt-=b;leftD-=h
            elif b<h*tail:items.append((Fraction(b,h),h,b))
        items.sort(); cum=list(accumulate(x[1] for x in items)); prices=[x[0] for x in items]+[tail]
        def spend(D):
            if D<=0:return 0
            # LP dual at the crossing slope, not a primal fractional filling.
            lam=prices[bisect_left(cum,D)]
            return int(lam*D-sum(max(0,lam*h-b) for _,h,b in items))
        for s in list(rest):
            y=3**s;q=2*y-1
            if s==0 or 8*pe*q**4<27*B:continue
            base=pe*A*q*prem; bits=cut*max(0,e-s-G)-debt
            for external in (False,True):
                b=bits+spend(leftD-benefit(q)-(benefit(min(ext)) if external else 0))
                lhs,rhs=(2*q*base,3*B) if external else (q*y*base,B*max(P,q)*(P//y+4))
                if (lhs<<max(b,0)) < (rhs<<max(-b,0)):break
            else:rest.remove(s)
    return rest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--only',nargs='+',type=int);ap.add_argument('--abundance',action='store_true');ap.add_argument('--abundance-only',action='store_true');ap.add_argument('--verify-accepted',action='store_true',help='verify every BothAudit witness with no discovery data');ap.add_argument('--list-ecpp',action='store_true',help='print the exact ECPP files referenced by BothAudit and exit');a=ap.parse_args()
    if a.verify_accepted or a.list_ecpp:
        need(not (a.only or a.abundance or a.abundance_only),'accepted mode requires all accepted rows')
        rows=load(H/'BothAudit.json');expected=tuple(r['e'] for r in rows)
        need(len(expected)==len(set(expected)),'duplicate accepted exponent')
        brief=json.dumps(sorted(expected),separators=(',',':'))
        need(len(rows)==42 and sha256(brief.encode()).hexdigest()=='953665a25a0746324a18b26e95e05882c4810f4ee5d54d479cc14220ac6db570','missing or changed exponent from the 42-row acceptance set')
        names=sorted({'ECPP/'+sha256(str(int(z)).encode('ascii')).hexdigest()[:24]+'.json' for r in rows for z in r['fs'] if int(z)>=2**64})
        if a.list_ecpp:
            print('\n'.join(names))
            if not a.verify_accepted:return
        print('accepted input:',len(rows),'rows,',len(names),'ECPP files; exponent digest',sha256(brief.encode()).hexdigest(),flush=True)
        for row in rows:
            e=row['e']; _,_,ok=audit_factor(e,row['fs'],accepted=True)
            need(ok, 'unsupported BothEuler exponent '+str(e))
        print('All accepted exponents independently proved:',brief);return
    raw={int(k):v for k,v in load(H/'Candidates.json').items()}; todo=set(a.only or raw); need(todo<=raw.keys(),'unknown exponent')
    if not a.abundance_only:
        fset=set(); sset=set(); eset=set()
        for e in sorted(todo,reverse=True):
            f,s,b=audit_factor(e,raw[e]);
            if f:fset.add(e)
            if s:sset.add(e)
            if b:eset.add(e)
            if f or s or b: print('PASS',e,'factor',f,'split',s,'both',b,flush=True)
        discovery={r['e'] for r in load(H/'Discovery.json')}&todo
        print('FactorGap',len(fset),sorted(fset));print('SourceSplit',len(sset),sorted(sset));print('BothEuler',len(eset),sorted(eset));print('PRP discovery not certified',sorted(discovery-fset))
        for filename,proved in [('StrictEarly.json',fset),('SplitAudit.json',sset),('BothAudit.json',eset)]:
            if (H/filename).exists():
                declared={r['e'] for r in load(H/filename)}&todo
                need(declared<=proved,filename+' has unsupported exponents: '+str(sorted(declared-proved)))
                print(filename, 'supported',len(declared),'newer proof extras',sorted(proved-declared))
    if a.abundance or a.abundance_only:
        old={row['e']:row for row in load(H.parent/'GapSupply2400'/'LiftDeep.json') if row['p']==3 and not row['closed'] and row['e'] in todo}
        audit={row['e']:row for row in load(H/'AbundanceAudit.json') if row['e'] in todo}
        need(old.keys()==audit.keys(),'abundance input rows changed'); closed=[]; delta=0
        for e,row in old.items():
            M=abundance(e,row['open_one']); want={s for i,j in audit[e]['open_one'] for s in range(i,j+1)}
            high,_,_=old_cells(e); full=not M and len(high)==e+1
            need(M==want and full==audit[e]['closed'],'abundance discrepancy e='+str(e))
            if full:closed.append(e)
            delta+=sum(j-i+1 for i,j in row['open_one'])-len(M)
        print('Abundance cells match:',len(old),'rows;',delta,'new (e,s); closed',sorted(closed))
if __name__=='__main__': main()
