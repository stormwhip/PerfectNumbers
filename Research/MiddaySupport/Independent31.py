"""Independent assigned-source forest replay using exact multiplicative DP.

Uses shared prime certificate arithmetic only; no dependency on Compose,
Scout, Weighted, or the discovery cache. Only conditional forest/direct packets.
"""
import argparse,gzip,json,sys
from functools import cache
from math import gcd,prod
from pathlib import Path
P=Path(__file__).resolve().parents[1]
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


@cache
def certified(n,rows):
    z=n
    for row in rows:
        req(z==row[0],'chain link');z=level(*row)
    return prime64(z)

def replay(x,tail=False):
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
        def freeze(x):return tuple(map(freeze,x)) if isinstance(x,list) else x
        used.add(str(n));return certified(n,freeze(ar))
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
    if tail:
        limits={150332843:101} if tail is True else tail
        for r,h in limits.items():
            req(r in roots and (D%r==0 or r in extra),'tail compulsion');cs0[r]=max(cs0[r],h)
    v={q:node(q,max(1,a),False)[0] for q,a in cs0.items()};normal=base*prod(v.values());out=[normal]
    if not locked:
        for q,a in cs0.items():
            for sp in (False,True):
                a0=node(q,max(a,1),sp)
                if a0:out.append(normal//v[q]*a0[not sp])
    b=min(out);req(b>B,'forest remains live');req(used==set(cs),'unused certificate');return len(str(b))-1


def verify31():
    X=json.loads(gzip.decompress((Path(__file__).resolve().parent/'Full31.json.gz').read_bytes()));t=X['leaf'];q=150332843
    req(X['assigned']==[[31,10]] and X['present']==[5] and X['absent']==[3,13,17] and set(t)=={'kind','q','cut','cells','tail'} and (t['kind'],t['q'],t['cut'])==('exp',q,100),'scope');req(prime64(q) and sig(31,10)%q==0 and q%4==3,'pivot')
    bad=3*13*17*19*7*11; required={str(f) for f in range(2,101,2) if gcd(sig(q,f),bad)==1};req(set(t['cells'])==required,'coverage');scores={}
    for k,u in [*t['cells'].items(),('tail',t['tail'])]:
        A=[[31,10]]+([] if k=='tail' else [[q,int(k)]]);K=set(u['roots'])|dict(u['owners']).keys();cs={str(r):X['ecpp'][str(r)] for r in K if r>=2**64};scores[k]=replay(dict(assigned=A,present=[5],absent=[3,13,17],leaf=u,ecpp=cs),k=='tail')
    print('independent Full31',len(required),'exact cells, minimum',min(scores.values()),'tail',scores['tail'])
def both():
    pkt=json.loads(gzip.decompress((Path(__file__).resolve().parent/'Both31.json.gz').read_bytes()));q=150332843;bad=19*7*11*13*17*29*37;scores=[];req(pkt['assigned']==[[31,10],[5,1]] and pkt['present']==[3,5] and pkt['absent']==[13,17,29,37] and prime64(q) and sig(31,10)%q==0,'both scope')
    def deep(A,r,cut,t):
        req((t['kind'],t['q'],t['cut'])==('exp',r,cut),'split');D=prod(sig(z,f)//(2 if f%2 else 1) for z,f in A);v=valuation(D,r);assert r in (q,3) and (r==3 or D%r==0);K={str(f) for f in range(2,cut+1,2) if f>=v and gcd(sig(r,f),bad)==1};req(set(t['cells'])==K,'incomplete exp');
        for k,u in [*t['cells'].items(),('tail',t['tail'])]:
            aa=A if k=='tail' else A+[[r,int(k)]];lims={r:cut+1} if k=='tail' else {}
            if r==q and k=='40':deep(aa,3,80,u);continue
            names=set(u['roots'])|dict(u['owners']).keys();cs={str(z):pkt['ecpp'][str(z)] for z in names if z>=2**64};scores.append(replay(dict(assigned=aa,present=pkt['present'],absent=pkt['absent'],leaf=u,ecpp=cs),lims))
    deep(pkt['assigned'],q,100,pkt['leaf']);print('independent Both31',len(scores),'leaves; min',min(scores))
if __name__=='__main__':both() if '--both' in sys.argv else verify31()
