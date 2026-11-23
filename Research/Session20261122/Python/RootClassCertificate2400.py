"""Exact dual certificates for the original odd-perfect-number root classes."""

import argparse
from functools import lru_cache
import gzip
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

from RoadblockDual import SCALE, log_bounds, odd_primes
from TerminalCertificate import DYADIC, allowed, build_model, sigma
from VerifyRootExponentCoverage import canonical_tasks

ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
TARGET = 2400


def make_model(root, limit, cutoff, edges, residual):
    forbidden = ORDER[:ORDER.index(root)]
    costs, rows, tail = build_model(forbidden, limit, cutoff, edges)
    # build_model inserts per-prime rows in increasing prime order, after the
    # abundance and Euler budget rows.
    bases = sorted((set(odd_primes(limit)) - set(forbidden)) | {q for _, _, q, _ in edges})
    root_terms, rhs = rows[2 + bases.index(root)]
    rows.append(([(i, -a) for i, a in root_terms], -rhs))
    if residual:
        for i, _ in root_terms:
            costs[i] = 0
    return costs, rows, tail


def archived_edges(archive):
    return archive["limit"], archive["cutoff"], [tuple(e) for e in archive["edges"]]


def model_inputs(root, archive, extra_edges, new_proofs=None, cutoff_override=None):
    if type(root) is not int or root not in ORDER:
        raise ValueError("invalid root")
    forbidden = ORDER[:ORDER.index(root)]
    limit, cutoff, old = archived_edges(archive)
    if cutoff_override is not None:
        if type(cutoff_override) is not int or not cutoff <= cutoff_override <= 60:
            raise ValueError("invalid exponent cutoff")
        cutoff = cutoff_override
    base = set(odd_primes(limit)) - set(forbidden)
    old = [e for e in old if e[0] in base and e[2] not in forbidden]
    # The caller must first verify the pinned terminal archive.
    edge_map = {(p, e, q): k for p, e, q, k in old}
    known_small = set(odd_primes(limit))
    proofs = {**archive["proofs"], **(new_proofs or {})}

    @lru_cache(maxsize=None)
    def prime(n):
        if n == 2 or n in known_small:
            return True
        known, factors = 1, set()
        for q, k, a in proofs.get(str(n), ()):
            if (any(type(v) is not int for v in (q, k, a))
                    or not 2 <= q < n or not 1 <= k <= n.bit_length()
                    or not 1 < a < n or q in factors or not prime(q)):
                return False
            factors.add(q)
            known *= q**k
            if known > n-1 or (n-1) % known or pow(a, n-1, n) != 1:
                return False
            if gcd(pow(a, (n-1)//q, n)-1, n) != 1:
                return False
        return n > 2 and known * known > n

    seen = set()
    for row in extra_edges:
        if len(row) != 4 or any(type(v) is not int for v in row):
            raise ValueError("malformed new factor relation")
        p, e, q, k = row
        key = p, e, q
        if (key in seen or p not in base or q <= 2 or q in forbidden
                or q == p or not 1 <= e <= cutoff or not 1 <= k <= 255
                or (e % 2 and not e % 4 == p % 4 == 1)
                or not allowed(p, e, forbidden) or sigma(p, e) % q**k or not prime(q)):
            raise ValueError(f"invalid new factor relation: {row}")
        seen.add(key)
        edge_map[key] = max(k, edge_map.get(key, 0))
    return limit, cutoff, sorted((*key, k) for key, k in edge_map.items())


def cyclotomic_tasks(root, min_m):
    return [t for t in canonical_tasks(ORDER)
            if t["root"] == root and not t["exact"] and t["exponent"] + 1 >= min_m
            and t["exponent"] + 1 > root
            and t["exponent"] + 1 in odd_primes(t["exponent"] + 1)]


def cyclotomic_abundance(root, tasks):
    upper = Fraction(1)
    for task in tasks:
        d = task["exponent"]
        m = d + 1
        value = sigma(root, d)
        count = 0
        while value >= 2*m+1:
            value //= 2*m+1
            count += 1
        ratio = Fraction(1)
        for j in range(1, count + 1):
            ratio *= Fraction(2*m*j+1, 2*m*j)
        upper = max(upper, ratio)
    return upper


def certificate_model(cert, archive):
    root = cert["root"]
    limit, cutoff, edges = model_inputs(root, archive, cert["extra_edges"], cert.get("prime_proofs"), cert.get("cutoff"))
    if "cyclotomic_min_m" not in cert:
        if "branch" in cert:
            raise ValueError("prime split needs a cyclotomic model")
        return make_model(root, limit, cutoff, edges, cert["residual"])
    min_m = cert["cyclotomic_min_m"]
    if type(min_m) is not int or min_m <= root or not cert["residual"]:
        raise ValueError("invalid cyclotomic model")
    tasks = cyclotomic_tasks(root, min_m)
    if not tasks:
        raise ValueError("empty cyclotomic model")
    limit = min(limit, 2*min_m)
    ms = [t["exponent"] + 1 for t in tasks]

    @lru_cache(maxsize=None)
    def disjoint(q):
        return q != root and all(q < 2*m+1 or pow(root, m, q) != 1 for m in ms)

    edges = [e for e in edges if e[0] <= limit and e[0] != root and disjoint(e[2])]
    forbidden = ORDER[:ORDER.index(root)]
    branch = cert.get("branch")
    if branch is not None:
        if (type(branch) is not list or len(branch) != 2 or type(branch[0]) is not int
                or type(branch[1]) is not bool or branch[0] == root
                or branch[0] in forbidden or branch[0] not in odd_primes(limit)):
            raise ValueError("invalid prime presence branch")
        if not branch[1]:
            forbidden = (*forbidden, branch[0])
            edges = [e for e in edges if e[0] != branch[0] and e[2] != branch[0]
                     and allowed(e[0], e[1], forbidden)]
    costs, rows, tail = build_model(forbidden, limit, cutoff, edges)
    bases = sorted((set(odd_primes(limit)) - set(forbidden)) | {q for _, _, q, _ in edges})
    if branch is not None and branch[1]:
        terms, rhs = rows[2 + bases.index(branch[0])]
        rows.append(([(i, -a) for i, a in terms], -rhs))
    root_terms, _ = rows[2 + bases.index(root)]
    rows[2 + bases.index(root)] = (root_terms, 0)
    gain = cyclotomic_abundance(root, tasks) * Fraction(root, root - 1)
    terms, d = rows[0]
    rows[0] = terms, d + log_bounds(gain.numerator, gain.denominator)[1]
    return costs, rows, tail


def lower_bound(cert, archive):
    if type(cert.get("residual")) is not bool:
        raise ValueError("invalid residual switch")
    costs, rows, tail = certificate_model(cert, archive)
    weights = cert["weights"]
    if len(weights) != len(rows) or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("invalid dual multipliers")
    reduced = [c * DYADIC for c in costs]
    total = 0
    for w, (terms, rhs) in zip(weights, rows):
        total -= w * rhs
        for i, a in terms:
            reduced[i] += w * a
    if reduced[tail] < 0:
        raise ValueError("negative unbounded-tail reduced cost")
    return total + sum(min(0, c) for i, c in enumerate(reduced) if i != tail)


def new_trial_edges(root, archive):
    forbidden = ORDER[:ORDER.index(root)]
    limit, cutoff, old = archived_edges(archive)
    known = {(p, e, q): k for p, e, q, k in old}
    primes = [p for p in odd_primes(limit) if p not in forbidden]
    for p in primes:
        for e in range(1, cutoff + 1):
            if (e % 2 and not e % 4 == p % 4 == 1) or not allowed(p, e, forbidden):
                continue
            n = sigma(p, e)
            for q in primes:
                if n == 1:
                    break
                if n % q:
                    continue
                k = 0
                while n % q == 0:
                    n //= q
                    k += 1
                if k > known.get((p, e, q), 0):
                    yield p, e, q, k


def generate(root, archive, residual, extra_edges, cyclotomic_min_m=None, branch=None, prime_proofs=None, cutoff=None):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    cert = dict(root=root, residual=residual, extra_edges=extra_edges)
    if cyclotomic_min_m is not None:
        cert["cyclotomic_min_m"] = cyclotomic_min_m
    if branch is not None:
        cert["branch"] = branch
    if prime_proofs:
        cert["prime_proofs"] = prime_proofs
    if cutoff is not None:
        cert["cutoff"] = cutoff
    costs, rows, tail = certificate_model(cert, archive)
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
    result = linprog([c / SCALE for c in costs], A_ub=matrix, b_ub=rhs,
                     bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    weights = [max(0, round(-float(w) * DYADIC)) for w in result.ineqlin.marginals]
    weights[0] = min(weights[0], costs[tail] * DYADIC // SCALE)
    cert["weights"] = weights
    return cert


@lru_cache(maxsize=4096)
def cyclotomic_forced_part(root, d):
    """A* times a size-only multiplier for Euler-even cyclotomic factors."""
    m = d + 1
    value = sigma(root, d)
    residual = value
    lift = 1
    trial_limit = 20000
    for q in _lift_primes():
        if q < 2*m+1 or q % (2*m) != 1 or q % 4 != 3:
            continue
        parity = 0
        while residual % q == 0:
            residual //= q
            parity ^= 1
        if parity:
            lift *= q
    if residual % 4 == 3:
        first = 2*m+1
        lower = first + 4*m*max(0, (trial_limit-first)//(4*m)+1)
        lift *= lower
    return root**d * value * lift


@lru_cache(maxsize=1)
def _lift_primes():
    return tuple(odd_primes(20000))


def accepted_shards(cert, archive, *, branch_only=False):
    if "branch" in cert and not branch_only:
        raise ValueError("conditional certificate requires a complementary branch")
    bound = lower_bound(cert, archive)
    target = TARGET * log_bounds(10)[1] * DYADIC
    if "cyclotomic_min_m" in cert:
        root = cert["root"]
        return [t["id"] for t in cyclotomic_tasks(root, cert["cyclotomic_min_m"])
                if bound + log_bounds(cyclotomic_forced_part(root, t["exponent"]))[0]
                * DYADIC > target]
    return [t["id"] for t in canonical_tasks(ORDER)
            if t["root"] == cert["root"]
            and bound + (t["exponent"] * log_bounds(t["root"])[0] * DYADIC
                         if cert["residual"] else 0) > target]


def main():
    from TerminalCertificate import verify

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "verify"))
    parser.add_argument("archive", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--root", type=int, choices=ORDER, default=17)
    parser.add_argument("--residual", action="store_true")
    parser.add_argument("--trial", action="store_true")
    parser.add_argument("--cyclotomic-min-m", type=int)
    args = parser.parse_args()
    archive = json.loads(gzip.decompress(args.archive.read_bytes()))
    if tuple(archive["roots"]) != tuple(sorted(ORDER)) or not verify(archive):
        raise ValueError("invalid original terminal archive")
    if args.mode == "generate":
        additions = list(new_trial_edges(args.root, archive)) if args.trial else []
        cert = generate(args.root, archive, args.residual, additions, args.cyclotomic_min_m)
        raw = (json.dumps(cert, separators=(",", ":")) + "\n").encode("ascii")
        args.certificate.write_bytes(gzip.compress(raw, mtime=0)
                                     if args.certificate.suffix == ".gz" else raw)
    else:
        raw = args.certificate.read_bytes()
        cert = json.loads(gzip.decompress(raw) if args.certificate.suffix == ".gz" else raw)
    power = lower_bound(cert, archive) * 10**6 // (log_bounds(10)[1] * DYADIC)
    shards = accepted_shards(cert, archive)
    print(f"root={cert['root']} residual={cert['residual']} "
          f"verified_lower_exponent={power // 10**6}.{power % 10**6:06d} "
          f"shards={len(shards)}")


if __name__ == "__main__":
    main()
