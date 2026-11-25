"""Independent Euler-location cover. Enumerate exact location costs on an ordinary forest
by sparse location dictionaries, with a different ECPP arithmetic implementation.
In a specialized row the known Euler prime is promoted and every other prime is ordinary.
"""
import json,gzip,sys,math
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'ThreeChainNext'));from Replay import elliptic,mr
ORDER=[19,7,11,31,13,3,5,17];B=10**2400

def require(c,m):
    if not c:raise ValueError(m)

def val(n,z):
    a=0
    while n%z==0:n//=z;a+=1
    return a

def verify(file):
    doc=json.loads(gzip.decompress(Path(file).read_bytes()));require(set(doc)=={'general','special','ecpp'},'fields');used=set();cs=doc['ecpp'];seed=doc['general'];p,e=seed['p'],seed['e'];require(type(p)==type(e)==int and p in ORDER and 2<=e<=7000 and e%2==0,'root');A=(p**(e+1)-1)//(p-1);ban=math.prod(ORDER[:ORDER.index(p)]);exc={int(z) for z in doc['special']};require(len(exc)==len(doc['special']),'duplicate exceptional label')
    @cache
    def checkprime(z):
        require(type(z)==int and z>2,'prime');q=z
        if q>=2**64:
            c=cs[str(z)];require(len(c)>0,'empty witness');used.add(str(z))
            for a in c:require(a[0]==q,'misbound witness');q=elliptic(*a)
        require(q<2**64 and mr(q),'terminal composite')
    def calc(r,sp=None):
        require(set(r)=={'roots','p','e','head','owners'} and (r['p'],r['e'])==(p,e),'row');cap=r['head'];require(type(cap)==int and 1<=cap<=512,'cap');k=set(r['roots']);ow=dict(r['owners']);require(k and len(k)==len(r['roots']) and len(ow)==len(r['owners']) and not k&set(ow),'unique');require(all(A%z==0 for z in k) and all(A*p%z for z in ow),'divisor scope');
        if sp is not None:k.add(sp);ow.pop(sp,None);require(sp%4==1 and sp!=p and ban%sp!=0,'Euler mismatch')
        V=k|ow.keys();kids={z:[] for z in V};
        for z in V:checkprime(z)
        for z,t in ow.items():require(t in V,'parent');kids[t].append(z)
        reach=list(k);seen=set(reach)
        for t in reach:
            for z in kids[t]:require(z not in seen,'cycle');seen.add(z);reach.append(z)
        require(seen==V,'disconnected');U=p*A*(sp or 1)*math.prod(ow);base=p**e*A
        for z in k:base//=z**val(A,z)
        # Work in integer costs. If a fixed location is absent from the currently
        # triggered subtree, the ordinary cost remains a safe relaxation for that location.
        @cache
        def cell(z,h):
            regular=B+1;alternative={};local=B+1
            for odd in (False,True):
                if sp is not None and (z==sp)!=odd:continue
                if odd and (z%4!=1 or (sp is None and z in exc)):continue
                step=4 if odd else 2;f=h+((1 if odd else 0)-h)%step;count=0
                while True:
                    n=z**f
                    if n>=(local if odd else regular) or count>=cap:
                        if odd:local=min(local,n)
                        else:regular=min(regular,n)
                        break
                    S=(n*z-1)//(z-1)
                    if math.gcd(S,ban)==1:
                        count+=1;S//=2 if odd else 1;C=S
                        while (g:=math.gcd(C,U))!=1:C//=g
                        a=n*C;children=[]
                        for q in kids[z]:
                            if S%q==0:
                                m,d=cell(q,val(S,q));a*=m;children.append((m,d))
                        if odd:local=min(local,a)
                        else:
                            regular=min(regular,a)
                            if sp is None:
                                for m,d in children:
                                    for q,w in d.items():alternative[q]=min(alternative.get(q,B+1),a//m*w)
                    f+=step
                    # q+1 divides every odd-index sigma; no legal odd cell when it shares a forbidden prime.
                    if odd and math.gcd(z+1,ban)>1:break
            if sp==z:return local,{}
            if sp is None and local<regular:alternative[z]=local
            return regular,{q:v for q,v in alternative.items() if v<regular}
        v0=base;props=[]
        for z in k:
            b,d=cell(z,max(1,val(A,z)));v0*=b;props.append((b,d))
        out=min([v0]+[v0//b*v for b,d in props for v in d.values()]);cell.cache_clear();return out
    vals=[calc(seed)]+[calc(doc['special'][str(z)],z) for z in sorted(exc)];require(min(vals)>B and used==set(cs),'open or unused ECPP');print('INDEPENDENT EULER COVER',p,e,[len(str(n))-1 for n in vals],flush=True);return p,e
if __name__=='__main__':
    for f in sys.argv[1:]:verify(f)
