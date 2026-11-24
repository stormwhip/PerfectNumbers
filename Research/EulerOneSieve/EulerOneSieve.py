#!/usr/bin/env python3
"""Euler-exponent-one sieve for roots 19, 7, 11, 31, 13.  Standard library only.

Strengthens TeichmullerBaseline.verify_even_exponent in the a = 1 branches:
  (R1) level cut: the non-Euler primes supply exactly e - s units of v_p, so
       only deficit primes of Teichmueller level t <= e - s can occur: U(e-s).
  (R2) prime q = j p^s - 1 with j = 2 (mod 4), p not dividing j.  Every j below
       the stopping j is excluded by a witness (R2 prime l | q, Fermat failure,
       R4 size bound with lcm(A, sq(j/2)), or R5 forbidden root | j/2).
  (R3) branch a >= 5 priced by q^a >= max(p^(5s)/D5(s), 5^5).
See Readme.md for statements and proofs.
"""
import json, sys, time
import TeichmullerBaseline as T

B = T.B
LIM = 1 << 16


def small_primes():
    f = bytearray([1]) * LIM
    f[:2] = b"\x00\x00"
    for i in range(2, 256):
        if f[i]:
            f[i * i::i] = bytes(len(f[i * i::i]))
    return [i for i in range(3, LIM) if f[i]]


PR = small_primes()


def lcm(a, b):
    from math import gcd
    return a // gcd(a, b) * b


