#!/usr/bin/env python3
"""Deterministic, restartable forced-prime exponent search for 10^2400.

No external packages. Search output is a candidate discovery log; each CLOSED
record is independently reproducible by running --verify on (p,d,q).
Only root-only shards with d+1 prime > p are scanned.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

BOUND = 10**2400
ROOT_ORDER = (19, 7, 11, 31, 13, 3, 5, 17)


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for t in range(3, math.isqrt(n) + 1, 2):
        if n % t == 0:
            return False
    return True


def forbidden_sigma_prime(q: int, exponent: int, forbidden: tuple[int, ...]) -> int | None:
    for f in forbidden:
        if ((exponent + 1) % f == 0 if q % f == 1
                else pow(q, exponent + 1, f) == 1):
            return f
    return None


def odd_part(n: int) -> int:
    return n // (n & -n)


def verify_forced_prime(p: int, d: int, exact: bool, forbidden: tuple[int, ...],
                        q: int, bound: int = BOUND) -> dict | None:
    """Return an exact, exhaustive proof trace or None when inconclusive.

    sigma(p^d)'s odd part A divides N. Each possible exact exponent e=v_q(N)
    is checked. From multiplicativity of sigma, A*odd(sigma(q^e)) divides N.
    Hence lcm(p^d*A, q^e, A*odd(sigma(q^e))) divides N.
    """
    if (p < 3 or d < 1 or q == p or q < 3 or q % 2 == 0
            or not is_prime_trial(q)):
        return None
    A = odd_part((pow(p, d+1) - 1) // (p-1))
    if A % q:
        return None
    P = pow(p, d) * A
    if P > bound:
        return None
    v, temp = 0, A
    while temp % q == 0:
        v += 1
        temp //= q
    max_e, residual = v, bound // P
    while residual >= q:
        residual //= q
        max_e += 1
    rows = []
    for e in range(v, max_e+1):
        ordinary = (e % 2 == 0)
        special = (q % 4 == 1 and e % 4 == 1 and not (exact and d % 2))
        if not ordinary and not special:
            continue
        f = forbidden_sigma_prime(q, e, forbidden)
        if f is not None:
            rows.append((e, 'FORBIDDEN_SIGMA', f))
            continue
        Sq = odd_part((pow(q, e+1)-1)//(q-1))
        necessary = math.lcm(P, pow(q, e), A*Sq)
        if necessary <= bound:
            return None
        rows.append((e, 'LCM_SIZE', necessary.bit_length()))
    if not rows:
        return None
    return {'root': p, 'exponent': d, 'exact': exact, 'forced_prime': q,
            'root_sigma_valuation': v, 'max_forced_prime_exponent': max_e,
            'cases': rows}


def exponent_ceiling(p: int) -> int:
    limit, value = 0, 1
    while value <= BOUND // p:
        value *= p
        limit += 1
    return limit


def tasks(order: tuple[int, ...]):
    for p in order:
        cap = exponent_ceiling(p)
        index = 0
        if p % 4 == 1:
            if 1 <= cap:
                yield p, index, 1, True
            index += 1
        if p == 3:
            leading, first = ((2,True),(4,True),(8,False),(14,False),(24,False)),7
        elif p == 7:
            leading, first = ((2,True),(8,False)),5
        else:
            leading, first = (),3
        for d, exact in leading:
            if d <= cap:
                yield p, index, d, exact
            index += 1
        for m in range(first, cap+2, 2):
            if is_prime_trial(m) and m-1 <= cap:
                yield p, index, m-1, False
                index += 1


def scan(args):
    started = time.monotonic()
    ck = Path(args.checkpoint)
    ck.parent.mkdir(parents=True, exist_ok=True)
    cfg = [args.prime_limit, args.residual_digits]
    status = {}
    if ck.exists():
        for line in ck.read_text(encoding='utf-8').splitlines():
            item = json.loads(line)
            if item.get('config') == cfg:
                status[item['id']] = item
    completed = found = 0
    with ck.open('a', encoding='utf-8', buffering=1) as output:
        def write(record):
            record['config'] = cfg
            output.write(json.dumps(record, separators=(',', ':')) + '\n')
        for p, index, d, exact in tasks(ROOT_ORDER):
            if args.root != 'all' and p != int(args.root):
                continue
            tid = f'P{p}_I{index:05d}'
            old = status.get(tid)
            if old and old['status'] in ('DONE','CLOSED','SKIPPED'):
                continue
            if args.hours and (time.monotonic()-started)/3600 >= args.hours:
                break
            forbidden = ROOT_ORDER[:ROOT_ORDER.index(p)]
            m = d+1
            if exact or m <= p or not is_prime_trial(m):
                write({'id':tid,'status':'SKIPPED','why':'unsupported exponent class'})
                continue
            if forbidden_sigma_prime(p,d,forbidden) is not None:
                write({'id':tid,'status':'SKIPPED','why':'direct forbidden sigma factor'})
                continue
            A = odd_part((pow(p,m)-1)//(p-1))
            P = pow(p,d)*A
            if P > BOUND:
                write({'id':tid,'status':'SKIPPED','why':'direct sigma-size'})
                continue
            R = BOUND//P
            if len(str(R)) > args.residual_digits:
                write({'id':tid,'status':'SKIPPED','why':'residual budget exceeds filter'})
                continue
            step = 2*m
            first_k = 1
            if old and old['status'] == 'PROGRESS':
                first_k = old['next_k']
            closed = None
            end_k = (args.prime_limit-1)//step
            for k in range(first_k, end_k+1):
                if args.hours and k % 1024 == 0 and (time.monotonic()-started)/3600 >= args.hours:
                    write({'id':tid,'status':'PROGRESS','next_k':k,'root':p,'exponent':d})
                    print('PAUSED_AT_LIMIT',tid,'next_k',k,flush=True)
                    return
                q = 1+step*k
                if pow(p,m,q) == 1 and is_prime_trial(q) and A % q == 0:
                    closed = verify_forced_prime(p,d,False,forbidden,q)
                    if closed:
                        break
                if k % args.checkpoint_every == 0:
                    write({'id':tid,'status':'PROGRESS','next_k':k+1,'root':p,'exponent':d})
            if closed:
                found += 1
                print('CLOSED',tid,'q',closed['forced_prime'],flush=True)
                write({'id':tid,'status':'CLOSED','proof':closed})
            else:
                write({'id':tid,'status':'DONE','root':p,'exponent':d})
            completed += 1
            if completed % 10 == 0:
                print('CHECKED',completed,'CLOSED',found,'SECONDS',round(time.monotonic()-started,1),flush=True)
    print('SUMMARY',json.dumps({'completed_this_run':completed,'closed_this_run':found,
                               'seconds':round(time.monotonic()-started,2)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--root', default='3', help='prime root or all')
    parser.add_argument('--exponent', type=int, default=2476)
    parser.add_argument('--exact', action='store_true')
    parser.add_argument('--forced-prime', type=int, default=980893)
    parser.add_argument('--prime-limit', type=int, default=2_000_000)
    parser.add_argument('--residual-digits', type=int, default=500)
    parser.add_argument('--checkpoint', default='Build/ForcedPrimeScan2400.jsonl')
    parser.add_argument('--checkpoint-every', type=int, default=20_000)
    parser.add_argument('--hours', type=float, default=0)
    args = parser.parse_args()
    if args.verify:
        p = int(args.root)
        if p not in ROOT_ORDER:
            parser.error('unknown root')
        out = verify_forced_prime(p,args.exponent,args.exact,
                                  ROOT_ORDER[:ROOT_ORDER.index(p)],args.forced_prime)
        if out is None:
            print('OPEN / INVALID',flush=True)
            raise SystemExit(1)
        print(json.dumps(out,indent=2))
    else:
        if args.prime_limit < 3 or args.prime_limit >= 2**63 or args.checkpoint_every < 1:
            parser.error('invalid scan limits')
        scan(args)


if __name__ == '__main__':
    main()
