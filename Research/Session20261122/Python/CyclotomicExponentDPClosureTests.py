#!/usr/bin/env python3
"""Exact tests and witness-forgery regression for forbidden-exponent DP leaves."""
from CyclotomicExponentDPClosure2400 import (
    BOUND, weighted_cyclotomic_certificate as certificate,
)
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER, ORIGINAL_ROOTS, RootTaskPin,
    VerificationError, verify_root_task_bundle,
)
from DirectRootClosures2400 import direct_root_bundle

EXPECTED = {
    5: (1626, 1636),
    17: (726, 732, 738, 742, 750, 756,
         760, 768, 772, 786, 796),
}

def run() -> None:
    if sum(map(len, EXPECTED.values())) != 13:
        raise RuntimeError("incorrect candidate count")
    for p, exponents in EXPECTED.items():
        forbidden = tuple(sorted(DEFAULT_CIRC_ORDER[:DEFAULT_CIRC_ORDER.index(p)]))
        for d in exponents:
            cert = certificate(p, d, forbidden)
            if cert is None or cert["max_abundance_num"] >= 2*cert["max_abundance_den"]:
                raise RuntimeError(f"missing exact weighted proof for {p}^{d}")
            pin = RootTaskPin(
                upper_bound_N=BOUND,
                root_set=ORIGINAL_ROOTS,
                root_order=DEFAULT_CIRC_ORDER,
                circ_order=DEFAULT_CIRC_ORDER,
                root_prime=p, root_exp=d, root_exact=False,
            )
            bundle = direct_root_bundle(pin)
            if (bundle is None or
                bundle["nodes"][0]["witness"]["reason"] !=
                    "CYCLOTOMIC_FORBIDDEN_EXPONENT_DP" or
                verify_root_task_bundle(pin, bundle)["status"] != "TREE_ACCEPTED"):
                raise RuntimeError(f"independent verifier rejected {p}^{d}")
            bundle["nodes"][0]["witness"]["d"] += 2
            try:
                verify_root_task_bundle(pin, bundle)
            except VerificationError:
                pass
            else:
                raise RuntimeError(f"forged exponent accepted for {p}^{d}")

    f17 = tuple(sorted(DEFAULT_CIRC_ORDER[:DEFAULT_CIRC_ORDER.index(17)]))
    f5 = tuple(sorted(DEFAULT_CIRC_ORDER[:DEFAULT_CIRC_ORDER.index(5)]))
    if certificate(17, 718, f17) is not None:
        raise RuntimeError("nonpositive strict margin was accepted")
    if certificate(5, 1620, f5) is not None:
        raise RuntimeError("nonpositive strict margin was accepted")
    if certificate(17, 726, f17, BOUND-1) is not None:
        raise RuntimeError("forged bound was accepted")
    if certificate(17, 727, f17) is not None:
        raise RuntimeError("odd representative was accepted")
    print("CyclotomicExponentDPClosureTests: PASS (13 exact integer leaves, forged pins rejected)")

if __name__ == "__main__":
    run()
