"""Inspect representative minimizing cells for prospective parity/abundancy/source cuts.

A floating scout witness is not a proof of all cells. In particular, any tail
state has a lower exponent bound but supplies no exact sigma to this audit.
"""
import argparse
from fractions import Fraction
from math import prod
from Scout import load,scorer,sigma,arithmetic,valuation


def audit(row):
    p,e=row['p'],row['e']; ban=(19,7) if p==11 else (19,)
    modes, trace=scorer(row,{q:w/row['den'] for q,w in row.get('rho',[])})
    labels={*row['roots'],*dict(row['owners'])}
    mode=min(modes,key=modes.get); witness=trace(mode)
    chosen={p:e,**{q:f for q,(h,f,k,w) in witness.items() if w is not False}}
    odd=next((q for q,f in chosen.items() if f%2),None)
    # This candidate row may contain merely conjecturally prime labels. The
    # structural checks below are prospective, even where exact integer arithmetic
    # is used. Parent equality in a finite state, not a lower floor, activates sigma.
    S=prod(arithmetic(q,f) for q,f in chosen.items()); X=prod(q**f for q,f in chosen.items())
    excess=[(q,f,v) for q,f in chosen.items() if (v:=valuation(S,q))>f]
    absent=[q for q in ban if S%q==0]
    balances={q:valuation(S,q) for q in labels if S%q==0}
    Q=set(chosen); I=Fraction(S*(2 if odd else 1),X); A=I; discount=Fraction(1)
    forced=[]
    for q,v in balances.items():
        if q in Q:continue
        v=max(v,witness[q][1]) if q in witness and witness[q][-1] is False and witness[q][2]!=2 else v
        def permitted(a):return all((a+1)%b if q%b==1 else pow(q,a+1,b)!=1 for b in ban)
        a=v+v%2
        while not permitted(a):a+=2
        y=Fraction(sigma(q,a),q**a); A*=y; forced.append(q)
        if odd is None and q%4==1 and all((q+1)%b for b in ban):
            c=v+(1-v)%4
            while not permitted(c):c+=4
            discount=min(discount,Fraction(sigma(q,c),q**c)/y)
    # Incoming root supply over known finite states; missing units cannot be
    # assigned solely to a displayed owner without a separate universal proof.
    source=sorted((q,f,v) for q,f in chosen.items() if q!=p and (v:=valuation(arithmetic(q,f),p)))
    return dict(p=p,e=e,mode=mode,score=round(modes[mode],9),finite=len(chosen),tail=len(witness)+1-len(chosen),Euler=odd,abundance_lower=float(A*discount),known_forced=len(forced),abundance_contradiction=A*discount>2,overfull=excess,forbidden=absent,p_sources=source,p_unfunded=e-sum(x[2] for x in source))

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('case',nargs='+'); args=a.parse_args()
    for s in args.case:
        p,e=map(int,s.split('x'));print(audit(load(p,e)))
