"""Exact checks on every explicit forest/LP remainder; unknown source overlap is retained."""
import hashlib
import json
import sys
from math import gcd
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ReplayCandidate import HERE,INPUT,residuals
import check


def run():
    cert=json.loads((INPUT/'P3E1162Complete.json').read_text())
    A=check.sigma(3,1162);Q=2*3**1067-1
    rows=[];collisions=[];large=[]
    for i,leaf in enumerate(cert['cell10']+cert['cell11']):
        rr=residuals(leaf)
        for kind,r,f,n in rr:
            d=gcd(n,A)
            if d>1:collisions.append([i,kind,r,f,str(d)])
            if n>=Q:large.append([i,kind,r,f,str(n)])
        rows.append({'index':i,'name':leaf['name'],'options':len(rr),
                     'max_remainder':str(max((n for *_,n in rr),default=1))})
    leaf=cert['cell10'][0]
    rr={(kind,r,f):n for kind,r,f,n in residuals(leaf)}
    x,y=rr['forest',17,20],rr['lp',499,6]
    assert (x,y,gcd(x,y))==(12754929700003,15469435877248501,13567)
    out={'status':'EXACT_REMAINDER_AUDIT_PARTIAL','accepted_actuals':[],
         'leaves':rows,'A_collisions':collisions,'remainders_not_below_Q_min':large,
         'shared_factor_witness':{'forest':[17,20,str(x)],'lp':[499,6,str(y)],'gcd':13567},
         'source_overlap':'Large unknown residual factors require source exclusion or a joint source charge.'}
    (HERE/'ResidualResults.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('42 leaves;',sum(r['options'] for r in rows),'remainders; A collisions',len(collisions),'; remainder >= Q',len(large))


if __name__=='__main__':run()
