#!/usr/bin/env python3
"""Second, independent cold check; deliberately does not import Verify.py."""
import hashlib
import json
import sys
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
P = Path(__file__).resolve().parent
DATA = json.loads((P/"Certificates.json").read_text(encoding="utf-8"))
B = 10**2400
CHECKS = 0


def need(x, message):
    global CHECKS
    CHECKS += 1
    if not x:
        raise ValueError(message)


def valuation(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def sigma(p, e):
    return (p**(e+1)-1)//(p-1)


def prime64(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n-1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    # Deterministic for every unsigned 64-bit integer.
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
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


def composite_or_unrecognized(n):
    # A Miller-Rabin witness proves compositeness at every size.  A pass is not
    # treated as primality: the candidate is conservatively retained.
    if n <= 1:
        return True
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return False
        if n % p == 0:
            return True
    d = n-1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1:
                break
        else:
            return True
    return False


def state(rows):
    odd_rows = [(p, e) for p, e in rows if e % 2]
    if len(odd_rows) > 1 or any(p % 4 != 1 or e % 4 != 1 for p, e in odd_rows):
        return None
    X = 1
    T = 1
    for p, e in rows:
        X *= p**e
        T *= sigma(p, e)
    S = T >> valuation(T, 2)
    if any(valuation(S, p) > e for p, e in rows):
        return None
    D = S//gcd(S, X)
    if X*D > B or T > 2*X:
        return None
    return X, S, D


def split(rows, pivot):
    X, _, D = state(rows)
    d = valuation(D, pivot)
    h = d
    raw = X*(D//pivot**d)*pivot**h
    live = []
    while raw <= B:
        e = h
        if len([1 for p, f in rows+[(pivot, e)] if f % 2]) <= 1:
            st = state(rows+[(pivot, e)])
            if st is not None:
                live.append(e)
        h += 1
        raw *= pivot
    return live, h


def roots_by_powering(p, g, order, depth):
    need((p-1) % order == 0, "bad order")
    roots = [pow(g, (p-1)//order*j, p) for j in range(1, order)]
    out = {1: roots}
    modulus = p
    for z in range(2, depth+1):
        modulus *= p
        # If r^order=1 mod p^(z-1), then (r^p)^order=1 mod p^z.
        roots = [pow(r, p, modulus) for r in roots]
        need(len(set(roots)) == order-1, "collapsed roots")
        need(all(pow(r, order, modulus) == 1 for r in roots), "bad lifted root")
        out[z] = roots
    return out


def deficit19():
    fixed = {19, 1109, 1176672733}
    w = 6
    cap_z = 276
    deficits = {}
    for order in (3, 9):
        h0 = order-1
        z0 = min(cap_z, (w*cap_z+h0-1)//h0)
        roots = roots_by_powering(19, 2, order, z0)
        for z in range(1, z0+1):
            exponent = w*(cap_z if z == z0 and z0 < cap_z else z)
            cap = 19**exponent
            for b in roots[z]:
                if b < 3 or not b % 2 or b in fixed or composite_or_unrecognized(b):
                    continue
                if b**h0 >= cap:
                    continue
                actual = min(cap_z, valuation(b**order-1, 19))
                ratio = Fraction(19**(w*actual), b**h0)
                key = str(b)
                if ratio > deficits.get(key, Fraction(1)):
                    deficits[key] = ratio
    return deficits


def check1109(Xbase):
    roots = roots_by_powering(1109, 2, 277, 4)
    for z in (1, 2, 3):
        for b in roots[z]:
            if b % 2:
                need(b**276 >= 1109**(100*z), "1109 loss")
    for b in roots[4]:
        if b % 2:
            need(b > 25_000_000, "1109 small depth-four root")
    need(Xbase*25_000_000**276 > B, "base cap")
    need(3**1108 > 1109**100, "order one")
    need(277*1109-1 > 5031, "LTE cap")


def main():
    begin = time.perf_counter()
    for entry in DATA["CertifiedPrimes"]:
        need(prime64(int(entry["p"])), "fixed prime failed independent MR64")
    first, tail = split([(19, 276)], 1176672733)
    need((len(first), tail) == (70, 188), "first domain")
    prefix = [(19, 276), (1176672733, 1)]
    live, tail = split(prefix, 1109)
    need(live == DATA["LiveExponents"] and tail == 555, "second domain")
    deficits = deficit19()
    U = Fraction(1)
    for b, text in DATA["Deficits19"].items():
        expected = Fraction(int(text["numerator"]), int(text["denominator"]))
        need(deficits.get(b) == expected, f"independent deficit mismatch at {b}")
        U *= expected
    need(len(deficits) == len(DATA["Deficits19"]), "independent deficit count")
    need(U == Fraction(int(DATA["DeficitProduct19"]["numerator"]),
                       int(DATA["DeficitProduct19"]["denominator"])), "product")
    check1109(state(prefix)[0])
    for row in DATA["TerminalChecks"]:
        h = row["h"]
        X, S, _ = state(prefix+[(1109, h)])
        c1 = 276-valuation(S, 19)
        c2 = h-valuation(S, 1109)
        need((c1, c2) == (row["c19"], row["c1109"]), "demand mismatch")
        need(X*19**(6*c1)*1109**(100*c2)*U.denominator > B*U.numerator,
             f"terminal {h}")
    elapsed = time.perf_counter()-begin
    print(json.dumps({"status": "INDEPENDENT_PASS", "closed_children": len(live),
                      "strict_tail": tail, "checks": CHECKS,
                      "elapsed_seconds": elapsed}, indent=2))
    print("Certificate SHA-256:", hashlib.sha256((P/"Certificates.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
