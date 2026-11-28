"""Exact local cuts. Recomputes each underlying divisor and integer comparison."""
from Prices import *
from CleanPrice import price2
from Emitters import certificate,inside_euler,first_not_rejected
from Explore import CASES
from hashlib import sha256
from sys import argv

def no_other_anchor(rows,r,h):
    # Checks normalization after adding an exact ordinary -> all budgets not
    # merely final lower mass. The caller authenticates the prime r if needed.
    fixed,odd,X,S,D,_=get_context(rows)
    Z=sig(r,h);T=S*Z;Y=X*r**h
    return gcd(Z,prod(BAN))!=1 or any(vp(T,p)>k for p,k in (*rows,(r,h))) or Y*(T//gcd(Y,T))>B

def fixed_tradeoff(k):
    rows=CASES[k];R,fixed,odd,X,S,D,spec=certificate(rows);p=rows[-1][0]
    assert odd==1 and len(spec)==1
    V,E=price2(rows,p);C=V*D**2/B;c=fixed[p]-vp(S,p)
    # D=square*S0, where S0 is its squarefree kernel, S0>=R.
    # If b is supplied by sources dividing D then N >=(V/X)*X D²/square /p^(2b).
    bmin=next((b for b in range(c+1) if F(D,R)*p**(2*b)>=C),c+1)
    squarefree_bmin=next((b for b in range(c+1) if p**(2*b)>=C),c+1)
    print(k,'fixed-Euler','V',floor10(V),'losses',len(E),'C',floor10(C),'bmin',bmin,'squarefree bmin',squarefree_bmin,flush=True)
    return bmin,squarefree_bmin

def free_high(k):
    rows=CASES[k];R,fixed,odd,X,S,D,spec=certificate(rows);p=rows[-1][0]
    assert odd==0 and len(spec)==1
    V,E=price2(rows,p);print(k,'Euler-high',V>B,'V',floor10(V),'losses',len(E),flush=True)
    C=V*D**2/B;c=fixed[p]-vp(S,p)
    bmin=next((b for b in range(c+1) if F(D,R)*p**(2*b)>=C),c+1)
    print(k,'all exponents >=2, Euler exterior required internal source units',bmin,flush=True)
    return (V>B,bmin)
if __name__=='__main__':
    for k in argv[1:] or ('6-2-150','6-256','12-1-108','12-1-102','12-96'):
        if k.startswith('12-1-'):fixed_tradeoff(k)
        else:free_high(k)
