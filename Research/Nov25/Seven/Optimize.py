"""Heuristic cutting-plane search for eighth-grid prices accepted by pinned replay."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import time
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix
from Search import H,load,scorer,arithmetic,sigma,nonsupport,valuation


def optimize(row,seconds=180,prior=None):
    t=time.monotonic(); r=dict(row); r['head']=max(120,r['head']); vertices=set(r['roots'])|dict(r['owners']).keys(); p,e=r['p'],r['e']; A=sigma(p,e); U=p*A*math.prod(dict(r['owners'])); logs={q:math.log10(q) for q in vertices};
    W=prior or {}; best=-math.inf; bw={}; all_q=set(W); planes={}; tried=set(); sf_out={}
    def plane(v,S):
        slope=Counter({q:-f for q,(h,f,k,w) in S.items()});
        for q in r['roots']:slope[q]+=valuation(A,q)
        for z,(h,f,k,w) in S.items():
            if w is False:continue
            key=(z,f)
            if key not in sf_out:
                s=arithmetic(z,f); k0=math.gcd(s,U); out={}
                # Iterating graph labels is cheap once this value is reduced.
                for q in vertices:
                    if k0%q==0:out[q]=valuation(s,q)
                sf_out[key]=out
            slope.update(sf_out[key])
        b=v-sum(W.get(q,0.0)*x*logs[q] for q,x in slope.items()); nz=tuple(sorted((q,x) for q,x in slope.items() if x)); all_q.update(q for q,x in nz if x>0)
        if nz not in planes or b<planes[nz]:planes[nz]=b
    def see(W):
        vals,tr=scorer(r,W); mn=min(vals.values()); return vals,tr,mn
    def optimum():
        qs=sorted(all_q); idx={q:i for i,q in enumerate(qs)}; m=len(qs); ys=[0]*m+[-1]
        b=[]; rr=[]; cc=[]; vv=[]
        for sl,c in planes.items():
            j=len(b);b.append(c)
            for q,x in sl:
                if q in idx:rr.append(j);cc.append(idx[q]);vv.append(-x*logs[q]/8)
            rr.append(j);cc.append(m);vv.append(1)
        aa=csr_matrix((vv,(rr,cc)),shape=(len(b),m+1))
        rc=milp(ys,integrality=[1]*m+[0],bounds=Bounds([0]*m+[-math.inf],[7]*m+[math.inf]),constraints=LinearConstraint(aa,[-math.inf]*len(b),b),options={'time_limit':min(8,max(1,seconds-(time.monotonic()-t)))})
        if rc.x is None:return {},-math.inf
        return {q:round(w)/8 for q,w in zip(qs,rc.x[:-1]) if round(w)},rc.x[-1]
    iterations=0
    while time.monotonic()-t<seconds:
        iterations+=1
        vals,tr,mn=see(W)
        if mn>best+1e-6:
            best=mn; bw=W.copy();print('price best',p,e,iterations,round(best,6),len(W),'planes',len(planes),'sec',round(time.monotonic()-t,1),flush=True)
            if best>2400.000001:break
        # Use handful of globally distinct Euler modes per iteration.
        for m,v in sorted(vals.items(),key=lambda kv:kv[1])[:7]:
            if math.isfinite(v) and v<max(2460,mn+100):plane(v,tr(m))
        tried.add(tuple(sorted(W.items())))
        W,cap=optimum()
        if tuple(sorted(W.items())) in tried or cap<=best+1e-7:
            break
    r['den']=8;r['rho']=[[q,round(w*8)] for q,w in bw.items() if w]; r['scout']=best
    fp=H/f'price-{p}x{e}.json';fp.write_text(json.dumps(r,separators=(',',':'))+'\n',encoding='utf-8'); return r,bw

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('case');a.add_argument('--seconds',type=int,default=180);a.add_argument('--start',type=Path); x=a.parse_args(); p,e=map(int,x.case.split('x'))
    r=json.loads(x.start.read_bytes()) if x.start else load(p,e)
    w={q:v/r['den'] for q,v in r.get('rho',[])}
    optimize(r,x.seconds,w)
