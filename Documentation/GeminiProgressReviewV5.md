# Gemini V5 Progress Integration — 2026-11-23

## Provenance and acceptance

Source: [full user-supplied Gemini report](../Research/Session20261123/Reports/ResearchResultV5.md) (archive path relative to this document: `../Research/Session20261123/Reports/ResearchResultV5.md`). The report describes experiments carried out by Gemini on Apple A18 Pro, Python 3.14.7 and C++17, including its claimed independent checker and adversarial tests.

**Repository verification status:** `EXTERNAL_REPORTED_PENDING_REPLAY`. The uploaded v5 report provides the full experimental `Rho128.cpp` source and textual results, but **not** the named primal/dual JSON certificates, manifests, 31 DAG JSON files, Python verifier modules, LP builder, milestone orchestrators, or all C++ executables. Consequently this commit does not elevate the report's `REPRODUCED_VERIFIED` labels to an independently reproduced repository-wide theorem. The report's 6.208 s figure is *verification of available closed tasks in Gemini's environment*, not an end-to-end 72-hour completion.

## Claimed v5 totals

| Root | Total | Claimed verified closed | Remaining open |
| ---: | ---: | ---: | ---: |
| 19 | 287 | 133 | 154 |
| 7 | 412 | 197 | 215 |
| 11 | 341 | 159 | 182 |
| 31 | 253 | 118 | 135 |
| 13 | 325 | 153 | 172 |
| 3 | 676 | 321 | 355 |
| 5 | 481 | 301 | 180 |
| 17 | 297 | 297 | 0 |
| **Total** | **3,072** | **1,679** | **1,393** |

Relative to the preceding Gemini report, the closed count increases by **30** and open count drops by **30**. Previous report's `P13_I00165` closure is **not reproduced**, remains OPEN and is tagged `REPORTED_ONLY`. Closed tasks within v5: 1,447 baseline I–V, 125 full C8, 73 rule-VI, 3 corrected rule-VII, and 31 proof DAG rule-VIII. Counts sum to 1,679.

Claimed whole-class LP bounds:
- `C_infinity`: `log10(N) >= 4195.086839541` (`TerminalCoprimeCertificate.json`).
- `C8` (root 17): `log10(N) >= 2936.543650157` (`ClassC8Certificate.json`).

Claims for new cuts:
- Root 5 `Root5_Ultra_V3Certificate.json`: residual `log10(Q_other) >= 865.2271`, 72 conditional LP shard closures, plus two corrected numerical-lift closures, hence 301/481 root-5 shards closed.
- Root 3 `Root3_Ultra_V3Certificate.json`: base 28.5299 decimal-digit lower bound, and `P3_I00368` improved to 2436.5350 through a corrected lift.
- Rule VIII: 31 certified factor-chain DAGs claimed (8,997 nodes); 18 of 19 previously reported DAGs reproduced, 13 newly found.
- Root-5 presence split on prime 17: exclusion branch has lower bound `log10(Q_other) >= 1100.4484`; **96 items on this one branch are NOT 96 globally closed tasks**; the complementary presence branch remains necessary.
- Root-3 presence split on prime 5: the `5|N` branch, especially `5^1||N`, remains difficult.

### Corrections to earlier mathematical claims

1. **Rule VII must be only a numerical size bound.** The minimum of candidate integer lifts need not divide every candidate lift. Report counterexample: `min(65,13,5)=5` but `5∤13`. Use `A*/A >= M_lift` only for size comparisons; never propagate it as `M_lift | A*/A` into LCM or valuations. Revalidate previously accepted rule-VII leaves under this fixed semantics.
2. **No transfer of root-17 LP to root-3 with excluded 5.** The mandatory root and excluded-prime sets differ. Dedicated root-3 `5∤N` model gives only `log10 N >= 217.821703609` in the report, insufficient to close that whole class.
3. **Proposed Rho128.cpp is a candidate factor finder, not a proof.** `is_prime128` is a finite-base probable-prime filter, and `factor_rec` can silently return on `d==n`. The output deduplicates factors and does not establish complete factorization or primality. It must be independently checked against exact input division, residual cofactor and Pratt certificates before any use as a proof leaf. Do not interpret factor lists as complete or certified.
4. **Coverage and disjunction.** When proving via `SPLIT_PRESENCE(17)` or `SPLIT_PRESENCE(5)`, both branches must be discharged before counting the top-level shard closed. Include `SPLIT_EXPONENT` parity/special-prime completeness for every DAG.

### Claimed manifest hashes for reproduction

- `RootManifest.json`: `7f26dc5021f891e5dfbb8cb79aaa16eb345e3f80c0152054e369d84b0a5bef8b`
- `OpenManifest_v5.json`: `84b3e6bf66b16227cb3576c58a52199cfafdedbe45f8b09856a8c0c9f008ddd5`
- `TerminalCoprimeCertificate.json`: `2ad9db90c903c0cd831338e01dfb8e147d690899e68a2a9faea6aab7ed0c0cd0`
- `ClassC8Certificate.json`: `189eaa6c96b135d71b2a13a831623f67d013229037821de248ad76f15d8f0195`
- `Root5_Ultra_V3Certificate.json`: `946888f54b45149c32e8e9df67d9fa59d71e5d3c98faf094b0b9cf2eafd19bfd`
- `Root3_Ultra_V3Certificate.json`: `36b76277e81dd520723f2aa143b57c9615f8a6830abbaf2a732ecdc005258f6a`

## Remaining work in priority order

**P0:** Import and independently replay all named v5 artifacts including 31 DAGs, complete open manifest, conditional LP evidence and the full verifier. Freeze model assumptions, validate exactly 1,679 task statuses and 1,393 open items with no double-counting. Repair or reject any mismatching certificate.

**P0:** Close the seven unfinished root classes. The largest frontiers are root 3 (355), root 7 (215), root 11 (182), root 5 (180), root 13 (172), root 19 (154), root 31 (135).

**P0:** Scale mathematical proof rules, especially root-3 `5^1||N` forced-branch roadblock, root-5 `17|N` branch, difficult root-19 indices 0,35,100; combine deeper sigma implications, proven factors of cyclotomic numbers, and state LP with a rigorous infinite-prime tail. Avoid claiming closure from a single disjunct.

**P1:** Integrate C++/GMP factor chain and roadblock search with complete split/leaf emission and deterministic verifier. Preserve failed branches as OPEN and record checkpoints/replay.

**P2:** Measure full execution on specified hardware: `T_prep + T_search + T_cert + T_verify <= 259200s`. With 1,393 shards open, no valid full-project runtime bound has yet been obtained.

**Current theorem status:** `INCOMPLETE_FRONTIER`.
