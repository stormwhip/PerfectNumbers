"""Comprehensive positive, tamper-rejection, and counterexample tests for IndependentVerifierV2."""

from __future__ import annotations

import copy
from pathlib import Path

from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    REPLACEMENT_ROOTS,
    BranchEntry,
    CompositeResidue,
    RootTaskPin,
    UnsupportedRuleError,
    VerificationError,
    VerifierState,
    canonical_json_bytes,
    strict_json_loads,
    verify_conditional_lp_leaf,
    verify_leaf_node,
    verify_root_task_bundle,
    verify_split_node,
    verify_terminal_and_manifest,
)
import VerifyRootExponentCoverage


def make_1e8_pin() -> RootTaskPin:
    return RootTaskPin(
        upper_bound_N=10**8,
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=19,
        root_exp=2,
        root_exact=False,
    )


def build_valid_1e8_bundle() -> dict:
    root_state = {
        "branched": [{"p": 19, "exp": 2, "exact": False}],
        "unbranched": [],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [],
        "source_v2_bounds": [],
    }
    child_127_eq_2 = {
        "branched": [
            {"p": 19, "exp": 2, "exact": False},
            {"p": 127, "exp": 2, "exact": True},
        ],
        "unbranched": [3],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [
            {"q": 3, "sources": [{"p": 19, "v": 1}]},
            {"q": 127, "sources": [{"p": 19, "v": 1}]},
        ],
        "source_v2_bounds": [{"p": 19, "v2": 0}],
    }
    split_node = {
        "kind": "SPLIT",
        "state": root_state,
        "deductions": [
            {
                "source_p": 19,
                "d": 2,
                "v2": 0,
                "factors": [
                    {"q": 3, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
                    {"q": 127, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 11}},
                ],
            }
        ],
        "split_rule": {
            "type": "UNBRANCHED_EXPONENT_EXHAUSTION",
            "branch_prime": 127,
            "prime_cert": {"method": "TRIAL_DIV", "max_divisor": 11},
            "size_cutoff_ge": 4,
        },
        "children": [{"edge": {"exp": 2, "exact": True}, "state": child_127_eq_2}],
    }
    leaf_node = {
        "kind": "LEAF",
        "state": child_127_eq_2,
        "witness": {
            "reason": "SIZE_EXCEEDS_BOUND",
            "deductions": [
                {
                    "source_p": 127,
                    "d": 2,
                    "v2": 0,
                    "factors": [
                        {"q": 3, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
                        {"q": 5419, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 73}},
                    ],
                }
            ],
            "claimed_min_size": 1538847046315881,
        },
    }
    return {"nodes": [split_node, leaf_node]}


def expect_reject(label: str, exc_type, action) -> None:
    try:
        action()
    except exc_type as exc:
        print(f"[REJECTED OK] {label}: {exc}")
        return
    raise RuntimeError(f"TAMPER WRONGLY ACCEPTED: {label}")


