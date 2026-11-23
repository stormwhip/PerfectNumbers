#!/usr/bin/env python3
"""Teichmueller-lift valuation pricing for roots 19, 7, 11, 31, 13.

Standard library only.  Every inequality is an exact integer comparison.
See Readme.md in this directory for the theorem and its proof.

Notation: p is the root prime, p^e || N with e even, A = sigma(p^e),
B = 10^2400.  kappa is the least o-1 over odd divisors o >= 3 of p-1.
"""
from math import gcd, isqrt

B = 10**2400
ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
ROOTS = (19, 7, 11, 31, 13)


def forbidden(p):
    return ORDER[:ORDER.index(p)]


def multiplicative_order(a, p):
    o, x = 1, a % p
    while x != 1:
        x = x * a % p
        o += 1
    return o


def kappa(p):
    odd = [o for o in range(3, p) if (p - 1) % o == 0 and o % 2]
    if not odd:
        raise ValueError("p-1 has no odd divisor >= 3")
    return min(odd) - 1


_SMALL = None


def _small_primorial():
    global _SMALL
    if _SMALL is None:
        flags = bytearray([1]) * 65536
        flags[:2] = b"\x00\x00"
        for i in range(2, 256):
            if flags[i]:
                flags[i * i::i] = bytes(len(flags[i * i::i]))
        prod = 1
        for i in range(3, 65536):
            if flags[i]:
                prod *= i
        _SMALL = prod
    return _SMALL


def may_be_prime(x):
    """False only for proven composites.  Composites passing are kept,
    which can only enlarge the deficit and weaken the bound."""
    if x < 3 or x % 2 == 0:
        return x == 2
    if x < 65536:
        return all(x % d for d in range(3, isqrt(x) + 1, 2))
    if gcd(x, _small_primorial()) != 1:
        return False
    return pow(2, x - 1, x) == 1


def fmin_euler(o):
    """Least f >= 5 with f = 1 (mod 4) and o | f+1 (requires o % 4 != 0)."""
    f = 5
    while (f + 1) % o:
        f += 4
    return f


def deficit_profile(p, top):
    """Exceptional primes up to level `top`.

    Returns (nonEuler, euler):
      nonEuler: list of (t, x, o) with x^(o-1) < p^(kappa*t)
      euler:    list of (t, x, fmin) with x = 1 mod 4 and x^fmin < p^(2t)
    Each x is the least positive lift x_t(a) of the Teichmueller
    representative of a modulo p^t, counted at its exact level.
    """
    kap = kappa(p)
    forb = set(forbidden(p))
    classes = []
    for a in range(2, p):
        o = multiplicative_order(a, p)
        if o >= 3 and o % 4:
            classes.append((a, o))
    non_euler, euler = [], []
    for a, o in classes:
        seq = [None, a]
        mod = p
        for t in range(2, top + 2):
            mod *= p
            seq.append(pow(seq[-1], p, mod))
        mod = p
        for t in range(1, top + 1):
            x = seq[t]
            if t > 1:
                mod *= p
            else:
                mod = p
            if x % p != a or pow(x, o, mod) != 1:
                raise AssertionError("Teichmueller lift failed")
            if seq[t + 1] == x:          # exact level of x exceeds t
                continue
            if x % 2 == 0 or x in forb or x == p:
                continue
            # Safe prefilters: x^k < p^n forces k*(bitlen(x)-1) < n*bitlen(p).
            bx, bp = x.bit_length() - 1, p.bit_length()
            ne = (o % 2 == 1 and (o - 1) * bx < kap * t * bp
                  and x**(o - 1) < p**(kap * t))
            fm = fmin_euler(o)
            eu = (x % 4 == 1 and fm * bx < 2 * t * bp
                  and x**fm < p**(2 * t))
            if not (ne or eu):
                continue
            if not may_be_prime(x):
                continue
            if ne:
                non_euler.append((t, x, o))
            if eu:
                euler.append((t, x, fm))
    non_euler.sort()
    euler.sort()
    return non_euler, euler


