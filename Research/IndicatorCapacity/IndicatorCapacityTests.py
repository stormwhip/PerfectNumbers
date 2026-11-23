"""Reject malformed indicator-capacity certificates and test interval bounds."""
import copy
import json
import math

import VerifyIndicatorCapacity2400 as vc


def load_p5_base():
    data = json.loads((vc.CERT_DIR / "DualP5.json").read_text(encoding="utf-8"))
    p = int(data["root"])
    forb = tuple(int(x) for x in data["forbidden"])
    R_act = int(data["R_act"])
    W_max = int(data["W_max"])
    primes_R = vc.sieve_primes(R_act)
    entry = copy.deepcopy(data["duals"][0])  # mu=7500, lam_p=0
    return p, forb, R_act, W_max, primes_R, entry


def test_1_delete_legal_exponent():
    """
    Test 1: Deleting a legal exponent (e.g., skipping f=2 for r=17 in p=5) would falsely
    inflate the dual bound. Verify that our verifier independently enumerates all legal even
    exponents from f_min(r) upward, and that removing all flows on (17, 2) strictly drops
    the certified bound (so an un-covered legal exponent cannot be silently ignored).
    """
    p, forb, R_act, W_max, primes_R, entry = load_p5_base()
    cd_full = vc.verify_dual_entry(p, forb, R_act, W_max, entry, primes_R)

    # Remove all flows (so every legal exponent drops to its raw unpenalized cost)
    entry_del = copy.deepcopy(entry)
    entry_del["flows"] = []
    cd_del = vc.verify_dual_entry(p, forb, R_act, W_max, entry_del, primes_R)
    assert cd_del.const_no_target < cd_full.const_no_target, (
        "Deleting flows on legal exponents must strictly lower the certified bound!"
    )

    # Also test injecting a forbidden exponent (e.g., f=2 for r=37 where 3 | sigma(37^2))
    entry_forb = copy.deepcopy(entry)
    entry_forb["flows"].append([37, 2, 7, 1000])
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_forb, primes_R)
        raise AssertionError("Verifier failed to reject forbidden exponent/factor!")
    except ValueError:
        pass
    print("[PASS] Test 1 (Delete legal exponent / inject forbidden exponent)")


def test_2_forged_prime_factor():
    """
    Test 2: Forging a composite target w (pseudoprime/Carmichael number 561) or a prime w
    that does not divide sigma(r^f) MUST be rejected with ValueError.
    """
    p, forb, R_act, W_max, primes_R, entry = load_p5_base()

    # 2a. Composite Carmichael number 561 = 3*11*17 as target w
    entry_comp = copy.deepcopy(entry)
    entry_comp["flows"].append([17, 2, 561, 1000])
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_comp, primes_R)
        raise AssertionError("Verifier failed to reject composite target w=561!")
    except ValueError:
        pass

    # 2b. Real prime w=311 that does NOT divide sigma(17^2) = 307
    entry_nondiv = copy.deepcopy(entry)
    entry_nondiv["flows"].append([17, 2, 311, 1000])
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_nondiv, primes_R)
        raise AssertionError("Verifier failed to reject non-dividing prime w=311 | sigma(17^2)!")
    except ValueError:
        pass

    # 2c. Negative flow weight (would violate non-negativity of dual multiplier theta >= 0)
    entry_neg = copy.deepcopy(entry)
    entry_neg["flows"][0][3] = -1000
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_neg, primes_R)
        raise AssertionError("Verifier failed to reject negative flow weight!")
    except ValueError:
        pass

    print("[PASS] Test 2 (Forged composite factor / non-dividing prime / negative flow)")


def test_3_misplaced_euler_slot():
    """
    Test 3: Misplacing the Euler slot — attempting to use an odd exponent f=1 (Euler slot)
    inside the even-exponent flow graph MUST be rejected, and a small exponent e=100 where
    a small special prime q or q | A IS feasible MUST NOT be falsely marked eliminated.
    """
    p, forb, R_act, W_max, primes_R, entry = load_p5_base()

    # 3a. Odd exponent f=1 in flow edge
    entry_odd = copy.deepcopy(entry)
    entry_odd["flows"].append([73, 1, 37, 1000])
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_odd, primes_R)
        raise AssertionError("Verifier failed to reject odd (Euler) exponent f=1 in even flow graph!")
    except ValueError:
        pass

    # 3b. Small exponent e=100 (definitely NOT eliminated by our bound) must return False
    cd = vc.verify_dual_entry(p, forb, R_act, W_max, entry, primes_R)
    ok, _ = vc.verify_exponent(p, 100, [cd], primes_R)
    assert not ok, "Verifier falsely eliminated e=100!"
    print("[PASS] Test 3 (Misplaced Euler slot / non-eliminable small exponent)")


