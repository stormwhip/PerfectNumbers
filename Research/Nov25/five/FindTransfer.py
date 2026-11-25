"""Discover an exact conditional terminal dual per root-3 late Euler case."""
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import json
from TerminalTransfer import model, SCALE, DYADIC, HERE, weighted, sigma, log_bounds


def find(root,exponent,s0,extra_forbidden=(),verify_all=True):
    m=model(root,exponent,s0,verify_all=verify_all,extra_forbidden=extra_forbidden)
    C, rows, groups, tail, _ = m
    rr=[];cc=[];vv=[];rhs=[]
    for i,(terms,b) in enumerate(rows):
        rhs.append(b/SCALE)
        for j,v in terms:
            rr.append(i);cc.append(j);vv.append(v/SCALE)
    sol=linprog([c/SCALE for c in C], A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rows),len(C))).tocsr(), b_ub=rhs,
                bounds=[(0,None) if j==tail else (0,1) for j in range(len(C))],method='highs')
    assert sol.success,sol.message
    w=[max(0,round(-v*DYADIC)) for v in sol.ineqlin.marginals]
    w[0]=min(w[0],C[tail]*DYADIC//SCALE)
    w=[[i,v] for i,v in enumerate(w) if v]
    mant=root**exponent*sigma(root,exponent)*(2*root**s0-1)
    a=weighted(m,w)+DYADIC*log_bounds(mant)[0]
    b=log_bounds(10)[1]*DYADIC
    print('conditional terminal floor',root,exponent,s0,a//b,'micro',a*10**6//b,flush=True)
    return dict(root=root,exponent=exponent,s0=s0,weights=w) if a>2400*b else None


if __name__=='__main__':
    jobs=((1162,1055),(1108,928),(990,787),(970,763),(856,629))
    rows=[]
    for e,s in jobs:
        try:
            row=find(3,e,s)
        except ValueError as ex:
            print(e,str(ex),flush=True)
            continue
        if row:
            rows.append(row)
            (HERE/'TransferDual.json').write_text(json.dumps({'rows':rows},separators=(',',':'))+'\n',encoding='utf-8')
