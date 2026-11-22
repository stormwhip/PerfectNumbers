# PerfectNumbers — Independent verification integration for 10^2400

Date: 2026-11-22. Base commit: b6b2f4c. Target bound B = 10^2400.
Search reference V21 is frozen. The files in this integration are experimental proof/runner components and do not certify all of B.

## Mathematical obligations

For an odd perfect number N, sigma(N)=2N. Euler's theorem implies N=pi^(4u+1)m^2 with pi=1 (mod 4). Partition by the first divisor of S={3,5,7,11,13,17,19,31} in ROOT_ORDER=(19,7,11,31,13,3,5,17), and the residual coprime class. A different root set defines a different global partition.

Original coprime certificate: log10(N)>=4183.209493; replacement S'=(S-{19})+{23}: 3954.197016. Original complete top-level exponent manifest has 3072 tasks, with counts 3:676, 5:481, 7:412, 11:341, 13:325, 17:297, 19:287, 31:253. Replacement has 3058. These counts indicate coverage obligations, not verified closed searches.

For a standard exponent branch d, require e>=d and (d+1)|(e+1), ensuring sigma(p^d)|sigma(p^e). For an exact exponent branch require e=d. Enumerate all allowable actual exponents below a certified integer size cutoff, then verify the union of the exponent-edge predicates covers them. Odd exact exponents must occupy the single Euler slot and satisfy p=e=1 (mod 4). If q is a target of sigma factors, sum v_q contributions over distinct source primes p; within one source retain only the strongest proved lower bound.

Exact integer lcm of known forced prime powers and certified residual divisors gives a sound size lower bound when overlaps exist; naive multiplication is unsafe (e.g. c=1009*1013 and forced 1009^2). Residual minimum-prime bounds are checked by deterministic trial division or PRIME_CUTOFF_GCD. For primality, probable-prime testing (GMP) is only a search accelerator; the final verifier requires Pratt, Pocklington, exact trial division or a still-to-be-implemented ECPP-equivalent checker. All unsupported rules remain unresolved.

For a roadblock with boundary b, calculate conservative abundance gap Delta_lo and remaining logarithmic size budget M_hi; choose a certified rational multiplier mu and verify the fixed-point dual inequality L_b(mu)>M_hi. Only then may the search enumerate all allowed new q<b in canonical order, forbidding prior candidates in each subsequent child. A conditional/state LP leaf must independently reconstruct its full feasible model and check all nonnegative dual multipliers, tail reduced costs, and an objective lower bound exceeding log B.

## New code and repaired defects

- IndependentVerifierV2.py: externally pinned root states, strict JSON and integer checks, parent-derived DAG, exact leaves and splitting, fixed-point roadblock and rational dual LP checks; F-1 modular obstruction bounded search and F-2 duplicate LP edge rejection applied. PRIME_CUTOFF_GCD verifier uses deterministic sieve.
- VerifierV2Tests.py / VerifierV2AuditTests.py: tampering, false root assumptions, overlap, prime witnesses, roadblock order and conditional LP regression.
- V21FrontierCodec.hpp: V2 state format, preserves forbidden_small append order and composites order, fixes fixed-CIRC_ORDER outer mask, source provenance invariant.
- FrontierLedgerV2.py / FrontierV2FaultTests.py / FrontierV2MixedEdgeTests.py: atomic mixed OPEN/CLOSED edges, persistent evidence, attempt tokens and simulated crash recovery.
- ProofTreeV21Frontier.cpp: immediate-root-prune fix, ordered split metadata, G1 reused probable-prime classification, optional G2/G3 prefilters and no-database mode. It remains an **unaudited experimental solver**.
- AuditRunner2400.py: read-only ledger access, node-content collision rejection, original/replacement manifest binding, strict verified closure criteria.
- FrontierWorkerDriver.py: provisional scheduler adapter. The current C++ metadata is not an IndependentVerifierV2 proof DAG, and CLOSED edges are recorded as deliberately unaudited.
- SingleFlightFactCache.hpp: standalone thread-safe immutable-value deduplicating cache; **not yet wired into the search**.

## Local verification performed for this integration

Python 3.11 -S -O passed: VerifierV2Tests, VerifierV2AuditTests, FrontierV2FaultTests, AuditRunnerTests, AuditRunnerAuditTests, FrontierV2MixedEdgeTests. C++17 compiled and passed V21FrontierCodecTests; ProofTreeV21Frontier compiled with GMP+OpenMP. A local 16-thread single-flight smoke test performed one shared computation. No-database small-shard smoke cases at bound 10^14 (root 7 shard 0; root 19 shard 0) returned PROGRAM PROVEN_UNAUDITED, not independent closure.

Reproduction:

    for n in VerifierV2Tests VerifierV2AuditTests FrontierV2FaultTests AuditRunnerTests AuditRunnerAuditTests FrontierV2MixedEdgeTests; do python3 -S -O Research/2026-11-22/Python/$n.py || exit 1; done
    g++ -std=c++17 -O2 Sources/Cpp/V21FrontierCodecTests.cpp -lgmpxx -lgmp -o /tmp/opn_codec && /tmp/opn_codec
    g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofTreeV21Frontier.cpp -lgmpxx -lgmp -o /tmp/opn_frontier
    OMP_NUM_THREADS=2 /tmp/opn_frontier bench-nodb 14 7 0 --no-db

## Open blockers in priority order

1. Bridge C++ search to an independently checkable full SPLIT/LEAF DAG, including closed edges and initial root pruning; link worker/ledger/proof-store to verifier with complete replay.
2. Port exact frozen V21 roadblock, circular split, residual strengthening and prefix/state LP semantics. The new C++ currently returns UNRESOLVED when it needs a roadblock; it cannot replace V21 on real 66/132/138/149 shards.
3. Certify all prime factors from real searches with deterministic certificates and implement a checkable large-prime fallback; conduct exhaustive mathematical soundness and mutation tests for all proof rules.
4. Connect and measure the single-flight cache with strict key (p,d+1) and unchanged remainder; run and compare real hard root-19 shards 0/100, which remained unfinished in short (20-second) paired pilots.
5. Run and independently verify all 3072 original-root shard proof DAGs, alongside the original terminal certificate. Require zero gaps, zero unresolved/failed, zero unchecked primality, zero open frontier.
6. Measure complete end-to-end wall time, including preparation, search, proof writing and verification, with fixed hardware/dataset/rules. For identical greedy slots J on a dependency DAG, the scheduling upper bound is T_search <= W_eff/J+(1-1/J)C with total work W_eff and critical path C, subject to all time overheads being represented. Short timeout samples do not establish a 72-hour bound.

Current final theorem status: INCOMPLETE_FRONTIER. No full 10^2400 proof or 72-hour benchmark is asserted.
