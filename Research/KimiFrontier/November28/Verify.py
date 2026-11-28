#!/usr/bin/env python3
"""Offline exact verifier for the (19,276), t=1176672733^1 fiber.

Usage from the repository root:
  python -I -S -B -X int_max_str_digits=0 Research/KimiFrontier/November28/Verify.py
  python -I -S -B -X int_max_str_digits=0 Research/KimiFrontier/November28/Verify.py --run-negative-tests

Only Python's standard library is used.  All proof decisions use integers or
Fraction, and explicit checks rather than assert statements.
"""
import copy
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from math import gcd, prod
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "Certificates.json"
B = 10**2400
E3_MIN = 5031
MR12_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MR12_LIMIT = 3317044064679887385961981
CHECKS = 0


class VerificationError(Exception):
    pass


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(message)


def sigma_power(p, h):
    return (p**(h + 1) - 1) // (p - 1)


def vp(n, p):
    require(n > 0 and p > 1, "invalid valuation input")
    value = 0
    while n % p == 0:
        n //= p
        value += 1
    return value


def odd_part(n):
    return n >> vp(n, 2)


def is_composite_witness(n):
    """True only on a proved composite; MR passes are conservatively retained."""
    if n <= 1:
        return True
    for p in MR12_BASES:
        if n == p:
            return False
        if n % p == 0:
            return True
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in MR12_BASES:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        witness = True
        for _ in range(s - 1):
            x = x*x % n
            if x == n - 1:
                witness = False
                break
        if witness:
            return True
    return False


