"""Independent, integer-only partial exclusions. Standard library; no candidate Euler bounds."""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'Candidate'))
import Check as check
sys.modules.setdefault("check",check)

B = 10**2400
CAP = B + 1
ABSENT = {7, 11, 13, 19, 31}
EXPONENTS = (856, 970, 990, 1108, 1162)


def mul(a, b):
    return min(CAP, a*b)


def power(a, n):
    assert a>=2 and n>=0
    if n > B.bit_length() or n*(a.bit_length()-1)>B.bit_length():
        return CAP
    z = 1
    while n:
        if n & 1:
            z = mul(z, a)
        a = mul(a, a)
        n //= 2
    return z


def supplier_discount(R=10000):
    # For r >= R, r^f >= (R^2)^k, since f >= 3^k-1 >= 2k.
    K = R*R
    numerator = denominator = 1
    active = 0
    for r in check.small_primes(R-1):
        if r <= 3 or r in ABSENT or r % 3 != 1:
            continue
        # If sigma(r^2) hits ABSENT, every exponent with k>=1 is forbidden.
        if not check.allowed(r, 2, ABSENT):
            continue
        best = Fraction(1)
        k = 1
        while True:
            f = 3**k-1
            candidate = Fraction(K**k, r**f)
            if candidate <= 1:
                # f/k strictly increases, so all subsequent ratios are <=1.
                break
            if check.allowed(r, f, ABSENT):
                best = max(best, candidate)
            else:
                # sigma(r^(3^k-1)) divides sigma(r^h) whenever v3(h+1)>=k.
                break
            k += 1
        if best > 1:
            active += 1
            numerator *= best.numerator
            denominator *= best.denominator
    return K, numerator, denominator, active


def run():
    assert check.prime64(43)
    # Explicitly exclude every candidate supplier below 43.
    for r in check.small_primes(42):
        if r > 3 and r % 3 == 1 and r not in ABSENT:
            assert not check.allowed(r, 2, ABSENT)
    K, dn, dd, active = supplier_discount()
    rows = []
    for e in EXPONENTS:
        assert check.prime64(e+1)
        root = 3**e
        assert root * 43**(2*e) > B
        # E1, q == 1 mod 3; q >= 37, a >= max(5,3^s-1).
        # E1, q == 2 mod 3; s=v3(q+1)+v3((a+1)/2), q>=2*3^s1-1.
        checked = 0
        worst = CAP
        threes=[3**j for j in range(e+1)]
        ordinary_table=[power(43,2*j) for j in range(e+1)]
        for s in range(1, e+1):
            ordinary = ordinary_table[e-s]
            a = max(5, threes[s]-1)
            bound = mul(root, mul(power(37, a), ordinary))
            assert bound > B, ('E1/q1', e, s)
            worst = min(worst, bound)
            for s2 in range(s+1):
                q = max(5, 2*threes[s-s2]-1)
                a = max(5, 2*threes[s2]-1)
                bound = mul(root, mul(power(q, a), ordinary))
                assert bound > B, ('E1/q2', e, s, s2)
                checked += 1
                worst = min(worst, bound)
        # E2: q|A => s<=e/2, hence ordinary supply U>=e/2.
        # O >= K^U / (dn/dd); omit q and A to retain disjointness.
        left = root * K**(e//2) * dd
        assert left > B * dn, ('E2', e)
        # Provide reproducible integer decimal floors without logarithms.
        def decimal_floor(n, d=1):
            lo, hi = 0, 10000
            while lo+1 < hi:
                mid = (lo+hi)//2
                if n >= d*10**mid:
                    lo = mid
                else:
                    hi = mid
            return lo
        row = {'e': e, 'E0_log10_floor': decimal_floor(root*43**(2*e)),
               'E1': 'EXCLUDED_BY_EXACT_INTEGER_COMPARISONS',
               'E1_q2_cases': checked, 'E2_log10_floor': decimal_floor(left,dn),
               'remaining': 'a=1, q does not divide A; E3 UNRESOLVED'}
        # If b=v3(sigma(r^f))>=1, q==2 mod 3 permits removing all factors
        # 3 from f+1: q|sigma(r^(m-1)), f+1=3^b*m. Consequently
        # r^f > (2q/3)^3 and N > (8/27)*3^e*q^4.
        cutoff=next((s for s in range(1,e+1)
                     if 8*root*(2*3**s-1)**4>27*B),None)
        row['source_b_positive_excluded_when_s_at_least']=cutoff
        rows.append(row)
        print(row, flush=True)
    result = {'status': 'VERIFIED_PARTIAL_ONLY', 'accepted_actuals': [],
              'supplier_dual_K': K, 'supplier_discount_active_primes': active,
              'supplier_discount_numerator': str(dn), 'supplier_discount_denominator': str(dd),
              'rows': rows}
    (HERE/'PartialResults.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    if not __debug__:raise SystemExit('Assertions must be enabled')
    run()
