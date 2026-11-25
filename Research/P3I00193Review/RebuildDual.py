"""Rebuild a candidate dual. scipy is used only for search, never ledger acceptance."""
import copy
import json
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from ReplayCandidate import HERE, INPUT, load_model, pools
import check


def build(leaf, m, required):
    lp = leaf['lp']
    P = lp['P']
    u, _ = pools(leaf)
    absent = m.ABS3 | set(leaf['absent_extra'])
    inf = lp['inf_dual']
    index = {r:i for i,r in enumerate(P)}
    nrows = len(P)+2+len(inf)
    abrow, urow = len(P), len(P)+1
    cols, costs, tags = [], [], []
    for r in P:
        fmax = 40 if r < 100 else 20 if r < 400 else 10
        fs = [f for f in range(2,fmax+1,2) if check.allowed(r,f,absent)]
        fe = fmax+2
        while not check.allowed(r,fe,absent):
            fe += 2
        for f in fs+[None]:
            col = {index[r]: 1.}
            if f is None:
                cost = Decimal(fe)*m.ln_lo(r)-m.ALPHA_HI*(m.ln_hi(fe+1)/m.LN3_LO if r%3==1 else 0)
                ab = m.ln_hi(r)-m.ln_lo(r-1)
                remcost = 0.
            else:
                S = check.sigma(r,f)
                cost = Decimal(f)*m.ln_lo(r)-m.ALPHA_HI*check.valuation(S,3)
                ab = m.ln_hi(S)-Decimal(f)*m.ln_lo(r)
                rem = S
                for t in set(P)|u|{2,3}:
                    while rem%t==0:
                        rem//=t
                remcost = float((1-2*m.LN3_HI/m.ln_lo(lp['L']))*m.ln_lo(rem)) if rem>1 else 0.
            col[abrow] = -float(ab)
            col[urow] = remcost
            for j,(src,fsrc,t,v,_,_) in enumerate(inf):
                coeff = float(r==src and f==fsrc)-float(r==t and (f is None or f>=v))
                if coeff:
                    col[len(P)+2+j] = coeff
            cols.append(col)
            costs.append(float(cost))
            tags.append([r,f])
    L=lp['L']
    c=float((m.ln_hi(L)-m.ln_lo(L-1))/(2*(m.ln_lo(L)-2*m.LN3_HI)))
    cols.append({abrow:-c,urow:-1.})
    costs.append(1.)
    mat=lil_matrix((nrows,len(cols)))
    for j,col in enumerate(cols):
        for i,v in col.items():mat[i,j]=v
    rhs=np.zeros(nrows)
    rhs[:len(P)]=1.
    rhs[abrow]=-float(required)
    opt=linprog(costs,A_ub=mat.tocsr(),b_ub=rhs,bounds=[(0,1)]*(len(cols)-1)+[(0,None)],method='highs')
    assert opt.success,opt.message
    lam=-opt.ineqlin.marginals
    def rat(x):
        v=Fraction(str(max(0.,x))).limit_denominator(10**10)
        return [v.numerator,v.denominator]
    new=copy.deepcopy(lp)
    new['sel_dual']={str(r):rat(lam[i]) for r,i in index.items() if lam[i]>0}
    new['ab_dual']=rat(lam[abrow])
    new['u_dual']=rat(lam[urow])
    new['inf_dual']=[row[:4]+rat(lam[len(P)+2+j]) for j,row in enumerate(inf)]
    return new,opt.fun


def main():
    m=load_model()
    cert=json.loads((INPUT/'P3E1162Complete.json').read_text())
    leaf=cert['cell10'][9]
    assert leaf['name']=='cell10_no17_23_29_37'
    u,p=pools(leaf)
    g,ab,resab,_=m.verify_forest(leaf['forest'],m.ABS3|set(leaf['absent_extra']),sorted(p),check.primality_checker(cert['primes']))
    L=leaf['lp']['L']
    req=m.LN43_LO-ab-resab-Decimal('1e-5')-(m.ln_hi(L)-m.ln_lo(L-1))
    dual, floating=build(leaf,m,req)
    value=m.verify_lp_dual(dual,m.ABS3|set(leaf['absent_extra']),u,req)
    result={'status':'CANDIDATE_DUAL_ONLY','leaf_index':9,'name':leaf['name'],
            'lp':dual,'search_primal_nats':floating,'legacy_decimal_dual_nats':str(value),
            'forest_nats':str(g),'required_abundance_candidate':str(req),
            'accepted_actuals':[]}
    (HERE/'RebuiltDual.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('rebuilt LP digits:',value/m.LN10_HI,flush=True)


if __name__=='__main__':main()