def verify_primes(entries):
    certified = {}
    small = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
    for item in entries:
        p = int(item["p"])
        if item["method"] == "small_prime":
            require(p in small, f"invalid small prime {p}")
        else:
            require(item["method"] == "pratt_primitive_root", "unknown primality method")
        g = int(item["g"])
        factors = {int(q): int(e) for q, e in item["p_minus_1_factors"]}
        require(prod(q**e for q, e in factors.items()) == p - 1,
                f"p-1 factorization failed for {p}")
        for q in factors:
            require(q in certified, f"uncertified Pratt factor {q}")
        require(pow(g, p - 1, p) == 1, f"Fermat check failed for {p}")
        for q in factors:
            require(pow(g, (p - 1)//q, p) != 1,
                    f"Lucas order check failed for {p},{q}")
        if p < MR12_LIMIT:
            require(not is_composite_witness(p), f"deterministic MR failed for {p}")
        certified[p] = {"g": g, "factors": factors}
    return certified


def exact_state(rows, primes):
    seen = set()
    for p, h in rows:
        require(p in primes and p >= 3 and p % 2 and h >= 1,
                f"invalid or uncertified exact row {(p,h)}")
        require(p not in seen, "duplicate exact base")
        seen.add(p)
    odd_rows = [(p, h) for p, h in rows if h % 2]
    if len(odd_rows) > 1 or any(p % 4 != 1 or h % 4 != 1 for p, h in odd_rows):
        return None
    X = prod(p**h for p, h in rows)
    T = prod(sigma_power(p, h) for p, h in rows)
    S = odd_part(T)
    if any(vp(S, p) > h for p, h in rows):
        return None
    D = S // gcd(S, X)
    require(gcd(X, D) == 1, "remaining divisor is not coprime to X")
    if X*D > B or T > 2*X:
        return None
    return X, T, S, D


def exact_split(rows, pivot, primes):
    state = exact_state(rows, primes)
    require(state is not None, "invalid split parent")
    X, _, _, D = state
    require(pivot in primes and pivot not in dict(rows) and D % pivot == 0,
            "invalid split pivot")
    d = vp(D, pivot)
    h = d
    base = X*(D//pivot**d)*pivot**h
    live = []
    while base <= B:
        if exact_state(rows + [(pivot, h)], primes) is not None:
            live.append(h)
        h += 1
        base *= pivot
    require(base > B, "strict tail did not overflow")
    return live, h


def hensel_roots(p, g, order, depth):
    require((p - 1) % order == 0, "order does not divide p-1")
    step = (p - 1)//order
    roots = sorted(pow(g, step*j, p) for j in range(1, order))
    require(len(roots) == order - 1, "root count mismatch")
    result = {1: roots}
    modulus = p
    for z in range(2, depth + 1):
        next_modulus = modulus*p
        lifted = []
        for r in roots:
            f = (pow(r, order, next_modulus) - 1)//modulus
            inverse = pow(order*pow(r, order - 1, p) % p, -1, p)
            digit = (-f*inverse) % p
            nr = r + digit*modulus
            require(pow(nr, order, next_modulus) == 1, "Hensel lift failed")
            lifted.append(nr)
        roots = lifted
        modulus = next_modulus
        result[z] = roots
    return result


def admissible_prime_base(b, fixed):
    # Overinclusion is safe: a probable prime or an unrecognized composite stays.
    return b >= 3 and b % 2 and b not in fixed and not is_composite_witness(b)


def deficit_19(weight, max_z, fixed, primes):
    """Exact loss table for b^(o-1) >= 19^(weight*z)/U_b."""
    require(1 <= weight <= 7 and max_z == 276, "unexpected 19 pricing parameters")
    require(primes[19]["factors"] == {2: 1, 3: 2}, "19-1 factorization changed")
    # Order one: 3^18 >= 19^6.  If A_u=3^(19^u-1), then
    # A_(u+1) >= A_u^19, so the base-u inequality inducts for every u<=276.
    require(3**18 >= 19**weight, "order-one dominance failed")
    # Nontrivial orders are 3 and 9.  Pay every LTE increment k=1,2 from
    # o*(19^k-1) additional exponent units; k>=3 exceeds the size cap.
    require(3*19**3 - 1 >= E3_MIN, "19 LTE tail is below exponent cap")
    for order in (3, 9):
        for k in (1, 2):
            require(3**(order*(19**k - 1)) >= 19**(weight*k),
                    "19 LTE increment dominance failed")
    deficits = {}
    for order in (3, 9):
        minimum_h = order - 1
        z0 = min(max_z, (weight*max_z + minimum_h - 1)//minimum_h)
        roots = hensel_roots(19, primes[19]["g"], order, z0)
        for z in range(1, z0 + 1):
            cap_z = max_z if z == z0 and z0 < max_z else z
            cap = 19**(weight*cap_z)
            for b in roots[z]:
                if not admissible_prime_base(b, fixed):
                    continue
                if b**minimum_h >= cap:
                    continue
                actual_z = min(max_z, vp(b**order - 1, 19))
                ratio = Fraction(19**(weight*actual_z), b**minimum_h)
                if ratio > deficits.get(str(b), Fraction(1)):
                    deficits[str(b)] = ratio
    return deficits


def product_fraction(deficits):
    result = Fraction(1)
    for ratio in deficits.values():
        result *= ratio
    return result


def verify_zero_deficit_1109(weight, X_base, fixed, primes):
    require(weight == 100, "unexpected 1109 weight")
    require(primes[1109]["factors"] == {2: 2, 277: 1}, "1109-1 factorization changed")
    require(3**1108 > 1109**weight, "1109 order-one dominance failed")
    require(277*1109 - 1 >= E3_MIN, "1109 LTE is below exponent cap")
    cap = 25_000_000
    require(X_base*cap**276 > B, "1109 supplier base cap failed")
    roots = hensel_roots(1109, primes[1109]["g"], 277, 4)
    for z in (1, 2, 3):
        for b in roots[z]:
            if b % 2:
                require(b**276 >= 1109**(weight*z),
                        f"1109 basic deficit at z={z}, b={b}")
    for b in roots[4]:
        if b % 2:
            require(b > cap, "1109 depth-four root below supplier cap")
    return Fraction(1)


def verify(data):
    start = time.perf_counter()
    require(data["BaselineCommit"] == "db71cc42ad2a62e3e362b8874757c1cff0b7772f",
            "frozen baseline mismatch")
    require(data["Key"] == [19, 276] and data["ShardID"] == "P19_I00057",
            "wrong exact key or shard")
    require(3**5030 <= B < 3**5031, "wrong exponent cap")
    primes = verify_primes(data["CertifiedPrimes"])
    root_rows = [(19, 276)]
    first_live, first_tail = exact_split(root_rows, 1176672733, primes)
    require(len(first_live) == 70 and first_tail == 188, "first-pivot domain changed")
    require(1 in first_live, "t=1 is not in the reconstructed first-pivot domain")

    prefix = [(19, 276), (1176672733, 1)]
    base_state = exact_state(prefix, primes)
    require(base_state is not None, "base fiber is arithmetically impossible")
    X_base = base_state[0]
    live, tail = exact_split(prefix, 1109, primes)
    require(len(live) == data["ExpectedLiveCount"] and tail == data["StrictTail"],
            "1109 branch set or strict tail changed")
    require(live == [int(x) for x in data["LiveExponents"]], "live branch list mismatch")
    require(all(h % 2 == 0 for h in live), "Euler-fixed fiber has an odd 1109 exponent")

    require(data["Weight19"] == 6 and data["Weight1109"] == 100,
            "pricing weight metadata mismatch")
    fixed = {19, 1176672733, 1109}
    deficits = deficit_19(data["Weight19"], 276, fixed, primes)
    expected_deficits = {b: Fraction(int(r["numerator"]), int(r["denominator"]))
                         for b, r in data["Deficits19"].items()}
    require(deficits == expected_deficits, "19 deficit table mismatch")
    U19 = product_fraction(deficits)
    expected_U19 = Fraction(int(data["DeficitProduct19"]["numerator"]),
                            int(data["DeficitProduct19"]["denominator"]))
    require(U19 == expected_U19, "19 deficit product mismatch")
    U1109 = verify_zero_deficit_1109(100, X_base, fixed, primes)
    require(U1109 == 1, "1109 deficit is not zero")

    # The odd supports are disjoint, hence effective indices are coprime and
    # reduced exponents add without charging the same source exponent twice.
    support19 = {q for q in primes[19]["factors"] if q > 2} | {19}
    support1109 = {q for q in primes[1109]["factors"] if q > 2} | {1109}
    require(support19.isdisjoint(support1109), "effective-index supports overlap")

    terminal_rows = []
    for h in live:
        state = exact_state(prefix + [(1109, h)], primes)
        require(state is not None, "a reconstructed live child is not live")
        X, _, S, _ = state
        c19 = 276 - vp(S, 19)
        c1109 = h - vp(S, 1109)
        require(c19 > 0 and c1109 > 0, "nonpositive target demand")
        lhs = X*19**(6*c19)*1109**(100*c1109)*U19.denominator
        rhs = B*U19.numerator
        require(lhs > rhs, f"terminal inequality failed at h={h}")
        terminal_rows.append({"h": h, "c19": c19, "c1109": c1109, "lhs_gt_rhs": True})
    require(terminal_rows == data["TerminalChecks"], "terminal certificate mismatch")
    require(data["NewlyClosedRelativeToAcceptedOverlay"] == [2, 4],
            "incremental exclusions changed")
    require(data["OtherFirstValuesRemainingOpen"] == [2, 8, 16, 18, 28],
            "remaining first values changed")
    require(data["NewCompleteKeys"] == 0 and data["NewClosedShards"] == 0,
            "conditional result was overcounted")
    elapsed = time.perf_counter() - start
    return {
        "status": "VERIFIED_CONDITIONAL",
        "fiber_closed": True,
        "live_children_closed": len(live),
        "new_local_exclusions": 2,
        "new_complete_keys": 0,
        "new_closed_shards": 0,
        "strict_tail": tail,
        "deficit_bases_19": len(deficits),
        "arithmetic_checks": CHECKS,
        "elapsed_seconds": elapsed,
    }


def expect_reject(name, function):
    try:
        function()
    except VerificationError as exc:
        print(f"[PASS - REJECTED] {name}: {exc}")
        return
    raise RuntimeError(f"negative test was accepted: {name}")


def run_negative_tests(data):
    def missing_new_child():
        bad = copy.deepcopy(data)
        bad["NewlyClosedRelativeToAcceptedOverlay"] = [2]
        verify(bad)
    expect_reject("omitted newly closed h=4", missing_new_child)

    def excessive_weight():
        bad = copy.deepcopy(data)
        bad["Weight19"] = 7
        # Directly exercise the actual dominance guard, not a metadata comparison.
        deficit_19(7, 276, {19, 1176672733, 1109}, verify_primes(data["CertifiedPrimes"]))
    expect_reject("unsupported weight 7 at 19", excessive_weight)

    def fake_prime():
        bad = copy.deepcopy(data["CertifiedPrimes"])
        bad.append({"p": "91", "g": "2", "method": "small_prime", "p_minus_1_factors": []})
        verify_primes(bad)
    expect_reject("composite prime label", fake_prime)

    def tampered_deficit():
        bad = copy.deepcopy(data)
        bad["DeficitProduct19"]["numerator"] = str(int(bad["DeficitProduct19"]["numerator"]) + 1)
        verify(bad)
    expect_reject("tampered exact deficit product", tampered_deficit)

    def deleted_terminal():
        bad = copy.deepcopy(data)
        bad["TerminalChecks"] = [r for r in bad["TerminalChecks"] if r["h"] != 4]
        verify(bad)
    expect_reject("deleted terminal h=4", deleted_terminal)


def main():
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    digest = hashlib.sha256(raw).hexdigest()
    if "--run-negative-tests" in sys.argv:
        run_negative_tests(data)
        print("ALL NEGATIVE TESTS REJECTED AS REQUIRED")
        return
    result = verify(data)
    print(json.dumps(result, indent=2, sort_keys=True))
    print("Certificate SHA-256:", digest)
    print("FIBER VERIFIED; FULL KEY AND SHARD REMAIN OPEN")


if __name__ == "__main__":
    main()