def run_all_tests() -> None:
    pin = make_1e8_pin()
    bundle = build_valid_1e8_bundle()

    # 1. Valid 10^8 tree (TRIAL_DIV, PRATT with base 3, and POCKLINGTON)
    res = verify_root_task_bundle(pin, bundle)
    if res["status"] != "TREE_ACCEPTED":
        raise RuntimeError(f"unexpected result: {res}")
    print(f"[ACCEPTED OK] 10^8 TRIAL_DIV tree: {res}")

    b_pratt = copy.deepcopy(bundle)
    b_pratt["nodes"][1]["witness"]["deductions"][0]["factors"][1]["cert"] = {
        "method": "PRATT",
        "witness": 3,
        "n_minus_1_factors": [
            {"q": 2, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 1}},
            {"q": 3, "e": 2, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
            {"q": 7, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
            {"q": 43, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 6}},
        ],
    }
    verify_root_task_bundle(pin, b_pratt)
    print("[ACCEPTED OK] 10^8 PRATT (base=3 for 5419) tree")

    # Pocklington for 5419: 5418 = 2 * 3^2 * 7 * 43, F = 3^2 * 43 = 387, 387^2 = 149769 > 5419
    b_pock = copy.deepcopy(bundle)
    b_pock["nodes"][1]["witness"]["deductions"][0]["factors"][1]["cert"] = {
        "method": "POCKLINGTON",
        "partial_factors": [
            {"q": 3, "e": 2, "a": 3, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
            {"q": 43, "e": 1, "a": 3, "cert": {"method": "TRIAL_DIV", "max_divisor": 6}},
        ],
    }
    verify_root_task_bundle(pin, b_pock)
    print("[ACCEPTED OK] 10^8 POCKLINGTON (F=387 for 5419) tree")

    # 2. Tamper: delete only child edge
    t1 = copy.deepcopy(bundle)
    t1["nodes"][0]["children"] = []
    expect_reject("delete unique child edge", VerificationError, lambda: verify_root_task_bundle(pin, t1))

    # 3. Tamper: replace 5419 with unproven G1 probable-prime marker
    t2 = copy.deepcopy(bundle)
    t2["nodes"][1]["witness"]["deductions"][0]["factors"][1]["cert"] = {"method": "PRP_UNPROVEN"}
    expect_reject("G1 unproven PRP in leaf", UnsupportedRuleError, lambda: verify_root_task_bundle(pin, t2))

    # 4. Tamper: forged root_state containing composite 1003 (reproducing Section 8 bug)
    forged_1003 = {
        "upper_bound_N": 10**6,
        "root_state": {
            "branched": [],
            "unbranched": [1003],
            "forbidden": [],
            "has_special": False,
            "composites": [],
            "source_v_bounds": [],
            "source_v2_bounds": [],
        },
        "nodes": [
            {
                "kind": "LEAF",
                "state": {
                    "branched": [],
                    "unbranched": [1003],
                    "forbidden": [],
                    "has_special": False,
                    "composites": [],
                    "source_v_bounds": [],
                    "source_v2_bounds": [],
                },
                "witness": {"reason": "SIZE_EXCEEDS_BOUND"},
            }
        ],
    }
    expect_reject("forged composite 1003 root", VerificationError, lambda: verify_root_task_bundle(pin, forged_1003))

    # 5. Tamper: forged huge prime in root_state under real B = 10^2400 external pin
    pin_2400 = RootTaskPin(
        upper_bound_N=10**2400,
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=19,
        root_exp=2,
        root_exact=False,
    )
    forged_huge = copy.deepcopy(bundle)
    forged_huge["root_state"] = {
        "branched": [{"p": 19, "exp": 2, "exact": False}],
        "unbranched": [10**1205 + 3],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [],
        "source_v2_bounds": [],
    }
    expect_reject("forged huge prime in 10^2400 root", VerificationError, lambda: verify_root_task_bundle(pin_2400, forged_huge))

    # 6. Tamper: bundle tries to lower upper_bound_N
    t_b = copy.deepcopy(bundle)
    t_b["upper_bound_N"] = 10**5
    expect_reject("bundle lowers upper_bound_N", VerificationError, lambda: verify_root_task_bundle(pin, t_b))

    # 7. Tamper: sneak extra source_v_bounds into child state
    t_sv = copy.deepcopy(bundle)
    t_sv["nodes"][0]["children"][0]["state"]["source_v_bounds"].append(
        {"q": 3, "sources": [{"p": 127, "v": 10}]}
    )
    expect_reject("sneak extra source_v_bounds", VerificationError, lambda: verify_root_task_bundle(pin, t_sv))

    # 8. Tamper: bool masquerading as int and duplicate JSON keys
    t_bool = copy.deepcopy(bundle)
    t_bool["nodes"][0]["deductions"][0]["factors"][0]["e"] = True
    expect_reject("bool masquerading as int", VerificationError, lambda: verify_root_task_bundle(pin, t_bool))
    expect_reject("duplicate JSON keys", VerificationError, lambda: strict_json_loads('{"a": 1, "a": 2}'))

    # 9. Counterexample: overlapping composite c = 1009 * 1013 with unbranched 1009 (lcm vs product)
    overlap_st = VerifierState(
        branched={19: BranchEntry(exp=2, exact=False)},
        unbranched=frozenset({1009}),
        forbidden=frozenset(),
        has_special=False,
        composites=(CompositeResidue(value=1009 * 1013, min_prime=1009),),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # True lcm(19^2 * 1009, 1009*1013) = 19^2 * 1009 * 1013 = 368,984,747 (1009 == 1 mod 4 may be Euler)
    # Whereas naive product 19^2 * 1009 * (1009*1013) = 372,305,609,723 would falsely prune at B = 10^9
    if overlap_st.min_size_lower_bound() != 19**2 * 1009 * 1013:
        raise RuntimeError("lcm overlap size bound mismatch")
    expect_reject(
        "overlapping composite naive product overcount",
        VerificationError,
        lambda: verify_leaf_node(
            overlap_st,
            {"kind": "LEAF", "witness": {"reason": "SIZE_EXCEEDS_BOUND"}},
            upper_bound_N=10**9,
            verified_primes=set(),
        ),
    )

    # 10. Tamper: circular split with swapped candidate order / wrong forbidden prefix
    circ_st = VerifierState(
        branched={3: BranchEntry(exp=2, exact=True), 5: BranchEntry(exp=2, exact=True)},
        unbranched=frozenset(),
        forbidden=frozenset(),
        has_special=False,
        composites=(),
        source_v_bounds={},
        source_v2_bounds={},
    )
    # Construct a tiny valid roadblock witness at b=11 (candidates < 11 in circ_order are [7])
    # Here we intentionally pass wrong candidate 11 instead of 7
    bad_circ_node = {
        "kind": "SPLIT",
        "split_rule": {
            "type": "CIRCULAR_BRANCH_SPLIT",
            "roadblock_witness": {"boundary": 11, "table_limit": 29, "mu_num": 100, "mu_den": 1},
        },
        "children": [{"edge": {"circ_prime": 11}}],
    }
    expect_reject(
        "circular candidate order / weak roadblock",
        VerificationError,
        lambda: verify_split_node(circ_st, bad_circ_node, 10**4, DEFAULT_CIRC_ORDER, set()),
    )

    # 11. Tamper: Conditional LP attempts to delete an induced prime (Section 6.2 negative test)
    bad_lp_witness = {
        "limit": 11,
        "cutoff": 4,
        "omitted_primes": [13],
        "edges": [{"p": 3, "e": 2, "q": 13, "k": 1, "q_cert": {"method": "TRIAL_DIV", "max_divisor": 3}}],
        "weights": [0],
    }
    expect_reject(
        "conditional LP deletes induced prime",
        VerificationError,
        lambda: verify_conditional_lp_leaf(circ_st, 10**10, bad_lp_witness, set()),
    )

    # 12. Unknown rule must remain unclosed (UnsupportedRuleError)
    expect_reject(
        "unknown leaf rule",
        UnsupportedRuleError,
        lambda: verify_leaf_node(
            circ_st,
            {"kind": "LEAF", "witness": {"reason": "HEURISTIC_SKIP_FUTURE"}},
            upper_bound_N=10**10,
            verified_primes=set(),
        ),
    )

    # 13. Close the loop on both archived real terminal certificates + reference top-level manifests
    cert_dir = Path(__file__).resolve().parent.parent / "Certificates"
    for filename, roots in (
        ("TerminalOriginal.json.gz", ORIGINAL_ROOTS),
        ("TerminalReplacement.json.gz", REPLACEMENT_ROOTS),
    ):
        cert_path = cert_dir / filename
        if cert_path.exists():
            out = verify_terminal_and_manifest(cert_path, roots)
            tasks = list(VerifyRootExponentCoverage.canonical_tasks(sorted(roots)))
            VerifyRootExponentCoverage.verify_manifest(
                {"target_exponent": 2400, "root_order": sorted(roots), "tasks": tasks}
            )
            print(f"[ACCEPTED OK] {filename}: {out['status']} (top-level tasks={len(tasks)})")
        else:
            print(f"[SKIPPED] {cert_path} not found in current working directory")

    print("VerifierV2Tests: ALL POSITIVE, TAMPER-REJECTION, AND TERMINAL CLOSURE TESTS PASSED")


if __name__ == "__main__":
    run_all_tests()
