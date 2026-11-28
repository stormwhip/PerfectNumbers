"""Integer (19,13,E) joint price in the difficult exact E^4 window."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,prod
from Net13 import PREFIX, B, sig, vp, loss as loss2, X as X0, M as M0, gain as gain2

L=44119464395283956806299428681
E=24104457298489411978880226626239089834405670981
ROWS=PREFIX+((L,2),(E,4))
PS=(19,13,E)
WS=(19,19,15)
X=prod(p**h for p,h in ROWS)
S=prod(sig(p,h) for p,h in ROWS)//2
CAP=tuple(dict(ROWS)[p]-vp(S,p) for p in PS)
R=14  # third target nontrivial, noncubic baseline exponents may be at least four

def need(ok,msg):
    if not ok:raise ValueError(msg)

def divs(n):return [o for o in range(3,5032,2) if n%o==0]

@cache
def roots(p,o,c):
    fs=[d for d in range(2,o+1) if o%d==0 and not any(d%i==0 for i in range(2,d))]
    a=2
    while True:
        g=pow(a,(p-1)//o,p)
        if g and all(pow(g,o//q,p)!=1 for q in fs):break
        a+=1
    rs=[pow(g,k,p)for k in range(1,o) if gcd(k,o)==1];m=p;out=[]
    for z in range(1,c+1):
        need(all(0<b<m and pow(b,o,m)==1 for b in rs),'root lift')
        out.append((m,tuple(sorted(rs))));m*=p;rs=[pow(b,p,m)for b in rs]
    return tuple(out)

def lengths():
    need(3**5030<=B<3**5031 and CAP==(275,274,3),'prefix demands')
    need(3**60>=19**19 and 3**60>=13**19,'small target LTE price')
    need(E>5031,'third target shift')
    opts=([0,1,*divs(18)],[0,1,*divs(12)],[0,*divs(E-1)])
    for h in range(2,5031,2):
        n=h+1
        lte=(vp(n,19),vp(n,13),0)
        oo=tuple(tuple(o for o in ls if o<2 or n%o==0) for ls in opts)
        for os in product(*oo):
            cost=sum(6*k for o,k in zip(os,lte) if o)+2*int(3 in os)+2*int(os[0]==9)+4*int(os[2]>3)
            need(cost<=h, ('length allocation',h,os,cost))
    return opts

def valid(b):
    return b>=3 and b%2==1 and b not in dict(ROWS) and b*b*X<=B and all(pow(a,b-1,b)==1 for a in (2,3,5,7,11,13,17) if a<b)

def keep(table,b,power,exp):
    if b>=3 and b%2 and exp*(b.bit_length()-1)<power.bit_length() and b**exp<power and valid(b):
        table[b]=max(table.get(b,1),Fraction(power,b**exp))

def merge(A,C):
    m,rr,pp=A;n,ss,qq=C;w=pp*qq;mod=m*n;I=pow(m,-1,n)
    return mod,tuple(sorted(r+m*((s-r)*I%n) for r in rr for s in ss)),w

def possible_class(rr,pp,e):return any(r>=3 and e*(r.bit_length()-1)<pp.bit_length() for r in rr)

@cache
def losses():
    opts=lengths()
    arr=[[(m,rr,m**w) for m,rr in roots(p,3,c)]for p,w,c in zip(PS,WS,CAP)]
    cube={};high19={};highE={};pair=[]
    for group in arr:
        for m,rr,power in group:
            for r in rr:keep(cube,r,power,20)
    for i,j in ((0,1),(0,2),(1,2)):
        for A in arr[i]:
            for C in arr[j]:
                G=merge(A,C)
                for r in G[1]:keep(cube,r,G[2],20)
                if (i,j)==(0,1):pair.append(G)
    for A in pair:
        for C in arr[2]:
            G=merge(A,C)
            for r in G[1]:keep(cube,r,G[2],20)
    for m,rr in roots(19,9,CAP[0]):
        for r in rr:keep(high19,r,m**19,20)
    for o in opts[2][2:]:
        need(o>3,'third order')
        for m,rr in roots(E,o,CAP[2]):
            for r in rr:keep(highE,r,m**15,40)
    keys=cube.keys()|high19.keys()|highE.keys()
    return {r:cube.get(r,1)*high19.get(r,1)*highE.get(r,1) for r in keys}

@cache
def gain(p,lo):
    best=None;hit=None;M=prod(q**(w*c) for q,w,c in zip(PS,WS,CAP))
    for h in range(lo+lo%2,5031,2):
        b=p**h
        if b*X>B:break
        if best is not None and b**10>=best*M:break
        ss=sig(p,h); vs=[vp(ss,p) for p in PS]
        if any(v>c for v,c in zip(vs,CAP)):continue
        z=Fraction(b**10*losses().get(p,1),prod(q**(w*v)for q,w,v in zip(PS,WS,vs)))
        if best is None or z<best:best,hit=z,h
    return best,hit

def compute(compelled):
    M=prod(q**(w*c) for q,w,c in zip(PS,WS,CAP));U=prod(losses().values());V=Fraction(X**10*M,U)
    credit=[]
    for q in compelled:
        need(q not in dict(ROWS) and S%q==0,'forced only')
        z,g=gain(q,vp(S,q));need(z is not None,'empty forced valuation');credit.append((q,g,z));V*=z
    return V,credit

if __name__=='__main__':
    from math import log10
    def l(x):return(log10(x.numerator)-log10(x.denominator))/10
    groups=[67,967,8311,11621,50627,392233,31,15413977,5,11]
    V,credit=compute(groups)
    print('E4 caps',CAP,'deficits',len(losses()),'log',l(V),'credits',[(q,g,l(z))for q,g,z in credit],flush=True)
    need(V>B**10,'E4 terminal')