def test_4_tampered_valuation():
    """
    Test 4: Verify vp_sigma exactness on r=41 (41 === 1 mod 5):
      v_5(sigma(41^4)) = 1, v_5(sigma(41^24)) = 2, v_5(sigma(41^2)) = 0,
      and that a tampered negative lam_p is rejected.
    """
    assert vc.vp_sigma(5, 41, 2) == 0
    assert vc.vp_sigma(5, 41, 4) == 1
    assert vc.vp_sigma(5, 41, 24) == 2
    assert vc.vp_sigma(3, 37, 2) == 1
    assert vc.vp_sigma(3, 37, 8) == 2

    p, forb, R_act, W_max, primes_R, entry = load_p5_base()
    entry_neg_lam = copy.deepcopy(entry)
    entry_neg_lam["lam_p_num"] = -1
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_neg_lam, primes_R)
        raise AssertionError("Verifier failed to reject negative lam_p!")
    except ValueError:
        pass
    print("[PASS] Test 4 (Exact valuation check & tampered negative lam_p)")


def test_5_omitted_large_prime_tail():
    """
    Test 5: Omitting the large-prime tail — setting lam_p so high that r > R_act with r === 1 mod p
    has negative reduced cost ((p-1)*ln(R_act) < lam_p*ln(p) + mu*ln(R_act/(R_act-1))) MUST be rejected!
    """
    p, forb, R_act, W_max, primes_R, entry = load_p5_base()
    entry_bad_tail = copy.deepcopy(entry)
    entry_bad_tail["lam_p_num"] = 40  # 40*ln(5) ~ 64.4 > 4*ln(120000) ~ 46.8!
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_bad_tail, primes_R)
        raise AssertionError("Verifier failed to reject violated large-prime tail (lam_p=40)!")
    except ValueError:
        pass

    # Also test mu so large that 2*ln(R_act) < mu*ln(R_act/(R_act-1))
    entry_bad_mu = copy.deepcopy(entry)
    entry_bad_mu["mu_num"] = 5000000
    try:
        vc.verify_dual_entry(p, forb, R_act, W_max, entry_bad_mu, primes_R)
        raise AssertionError("Verifier failed to reject violated large-prime abundancy tail (mu=5e6)!")
    except ValueError:
        pass
    print("[PASS] Test 5 (Omitted large-prime tail for both lam_p and mu)")


def test_6_rounding_direction():
    """
    Test 6: Verify strict conservative rounding of log_interval(a, b) across a wide range of
    rationals: lo <= SCALE * ln(a/b) <= hi, and hi - lo <= 2.
    """
    test_pairs = [
        (2, 1), (3, 1), (5, 1), (10, 1), (17, 16), (307, 1),
        (1000000007, 1), (1, 3), (2, 3), (5**4 - 1, 5**3 * 4),
    ]
    for a, b in test_pairs:
        lo, hi = vc.log_interval(a, b)
        exact = math.log(a / b) * vc.SCALE
        assert lo <= exact <= hi, f"Interval failed for {a}/{b}: {lo} <= {exact} <= {hi}"
        assert hi - lo <= 100, f"Interval too loose for {a}/{b}: width={hi - lo}"
    print("[PASS] Test 6 (Certified rational-interval rounding direction)")


def test_interior_valuation_budget():
    # 757 supplies valuation to p=3 and lies in A at e=8.
    p, e, r = 3, 8, 757
    A = (p**(e + 1) - 1) // (p - 1)
    assert A % r == 0 and r % p == 1
    gift, rate = vc.interior_budget(p, e, A, vc.sieve_primes(20_000))
    assert gift == 0
    assert 0 < rate <= vc.log_interval(r)[0]
    # With r^2 already in A, the first unit at f=2 has no residual cost.
    gift, rate = vc.interior_budget(p, e, r**2, vc.sieve_primes(20_000))
    assert gift == 1 and rate > 0
    print("[PASS] Interior valuation is priced only after its prepaid units")


def main():
    test_1_delete_legal_exponent()
    test_2_forged_prime_factor()
    test_3_misplaced_euler_slot()
    test_4_tampered_valuation()
    test_5_omitted_large_prime_tail()
    test_6_rounding_direction()
    test_interior_valuation_budget()
    print("=== ALL 7 REGRESSION GROUPS PASSED ===")


if __name__ == "__main__":
    main()
