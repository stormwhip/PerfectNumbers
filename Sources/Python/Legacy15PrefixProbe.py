#!/usr/bin/env python3
"""Profile all consecutive 15-prime exclusion prefix LP lower bounds for 2400.

This inexpensive one-dimensional study determines whether returning to the
original Ochem--Rao prime list would allow late-root automatic elimination.
"""
import time
from IntervalCertificate61 import solve_and_certify

ROOTS15=(127,19,7,11,331,31,97,61,13,398581,1093,3,5,307,17)
for i in range(len(ROOTS15)+1):
    forbidden=set(ROOTS15[:i])
    start=time.monotonic()
    primal,rigorous=solve_and_certify(
        forbidden_S=forbidden,P_max=4000,a_cut=16,certify=True)
    print(f"FIFTEEN_PREFIX count={i} last_excluded={ROOTS15[i-1] if i else 0} "
          f"next_root={ROOTS15[i] if i<len(ROOTS15) else 0} "
          f"float={primal:.12f} interval={rigorous:.12f} "
          f"greater_2400={int(rigorous>2400)} "
          f"elapsed={time.monotonic()-start:.4f}",flush=True)
