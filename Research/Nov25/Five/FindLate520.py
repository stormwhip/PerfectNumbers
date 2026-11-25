"""Optional SciPy witness generator. Numerical output has no authority until replayed."""
import argparse
from pathlib import Path
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import json
from Late520 import model, SCALE, DYADIC, HERE, weighted, Q, P5, A, log_bounds

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True,help='new file; the tracked packet is never overwritten')
args=parser.parse_args()
if args.output.resolve()==(HERE/'Late520Dual.json').resolve():
    raise ValueError('choose a scratch path for discovery')
m=model()
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
a=weighted(m,w)+DYADIC*log_bounds(P5*A*Q)[0]
assert a>2400*DYADIC*log_bounds(10)[1]
print('exact replay floor',a//(DYADIC*log_bounds(10)[1]),flush=True)
with args.output.open('x',encoding='utf-8',newline='\n') as out:
    out.write(json.dumps({'weights':w},separators=(',',':'))+'\n')
