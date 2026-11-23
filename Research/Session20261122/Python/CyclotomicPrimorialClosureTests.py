#!/usr/bin/env python3
"""Regression for exact cyclotomic/Euler primorial root leaves."""
from CyclotomicPrimorialClosure2400 import (
    BOUND, cyclotomic_primorial_certificate as certificate,
)
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER, ORIGINAL_ROOTS, RootTaskPin,
    VerificationError, verify_root_task_bundle,
)
from DirectRootClosures2400 import direct_root_bundle

EXPECTED = {
    11: (1152,),
    5: (1656, 1662, 1666, 1668, 1692, 1696, 1698, 1708),
    17: (808, 810, 820, 822, 826, 828, 838, 852, 856,
         858, 862, 876, 880, 882, 886, 906, 910, 918,
         928, 936, 940, 946, 952, 966, 970),
}

def run() -> None:
    for p, ds in EXPECTED.items():
        forbidden = tuple(sorted(DEFAULT_CIRC_ORDER[:DEFAULT_CIRC_ORDER.index(p)]))
        for d in ds:
            result = certificate(p, d, forbidden)
            if result is None:
                raise RuntimeError(f"expected rational proof for {p}^{d}")
            if result["max_abundance_num"] >= 2 * result["max_abundance_den"]:
                raise RuntimeError("rational upper bound does not exclude abundance=2")
    if sum(map(len, EXPECTED.values())) != 34:
        raise RuntimeError("unexpected candidate census")
    if certificate(17, 808, ()) is not None:
        raise RuntimeError("unauthorized missing forbidden-prefix closure")
    if certificate(17, 808, tuple(sorted(DEFAULT_CIRC_ORDER[:-1])), BOUND - 1) is not None:
        raise RuntimeError("unapproved bound")
    if certificate(19, 936, ()) is not None:
        raise RuntimeError("failed positive-margin check")
    if certificate(5, 1657, ()) is not None:
        raise RuntimeError("even-exponent assumption violated")

    for p, d in ((5, 1656), (17, 808)):
        pin = RootTaskPin(
            upper_bound_N=BOUND,
            root_set=ORIGINAL_ROOTS,
            root_order=DEFAULT_CIRC_ORDER,
            circ_order=DEFAULT_CIRC_ORDER,
            root_prime=p, root_exp=d, root_exact=False,
        )
        bundle = direct_root_bundle(pin)
        if (bundle is None
                or bundle["nodes"][0]["witness"]["reason"] != "CYCLOTOMIC_EULER_PRIMORIAL"
                or verify_root_task_bundle(pin, bundle)["status"] != "TREE_ACCEPTED"):
            raise RuntimeError(f"verifier failed genuine primorial proof for {p}^{d}")
        bundle["nodes"][0]["witness"]["d"] += 2
        try:
            verify_root_task_bundle(pin, bundle)
        except VerificationError:
            pass
        else:
            raise RuntimeError("forged source exponent accepted")
    print("CyclotomicPrimorialClosureTests: PASS (34 bounds, 33 additional root leaves)")

if __name__ == "__main__":
    run()
