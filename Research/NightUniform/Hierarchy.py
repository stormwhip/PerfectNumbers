"""One universally quantified secondary-root stage; true = proof, false = unknown.
The tail f>=F has NO assumed sigma factor of q. Retain root p actual p^e and exact head q^f only.
"""
from MaskSieve import H,R,ROOTS,B,sig,ratio,exponent_ok,minexp,smallprimes,factors,allcost
import math,time,json,collections
from functools import cache
from fractions import Fraction as Fr
CUT=24
@cache
def branchfacts(q,f):return tuple(t for t in smallprimes() if sig(q,f)%t==0)
@cache
def forced(p,e,m):
    P=tuple(q for i,q in enumerate(ROOTS) if m>>i&1); bad=tuple(q for q in ROOTS if q not in P);return frozenset(P)|frozenset(factors(p,e)),bad
@cache
def strong(K,bad,locked):
    normal=Fr(1);mult=Fr(1)
    for r in K:
        v=ratio(r,minexp(r,False,bad));normal*=v
        if not locked and minexp(r,True,bad):mult=min(mult,ratio(r,minexp(r,True,bad))/v)
    return normal*mult

def leaves(p,e,q,mask,prior):
    K,bad=forced(p,e,mask); A=sig(p,e); v=0;t=A
    while t%q==0:v+=1;t//=q
    def check(f,tail):
        X=p**e*q**f;S=A if tail else A*sig(q,f);fixed=(p,q);D=S//math.gcd(2*X,S)
        # In a tail q^f is a lower bound, not its exact component: strip q from A before charging separately.
        if tail:D=t
        elif math.gcd(X,D)>1:return True
        if X*D>B:return True
        L=K if tail else K|frozenset(branchfacts(q,f));L=L.difference(fixed)
        return ratio(p,e)*ratio(q,f)*strong(L,bad,f%2==1)>2
    for euler in (False,True):
        if euler and (q%4!=1 or not minexp(q,True,bad)):continue
        fr=minexp(q,euler,bad);step=4 if euler else 2;f=fr
        while True:
            if f>=v and exponent_ok(q,f,bad):
                tail=f>CUT
                if not check(f,tail):return False
                if tail:break
            f+=step
    return True

def main():
    t=time.perf_counter();D=json.loads((H/'ResidualAudit.json').read_text());rows=[];cert=[];c=collections.Counter()
    for p,e,ms in D['rows']:
        left=[]
        for m in ms:
            K,bad=forced(p,e,m);other=sorted(K-{p},key=lambda q:(q not in ROOTS,q));
            for q in other:
                if leaves(p,e,q,m,None):cert.append([p,e,m,q]);c[p]+=1;break
            else:left.append(m)
        rows.append([p,e,left]);
    closed=[(p,e) for p,e,ms in rows if not ms];S=json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'];shards=[s['id'] for s in S if all((s['root'],e) in closed for e in s['remaining_actuals'])];(H/'HierarchyAudit.json').write_text(json.dumps(dict(conditional=cert,closed=closed,closed_shards=shards,rows=rows),separators=(',',':'))+'\n');print(c,len(closed),shards,'seconds',time.perf_counter()-t)
if __name__=='__main__':main()
