"""Generate and independently verify a rational terminal-LP certificate."""

import argparse
from functools import lru_cache
import gzip
import json
from math import gcd
from pathlib import Path

from RoadblockDual import SCALE, log_bounds, odd_primes

DYADIC = 1 << 24
ORIGINAL = (3, 5, 7, 11, 13, 17, 19, 31)
REPLACEMENT = (3, 5, 7, 11, 13, 17, 23, 31)


def allowed(p, e, forbidden):
    # Modular geometric sum, including the case p=1 modulo r.
    return all((e + 1) % r if p % r == 1 else
               (pow(p, e + 1, r) - 1) % r for r in forbidden)


def sigma(p, e):
    return (p ** (e + 1) - 1) // (p - 1)


def build_model(roots, limit, cutoff, edges):
    forbidden = set(roots)
    base = set(odd_primes(limit)) - forbidden
    options = {}
    costs = []
    abundances = []
    specials = []
    implications = []

    def add(p, e, special, exact):
        loglo = log_bounds(p)[0]
        abhi = (log_bounds(sigma(p, e), p**e)[1] if exact
                else log_bounds(p, p - 1)[1])
        i = len(costs)
        costs.append(e * loglo)
        abundances.append(abhi)
        if special:
            specials.append(i)
        options.setdefault(p, []).append((i, e, special, exact))

    for p in sorted(base | {q for _, _, q, _ in edges}):
        for first, step, special in ((2, 2, False), (1, 4, True)):
            if special and (p % 4 != 1 or not allowed(p, 1, forbidden)):
                continue
            stop = cutoff if p in base else 0
            for e in range(first, stop + 1, step):
                if allowed(p, e, forbidden):
                    add(p, e, special, True)
            e = first + step * max(0, (stop - first) // step + 1)
            while not allowed(p, e, forbidden):
                e += step
            add(p, e, special, False)

    tail = limit + 1
    tail_loglo = log_bounds(tail)[0]
    tail_abhi = log_bounds(tail, tail - 1)[1]
    tail_index = len(costs)
    costs.extend((2 * tail_loglo * SCALE // tail_abhi, tail_loglo))
    abundances.extend((SCALE, tail_abhi))
    specials.append(tail_index + 1)

    # Every row is encoded with all entries and RHS multiplied by SCALE.
    rows = [(list(enumerate(-h for h in abundances)), -log_bounds(2)[0]),
            ([(i, SCALE) for i in specials], SCALE)]
    rows.extend(([(i, SCALE) for i, _, _, _ in opts], SCALE)
                for opts in options.values())
    exact_options = {(p, e): (i, special) for p, opts in options.items()
                     for i, e, special, exact in opts if exact}
    for p, e, q, k in edges:
        i, is_special = exact_options[p, e]
        terms = [(j, -SCALE) for j, f, special, exact in options[q]
                 if (not is_special or not special) and (not exact or f >= k)]
        implications.append(([(i, SCALE)] + terms, 0))
    rows.extend(implications)
    return costs, rows, tail_index


def generate(roots, limit, cutoff, factor_limit):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    from sympy import factorint, isprime
    from sympy.ntheory.factor_ import factor_cache

    proofs = {2: []}
    trial_primes = (2, *odd_primes(factor_limit))

    def factor(n, limit=factor_limit):
        factor_cache.cache_clear()
        try:
            return factorint(n, limit=limit)
        except ValueError:
            if limit is None:
                raise
            # A bounded SymPy run can reject a composite intermediate cache entry.
            # Fall back to certified trial factors and retain any probable-prime
            # remainder as a candidate for the independent Pocklington prover.
            factors = {}
            for p in trial_primes:
                while n % p == 0:
                    n //= p
                    factors[p] = factors.get(p, 0) + 1
                if p * p > n:
                    break
            if n > 1 and isprime(n):
                factors[n] = factors.get(n, 0) + 1
            return factors

    def cyclotomic_parts(p, n):
        parts = {1: p - 1}
        for d in range(2, n + 1):
            if n % d == 0:
                value = p**d - 1
                for k, part in parts.items():
                    if d % k == 0:
                        value //= part
                parts[d] = value
        return tuple(value for d, value in parts.items() if d != 1)

    @lru_cache(maxsize=None)
    def prove(n):
        if n == 2:
            return True
        if n < 2 or not isprime(n):
            return False
        known = 1
        witnesses = []
        for q, k in sorted(factor(n - 1).items()):
            q, k = int(q), int(k)
            if not prove(q):
                continue
            for a in range(2, min(n, 40)):
                if pow(a, n - 1, n) == 1 and gcd(pow(a, (n - 1) // q, n) - 1, n) == 1:
                    known *= q**k
                    witnesses.append([q, k, a])
                    break
            if known * known > n:
                proofs[n] = witnesses
                return True
        return False

    edges = []
    for p in odd_primes(limit):
        if p in roots:
            continue
        for e in range(1, cutoff + 1):
            if e % 2 and (e % 4 != 1 or p % 4 != 1):
                continue
            if not allowed(p, e, roots):
                continue
            known = {}
            for part in cyclotomic_parts(p, e + 1):
                for q, k in factor(part, None if p == 61 and e in (10, 12) else factor_limit).items():
                    q, k = int(q), int(k)
                    if q > 2 and prove(q):
                        known[q] = known.get(q, 0) + k
            edges.extend((p, e, q, k) for q, k in known.items())
    edges.sort()
    costs, rows, tail = build_model(roots, limit, cutoff, edges)
    ii, jj, values, rhs = [], [], [], []
    for i, (terms, d) in enumerate(rows):
        for j, a in terms:
            ii.append(i)
            jj.append(j)
            values.append(a / SCALE)
        rhs.append(d / SCALE)
    matrix = coo_matrix((values, (ii, jj)), shape=(len(rows), len(costs))).tocsr()
    bounds = [(0, 1)] * len(costs)
    bounds[tail] = (0, None)
    c = [x / SCALE for x in costs]
    result = linprog(c, A_ub=matrix, b_ub=rhs, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    weights = [max(0, round(-float(x) * DYADIC)) for x in result.ineqlin.marginals]
    weights[0] = min(weights[0], costs[tail] * DYADIC // SCALE)
    certificate = {"roots": roots, "limit": limit, "cutoff": cutoff, "edges": edges,
                   "proofs": proofs, "weights": weights}
    print(f"numerical LP exponent: {result.fun * SCALE / log_bounds(10)[1]:.9f}", flush=True)
    return certificate


def verify(cert):
    roots, limit, cutoff = cert["roots"], cert["limit"], cert["cutoff"]
    if tuple(roots) not in (ORIGINAL, REPLACEMENT) or limit < max(roots) or cutoff < 1:
        raise ValueError("invalid LP parameters")
    proofs = {int(p): witness for p, witness in cert["proofs"].items()}

    @lru_cache(maxsize=None)
    def prime(n):
        if n == 2:
            return True
        rows = proofs.get(n, ())
        known = 1
        seen = set()
        for q, k, a in rows:
            if not (2 <= q < n and k > 0 and 1 < a < n) or q in seen or not prime(q):
                return False
            seen.add(q)
            known *= q**k
            if pow(a, n - 1, n) != 1 or gcd(pow(a, (n - 1) // q, n) - 1, n) != 1:
                return False
        return n > 2 and (n - 1) % known == 0 and known * known > n

    edges = [tuple(edge) for edge in cert["edges"]]
    if edges != sorted(set(edges)):
        raise ValueError("duplicate or unordered factor relations")
    base = set(odd_primes(limit)) - set(roots)
    for p, e, q, k in edges:
        if not (p in base and q > 2 and q not in roots and q != p and k > 0 and prime(q)
                and 1 <= e <= cutoff and (e % 2 == 0 or (e % 4 == p % 4 == 1))
                and allowed(p, e, roots) and sigma(p, e) % q**k == 0):
            raise ValueError(f"invalid factor relation: {(p, e, q, k)}")
    costs, rows, tail = build_model(roots, limit, cutoff, edges)
    weights = cert["weights"]
    if len(weights) != len(rows) or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("invalid dual multipliers")
    reduced = [c * DYADIC for c in costs]
    rhs_term = 0
    for w, (terms, d) in zip(weights, rows):
        rhs_term -= w * d
        for i, a in terms:
            reduced[i] += w * a
    if reduced[tail] < 0:
        raise ValueError("negative unbounded-tail reduced cost")
    bound = rhs_term + sum(min(0, c) for i, c in enumerate(reduced) if i != tail)
    log10_scaled_upper = log_bounds(10)[1] * DYADIC
    exponent_millionths = bound * 10**6 // log10_scaled_upper
    print(f"independent lower exponent: {exponent_millionths // 10**6}."
          f"{exponent_millionths % 10**6:06d}; options={len(costs)}, "
          f"rows={len(rows)}, factor_relations={len(edges)}")
    return bound > 2400 * log10_scaled_upper


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "verify"))
    parser.add_argument("file", type=Path)
    parser.add_argument("--roots", choices=("original", "replacement"), default="replacement")
    parser.add_argument("--limit", type=int, default=4000)
    parser.add_argument("--cutoff", type=int, default=16)
    parser.add_argument("--factor-limit", type=int, default=1000)
    args = parser.parse_args()
    if args.mode == "generate":
        roots = ORIGINAL if args.roots == "original" else REPLACEMENT
        cert = generate(roots, args.limit, args.cutoff, args.factor_limit)
        data = (json.dumps(cert, separators=(",", ":")) + "\n").encode("ascii")
        args.file.write_bytes(gzip.compress(data, mtime=0) if args.file.suffix == ".gz" else data)
    else:
        data = args.file.read_bytes()
        cert = json.loads(gzip.decompress(data) if args.file.suffix == ".gz" else data)
    return 0 if verify(cert) else 1


if __name__ == "__main__":
    raise SystemExit(main())