def ceil_div(a, b):
    return -(-a // b)


def ilog(n, b):
    k, x = 0, b
    while x <= n:
        x *= b
        k += 1
    return k


def max_exponent(p):
    """Profile depth: any exponent above it has p^e*odd(sigma(p^e)) > p^(2e)/2 > B."""
    return ilog(B, p) // 2 + 1


class Profile:
    """U(e) >= prod p^(kappa t)/x^(o-1) over non-Euler deficit primes of level <= e;
    D(e) >= max p^(2t)/x^fmin over Euler deficit primes of level <= e."""

    def __init__(self, p, top=None):
        top = max_exponent(p) if top is None else top
        self.p, self.top, self.kap = p, top, kappa(p)
        self.non_euler, self.euler = deficit_profile(p, top)

    def U(self, e):
        if e > self.top:
            raise ValueError("profile too short")
        k, den = 0, 1
        for t, x, o in self.non_euler:
            if t <= e:
                k += self.kap * t
                den *= x**(o - 1)
        return max(1, ceil_div(self.p**k, den))

    def D(self, e):
        if e > self.top:
            raise ValueError("profile too short")
        best = 1
        for t, x, fm in self.euler:
            if t <= e:
                best = max(best, ceil_div(self.p**(2 * t), x**fm))
        return best


def sigma(p, e):
    return (p**(e + 1) - 1) // (p - 1)


def odd_part(n):
    return n // (n & -n)


def verify_even_exponent(p, e, prof):
    """Return (True, rule) when every odd perfect N <= B with p^e || N,
    e even, and the forbidden roots coprime to N is impossible."""
    if e % 2 or e < 2:
        raise ValueError("even exponent required")
    A = sigma(p, e)
    pe = p**e
    if pe * A > B:
        return True, "base-size"
    if e > prof.top:
        raise AssertionError("p^(2e) <= B contradicts max_exponent")
    if any(A % z == 0 for z in forbidden(p)):
        return True, "forbidden-factor"
    kap = prof.kap
    U = prof.U(e)
    D = prof.D(e)
    # (a) Euler exponent >= 5: N >= p^e * p^(2K)/U * p^(2K_q)/D = p^(3e)/(U D).
    if not p**(3 * e) > B * U * D:
        return False, "euler-exponent-five"
    # (b),(c) Euler exponent 1 with s = v_p(q+1), so q >= 2p^s - 1.
    for s in range(0, e + 1):
        q_lo = 2 * p**s - 1
        if 2 * s <= e:
            ok = q_lo * pe * p**(kap * (e - s)) > B * U
        else:
            # Lemma 3: q does not divide A, so A divides the even-exponent part.
            ok = q_lo * pe * max(A * U, p**(kap * (e - s))) > B * U
        if not ok:
            return False, f"euler-exponent-one-s{s}"
    return True, "teichmuller-valuation"


def verify_odd_root_exponent(p, e, prof):
    """p = 1 (mod 4) is the Euler prime: every other prime has even exponent."""
    if p % 4 != 1 or e % 4 != 1:
        raise ValueError("odd root exponent must be an Euler exponent")
    if e > prof.top:
        raise AssertionError("odd exponent beyond profile")
    if p**(e * (1 + prof.kap)) > B * prof.U(e):
        return True, "teichmuller-valuation-euler-root"
    return False, "euler-root-open"


def check_lemmas(p):
    """Integer side conditions used in the proof (Readme, Lemma 2 and 3)."""
    kap = kappa(p)
    if kap < 2:
        raise AssertionError("kappa >= 2 is required")
    # r = 1 (mod p): r^(p^v-1) >= (2p+1)^((p-1)v) >= p^(kappa v).
    if not kap <= p - 1:
        raise AssertionError("kappa <= p-1")
    # Extra p-adic units from v_p((f+1)/o) = j >= 1 for an even exponent:
    # r^(o(p^j-1)) >= 3^(3(p-1)j) >= p^(kappa j).
    if not 3**(3 * (p - 1)) >= p**kap:
        raise AssertionError("non-Euler LTE increment")
    # Euler exponent: q^(f-fmin) >= 3^(6(p^j-1)) >= p^(2j).
    if not 3**(6 * (p - 1)) >= p**2:
        raise AssertionError("Euler LTE increment")
    # q = -1 (mod p): q^(f-2) >= p^(2p^j-3) >= p^(2j) for j >= 1.
    if not 2 * p - 3 >= 2:
        raise AssertionError("Euler order-two increment")
    return True


def covered_exponents(p, d, exact):
    """All legal actual exponents e <= log_p B represented by the shard."""
    out = []
    e = d
    m = d + 1
    k = 1
    while p**e <= B:
        if e % 2 == 0 or (e % 4 == 1 and p % 4 == 1):
            out.append(e)
        if exact:
            break
        k += 1
        e = k * m - 1
    return out


def verify_shard(p, d, exact, prof):
    """Close a shard if every covered actual exponent is excluded."""
    detail = []
    for e in covered_exponents(p, d, exact):
        ae = odd_part(sigma(p, e))
        if p**e * ae > B:
            detail.append((e, "base-size"))
            continue
        if e % 2:
            if any(ae % z == 0 for z in forbidden(p)):
                detail.append((e, "forbidden-factor"))
                continue
            ok, rule = verify_odd_root_exponent(p, e, prof)
        else:
            ok, rule = verify_even_exponent(p, e, prof)
        detail.append((e, rule))
        if not ok:
            return False, detail
    return True, detail
