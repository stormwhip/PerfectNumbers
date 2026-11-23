"""Recompute exact root-shard contradictions using partial sigma valuations."""

from functools import lru_cache
from math import gcd, lcm

from RoadblockDual import odd_primes
from TerminalCertificate import allowed, sigma

TRIAL_LIMIT = 20000


@lru_cache(maxsize=65536)
def compatible(q, least, greatest, forbidden, special_allowed, root_step=1):
    """Return complete compatible exponent lists by parity."""
    even = tuple(
        e for e in range(least + least % 2, greatest + 1, 2)
        if (e + 1) % root_step == 0 and allowed(q, e, forbidden))
    odd = ()
    if special_allowed and q % 4 == 1:
        odd = tuple(e for e in range(least + (1-least)%4, greatest + 1, 4)
                    if (e + 1) % root_step == 0 and allowed(q, e, forbidden))
    return even, odd


def valuation(n, q):
    e = 0
    while n % q == 0:
        n //= q
        e += 1
    return e


def max_extra_exponent(q, cap):
    if cap < q:
        return 0
    # 2**cap.bit_length() > cap and q >= 3.
    lo, hi = 0, cap.bit_length()
    while hi - lo > 1:
        mid = (hi + lo) // 2
        if q**mid <= cap:
            lo = mid
        else:
            hi = mid
    return lo


def odd_sigma(q, e):
    s = sigma(q, e)
    return s // (s & -s)


def analyze(root, d, exact, forbidden, bound, fixed=(), steps=12):
    """Return a verified contradiction or None. Fixed branches are exact."""
    forced_sigma = {root: odd_sigma(root, d)}
    fixed = dict(fixed)
    if exact:
        fixed[root] = d
    for q, e in fixed.items():
        forced_sigma[q] = lcm(forced_sigma.get(q, 1), odd_sigma(q, e))
    divisor = 1
    for s in forced_sigma.values():
        divisor *= s

    candidates = tuple(odd_primes(TRIAL_LIMIT))
    choices = {}
    for _ in range(steps):
        if any(divisor % q == 0 for q in forbidden):
            return "FORBIDDEN_SIGMA_PRODUCT"
        lower = {q: valuation(divisor, q) for q in fixed}
        lower[root] = valuation(divisor, root)
        for q in candidates:
            if q not in lower and divisor % q == 0:
                lower[q] = valuation(divisor, q)
        base = lcm(divisor, root**d, *(q**e for q, e in fixed.items()))
        if base > bound:
            return "SIGMA_PRODUCT_SIZE"
        special = [q for q, e in fixed.items() if e % 2]
        if len(special) > 1 or any(q % 4 != 1 or fixed[q] % 4 != 1 for q in special):
            return "EULER"
        domains = {}
        regular, odd = {}, {}
        for q, v in lower.items():
            already = max(v, fixed.get(q, d if q == root else 0))
            cap = already + max_extra_exponent(q, bound // base)
            if q in fixed:
                e = fixed[q]
                if (e < max(1, v, d if q == root else 0)
                        or (q == root and (e + 1) % (d + 1))
                        or not allowed(q, e, forbidden)):
                    return "FIXED_EXPONENT"
                even_q, odd_q = ((), (e,)) if e % 2 else ((e,), ())
            else:
                even_q, odd_q = compatible(q, max(1, already), cap, forbidden,
                                           not special, root_step=d+1 if q == root else 1)
                if not even_q and not odd_q:
                    return "EMPTY_EXPONENT_DOMAIN"
            domains[q] = even_q, odd_q
            if even_q:
                regular[q] = q**(even_q[0] - already)
            if odd_q:
                odd[q] = q**(odd_q[0] - already)
        odd_required = set(lower) - set(regular)
        if len(odd_required) > 1:
            return "EULER"
        regular_cost = 1
        for value in regular.values():
            regular_cost *= value
        size_if_special = {q: base * (regular_cost // regular.get(q, 1)) * cost
                           for q, cost in odd.items() if not odd_required - {q}}
        regular_feasible = not odd_required and base * regular_cost <= bound
        special_feasible = {q for q, size in size_if_special.items() if size <= bound}
        if not regular_feasible and not special_feasible:
            return "VALUATION_LIFT_SIZE"
        if not regular_feasible and len(special_feasible) == 1:
            odd_required = special_feasible
        old_divisor = divisor
        abund_num = abund_den = 1
        choices = {}
        for q, (even_q, odd_q) in domains.items():
            active = (() if q in odd_required else even_q) + (
                odd_q if q in special_feasible else ())
            minimum = min(active)
            abund_num *= sigma(q, minimum)
            abund_den *= q**minimum
            if q not in fixed:
                choices[q] = tuple(sorted(active))
            common = 0
            for e in active:
                common = gcd(common, e + 1)
                if common == 1:
                    break
            if common > 1:
                previous = forced_sigma.get(q, 1)
                current = lcm(previous, odd_sigma(q, common-1))
                forced_sigma[q] = current
                divisor *= current // previous
        if abund_num > 2 * abund_den:
            return "FORCED_ABUNDANCE"
        if divisor == old_divisor:
            break
    return choices


def contradicts(root, d, exact, forbidden, bound, node_budget=1, split_cap=12):
    """Explore complete exact-exponent splits within fixed resource limits."""
    unseen = [()]
    nodes = 0
    direct = None
    while unseen and nodes < node_budget:
        fixed = unseen.pop()
        nodes += 1
        result = analyze(root, d, exact, forbidden, bound, fixed)
        if isinstance(result, str):
            if nodes == 1:
                direct = result
            continue
        options = [(len(es), -q, es) for q, es in result.items() if len(es) <= split_cap]
        if not options:
            return None
        _, negative_q, es = min(options)
        unseen.extend(fixed + ((-negative_q, e),) for e in es)
    if unseen:
        return None
    return direct or "VALUATION_FACTOR_TREE"
