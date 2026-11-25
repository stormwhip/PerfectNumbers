"""All root (5,520) Euler cases before the separate late terminal dual."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
for path in (R/'NightFive', R/'NightFiveReview'):
    sys.path.insert(0, str(path))
from PaidCheck import root, load_duals, I
from LocalModel import Bank, LIMIT, SCALE, primes, lo, hi, ab, iroot

E, S0, T = 520, 445, 100000
P = 5**(E+1)
PE = P//5
A = (P-1)//4
B = 10**2400


def independent():
    bank = json.loads((I.CERT_DIR/'DualP5.json').read_bytes())
    ps = primes(bank['R_act'])
    d = [Bank(x,bank['R_act'],ps) for x in bank['duals']]
    n = iroot(A,T)
    assert all(A % p for p in primes(T))
    assert all(A % p for dv in d for p in dv.th)
    J = iroot(iroot(B,3)+1,5)
    assert J == 5
    abundance = lo(2)-ab(5)-n*ab(T)
    coeff = [(v, min(v.lam*lo(5),4*lo(T))) for v in d]
    fees = [(v,L,lo(PE*A)+v.mu*abundance+v.C-(n*L+3)//4) for v,L in coeff]
    # Internal Euler: A=qC forces 4C=1 mod 5^v_5(q+1), hence
    # v_5(q+1) <= E//2; its exact exponent supplies at most J more.
    assert max(b+L*(E-E//2-J) for _,L,b in fees)>LIMIT
    closed = {'high':0,'direct':0,'source':0,'paid_checks':0}
    for s in range(E+1):
        Y = 5**s
        Q = max(5,2*Y-1)
        qcost = lo(Q)
        k = E-s
        assert max(b+L*k+max(lo(3125),max(0,5*s-5)*lo(5))-v.dq
                   for v,L,b in fees)>LIMIT
        closed['high']+=1
        if s>=S0:
            continue
        def reduce(v):
            return min(v.dq,v.mu*ab(Q)) if Q>10**18 else v.dq
        staged = [(v,L,b+L*k-reduce(v)) for v,L,b in fees]
        if max(b+qcost for _, _, b in staged)>LIMIT:
            closed['direct']+=1
            continue
        assert s>0
        # Independent, directed evaluation of the internal emitter gap;
        # main NightFive replay uses truncated integer logarithms.
        unit = qcost+lo(2)-hi(3)
        assert max(b+qcost+unit-v.de for v,L,b in staged)>LIMIT
        gap = lo(Q*Q*Y)-hi(max(P,Q)*(P//Y+4))
        assert max(b+gap for _,_,b in staged)>LIMIT
        closed['source']+=1
        if 32*PE*Q**6<243*B:
            assert Q>I.MAX_EXPONENT+1
            for j in range(1,min(J,k)+1):
                paid = qcost+5**j*unit
                assert max(b-L*j+paid-v.de for v,L,b in staged)>LIMIT
                assert max(b-L*j+paid-hi(A) for v,L,b in staged)>LIMIT
                closed['paid_checks']+=1
    return closed


def verify(verbose=False):
    if not __debug__:
        raise ValueError('requires assertions; no -O')
    p = I.sieve_primes(T)
    assert all(A%z for z in p)
    row = root(E,[],p,T,load_duals())
    assert row['known'] and row['rough'] and row['higher']==[] and row['forced']==[]
    assert row['one'] == [[S0,E]]
    closed = independent()
    assert closed['direct']+closed['source']==S0
    if verbose:
        print('early/internal/high Euler:',closed,'remaining a=1 windows',row['one'])
    return closed


if __name__=='__main__':
    verify(verbose=True)
