import argparse
from collections import Counter, defaultdict
from functools import cache
from itertools import product
from math import gcd, prod
from pathlib import Path
import json

B = 10**2400
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
HITS = ({3, 5, 7}, {3, 5, 11}, {3, 5, 13}, {3, 7, 11, 13, 19, 31})

def require(condition, message):
    if not condition:
        raise ValueError(message)

def support_cells(p):
    root_bans = set(ROOTS[:ROOTS.index(p)])
    result = {}
    for has3, has5 in product((0, 1), repeat=2):
        present = {p} | {q for q, has in ((3, has3), (5, has5)) if has}
        absent = root_bans | {q for q, has in ((3, has3), (5, has5)) if not has}
        for hit in HITS:
            allowed = hit - absent
            if len(allowed) == 1:
                present |= allowed
        if not present & absent and all(hit - absent for hit in HITS):
            result[f"{has3}{has5}"] = (present, absent)
    return result

def load_ledger(path):
    tsv = path.read_text(encoding="utf-8").split("<!-- LEDGER_BEGIN -->\n", 1)[1]
    tsv = tsv.split("\n<!-- LEDGER_END -->", 1)[0]
    lines = tsv.splitlines()
    require(lines[0] == "~~~tsv" and lines[-1] == "~~~", "ledger delimiters")
    require(lines[1] == "id\tp\td\ttype\tactuals", "ledger header")
    rows = {}
    for line in lines[2:-1]:
        label, p, d, kind, actuals = line.split("\t")
        p, d = int(p), int(d)
        exponents = tuple(map(int, actuals.split(",")))
        require(p in ROOTS and label.startswith(f"P{p}_I") and label not in rows, "shard ID")
        require(kind in ("E", "D") and exponents == tuple(sorted(set(exponents))), "shard format")
        for e in exponents:
            require(e > 0 and (e == d if kind == "E" else (e+1) % (d+1) == 0), "index coverage")
            require(p**e <= B and (e % 2 == 0 or p % 4 == e % 4 == 1), "illegal root exponent")
        rows[label] = (p, d, kind, exponents)
    pairs = {(p, e) for p, _, _, es in rows.values() for e in es}
    totals = (len(rows), len(pairs), sum(len(es) for _, _, _, es in rows.values()),
              sum(len(es) == 1 for _, _, _, es in rows.values()))
    require(totals == (204, 244, 266, 181), "baseline totals")
    require(Counter(p for p, _, _, _ in rows.values()) ==
            {19: 54, 7: 52, 11: 30, 31: 16, 13: 24, 3: 28}, "root shard totals")
    return rows, pairs

def sigma(r, f):
    return (r**(f+1)-1)//(r-1)

def valuation(n, q):
    count = 0
    while n % q == 0:
        n //= q
        count += 1
    return count

