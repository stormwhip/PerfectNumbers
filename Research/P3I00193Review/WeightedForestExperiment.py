"""Conditional Lagrangian forest experiment: charge inactive nodes for abundance.

Uses the legacy Decimal enclosures and conditional external-volume allocation.
No mathematical acceptance is emitted.
"""
import json
import copy
import sys
from decimal import Decimal as D
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ReplayCandidate import HERE,INPUT,load_model,pools
import check


def solve(leaf,m):
    u,p=pools(leaf);forest=leaf['forest'];lp=leaf['lp'];L=lp['L']
    absent=m.ABS3|set(leaf['absent_extra']);lam=m.frac_dec(*lp['ab_dual'])
    strip=u|p|{2,3};options={};optional={}
    def cost(r,f):
        v=check.valuation(f+1,3) if r%3==1 else 0
        return D(f)*m.ln_lo(r)-m.ALPHA_HI*v
    def abundance(r,f=None):
        return m.ln_hi(r)-m.ln_lo(r-1) if f is None else m.ln_hi(check.sigma(r,f))-D(f)*m.ln_lo(r)
    def tail(r,f):
        v=m.ln_hi(f+1)/m.LN3_LO if r%3==1 else D(0)
        return D(f)*m.ln_lo(r)-m.ALPHA_HI*v-lam*abundance(r)
    def residual(n):
        for t in strip:
            while n%t==0:n//=t
        value=D(0);ab=D(0)
        for q in m.SMALL_P_50K:
            if q*q>n:break
            if n%q==0:
                v=check.valuation(n,q);n//=q**v
                value+=v*(m.ln_lo(q)-(2*m.LN3_HI if q%3==1 else 0))
                ab+=m.ln_hi(q)-m.ln_lo(q-1)
        if n>1:
            if n<50000:
                value+=m.ln_lo(n)-(2*m.LN3_HI if n%3==1 else 0)
                ab+=m.ln_hi(n)-m.ln_lo(n-1)
            else:value+=(1-2*m.LN3_HI/m.ln_lo(50000))*m.ln_lo(n)
        return value-lam*ab
    for r in u:
        cut=forest['cut_even'][str(r)]
        fs=[f for f in range(2,cut,2) if check.allowed(r,f,absent)]
        fe=cut
        while not check.allowed(r,fe,absent):fe+=2
        options[r]=(fs,fe)
        optional[r]=min([D(0),tail(r,fe)]+[cost(r,f)-lam*abundance(r,f) for f in fs])
    memo={}
    def dp(r,minimum):
        key=(r,minimum)
        if key in memo:return memo[key]
        fs,fe=options[r];ft=max(fe,minimum+(minimum%2))
        best=tail(r,ft)-optional[r]
        for f in fs:
            if f<minimum:continue
            S=check.sigma(r,f)
            value=cost(r,f)-lam*abundance(r,f)-optional[r]+residual(S)
            for child in forest['edges'].get(str(r),[]):
                if S%child==0:value+=dp(child,check.valuation(S,child))
            best=min(best,value)
        memo[key]=best;return best
    weighted=sum(optional.values(),D(0))+sum((dp(r,2) for r in forest['roots']),D(0))
    large_ab=(m.ln_hi(50000)-m.ln_lo(49999))/(2*m.ln_lo(50000))*m.TARGET_NATS_HI
    req=m.LN43_LO-large_ab-D('1e-5')-(m.ln_hi(L)-m.ln_lo(L-1))
    other=m.verify_lp_dual(lp,absent,u,req)
    return {'name':leaf['name'],'weighted_net_plus_lp_digits_candidate':str((weighted+other)/m.LN10_HI),
            'optional_nodes_with_negative_reduced_cost':sum(v<0 for v in optional.values())}


def main():
    c=json.loads((INPUT/'P3E1162Complete.json').read_text());m=load_model();rows=[]
    for i in [0,2,3,4,8,9,12]:
        leaf=(c['cell10']+c['cell11'])[i]
        row=solve(leaf,m);row['best_multiplier_scale']=[1,1]
        if i in [4,8,9]:
            for numerator in range(1,10):
                trial=copy.deepcopy(leaf);lp=trial['lp'];scale=Fraction(numerator,10)
                def scaled(pair):
                    f=Fraction(*pair)*scale
                    return [f.numerator,f.denominator]
                lp['sel_dual']={r:scaled(pair) for r,pair in lp['sel_dual'].items()}
                for name in ['ab_dual','u_dual']:lp[name]=scaled(lp[name])
                lp['inf_dual']=[item[:4]+scaled(item[4:]) for item in lp['inf_dual']]
                candidate=solve(trial,m)
                if D(candidate['weighted_net_plus_lp_digits_candidate'])>D(row['weighted_net_plus_lp_digits_candidate']):
                    row=candidate;row['best_multiplier_scale']=[numerator,10]
        row['leaf_index']=i;rows.append(row);print(row,flush=True)
    (HERE/'WeightedForestResults.json').write_text(json.dumps({'status':'CONDITIONAL_WEIGHTED_FOREST_ONLY','accepted_actuals':[],'rows':rows},indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
