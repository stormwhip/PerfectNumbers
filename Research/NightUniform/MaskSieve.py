"""Exact cross-root support partition; never uses an Euler-source valuation or factors a cofactor."""
import collections,json,math,time
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
H=Path(__file__).resolve().parent; R=H.parent; ROOTS=(19,7,11,31,13,3,5,17); B=10**2400
@lru_cache(None)
def sig(p,e):return (p**(e+1)-1)//(p-1)
@lru_cache(None)
def ratio(p,e):return F(sig(p,e),p**e)
def exponent_ok(p,e,bad):return all((e+1)%q if p%q==1 else pow(p,e+1,q)!=1 for q in bad)
@lru_cache(None)
def minexp(p,special,bad):
    if special and (p%4!=1 or not exponent_ok(p,1,bad)):return None
    e=1 if special else 2
    while not exponent_ok(p,e,bad):e+=4 if special else 2
    return e
@lru_cache(None)
def model(mask):
    P=tuple(p for i,p in enumerate(ROOTS) if mask>>i&1);bad=tuple(q for q in ROOTS if q not in P); return [(z,tuple(minexp(p,p==z,bad) for p in P)) for z in (0,*P) if not z or minexp(z,True,bad)]
@lru_cache(None)
def smallprimes():return tuple(p for p in range(3,10001,2) if all(p%d for d in range(3,math.isqrt(p)+1,2)))
@lru_cache(None)
def factors(p,e):
    n=sig(p,e);return tuple(q for q in smallprimes() if n%q==0)
@lru_cache(None)
def allcost(rs,z,bad):
    result=F(1)
    for q in rs:result*=ratio(q,minexp(q,q==z,bad))
    return result

def calc(p,e,mask):
    P=tuple(q for i,q in enumerate(ROOTS) if mask>>i&1); bad=tuple(q for q in ROOTS if q not in P)
    if not exponent_ok(p,e,bad):return 'forced-root'
    K=tuple(sorted(set(P)|set(factors(p,e))-{2})); A=sig(p,e); K=tuple(q for q in K if q!=p)
    for z in (p,) if e%2 else (0,*[q for q in K if minexp(q,True,bad)]):
        if e%2 and not minexp(p,True,bad):continue
        if ratio(p,e)*allcost(K,z,bad)>2:continue
        n=p**e*(A if A%2 else A//2); t=A
        for q in K:
            v=0
            while t%q==0:v+=1;t//=q
            f=max(v,minexp(q,z==q,bad));step=4 if z==q else 2;k=1 if z==q else 0; f+=(k-f)%step
            while not exponent_ok(q,f,bad):f+=step
            n*=q**(f-v)
            if n>B:break
        if n<=B:return 'open'
    return 'abundance-or-size'

def main():
    t=time.perf_counter(); S=json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards']; keys=sorted({(s['root'],e) for s in S for e in s['remaining_actuals']}); stats=collections.Counter(); rows=[]
    for p,e in keys:
        i=ROOTS.index(p); masks=range(1<<i,256,2<<i); left=[]
        for m in masks:
            why=calc(p,e,m);stats[p,why]+=1
            if why=='open':left.append(m)
        rows.append([p,e,left]);
    closed={(p,e) for p,e,ms in rows if not ms}; shards=[s['id'] for s in S if all((s['root'],e) in closed for e in s['remaining_actuals'])];out=dict(roots=ROOTS,counts={str(k):v for k,v in stats.items()},closed=sorted(closed),closed_shards=shards,rows=rows)
    (H/'MaskAudit.json').write_text(json.dumps(out,separators=(',',':'))+'\n'); print(out['counts'],len(closed),len(shards),'seconds',time.perf_counter()-t)
if __name__=='__main__':main()
