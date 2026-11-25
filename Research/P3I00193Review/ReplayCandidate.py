"""Diagnostic replay only. Never emits an accepted exponent or modifies a ledger."""
import argparse
import hashlib
import json
import sys
import time
from functools import cache
from decimal import Decimal
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'Candidate'
sys.path.insert(0, str(INPUT))
import Check as check
sys.modules.setdefault("check",check)


def load_model():
    source = (INPUT / 'VerifyP31162.py').read_text(encoding='utf-8')
    source = source.replace('def ln_lo(x):', '@cache\ndef ln_lo(x):')
    source = source.replace('def ln_hi(x):', '@cache\ndef ln_hi(x):')
    source = source.replace('    def extra_ord_full(U):', '    @cache\n    def extra_ord_full(U):')
    source = source.replace('q % 3 == 2 or (vq == 1 and q >= 81)', 'q % 3 == 2')
    source = source.replace('tmp % 3 == 2 or tmp >= 81', 'tmp % 3 == 2')
    # Necessary r^f*q <= C replaces the stronger, unjustified r^f*sigma(r^f) <= C.
    source = source.replace('pow(r, f_hi) * check.sigma(r, f_hi)', 'pow(r, f_hi) * S_min')
    source = source.replace('pow(r, f) * S > B_rem', 'pow(r, f) * S_min > B_rem')
    source = source.replace('float(ln_hi(B_rem)) / (2.0 * lr)', 'float(ln_hi(B_rem // S_min)) / lr')
    source = source.replace('if S < min_q[idx]:', 'if S < min_q[idx] or pow(r, f) * min_q[idx] > B_rem:')
    scope = {'__name__': 'candidate_diagnostic', '__file__': str(INPUT / 'VerifyP31162.py'), 'cache': cache}
    exec(compile(source, scope['__file__'], 'exec'), scope)
    return type('Model', (), scope)


def pools(leaf):
    forest = leaf['forest']
    u = set(forest['roots']) if forest else set()
    if forest:
        for children in forest['edges'].values():
            u.update(children)
    return u, set(leaf['lp']['P']) if leaf['lp'] else set()


def residuals(leaf):
    u, p = pools(leaf)
    strip = u | p | {2, 3}
    absent = {7, 11, 13, 19, 31} | set(leaf['absent_extra'])
    rows = []
    options = []
    if leaf['forest']:
        options += [('forest', int(r), f) for r, cut in leaf['forest']['cut_even'].items()
                    for f in range(2, cut, 2)]
    if leaf['lp']:
        options += [('lp', r, f) for r in p for f in range(2, (40 if r < 100 else 20 if r < 400 else 10) + 1, 2)]
    for kind, r, f in options:
        if not check.allowed(r, f, absent):
            continue
        n = check.sigma(r, f)
        for t in strip:
            while n % t == 0:
                n //= t
        if n > 1:
            rows.append((kind, r, f, n))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=HERE / 'ReplayResults.json')
    ap.add_argument('--skip-source', action='store_true', help='Leaf diagnostics only; source check explicitly unverified')
    args = ap.parse_args()
    start = time.monotonic()
    m = load_model()
    cert = json.loads((INPUT / 'P3E1162Complete.json').read_text())
    prime = check.primality_checker(cert['primes'])
    assert all(prime(int(n)) for n in cert['primes'])
    print('166 primality certificates verified', flush=True)
    m.verify_trial_division_A(cert['R_A'], cert['R_A_all'])
    print('A trial divisions verified', flush=True)
    bounds = m.verify_euler_bounds(1162, cert['R_A'])
    print('candidate Euler bounds computed', flush=True)
    base = min(bounds[3:5])
    m.verify_partition(cert['cell10'], [], [5], [17, 23, 29, 37, 41])
    split = [17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157]
    m.verify_partition(cert['cell11'], [5], [], split)
    leaves = cert['cell10'] + cert['cell11']
    aux = set().union(*(set.union(*pools(lf)) for lf in leaves))
    # Also test every possible residual prime below the forest trial-division limit.
    expanded = aux | {r for r in check.small_primes(50000) if r > 3 and r not in m.ABS3}
    if not args.skip_source:
        m.verify_not_euler_source(expanded, bounds[5], 1162)
        print('expanded source pool verified:',len(expanded),flush=True)
    A = check.sigma(3, 1162)
    output = {'status': 'DIAGNOSTIC_MATH_PENDING', 'accepted_actuals': [],
              'primality_certificates': len(cert['primes']), 'partition_leaves': len(leaves),
              'source_primes_original': len(aux), 'source_primes_expanded': len(expanded),
              'source_enumeration_verified': not args.skip_source,
              's_min_candidate': bounds[5], 'leaves': [], 'residual_A_collisions': [],
              'frozen_hash_convention': 'LF-normalized SHA-256',
              'frozen': {name: hashlib.sha256((HERE.parent / 'Midday' / name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
                         for name in ['Registry.json', 'Delta.json']}}
    for index, leaf in enumerate(leaves):
        u, p = pools(leaf)
        absent = m.ABS3 | set(leaf['absent_extra'])
        g, ab, resab, _ = m.verify_forest(leaf['forest'], absent, sorted(p), prime) if leaf['forest'] else (Decimal(0),)*3 + (set(),)
        lp = Decimal(0)
        safe_ab_lp = Decimal(0)
        all_u_ab = sum((m.ln_hi(r)-m.ln_lo(r-1) for r in u), Decimal(0))
        if leaf['lp']:
            L = leaf['lp']['L']
            req = m.LN43_LO - ab - resab - Decimal('1e-5') - (m.ln_hi(L)-m.ln_lo(L-1))
            lp = m.verify_lp_dual(leaf['lp'], absent, u, req)
            req_all = req + ab - all_u_ab
            safe_ab_lp = m.verify_lp_dual(leaf['lp'], absent, u, req_all)
        rr = residuals(leaf)
        for kind, r, f, rem in rr:
            d = gcd(rem, A)
            if d > 1:
                output['residual_A_collisions'].append([index, kind, r, f, str(d)])
        row = {'index': index, 'name': leaf['name'], 'forest_digits': str(g/m.LN10_HI),
               'lp_digits': str(lp/m.LN10_HI), 'total_digits': str((base+g+lp)/m.LN10_HI),
               'all_forest_support_abundance_digits': str((base+g+safe_ab_lp)/m.LN10_HI),
               'active_abundance_upper': str(ab), 'all_forest_abundance_upper': str(all_u_ab),
               'residual_options': len(rr)}
        output['leaves'].append(row)
        print(index, leaf['name'], row['total_digits'][:18], flush=True)
    output['elapsed_seconds'] = round(time.monotonic()-start, 3)
    args.output.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print('DIAGNOSTIC ONLY; accepted_actuals=[]', flush=True)


if __name__ == '__main__':
    main()
