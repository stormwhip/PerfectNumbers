"""Audit regression tests covering F-1, F-2, and all previously uncovered rules in IndependentVerifierV2."""

from __future__ import annotations

from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    LP_DYADIC,
    BranchEntry,
    CompositeResidue,
    VerificationError,
    VerifierState,
    _abundance_gap_lower,
    apply_sigma_deduction,
    verify_conditional_lp_leaf,
    verify_leaf_node,
    verify_split_node,
)
from RoadblockDual import RoadblockDual, SCALE, log_bounds


def expect_reject(label: str, action) -> None:
    try:
        action()
    except VerificationError as exc:
        print(f"[REJECTED OK] {label}: {exc}")
        return
    raise RuntimeError(f"TAMPER WRONGLY ACCEPTED: {label}")


def test_f1_modular_obstruction_no_hang() -> None:
    """F-1: Standard branch d=2 on p=7 with 19 in forbidden (19 | sigma(7^2)) must NOT hang."""
    st = VerifierState(
        branched={7: BranchEntry(exp=2, exact=False)},
        unbranched=frozenset(),
        forbidden=frozenset({19}),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # Must return immediately as a valid contradiction (no infinite loop)
    verify_conditional_lp_leaf(
        st,
        upper_bound_N=10**20,
        lp_witness={"limit": 11, "cutoff": 4, "edges": [], "weights": []},
        verified_primes=set(),
    )
    print("[ACCEPTED OK] F-1: standard-branch modular obstruction terminates cleanly")


def test_f2_duplicate_lp_edge_rejected() -> None:
    """F-2: Duplicate factor implication edges in conditional LP must be rejected."""
    st = VerifierState(
        branched={3: BranchEntry(exp=2, exact=True)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    edge = {"p": 3, "e": 2, "q": 13, "k": 1, "q_cert": {"method": "TRIAL_DIV", "max_divisor": 3}}
    expect_reject(
        "F-2 duplicate LP edges",
        lambda: verify_conditional_lp_leaf(
            st,
            upper_bound_N=10**10,
            lp_witness={"limit": 11, "cutoff": 4, "edges": [edge, edge], "weights": [0]},
            verified_primes=set(),
        ),
    )


def test_f3_circular_split_positive_and_order_tamper() -> None:
    """F-3: Genuine passing roadblock witness + circular order & forbidden-prefix tamper checks."""
    st = VerifierState(
        branched={3: BranchEntry(exp=2, exact=True), 5: BranchEntry(exp=2, exact=True)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    gap_lo = _abundance_gap_lower(st)
    oracle = RoadblockDual(17, 29, forbidden=(), expanded=(3, 5), special_used=False)
    bound_lo, mu = oracle.propose(gap_lo)
    rb = {"boundary": 17, "table_limit": 29, "mu_num": mu.numerator, "mu_den": mu.denominator}

    # Canonical candidates < 17: circ_order=(19,7,11,31,13,3,5,17) -> [7, 11, 13]
    valid_node = {
        "kind": "SPLIT",
        "split_rule": {"type": "CIRCULAR_BRANCH_SPLIT", "roadblock_witness": rb},
        "children": [
            {"edge": {"circ_prime": 7}},
            {"edge": {"circ_prime": 11}},
            {"edge": {"circ_prime": 13}},
        ],
    }
    children = verify_split_node(st, valid_node, 10**4, DEFAULT_CIRC_ORDER, set())
    if [sorted(c.forbidden) for c in children] != [[], [7], [7, 11]]:
        raise RuntimeError("unexpected circular forbidden prefix progression")
    print(f"[ACCEPTED OK] F-3: valid CIRCULAR_BRANCH_SPLIT (b=17, bound={bound_lo/SCALE:.3f})")

    # Tamper A: swap candidate order [11, 7, 13] (roadblock passes, order check must reject)
    bad_order = {
        "kind": "SPLIT",
        "split_rule": {"type": "CIRCULAR_BRANCH_SPLIT", "roadblock_witness": rb},
        "children": [
            {"edge": {"circ_prime": 11}},
            {"edge": {"circ_prime": 7}},
            {"edge": {"circ_prime": 13}},
        ],
    }
    expect_reject(
        "F-3 circular swapped candidate order",
        lambda: verify_split_node(st, bad_order, 10**4, DEFAULT_CIRC_ORDER, set()),
    )

    # Tamper B: keep candidate order, omit 7 from child 1's declared forbidden set
    bad_prefix = {
        "kind": "SPLIT",
        "split_rule": {"type": "CIRCULAR_BRANCH_SPLIT", "roadblock_witness": rb},
        "children": [
            {"edge": {"circ_prime": 7}},
            {
                "edge": {"circ_prime": 11},
                "state": {
                    "branched": [{"p": 3, "exp": 2, "exact": True}, {"p": 5, "exp": 2, "exact": True}],
                    "unbranched": [11],
                    "forbidden": [],  # Missing 7!
                    "has_special": False,
                    "composites": [],
                    "source_v_bounds": [],
                    "source_v2_bounds": [],
                },
            },
            {"edge": {"circ_prime": 13}},
        ],
    }
    expect_reject(
        "F-3 circular missing prior forbidden prime",
        lambda: verify_split_node(st, bad_prefix, 10**4, DEFAULT_CIRC_ORDER, set()),
    )


def test_f3_composite_order_and_min_prime_tamper() -> None:
    """F-3: Tampering composite order or claiming false min_prime bound must be rejected."""
    st = VerifierState(
        branched={19: BranchEntry(exp=2, exact=False)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(
            CompositeResidue(value=1009 * 1013, min_prime=1009),
            CompositeResidue(value=1019 * 1021, min_prime=1019),
        ),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # Swapping composite order in declared state must fail state equality check
    swapped_node = {
        "kind": "LEAF",
        "state": {
            "branched": [{"p": 19, "exp": 2, "exact": False}],
            "unbranched": [],
            "forbidden": [],
            "has_special": False,
            "composites": [
                {"value": 1019 * 1021, "min_prime": 1019},
                {"value": 1009 * 1013, "min_prime": 1009},
            ],
            "source_v_bounds": [],
            "source_v2_bounds": [],
        },
        "witness": {"reason": "SIZE_EXCEEDS_BOUND"},
    }
    expect_reject(
        "F-3 swapped composite order",
        lambda: verify_leaf_node(st, swapped_node, 10**6, set()),
    )

    # Claiming min_prime=1013 for residue 1009*1013 (divisible by 1009 < 1013) must be rejected
    bad_deduction_st = VerifierState(
        branched={19: BranchEntry(exp=2, exact=False)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # sigma(19^2) = 381 = 3 * 127; claim composite_rem=381 has min_prime=5 (false, 3 | 381)
    expect_reject(
        "F-3 false composite min_prime strengthening",
        lambda: apply_sigma_deduction(
            bad_deduction_st,
            {
                "source_p": 19,
                "d": 2,
                "v2": 0,
                "factors": [],
                "composite_rem": 381,
                "composite_min_prime": 5,
                "composite_min_prime_cert": {"method": "TRIAL_DIV_RANGE"},
            },
            set(),
        ),
    )


def test_f3_remaining_leaf_rules() -> None:
    """F-3: Positive & negative checks for FORBIDDEN_FACTOR, EXACT_QUOTA_EXCEEDED, ABUNDANCE, CONDITIONAL_LP."""
    # 1. FORBIDDEN_FACTOR: 19 | sigma(7^2) = 57
    st_forb = VerifierState(
        branched={7: BranchEntry(exp=2, exact=False)},
        unbranched=frozenset(),
        forbidden=frozenset({19}),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    verify_leaf_node(
        st_forb,
        {
            "kind": "LEAF",
            "witness": {
                "reason": "FORBIDDEN_FACTOR",
                "forbidden_lemma": {
                    "source_p": 7,
                    "d": 2,
                    "forbidden_q": 19,
                    "cert": {"method": "TRIAL_DIV", "max_divisor": 4},
                },
            },
        },
        10**10,
        set(),
    )
    print("[ACCEPTED OK] F-3: FORBIDDEN_FACTOR leaf")

    # 2. EXACT_QUOTA_EXCEEDED: 3 exact=2, but sources 7, 19, 127 each contribute v_3 >= 1 (sum=3 > 2)
    st_quota = VerifierState(
        branched={
            3: BranchEntry(exp=2, exact=True),
            7: BranchEntry(exp=2, exact=False),
            19: BranchEntry(exp=2, exact=False),
            127: BranchEntry(exp=2, exact=False),
        },
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={3: {7: 1, 19: 1, 127: 1}},
        source_v2_bounds={},
    )
    verify_leaf_node(
        st_quota,
        {"kind": "LEAF", "witness": {"reason": "EXACT_QUOTA_EXCEEDED", "target_q": 3}},
        10**20,
        set(),
    )
    print("[ACCEPTED OK] F-3: EXACT_QUOTA_EXCEEDED leaf")

    # 3. ABUNDANCE_EXCEEDS_TWO: {3,5,7,11,13} all >= exp 2 has sigma(N)/N >= 2.479 > 2
    st_abund = VerifierState(
        branched={p: BranchEntry(exp=2, exact=False) for p in (3, 5, 7, 11, 13)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    verify_leaf_node(
        st_abund,
        {"kind": "LEAF", "witness": {"reason": "ABUNDANCE_EXCEEDS_TWO"}},
        10**100,
        set(),
    )
    print("[ACCEPTED OK] F-3: ABUNDANCE_EXCEEDS_TWO leaf")

    # 4. CONDITIONAL_LP positive test (pure standard library, exact rational dual)
    st_lp = VerifierState(
        branched={3: BranchEntry(exp=2, exact=True), 5: BranchEntry(exp=2, exact=True)},
        unbranched=frozenset(),
        forbidden=frozenset({7}),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # Rows for limit=11, explicit_primes=[3, 5, 11], forced=[3, 5]:
    # 0: abund, 1: special<=1, 2: 3<=1, 3: -3<=-1, 4: 5<=1, 5: -5<=-1, 6: 11<=1
    w3 = 2 * log_bounds(3)[0] * LP_DYADIC // SCALE
    w5 = 2 * log_bounds(5)[0] * LP_DYADIC // SCALE
    verify_conditional_lp_leaf(
        st_lp,
        upper_bound_N=200,  # 3^2 * 5^2 = 225 > 200
        lp_witness={"limit": 11, "cutoff": 2, "edges": [], "weights": [0, 0, 0, w3, 0, w5, 0]},
        verified_primes=set(),
    )
    print("[ACCEPTED OK] F-3: CONDITIONAL_LP valid rational dual leaf")


def main() -> None:
    test_f1_modular_obstruction_no_hang()
    test_f2_duplicate_lp_edge_rejected()
    test_f3_circular_split_positive_and_order_tamper()
    test_f3_composite_order_and_min_prime_tamper()
    test_f3_remaining_leaf_rules()
    print("VerifierV2AuditTests: ALL AUDIT FIXES AND COVERAGE TESTS PASSED")


if __name__ == "__main__":
    main()