def small_primes(limit):
    sieve = bytearray(b"\x01") * (limit+1)
    sieve[:2] = b"\x00\x00"
    for q in range(2, limit+1):
        if sieve[q]:
            yield q
            if q*q <= limit:
                sieve[q*q::q] = b"\x00" * ((limit-q*q)//q+1)

def trial_factors(n, limit):
    found = []
    for q in small_primes(limit):
        if q*q > n:
            if n > 1:
                found.append((n, 1))
                n = 1
            break
        if n % q == 0:
            v = valuation(n, q)
            n //= q**v
            found.append((q, v))
    return found, n

def prime64(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    s = valuation(n-1, 2)
    d = (n-1) >> s
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n:
            x = pow(a, d, n)
            if x in (1, n-1):
                continue
            for _ in range(s-1):
                x = x*x % n
                if x == n-1:
                    break
            else:
                return False
    return True

def primality_checker(table):
    @cache
    def prime(n):
        require(type(n) is int and n >= 2, "invalid prime input")
        if n < 2**64:
            return prime64(n)
        witnesses = table.get(str(n), [])
        known = 1
        seen = set()
        for q, multiplicity, a in witnesses:
            require(type(q) is int and 2 <= q < n and q not in seen and prime(q), "prime factor witness")
            require(type(multiplicity) is int and 1 <= multiplicity <= n.bit_length(), "factor multiplicity")
            require(type(a) is int and 1 < a < n, "witness base")
            known *= q**multiplicity
            require((n-1) % known == 0 and pow(a, n-1, n) == 1 and
                    gcd(pow(a, (n-1)//q, n)-1, n) == 1, "Pocklington identity")
            seen.add(q)
        return known*known > n
    return prime

def node_state(fixed, absent):
    x = prod(r**f for r, f in fixed.items())
    s = prod(sigma(r, f) for r, f in fixed.items())
    d = s // gcd(s, 2*x)
    odd = [(r, f) for r, f in fixed.items() if f % 2]
    empty = (x*d > B or s > 2*x or gcd(x, d) != 1
             or any(d % q == 0 or q in fixed for q in absent)
             or len(odd) > 1 or any(r % 4 != 1 or f % 4 != 1 for r, f in odd))
    return x, d, bool(odd), empty

def allowed(r, exponent, absent):
    return all(pow(r, exponent+1, q*(r-1)) != 1 for q in absent)

def exponent_options(r, minimum, budget, absent, odd_allowed):
    value = r**minimum
    e = minimum
    while value <= budget:
        parity_ok = e % 2 == 0 or odd_allowed and e % 4 == 1
        if parity_ok and allowed(r, e, absent):
            yield e
        value *= r
        e += 1

def size_bound(x, d, odd_used, fixed, present, absent, factors, prime):
    given = set(factors)
    require(len(given) == len(factors), "duplicate size factor")
    require(all(type(r) is int and r > 2 and prime(r) and r not in fixed
                and (r in present or d % r == 0) for r in given), "unsupported size factor")
    selected = given | (present - fixed.keys())
    residue = d
    even_cost, odd_cost = {}, {}
    for r in sorted(selected):
        c = valuation(d, r)
        residue //= r**c
        even_cost[r] = B+1
        if not odd_used and r % 4 == 1:
            odd_cost[r] = B+1
        for e in exponent_options(r, max(1, c), B//x, absent, r in odd_cost):
            if e % 2 == 0 and even_cost[r] == B+1:
                even_cost[r] = r**e
            elif e % 2 and odd_cost[r] == B+1:
                odd_cost[r] = r**e
            if even_cost[r] != B+1 and odd_cost.get(r, 0) != B+1:
                break
    even_product = prod(even_cost.values())
    return x*residue*min([even_product] +
                         [even_product//even_cost[r]*power for r, power in odd_cost.items()])

def verify_tree(tree, fixed, present, absent, prime):
    x, d, odd_used, empty = node_state(fixed, absent)
    kind = tree["kind"]
    if kind == "direct":
        require(empty, "invalid direct leaf")
    elif kind == "size":
        require(empty or size_bound(x, d, odd_used, fixed, present, absent,
                                    tree["factors"], prime) > B, "invalid size leaf")
    elif kind == "split":
        require(not empty, "use direct for an already empty split")
        r = tree["r"]
        require(type(r) is int and r > 2 and r not in fixed and r not in absent and
                prime(r) and (r in present or d % r == 0), "unsupported split prime")
        exponents = list(exponent_options(r, max(1, valuation(d, r)), B//x,
                                          absent, not odd_used and r % 4 == 1))
        children = tree["children"]
        require(children.keys() == {str(e) for e in exponents}, "missing or extra exponent branch")
        for e in exponents:
            verify_tree(children[str(e)], fixed | {r: e}, present, absent, prime)
    else:
        raise ValueError(f"unknown kind {kind}")

def verify(cert, pairs):
    p, e = cert["p"], cert["e"]
    require(type(p) is type(e) is int and (p, e) in pairs, "certificate index not open")
    cells = support_cells(p)
    require(cert["cells"].keys() == cells.keys(), "support cases are not exhaustive")
    prime = primality_checker(cert.get("primes", {}))
    for name, (present, absent) in cells.items():
        verify_tree(cert["cells"][name], {p: e}, present, absent, prime)
    return p, e

def project(rows, excluded):
    closed, left = [], {}
    for label, (p, d, kind, es) in rows.items():
        surviving = [e for e in es if (p, e) not in excluded]
        if surviving:
            left[label] = {"p": p, "d": d, "type": kind, "actuals": surviving}
        else:
            closed.append(label)
    return closed, left

def summary(rows):
    uses, one = defaultdict(list), Counter()
    for label, (p, _, _, es) in rows.items():
        for e in es:
            uses[p, e].append(label)
        if len(es) == 1:
            one[p, es[0]] += 1
    return [{"p": p, "e": e, "immediate": one[p,e], "shards": uses[p,e]}
            for p, e in sorted(uses, key=lambda pe: (-one[pe], -len(uses[pe]), pe))]

def probe(p, e, limit):
    found, residual = trial_factors(sigma(p, e), limit)
    x, d, odd, _ = node_state({p:e}, set())
    factors = [r for r, _ in found if d % r == 0]
    cells = {}
    for name, (present, absent) in support_cells(p).items():
        _, _, _, empty = node_state({p:e}, absent)
        lower = empty or size_bound(x, d, odd, {p:e}, present, absent,
                                    factors, primality_checker({})) > B
        cells[name] = {"present": sorted(present), "absent": sorted(absent),
                       "trial_size_proves": lower}
    return {"p": p, "e": e, "factors": found, "residual": str(residual), "cells": cells}

def selftest(rows, pairs):
    require(len(project(rows, set())[1]) == 204 and len(project(rows, pairs)[0]) == 204, "projection")
    require(set(support_cells(19)) == {"00", "01", "10", "11"} and
            set(support_cells(3)) == {"10", "11"} and "00" not in support_cells(11), "support cells")
    require(trial_factors(381, 100) == ([(3, 1), (127, 1)], 1), "trial factor sample")
    require(node_state({19:2}, {3})[-1], "forbidden divisor")
    require(prime64(127) and not prime64(341) and not prime64(1), "primality")
    verify_tree({"kind":"direct"}, {19:2}, {19}, {3}, primality_checker({}))
    try:
        verify_tree({"kind":"direct"}, {19:2}, {19}, set(), primality_checker({}))
    except ValueError:
        pass
    else:
        raise ValueError("false leaf accepted")
    try:
        verify_tree({"kind":"split","r":127,"children":{}}, {19:2}, {19}, set(), primality_checker({}))
    except ValueError:
        pass
    else:
        raise ValueError("missing branches accepted")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", type=Path,
                        default=Path(__file__).with_name("PerfectNumbers2400_Gemini_Standalone.md"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("selftest")
    sub.add_parser("summary")
    target = sub.add_parser("probe")
    target.add_argument("p", type=int)
    target.add_argument("e", type=int)
    target.add_argument("--limit", type=int, default=10000)
    sub.add_parser("verify").add_argument("files", type=Path, nargs=1)
    sub.add_parser("update").add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    rows, pairs = load_ledger(args.markdown)
    if args.command == "selftest":
        selftest(rows, pairs)
        print("PASS 204 shards, 244 distinct exponents, 266 incidences, 181 singletons")
        return
    if args.command == "summary":
        out = summary(rows)
    elif args.command == "probe":
        require((args.p, args.e) in pairs and 2 <= args.limit <= 1_000_000, "probe arguments")
        out = probe(args.p, args.e, args.limit)
    else:
        accepted = {verify(json.loads(path.read_text(encoding="utf-8")), pairs) for path in args.files}
        closed, left = project(rows, accepted)
        out = {"accepted": sorted(accepted), "closed": closed}
        if args.command == "update":
            out["remaining_shards"] = left
            out["remaining_pairs"] = len(pairs - accepted)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
