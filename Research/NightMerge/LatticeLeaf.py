"""Independently verify one polynomial small-root cut. No LLL or nonstandard libraries."""
from fractions import Fraction
from math import gcd,comb

def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return p

def remainder(a,b):
    a=list(map(Fraction,a));b=trim(b)
    while a and len(a)>=len(b):
        q=a[-1]/b[-1];t=len(a)-len(b)
        for i,v in enumerate(b):a[t+i]-=q*v
        a=trim(a)
    return a

def sign_at(p,x):
    v=0
    for t in p[::-1]:v=v*x+t
    return (v>0)-(v<0)

def variations(s):
    s=[x for x in s if x];return sum(a!=b for a,b in zip(s,s[1:]))

def no_real_roots(coeff,lo,hi):
    p=trim(coeff)
    if not p or sign_at(p,lo)==0 or sign_at(p,hi)==0:return False
    chain=[p,trim([i*p[i] for i in range(1,len(p))])]
    while chain[-1]:
        rem=remainder(chain[-2],chain[-1]);chain.append([-v for v in rem])
    return variations(sign_at(v,lo) for v in chain[:-1])==variations(sign_at(v,hi) for v in chain[:-1])

def build(C,c,z,T,low,high,dim,m):
    first=low+(z-low)%T;radius=(high-first)//T;mid=radius//2;center=first+T*mid;K=max(1,radius-mid)
    b=(center*pow(T,-1,C))%C;b=b if 2*b<C else b-C;basis=[]
    for i in range(dim):
        h=min(i,m);off=i-h;mul=C**((m-h+c-1)//c);row=[0]*dim
        for j in range(h+1):row[off+j]=mul*comb(h,j)*b**(h-j)
        basis.append(row)
    return first,radius,mid,center,K,basis

def verify(C,c,z,T,lo,hi,w):
    if not (C>1 and 1<=c and 0<=z<T and 1<lo<=hi and gcd(C,T)==1):return False
    dim,m,alpha,split=w
    if not(2<=dim<=20 and 1<=m<dim and len(alpha)==dim and all(type(a)==int for a in alpha)):return False
    first,radius,mid,center,K,rows=build(C,c,z,T,lo,hi,dim,m)
    if radius<0:return True
    b=[sum(a*row[j] for a,row in zip(alpha,rows)) for j in range(dim)]
    if not any(b) or sum(abs(x)*K**j for j,x in enumerate(b))>=first**m:return False
    # If r=first+T*i really divides C to power c, r|x+b0, and every constructed basis polynomial is divisible by r^m at x=i-mid. Thus b(x)=0. Exclude all integer roots:
    # split contains ALL rational factors as proved by exact polynomial divisions and final Sturm zero-count on remaining finite subintervals.
    poly=trim(b);lower=-mid;upper=radius-mid
    for row in split:
        t,d=row
        if type(t)!=int or type(d)!=int or d<=0 or gcd(t,d)!=1:return False
        if t%d==0 and lower<=t//d<=upper and C%(center+T*(t//d))**c==0:return False
        q=[];p=list(map(Fraction,poly));root=Fraction(t,d)
        for v in p[:0:-1]:q.append(v+(q[-1]*root if q else 0))
        if p[0]+(q[-1]*root if q else 0)!=0:return False
        poly=trim(q[::-1]);
        if not poly:return False
    return no_real_roots(poly,lower,upper)
