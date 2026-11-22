#!/usr/bin/env python3
"""Regression and forgery-rejection tests for finite-quotient leaves."""
from FiniteQuotientClosure2400 import (
    BOUND, ROOT_ORDER, TARGETS, finite_quotient_certificate,
    factor, sigma_from_factorization, spf_table,
)


def expect_invalid(fn) -> None:
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError("a forged finite-quotient pin was accepted")


def run() -> None:
    table = spf_table(1_411_815)
    for n in (1, 3, 9, 405, 480249, 693693, 1411815):
        fs = factor(n, table)
        product = 1
        for p, e in fs:
            product *= p**e
        if product != n:
            raise RuntimeError(f"factorization mismatch: {n}")
        actual = sigma_from_factorization(fs)
        expected = sum(i for i in range(1, n + 1) if n % i == 0)
        if actual != expected:
            raise RuntimeError(f"sigma mismatch: {n}")

    expected = {
        (19, 936): (1411815, 705908, 2),
        (11, 1150): (56941, 28471, 0),
        (11, 1152): (3, 2, 0),
    }
    for p, d in TARGETS:
        forbidden = tuple(ROOT_ORDER[:ROOT_ORDER.index(p)])
        r = finite_quotient_certificate(p, d, forbidden)
        v = expected[(p, d)]
        if ((r["quotient_max"], r["quotients_checked"],
             r["rejection_counts"].get("OVER_ABUNDANCE", 0)) != v
                or r["unresolved"] != 0):
            raise RuntimeError(f"finite quotient mismatch: {r}")

    expect_invalid(lambda: finite_quotient_certificate(19, 938, ()))
    expect_invalid(lambda: finite_quotient_certificate(11, 1150, (19,)))
    expect_invalid(lambda: finite_quotient_certificate(11, 1150, (19, 7), BOUND - 1))
    print("FiniteQuotientClosureTests: PASS (734381 odd quotients exhausted, no open leaf)")


if __name__ == "__main__":
    run()
