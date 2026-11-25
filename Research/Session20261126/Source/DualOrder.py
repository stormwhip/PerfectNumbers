"""Two-sided order sieve: count source-valuation cells forcing a small exact exponent.
The base subdomain is E3 (q,+1; external to A; s>=1). No high-Euler claim.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from OtherRoots import floorcut,B,S,j

def sigma(r,f):return (r**(f+1)-1)//(r-1)

def inv_sigma(p,e,b,s,external):
    # Suppose p does not divide f+1 but source has positive b and d=ord_p r
    # is a proper divisor of f+1. Then p^b divides sigma(r^(d-1)).
    Q=2*p**s-1; Y=p**b; A=sigma(p,e);P=p**e
    # Both q and p^b divide sigma(r^f); they are coprime.
    F=max((2*Q*Y)//3, 9*(2*Y)**3//27)
    cost=P*Q*F
    square=(P//Y)*F**2
    if external:cost*=A;square*=A
    return max(cost,square)>B

def direct(p,e,b,s,external):
    Q=2*p**s-1;Y=p**b;P=p**e;A=sigma(p,e);F=(2*Q*Y)//3
    return max(P*Q*F,(P//Y)*F**2)*(A if external else 1)>B

def group(p,e,ext):
    s0=floorcut(p,e,p,ext);pr=floorcut(p,e,3,ext)
    # Starting where both restrictions hold isolates small double-primitive sources.
    if pr is None:return None
    s0=max(s0,pr)
    nforced=0;examples=[];windows=[]
    for s in range(s0,e):
        # Search positive b. Both inequalities in inv_sigma increase in b after
        # dividing by p^b: F=max(c1*p^b,c2*p^(3b)), with floors. Direct
        # floating-free scan below uses no assumed monotonicity at endpoints.
        # To avoid repeated exponentiation, compute and cache powers.
        hits=[]; q=2*p**s-1;P=p**e;X=sigma(p,e) if ext else 1;Y=1
        for b in range(1,e-s+1):
            Y*=p; F=(2*q*Y)//3
            if max(P*q*F,(P//Y)*F**2)*X>B:continue
            F=max(F,9*(2*Y)**3//27)
            if max(P*q*F,(P//Y)*F**2)*X>B:hits.append(b)
        if hits:
            assert hits==list(range(hits[0],hits[-1]+1))
            nforced+=len(hits);windows.append([s,hits[0],hits[-1]])
    nlist=[o for o in range(3,p,2) if (p-1)%o==0]
    return dict(s_min=s0,ordinary_exponents=[o-1 for o in nlist],forced_cells=nforced,windows=windows)

if __name__=='__main__':
    assert __debug__
    report=[]
    for p in (7,11,13,19,31):
        e=max(e for rr in j['remaining_shards'] if rr['root']==p for e in rr['remaining_actuals'])
        report.append(dict(p=p,e=e,all_sources=group(p,e,False),outside_A=group(p,e,True)))
    print(json.dumps(dict(status='CONDITIONAL_ONLY',accepted_actuals=[],report=report),separators=(',',':')))
