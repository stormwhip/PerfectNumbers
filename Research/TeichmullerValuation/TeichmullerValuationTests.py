"""Brute-force checks of the valuation identities and single-prime bounds."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import VerifyTeichmullerValuation2400 as tv


def primes(n):
    flags = bytearray([1]) * (n + 1)
    flags[:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytes(len(flags[i * i::i]))
    return [i for i in range(n + 1) if flags[i]]


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


SMALL = primes(6000)
TOP = 12          # profile depth used by the brute-force tests


def profiles():
    return {p: tv.Profile(p, TOP) for p in tv.ROOTS}


def deficit_of(prof, r):
    """Exact non-Euler and Euler deficit integers recorded for prime r."""
    ne = [tv.ceil_div(prof.p**(prof.kap * t), x**(o - 1))
          for t, x, o in prof.non_euler if x == r]
    eu = [tv.ceil_div(prof.p**(2 * t), x**fm) for t, x, fm in prof.euler if x == r]
    return (ne[0] if ne else 1), (eu[0] if eu else 1)


def test_valuation_identity():
    """v_p(sigma(r^f)) = [o | f+1](lambda(r) + v_p((f+1)/o)) for o > 1."""
    for p in tv.ROOTS:
        for r in SMALL[1:120]:
            if r == p:
                continue
            o = tv.multiplicative_order(r, p)
            lam = vp(r**o - 1, p)
            for f in range(1, 80):
                v = vp((r**(f + 1) - 1) // (r - 1), p)
                if o == 1:
                    assert v == vp(f + 1, p)
                elif (f + 1) % o:
                    assert v == 0
                else:
                    assert v == lam + vp((f + 1) // o, p)
    print("[PASS] valuation identity")


def test_teichmuller_levels():
    """Every prime r < p^t of level >= t equals the recorded lift x_t(r mod p)."""
    for p in (7, 11, 13):
        for t in (1, 2, 3):
            mod = p**t
            for r in SMALL:
                if r >= mod or r == p:
                    continue
                o = tv.multiplicative_order(r, p)
                if pow(r, o, mod) != 1:
                    continue
                assert r == pow(r % p, p**(t - 1), mod), (p, t, r)
    print("[PASS] Teichmueller lifts")


def test_single_prime_bounds(profs):
    """Lemma 1 and Lemma 2 by brute force for small primes and exponents."""
    for p, prof in profs.items():
        forb = set(tv.forbidden(p))
        for r in SMALL[1:]:
            if r == p or r in forb:
                continue
            dne, deu = deficit_of(prof, r)
            for f in range(2, 60, 2):
                k = vp((r**(f + 1) - 1) // (r - 1), p)
                if k > TOP:
                    continue
                assert r**f * dne >= p**(prof.kap * k), (p, r, f)
            if r % 4 == 1:
                for f in range(5, 62, 4):
                    k = vp((r**(f + 1) - 1) // (r - 1), p)
                    if k > TOP:
                        continue
                    assert r**f * deu >= p**(2 * k), (p, r, f)
    print("[PASS] single-prime lower bounds")


def test_deficit_needed(profs):
    """Removing a recorded deficit breaks Lemma 1 for that prime."""
    prof = profs[19]
    assert any(x == 7 for _, x, _ in prof.non_euler)
    # 7 has order 3 mod 19 and 7^3 - 1 = 2 * 3^2 * 19, level 1, sigma(7^2) = 3 * 19.
    assert vp(7**2 + 7 + 1, 19) == 1 and 7**2 < 19**2
    assert deficit_of(prof, 7)[0] > 1
    print("[PASS] deficit table records 7 for root 19")


def test_lemmas_and_rules():
    for p in tv.ROOTS:
        assert tv.check_lemmas(p)
    assert [tv.kappa(p) for p in tv.ROOTS] == [2, 2, 4, 2, 2]
    for p in tv.ROOTS:
        assert all(tv.fmin_euler(o) % 4 == 1 and (tv.fmin_euler(o) + 1) % o == 0
                   for o in range(3, p) if o % 4)
    # Composites are kept only if they are base-2 pseudoprimes.
    assert not tv.may_be_prime(65537 * 65539)
    assert tv.may_be_prime(65537)
    print("[PASS] side lemmas")


def test_shards():
    prof = tv.Profile(7)
    ok, detail = tv.verify_shard(7, 1380, False, prof)
    assert ok and detail == [(1380, "teichmuller-valuation")]
    ok, detail = tv.verify_shard(7, 1128, False, prof)
    assert not ok
    # A forged empty profile must not close more than the true one.
    forged = tv.Profile(7)
    forged.non_euler = []
    assert forged.U(1000) == 1 < prof.U(1000)
    print("[PASS] shard decisions")


if __name__ == "__main__":
    test_valuation_identity()
    test_teichmuller_levels()
    test_lemmas_and_rules()
    profs = profiles()
    test_single_prime_bounds(profs)
    test_deficit_needed(profs)
    test_shards()