def square_up(m):
    """prod r^(2 ceil(v_r(m)/2)) over primes r | m (m odd, small)."""
    out, r = 1, 3
    while r * r <= m:
        if m % r == 0:
            v = 0
            while m % r == 0:
                m //= r
                v += 1
            out *= r**(2 * ((v + 1) // 2))
        r += 2
    if m > 1:
        out *= m * m
    return out


def a1_ok(p, e, s, q, prof, A):
    """Exact branch (b)/(c) inequality with q >= the given value."""
    pe, kap, U = p**e, prof.kap, prof.U(e - s)
    if 2 * s <= e:
        return q * pe * p**(kap * (e - s)) > B * U
    return q * pe * max(A * U, p**(kap * (e - s))) > B * U


def sieve_s(p, e, s, prof, A, jcap):
    """Return (ok, witnesses, j_stop).  witnesses[(j)] = l or 0."""
    ps = p**s
    wit = []
    inv = {l: pow(ps, -1, l) for l in PR if l != p}
    j = 2
    while j <= jcap:
        if j % p:
            q = j * ps - 1
            if a1_ok(p, e, s, q, prof, A):
                return True, wit, j
            w = None
            # (R5) q+1 = j p^s divides 2N, so a forbidden root dividing j kills q.
            for z in T.forbidden(p):
                if (j // 2) % z == 0:
                    w = -z
                    break
            if w is not None:
                wit.append((j, w))
                j += 4
                continue
            for l in PR:
                if l != p and j % l == inv[l] and q != l:
                    w = l
                    break
            if w is None and pow(2, q - 1, q) != 1:
                w = 0
            if w is None:
                # (R4) q may be prime.  sigma(q) = q+1 = j p^s, so m = j/2 | N
                # with every prime of m at an even exponent; if q does not
                # divide A, then q, p^e, lcm(A, m') are pairwise coprime.
                if A % q == 0:
                    return False, wit, j
                mq = square_up(j // 2)
                if not (q * p**e * max(lcm(A, mq) * prof.U(e - s),
                                       p**(prof.kap * (e - s)))
                        > B * prof.U(e - s)):
                    return False, wit, j
                w = -1
            wit.append((j, w))
        j += 4
    return False, wit, j


def euler5_profile(p, top):
    """Euler deficit primes for the a >= 5 pricing q^a >= p^(5s)/D5(s).
    Lists (t, x, f0) for x = x_t(a0) = 1 mod 4 at exact level t with x^f0 < p^(5t),
    f0 = lcm(o,2) - 1, o = ord_p(x) >= 3, 4 does not divide o."""
    forb = set(T.forbidden(p))
    out = []
    for a in range(2, p):
        o = T.multiplicative_order(a, p)
        if o < 3 or o % 4 == 0:
            continue
        f0 = (o if o % 2 == 0 else 2 * o) - 1
        seq, mod = [None, a], p
        for t in range(2, top + 2):
            mod *= p
            seq.append(pow(seq[-1], p, mod))
        for t in range(1, top + 1):
            x = seq[t]
            if pow(x, o, p**t) != 1 or x % p != a:
                raise AssertionError("lift")
            if seq[t + 1] == x or x % 4 != 1 or x in forb or x == p:
                continue
            if x**f0 < p**(5 * t) and T.may_be_prime(x):
                out.append((t, x, f0))
    out.sort()
    return out


class Prof2:
    def __init__(self, p):
        self.p = p
        self.base = T.Profile(p)
        self.kap, self.top = self.base.kap, self.base.top
        self.e5 = euler5_profile(p, self.top)

    def U(self, n):
        return self.base.U(n)

    def D5(self, s):
        best = 1
        for t, x, f0 in self.e5:
            if t <= s:
                best = max(best, T.ceil_div(self.p**(5 * t), x**f0))
        return best


def verify(p, e, pr, jcap=10**6):
    """Return (ok, rule, data)."""
    A = T.sigma(p, e)
    pe, kap = p**e, pr.kap
    if pe * A > B:
        return True, "base-size", None
    if any(A % z == 0 for z in T.forbidden(p)):
        return True, "forbidden-factor", None
    # (a') a >= 5, s = b_p(q, a) in [0, e].
    # q is a prime = 1 (mod 4), so q^a >= 5^5 as well.
    for s in range(e + 1):
        U, D = pr.U(e - s), pr.D5(s)
        if not p**(e + kap * (e - s)) * max(p**(5 * s), 3125 * D) > B * U * D:
            return False, f"a5-s{s}", None
    # (b'),(c') a = 1.
    data = []
    for s in range(e + 1):
        if a1_ok(p, e, s, 2 * p**s - 1, pr, A):
            continue
        ok, wit, j = sieve_s(p, e, s, pr, A, jcap)
        if not ok:
            return False, f"a1-s{s}-j{j}", None
        data.append([s, j, wit])
    return True, "euler-one-sieve", data


def check_record(rec, pr):
    """Replay one actual-exponent record from its stored witnesses only."""
    p, e = rec["root"], rec["exponent"]
    A = T.sigma(p, e)
    pe, kap = p**e, pr.kap
    assert e % 2 == 0 and pe * A <= B
    assert not any(A % z == 0 for z in T.forbidden(p))
    for s in range(e + 1):
        U, D = pr.U(e - s), pr.D5(s)
        assert p**(e + kap * (e - s)) * max(p**(5 * s), 3125 * D) > B * U * D, ("a5", s)
    windows = {w[0]: w[1:] for w in rec["proof_data"]["windows"]}
    for s in range(e + 1):
        if a1_ok(p, e, s, 2 * p**s - 1, pr, A):
            assert s not in windows
            continue
        j_stop, wit = windows[s][:2]
        ps = p**s
        assert len(windows[s]) == 2
        assert a1_ok(p, e, s, j_stop * ps - 1, pr, A), ("stop", s)
        need = [j for j in range(2, j_stop, 4) if j % p]
        assert [j for j, _ in wit] == need, ("coverage", s)
        for j, w in wit:
            q = j * ps - 1
            if w > 1:
                assert q % w == 0 and q != w
            elif w == 0:
                assert pow(2, q - 1, q) != 1
            elif w == -1:
                assert A % q != 0
                mq = square_up(j // 2)
                assert q * pe * max(lcm(A, mq) * U_(pr, e, s),
                                    p**(kap * (e - s))) > B * U_(pr, e, s)
            else:
                assert -w in T.forbidden(p) and (j // 2) % (-w) == 0
    return True


def U_(pr, e, s):
    return pr.U(e - s)


def make_record(p, e, pr, jcap):
    ok, rule, data = verify(p, e, pr, jcap)
    if not ok:
        return None, rule
    return {"root": p, "exponent": e, "method": "EulerOneSieve:" + rule,
            "proof_data": {"windows": data,
                           "witness_codes": "l>1: prime l | q; 0: 2^(q-1) != 1 mod q; "
                                            "-1: q not | A and lcm(A, sq(j/2)) bound; "
                                            "-z: forbidden root z | j/2"}}, rule


def check_r3_lemmas(p, smax):
    """Integer side conditions of the a >= 5 pricing (Readme, R3), for 1 <= s, j <= smax."""
    import math
    lp, l3 = math.log(p), math.log(3)
    for s in range(1, smax + 1):
        # order 1: a >= 2p^s - 1, q >= 2p + 1 > p, so q^a > p^(2p^s - 1) >= p^(5s)
        assert 2 * p**s - 1 >= 5 * s
        # order 2, j = s >= 1: 2p^j - 1 >= 5 + 5j (gives t(2p^j-1) >= 5t + 5j for t >= 1)
        assert 2 * p**s - 1 >= 5 + 5 * s
    # order o >= 3: 3^(6(p^j-1)) >= p^(5j); 6(p^j-1) ln 3 >= 5 j ln p, checked exactly for j <= 3,
    # and for j >= 3 the left side grows by a factor >= p while the right grows additively.
    for j in range(1, 4):
        assert 3**(6 * (p**j - 1)) >= p**(5 * j)
    assert 6 * (p - 1) * l3 > 5 * lp
    return True


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", type=str, help="JSON list of [p,e] to try")
    ap.add_argument("--jcap", type=int, default=40000)
    ap.add_argument("--records", type=str, default="ActualExponentRecords.json")
    ap.add_argument("--proved", type=str, default="proved.json")
    ap.add_argument("--check", type=str, help="replay a records file")
    a = ap.parse_args()
    profs = {}
    if a.search:
        recs, proved = [], []
        for p, e in json.load(open(a.search)):
            pr = profs.setdefault(p, Prof2(p))
            t0 = time.time()
            rec, rule = make_record(p, e, pr, a.jcap)
            print(p, e, rule, round(time.time() - t0, 2), flush=True)
            if rec:
                recs.append(rec)
                proved.append([p, e])
        json.dump(recs, open(a.records, "w"))
        json.dump(proved, open(a.proved, "w"))
    if a.check:
        recs = json.load(open(a.check))
        for p in T.ROOTS:
            T.check_lemmas(p)
            check_r3_lemmas(p, 60)
        for rec in recs:
            pr = profs.setdefault(rec["root"], Prof2(rec["root"]))
            check_record(rec, pr)
            print("replayed", rec["root"], rec["exponent"], "ok", flush=True)
        print("all", len(recs), "records replayed")


if __name__ == "__main__":
    main()

