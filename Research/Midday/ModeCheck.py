"""Exact certificate: every possible Euler location is covered by at least one row.
Schema: ordinary proof for all Euler primes outside a finite exceptional set, plus
an independent alternative graph for each exceptional prime, promoted and exact-Euler.
"""
from pathlib import Path
from functools import lru_cache,cache
from math import gcd,prod
import argparse,sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'RootFiveNext'));from PrimeCheck import prime64,level
B=10**2400;ORDER=(19,7,11,31,13,3,5,17)
def need(c,t):
    if not c:raise ValueError(t)
def vp(n,q):
    k=0
    while n%q==0:k+=1;n//=q
    return k

def run(row,certs,exceptions,euler,prime):
    p,e=row['p'],row['e'];A=(p**(e+1)-1)//(p-1); head=row['head'];need(type(e)==int and type(p)==int and p in ORDER and 2<=e<10000 and not e%2 and type(head)==int and 0<head<=512,'domains');need(set(row)=={'p','e','roots','owners','head'},'row fields');K=set(row['roots']);ow=dict(row['owners']);need(K and len(K)==len(row['roots']) and len(ow)==len(row['owners']) and not K&ow.keys(),'labels');need(all(A%z==0 for z in K) and all(p*A%z for z in ow),'root geometry');V=K|ow.keys();ban=ORDER[:ORDER.index(p)];need(all(prime(z) and z!=p for z in V),'prime/scope') # forbidden labels can be unused candidates
    if euler is not None:
        need(prime(euler) and euler%4==1 and euler not in (p,*ban),'invalid Euler');K.add(euler);ow.pop(euler,None);V.add(euler)
    kids={v:[] for v in V}
    for z,w in ow.items():need(w in V,'parent');kids[w].append(z)
    seen=set();todo=list(K)
    while todo:
        z=todo.pop();need(z not in seen,'cycle');seen.add(z);todo.extend(kids[z])
    need(seen==V,'unreachable');U=p*A*prod(ow)*(euler or 1);LB=B+1
    @cache
    def node(z,h):
        # no,flex for a whole subtree, or fixed-mode scalar stored twice.
        no=flex=LB
        for odd in (False,True):
            if euler is not None and (z==euler)!=odd:continue
            if odd and (z in exceptions or z%4!=1 or any((z+1)%b==0 for b in ban)):continue
            step=4 if odd else 2;f=h+((1 if odd else 0)-h)%step;count=0
            while True:
                if any(pow(z,f+1,b*(z-1))==1 for b in ban):f+=step;continue
                n=z**f
                if count==head or n>=(flex if odd else max(no,flex)):
                    if not odd or euler is not None:no=min(no,n)
                    flex=min(flex,n);break
                S=(n*z-1)//(z-1)//(2 if odd else 1);C=S
                while (g:=gcd(C,U))!=1:C//=g
                sub=[node(t,vp(S,t)) for t in kids[z] if S%t==0];w=n*C*prod(v for v,_ in sub)
                if not odd or euler is not None:no=min(no,w)
                if not odd and euler is None:w=min([w]+[w//v*s for v,s in sub])
                flex=min(flex,w);count+=1;f+=step
        return no,flex
    c={z:vp(A,z) for z in K};pairs=[node(z,max(h,1)) for z,h in c.items()];v=p**e*(A//prod(z**h for z,h in c.items()))*prod(x for x,y in pairs);val=min([v]+[v//x*y for x,y in pairs]) if euler is None else v
    node.cache_clear();return val

def replay(doc):
    need(set(doc)=={'general','special','ecpp'},'packet fields');gen=doc['general'];special=doc['special'];cs=doc['ecpp'];p,e=gen['p'],gen['e'];ex={int(k) for k in special};seen=set()
    @cache
    def prime(z):
        if type(z)!=int or z<3:return False
        t=z
        if t>=2**64:
            chain=cs[str(z)];need(chain,'missing chain');seen.add(str(z))
            for r in chain:need(r[0]==t,'bad chain');t=level(*r)
        return prime64(t)
    bounds=[run(gen,cs,ex,None,prime)]
    for z in sorted(ex):
        row=special[str(z)];need((row['p'],row['e'])==(p,e),'target mismatch');bounds.append(run(row,cs,set(),z,prime))
    need(min(bounds)>B and seen==set(cs),'threshold or unused certificate');return p,e,[len(str(x))-1 for x in bounds]
if __name__=='__main__':
    for name in sys.argv[1:]:print('PASS',replay(json.loads(gzip.decompress(Path(name).read_bytes()))))
