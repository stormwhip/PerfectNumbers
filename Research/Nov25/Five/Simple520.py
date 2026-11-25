"""Independent simpler covering argument for (5,520), with no Euler emitter lemma."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from Early520 import E, T, PE, A, B, I, Bank, LIMIT, primes, lo, ab, iroot, load_duals
from Late520 import verify as late
from Verify520 import decimal_logs
from DualTree import abhi, lnlo, LP

S0 = 300


def margins(rows, log_low, ab_high, limit):
    # For q | A the already charged q^c must not be charged again. Euler
    # supply is <=260+5: see proof below. Any residual Euler q-power cost is ignored.
    assert max(base+L*(E-E//2-5) for base,L,mu,dq in rows)>limit
    for s in range(E+1):
        Q = max(5,2*5**s-1)
        k = E-s
        # High Euler q^a, a>=5: q^a>=5^5 and q^a>=5^{5s-5}.
        # q=1 mod 5 has s=v5(a+1), hence a>=5^s-1. q=-1 mod 5
        # has s=t+j with t=v5(q+1)>=1, j=v5(a+1), and q>=5^t.
        # For j<=1, at>=5t>=5s-5. For j>=2, a-5>=5^j-6>=5j-5.
        # The remaining residue classes cannot supply 5 because a+1 is 2 mod 4.
        assert max(base+L*k+max(log_low(3125),max(0,5*s-5)*log_low(5))-dq
                   for base,L,mu,dq in rows)>limit
        if s<S0:
            # q is outside A. For s>=1, Q follows from q+1 even and 5^s|q+1.
            assert max(base+L*k+log_low(Q)-(min(dq,mu*ab_high(Q)) if Q>10**18 else dq)
                       for base,L,mu,dq in rows)>limit


def verify(verbose=False):
    if not __debug__:
        raise ValueError('requires assertions; no -O')
    # q|A forces 4(A/q)≡1 mod 5^t for t=v5(q+1), capped by
    # t≤E because σ(q^a) already supplies t≤E. A/q >= (5^t+1)/4
    # and q >=2*5^t-1 imply 2t≤E by 4A =5^(E+1)-1.
    # Also a≤log_5 B and so v5(a+1)≤5, proving the 265 cap.
    assert 5**6>I.MAX_EXPONENT+1
    assert (2*5**(E//2+1)-1)*(5**(E//2+1)+1)>4*A
    p = I.sieve_primes(T)
    assert all(A%z for z in p) and A%2==1
    n = I.ilog(A,T); target=I.LN2_LO-abhi(5)-n*abhi(T)
    rows=[]
    for d in load_duals():
        assert all(A%z for z in d.theta_map)
        L=min(d.lam_p*LP,4*lnlo(T))
        base=lnlo(PE*A)+d.mu*target+d.const_no_target-(n*L+3)//4
        rows.append((base,L,d.mu,d.delta_q))
    margins(rows,lnlo,abhi,I.LN_B_HI)

    raw=json.loads((I.CERT_DIR/'DualP5.json').read_bytes())
    p0=primes(raw['R_act']); n=iroot(A,T); target=lo(2)-ab(5)-n*ab(T)
    rows=[]
    for entry in raw['duals']:
        d=Bank(entry,raw['R_act'],p0)
        assert all(A%z for z in d.th)
        L=min(d.lam*lo(5),4*lo(T))
        rows.append((lo(PE*A)+d.mu*target+d.C-(n*L+3)//4,L,d.mu,d.dq))
    margins(rows,lo,ab,LIMIT)
    if verbose:
        print(f'closed internal Euler, {E+1} external high-Euler cells, and {S0} external first-power cells by direct inequalities')
    Q=2*5**S0-1
    late(verbose=verbose,lower_q=Q)
    late(verbose=verbose,logs=decimal_logs,verify_all=False,lower_q=Q)
    return {(5,E)}


if __name__=='__main__':
    verify(verbose=True)
