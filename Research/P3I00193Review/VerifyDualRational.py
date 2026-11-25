"""Exact rational reduced-cost checking with enclosed, correctly rounded Decimal logarithms.

Certifies a numerical dual of the stated relaxation, conditional on its abundance
and external-volume inequalities. This does not certify the forest/LP decomposition.
"""
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import cache
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ReplayCandidate import HERE, INPUT, pools
import check


@cache
def logs(n):
    assert type(n) is int and n > 0
    with localcontext() as ctx:
        ctx.prec=80
        # Decimal.ln is correctly rounded ROUND_HALF_EVEN. Adjacent decimal
        # numbers enclose the real logarithm. All subsequent arithmetic is rational.
        v=Decimal(n).ln()
        return F(v.next_minus()),F(v.next_plus())


def verify(lp, absent, forest, required):
    P=lp['P']; ps=set(P); L=lp['L']
    assert len(ps)==len(P) and ps.isdisjoint(absent|forest|{2,3})
    assert all(check.prime64(r) for r in P)
    assert L==next(r for r in check.small_primes(50000) if r not in ps|absent|forest|{2,3})
    assert L>9, 'positive external net-cost coefficient required'
    l3,h3=logs(3)
    c=(logs(L)[1]-logs(L-1)[0])/(2*(logs(L)[0]-2*h3))
    sel={int(r):F(*v) for r,v in lp['sel_dual'].items()}
    ab,u=F(*lp['ab_dual']),F(*lp['u_dual'])
    assert ab>=0 and u>=0 and all(r in ps and v>=0 for r,v in sel.items())
    inflow=lp['inf_dual']
    for src,f,t,v,n,d in inflow:
        assert src in ps and t in ps and n>=0 and d>0
        assert check.valuation(check.sigma(src,f),t)>=v
    ext_rc=1-ab*c-u
    assert ext_rc>=0, 'unbounded external-volume column rejected'
    penalty=F(0); count=0
    for r in P:
        fmax=40 if r<100 else 20 if r<400 else 10
        opts=[f for f in range(2,fmax+1,2) if check.allowed(r,f,absent)]
        fe=fmax+2
        while not check.allowed(r,fe,absent):fe+=2
        for f in opts+[None]:
            if f is None:
                vbound=logs(fe+1)[1]/l3 if r%3==1 else F(0)
                cost=fe*logs(r)[0]-4*h3*vbound
                abundance=logs(r)[1]-logs(r-1)[0]
                volume=F(0)
            else:
                S=check.sigma(r,f)
                cost=f*logs(r)[0]-4*h3*check.valuation(S,3)
                abundance=logs(S)[1]-f*logs(r)[0]
                rem=S
                for t in ps|forest|{2,3}:
                    while rem%t==0:rem//=t
                volume=(1-2*h3/logs(L)[0])*logs(rem)[0] if rem>1 else F(0)
            rc=cost+sel.get(r,F(0))-ab*abundance+u*volume
            for src,fs,t,v,n,d in inflow:
                val=F(n,d)
                if r==src and f==fs:rc+=val
                if r==t and (f is None or f>=v):rc-=val
            penalty+=min(F(0),rc)
            count+=1
    value=-sum(sel.values(),F(0))+ab*required+penalty
    return value,ext_rc,count


def run():
    cert=json.loads((INPUT/'P3E1162Complete.json').read_text())
    new=json.loads((HERE/'RebuiltDual.json').read_text())
    leaf=cert['cell10'][new['leaf_index']]
    forest,_=pools(leaf)
    req=F(new['required_abundance_candidate'])
    value,rc,count=verify(new['lp'],{7,11,13,19,31}|set(leaf['absent_extra']),forest,req)
    digits=value/logs(10)[1]
    floor10=digits.numerator*10**10//digits.denominator
    result={'status':'EXACT_RATIONAL_DUAL_CONDITIONAL_MODEL', 'accepted_actuals':[],
            'checked_bounded_columns':count,'lp_digits_lower_decimal':f'{floor10//10**10}.{floor10%10**10:010}',
            'external_reduced_cost_numerator':str(rc.numerator),
            'external_reduced_cost_denominator':str(rc.denominator),
            'required_abundance_rational':[str(req.numerator),str(req.denominator)],
            'dual_lower_nats_rational':[str(value.numerator),str(value.denominator)]}
    assert digits>F(1694957938419,10**10)
    (HERE/'RationalDualResults.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'],result['lp_digits_lower_decimal'],count)


if __name__=='__main__':
    if not __debug__:raise SystemExit('Assertions must be enabled')
    run()
