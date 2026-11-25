"""Second terminal replay arithmetic on the same explicit branch packet.

Decimal logarithms are enclosed separately and used at rational dyadic weights.
No import of Terminal.model or price.
"""
import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from functools import cache
import gzip,json
from math import gcd,prod,isqrt
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[1]/'RootFiveNext'))
from PrimeCheck import level,prime64
R=(19,7,11,31,13,3,5,17);L=5001;S=2**80;Y=2**24


def ck(b,msg):
    if not b:raise ValueError(msg)


@cache
def ld(n,d=1):
    with localcontext() as c:
        c.prec=82
        ln=Decimal(n).ln();lt=Decimal(d).ln()
        c.rounding='ROUND_FLOOR';sl=(ln.next_minus()-lt.next_plus())*S
        c.rounding='ROUND_CEILING';su=(ln.next_plus()-lt.next_minus())*S
        return int(sl.to_integral_value(rounding='ROUND_FLOOR')),int(su.to_integral_value(rounding='ROUND_CEILING'))


def val(n,q):
    i=0
    while n%q==0:n//=q;i+=1
    return i


def strip(n,G):
    while (c:=gcd(n,G))!=1:n//=c
    return n


@cache
def sg(q,f):return (q**(f+1)-1)//(q-1)


def integerlog(n,b):
    t=0
    while n>=b:n//=b;t+=1
    return t


def allowed(r,f,bad):
    return all(pow(r,f+1,q*(r-1))!=1 for q in bad)


def run(P):
    ck(set(P)=={'assigned','present','absent','leaf','ecpp'},'packet')
    A=P['assigned'];p,e=A[0];sure=P['present'];ban=P['absent'];F=P['leaf'];cs=P['ecpp'];used=set()
    ck(p in (13,19,31) and type(e)==int and e>=2 and not e%2,'root')
    bad=(*R[:R.index(p)],*ban)
    ck(len(bad)==len(set(bad)) and len(set(sure))==len(sure) and not set(sure)&set(bad),'support')
    ck(F['kind']=='terminal' and set(F)=={'kind','promoted','edges','weights'},'leaf')
    @cache
    def prime(x):
        if not(type(x)==int and x>2):return False
        if x<2**64:return prime64(x)
        a=x;pc=cs[str(x)];ck(bool(pc),'empty chain')
        for row in pc:
            ck(a==row[0],'ECPP link');a=level(*row)
        used.add(str(x));return prime64(a)
    ck(all(prime(q) for q in (*sure,*bad)),'support prime')
    ex=dict(A);odd=[q for q,f in A if f%2];ck(len(ex)==len(A) and len(odd)<=1,'exact support')
    ck(all(type(f)==int and 1<=f<=6000 and prime(q) and q not in bad and (not f%2 or q%4==f%4==1) and allowed(q,f,bad) for q,f in A),'exact component')
    X=prod(q**f for q,f in A);Y0=prod(sg(q,f)//(2 if f%2 else 1) for q,f in A);D=strip(Y0,prod(ex));ck(all(val(Y0,q)<=f for q,f in A),'assigned valuations')
    small=tuple(n for n in range(3,L,2) if all(n%d for d in range(3,isqrt(n)+1,2)))
    M={q:36 for q in small if q not in bad and q not in ex}
    seen=set()
    for q,c in F['promoted']:
        ck(prime(q) and q not in bad and q not in ex and q not in seen and type(c)==int and 0<=c<=160,'promoted')
        seen.add(q);M[q]=max(M.get(q,0),c)
    for q in sure:
        if q not in ex:M.setdefault(q,0)
    T=defaultdict(set)
    for r,q in F['edges']:
        ck(r in M and q in M and r!=q and q not in T[r],'edge');T[r].add(q)
    W=prod(M)*prod(ex);D0=strip(D,W);ck(gcd(D0,prod(small))==1,'rough')
    h={q:val(D,q) for q in M};cost=[];ab=[];special=[];opts={};incoming=defaultdict(list)
    A0=ld(L,L-1)[1]
    for r,c in sorted(M.items()):
        O=opts[r]=[]
        for f,step in ((2,2),(1,4)):
            sp=step==4
            if sp and (odd or r%4!=1 or not allowed(r,1,bad)):continue
            while f<h[r] or not allowed(r,f,bad):f+=step
            while True:
                j=len(cost);exact=f<=c;O.append((j,f,exact));low=f*ld(r)[0];high=ld(r,r-1)[1]
                if exact:
                    sig=sg(r,f);core=sig//(2 if sp else 1);u=strip(core,W)
                    low+=ld(u)[0];high=ld(sig,r**f)[1]+integerlog(u,L)*A0
                    for q in sorted(T[r]|set(ex)):
                        v=val(core,q)
                        if v:incoming[q].append((j,v))
                cost.append(low);ab.append(high)
                if sp:special.append(j)
                if not exact:break
                f+=step
                while not allowed(r,f,bad):f+=step
    tail=len(cost);cost.append(2*ld(L)[0]*S//A0);ab.append(S)
    if not odd:special.append(len(cost));cost.append(ld(L)[0]);ab.append(A0)
    free=sum(ld(sg(q,f),q**f)[1] for q,f in A)+integerlog(D0,L)*A0
    rows=[({i:-v for i,v in enumerate(ab)},free-ld(2)[0])]
    if not odd:rows.append(({i:S for i in special},S))
    for q,O in opts.items():
        if incoming[q]:
            row={i:v*S for i,v in incoming[q]};cap=O[-1][1]
            cap=max(f for i,f,x in O)+integerlog(10**2400,q)
            for j,f,x in O:row[j]=-S*(f if x else cap)
            rows.append((row,-S*h[q]))
    for q in ex:
        if incoming[q]:rows.append(({i:v*S for i,v in incoming[q]},S*(ex[q]-val(Y0,q))))
    for q,O in opts.items():
        for j,v in incoming[q]:rows.append(({j:S,**{i:-S for i,f,x in O if not x or f>=v+h[q]}},0))
    r=[Y*v for v in cost];c=Y*ld(X*D0)[0];last=-1
    for n,w in F['weights']:
        ck(type(n)==type(w)==int and last<n<len(rows) and w>0,'weights');last=n
        m,b=rows[n];c-=w*b
        for j,v in m.items():r[j]+=w*v
    ck(r[tail]>=0,'unbounded tail')
    c+=sum(min(r[j] for j,_,_ in O) if h[q] or q in sure else min(0,*(r[j] for j,_,_ in O)) for q,O in opts.items())
    if not odd:c+=min(0,r[tail+1])
    ck(used==set(cs),'unused cert')
    k=Y*ld(10)[1]
    ck(c>2400*k,'open')
    return c//k


def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('packet',nargs='+');o=a.parse_args()
    for f in o.packet:
        x=json.loads(gzip.decompress(Path(f).read_bytes()));print('INDEPENDENT CONDITIONAL',x['assigned'],x['present'],x['absent'],run(x),flush=True)

if __name__=='__main__':main()
