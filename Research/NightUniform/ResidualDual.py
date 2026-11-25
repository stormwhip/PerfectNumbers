"""Factorization-free lower bound for residual abundance in a cross-root mask.
Exact integer dyadic logs (reused atanh enclosure) for all proof decisions. No external optimizer.
"""
import sys,collections,time,json,math,functools
from pathlib import Path
from MaskSieve import H,R,ROOTS,B,minexp,smallprimes,sig,factors,exponent_ok
sys.path.insert(0,str(R/'Session20261122/Python'))
from RoadblockDual import log_bounds,SCALE
LAMBDA=(10,25,50,100,200,400,800,1600,3200,6400,10000,15000,20000,30000,50000,80000)
LOW2=log_bounds(2)[0]; LIMIT=2400*log_bounds(10)[1]; Q=smallprimes(); known=set(Q);cache=functools.lru_cache
@cache(None)
def gain(q):return log_bounds(q,q-1)[1]
@cache(None)
def cost(q):return log_bounds(q)[0]
@cache(None)
def dualtable(bad):
    # Forbidden roots and all eight original roots never occur among residual candidates.
    # Every unknown external Euler option only improves its reduced cost relative to its ordinary option once.
    A=[0]*len(LAMBDA); discount=[0]*len(A)
    for q in Q:
        if q in ROOTS:continue
        h=gain(q);l=cost(q); ordinary=minexp(q,False,bad)*l; g=minexp(q,True,bad)
        for j,w in enumerate(LAMBDA):
            reduced=min(0,ordinary-w*h);A[j]+=reduced
            if g:discount[j]=max(discount[j],reduced-min(0,g*l-w*h))
    assert cost(10001)>=max(LAMBDA)*gain(10001) # for any exponent >=1, all generic tails nonnegative
    return A,discount
@cache(None)
def partial(p,e):
    A=sig(p,e);C=A//2 if e%2 else A; fs={}
    for q in factors(p,e):
        v=0
        while C%q==0:C//=q;v+=1
        if v:fs[q]=v
    k=0;t=C
    while t>=10001:t//=10001;k+=1
    return fs,k,log_bounds((p**e)*(sig(p,e)//(2 if e%2 else 1)))[0],log_bounds(A,p**e)[1]
def test(p,e,m):
    P=tuple(q for i,q in enumerate(ROOTS) if m>>i&1); bad=tuple(q for q in ROOTS if q not in P); fs,k,base,h=partial(p,e); K=tuple((set(fs)|set(P))-{p}); deficit=LOW2-h-sum(gain(q) for q in K)-k*gain(10001)
    if deficit<=0:return False
    A,discount=dualtable(bad); a=A.copy()
    for q in K:
        if q in ROOTS:continue
        c=minexp(q,False,bad)*cost(q);h=gain(q)
        for j,w in enumerate(LAMBDA):a[j]-=min(0,c-w*h)
    def fmin(q,z):
        step=4 if z else 2; v=fs.get(q,0); f=max(v,minexp(q,z,bad));f+=((1 if z else 0)-f)%step
        while not exponent_ok(q,f,bad):f+=step
        return (f-v)*cost(q)
    ordinary={q:fmin(q,False) for q in K}; base+=sum(ordinary.values()); discount_in=0
    if e%2==0:
        discount_in=max((ordinary[q]-fmin(q,True) for q in K if minexp(q,True,bad)),default=0)
    return max(base+w*deficit+a[j]-(max(discount_in,discount[j]) if not e%2 else 0) for j,w in enumerate(LAMBDA))>LIMIT

def main():
    s=time.perf_counter();D=json.loads((H/'MaskAudit.json').read_text()); rows=[];c=collections.Counter(); allc=[]
    for p,e,ms in D['rows']:
        left=[m for m in ms if not test(p,e,m)];c[p]+=len(ms)-len(left); rows.append([p,e,left]);
        if not left:allc.append((p,e))
    S=json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards']; shard=[x['id'] for x in S if all((x['root'],e) in allc for e in x['remaining_actuals'])]; out=dict(conditional=c,closed=allc,closed_shards=shard,rows=rows);(H/'ResidualAudit.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(c,len(allc),shard,'seconds',time.perf_counter()-s)
if __name__=='__main__':main()
