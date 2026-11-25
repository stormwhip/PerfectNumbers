"""Independent assigned-source forest replay using exact multiplicative DP.

Uses shared prime certificate arithmetic only; no dependency on Compose,
Scout, Weighted, or the discovery cache. Only conditional forest/direct packets.
"""
import argparse,gzip,json,sys
from functools import cache
from math import gcd,prod
from pathlib import Path
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'RootFiveNext'))
from PrimeCheck import prime64,level
R=(19,7,11,31,13,3,5,17);B=10**2400


def req(x,msg):
    if not x:raise ValueError(msg)


def valuation(n,p):
    v=0
    while n%p==0:n//=p;v+=1
    return v


def trim(D,U):
    while (g:=gcd(D,U))>1:D//=g
    return D


@cache
def sig(q,f):return (q**(f+1)-1)//(q-1)


def replay(x):
    req(set(x)=={'assigned','present','absent','leaf','ecpp'},'schema')
    A=x['assigned'];p,e=A[0];extra=x['present'];leaf=x['leaf'];cs=x['ecpp'];used=set()
    req(type(p)==int and p in (13,19,31) and type(e)==int and e>=2 and not e%2,'root')
    bad=(*R[:R.index(p)],*x['absent'])
    req(len(set(bad))==len(bad) and len(set(extra))==len(extra) and not set(extra)&set(bad),'support')
    @cache
    def prime(n):
        if type(n)!=int or n<=2:return False
        if n<2**64:return prime64(n)
        t=n;ar=cs[str(n)];req(bool(ar),'chain')
        for row in ar:
            req(t==row[0],'chain link');t=level(*row)
        used.add(str(n));return prime64(t)
    K0=dict(A);locked=sum(f%2 for q,f in A)
    req(len(A)==len(K0) and all(prime(q) and type(f)==int and 1<=f<=6000 for q,f in A) and all(prime(q) for q in (*bad,*extra)),'exact assigned prime')
    X=prod(q**f for q,f in A);S=prod(sig(q,f)//(2 if f%2 else 1) for q,f in A)
    D=trim(S,prod(K0));M=X*D
    conflict=(locked>1 or any(f%2 and q%4!=1 or f%2 and f%4!=1 for q,f in A) or gcd(X*S,prod(bad))>1 or any(valuation(S,q)>f for q,f in A))
    if leaf['kind']=='direct':
        req(set(leaf)=={'kind'} and (conflict or M>B),'direct remains live'); req(used==set(cs),'unused certificate');return None
    req(leaf['kind']=='forest' and set(leaf)=={'kind','roots','owners','head'} and not conflict,'forest fields')
    roots=set(leaf['roots']);parents=dict(leaf['owners']);support=roots|parents.keys();n=leaf['head']
    req(type(n)==int and 1<=n<=1024 and len(roots)==len(leaf['roots']) and len(parents)==len(leaf['owners']) and not roots&parents.keys(),'forest shape')
    req(all(prime(q) and q not in K0 and q not in bad for q in support),'forest prime/scope')
    req(all(not D%q or q in extra for q in roots),'compulsion')
    req(all(D%q and q not in extra and z in support for q,z in parents.items()),'scope')
    kid={z:[] for z in support}
    for q,z in parents.items():kid[z].append(q)
    seen=set();todo=list(roots)
    while todo:
        q=todo.pop();req(q not in seen,'cycle');seen.add(q);todo+=kid[q]
    req(seen==support,'reachability')
    U=X*D*prod(parents)*prod(extra)
    def legal(q,f):return all(pow(q,f+1,b*(q-1))!=1 for b in bad)
    @cache
    def node(q,v,sp):
        if sp and (locked or q%4!=1 or not legal(q,1)):
            return None
        step=4 if sp else 2;f=(1 if sp else 2)
        f+=step*max(0,-((f-v)//step));head=0;allord=flex=B+1
        while head<n and q**f<max(allord,flex):
            if legal(q,f):
                head+=1;ss=sig(q,f)//(2 if sp else 1)
                active=[(z,k) for z in kid[q] if (k:=valuation(ss,z))]
                vals=[node(z,k,False)[0] for z,k in active]
                base=q**f*trim(ss,U);z0=base*prod(vals)
                ans=[z0]
                if not sp and not locked:
                    for (z,k),w in zip(active,vals):
                        ordv=node(z,k,False)[1];ev=node(z,k,True)
                        if ev:ordv=min(ordv,ev[0])
                        ans.append(z0//w*ordv)
                allord=min(allord,z0);flex=min(flex,*ans)
            f+=step
        return min(allord,q**f),min(flex,q**f)
    cs0={q:valuation(D,q) for q in roots};base=M//prod(q**v for q,v in cs0.items())
    v={q:node(q,max(1,a),False)[0] for q,a in cs0.items()};normal=base*prod(v.values());out=[normal]
    if not locked:
        for q,a in cs0.items():
            for sp in (False,True):
                a0=node(q,max(a,1),sp)
                if a0:out.append(normal//v[q]*a0[not sp])
    b=min(out);req(b>B,'forest remains live');req(used==set(cs),'unused certificate');return len(str(b))-1


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('packet',nargs='+',type=Path);a=ap.parse_args()
    for f in a.packet:
        x=json.loads(gzip.decompress(f.read_bytes()));print('INDEPENDENT CONDITIONAL',x['assigned'],x['present'],x['absent'],replay(x),flush=True)
