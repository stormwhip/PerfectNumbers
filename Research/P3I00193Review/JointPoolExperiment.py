"""One selection variable family per prime in forest union LP; floating search only.

All forest nodes have abundance columns, including unactivated nodes. Forest
and LP residual demands share one external-volume constraint. No forest bound
is added separately. Unknown residual/source overlap remains a pending premise.
"""
import json
import sys
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from ReplayCandidate import HERE,INPUT,load_model,pools
import check


def solve(leaf,m):
    u,p=pools(leaf);pool=sorted(u|p);ps=set(pool)
    absent=m.ABS3|set(leaf['absent_extra'])
    L=next(r for r in check.small_primes(50000) if r not in ps|absent|{2,3})
    opts={};data=[];inflows=[]
    for r in pool:
        stop=leaf['forest']['cut_even'][str(r)] if r in u else (42 if r<100 else 22 if r<400 else 12)
        fs=[f for f in range(2,stop,2) if check.allowed(r,f,absent)]
        fe=stop
        while not check.allowed(r,fe,absent):fe+=2
        opts[r]=[]
        for f in fs+[None]:
            j=len(data);opts[r].append((f,j))
            if f is None:
                cost=Decimal(fe)*m.ln_lo(r)-m.ALPHA_HI*(m.ln_hi(fe+1)/m.LN3_LO if r%3==1 else 0)
                ab=m.ln_hi(r)-m.ln_lo(r-1);vol=Decimal(0)
            else:
                S=check.sigma(r,f);rem=S
                cost=Decimal(f)*m.ln_lo(r)-m.ALPHA_HI*check.valuation(S,3)
                ab=m.ln_hi(S)-Decimal(f)*m.ln_lo(r)
                for t in ps|{2,3}:
                    while rem%t==0:rem//=t
                vol=(1-2*m.LN3_HI/m.ln_lo(L))*m.ln_lo(rem) if rem>1 else Decimal(0)
                if r in u:
                    for child in leaf['forest']['edges'].get(str(r),[]):
                        v=check.valuation(S,child)
                        if v:inflows.append((j,child,v))
                if r in p:
                    for src,fsrc,t,v,_,_ in leaf['lp']['inf_dual']:
                        if src==r and fsrc==f:inflows.append((j,t,v))
            data.append((float(cost),float(ab),float(vol)))
    n=len(data)+1
    required=set(leaf['present'])
    assert required<=ps
    nr=len(pool)+len(required)+2+len(inflows)
    mat=lil_matrix((nr,n));rhs=np.zeros(nr);row=0
    for r in pool:
        for _,j in opts[r]:mat[row,j]=1
        rhs[row]=1;row+=1
    for r in sorted(required):
        for _,j in opts[r]:mat[row,j]=-1
        rhs[row]=-1;row+=1
    for j,(_,ab,_) in enumerate(data):mat[row,j]=-ab
    c=(m.ln_hi(L)-m.ln_lo(L-1))/(2*(m.ln_lo(L)-2*m.LN3_HI))
    mat[row,n-1]=-float(c)
    rhs[row]=-float(m.LN43_LO-Decimal('1e-5')-(m.ln_hi(L)-m.ln_lo(L-1)));row+=1
    for j,(_,_,v) in enumerate(data):mat[row,j]=v
    mat[row,n-1]=-1;row+=1
    for j,t,v in inflows:
        mat[row,j]+=1
        for f,k in opts[t]:
            if f is None or f>=v:mat[row,k]-=1
        row+=1
    opt=linprog([c for c,_,_ in data]+[1.],A_ub=mat.tocsr(),b_ub=rhs,bounds=[(0,1)]*(n-1)+[(0,None)],method='highs')
    assert opt.success,opt.message
    return {'name':leaf['name'],'pool_primes':len(pool),'columns':n,'constraints':nr,
            'joint_net_digits_float':opt.fun/float(m.LN10_HI),
            'minimum_inequality_slack_float':float(min(opt.ineqlin.residual))}


def main():
    cert=json.loads((INPUT/'P3E1162Complete.json').read_text());m=load_model();rows=[]
    for i in [0,2,3,4,8,9,12]:
        row=solve((cert['cell10']+cert['cell11'])[i],m);row['leaf_index']=i;rows.append(row);print(row,flush=True)
    (HERE/'JointPoolResults.json').write_text(json.dumps({'status':'FLOATING_JOINT_RELAXATION_ONLY','accepted_actuals':[],'rows':rows},indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
