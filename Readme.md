# PerfectNumbers

Computational research on lower bounds for odd perfect numbers (OPNs), combining factor-chain proof trees with endgame linear programming and interval-based certificates.

## Research status

- **Verified upstream reference:** Ochem and Rao (2012) established a published bound of \(N > 10^{1500}\). The reference paper is in [References/OchemRao2012.pdf](References/OchemRao2012.pdf).
- **Historical local results:** earlier project notes report an endgame LP certificate above \(10^{3129}\) conditional on exclusion of the 15 forbidden primes, and a complete 15-root search at exponent 1500. Those results remain historical claims until independently reproduced and audited in this repository.
- **Research target:** obtain a complete, independently checkable unconditional bound exceeding \(10^{2200}\). An endgame-only estimate is not a complete unconditional proof.

## Repository layout

| Location | Contents |
| --- | --- |
| [Sources/Cpp](Sources/Cpp) | GMP factorization index builder and proof-tree versions V1–V10 |
| [Sources/Python](Sources/Python) | LP baseline, ablation study, interval dual certificate |
| [Documentation](Documentation) | Technical LaTeX report and preserved historical research handoff |
| [References](References) | Original Ochem–Rao reference paper |
| [Records](Records) | Experiment log, milestone ledger and proof validation checklist |
| [.github/workflows](.github/workflows) | Explicitly triggered reproducibility workflows |

Tracked project filenames and directories use English PascalCase. GitHub's required `.github/workflows` location and `.gitignore` remain conventional.

## Reproduce locally

Install Linux build dependencies `g++`, `libgmp-dev`, `zlib1g-dev`, and `python3`. For Python experiments:

```bash
python -m pip install -r Requirements.txt
python Sources/Python/Baseline.py
python Sources/Python/Ablation.py
python Sources/Python/IntervalCertificate.py
```

For C++ (from the repository root):

```bash
mkdir -p Build
g++ -std=c++17 -O2 Sources/Cpp/BuildIndex.cpp -lz -o Build/BuildIndex
g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofTreeV5.cpp -lgmpxx -lgmp -o Build/ProofTreeV5
cd Build
./BuildIndex CheckFacts.txt.gz
./ProofTreeV5 300 17
```

The historical builder writes `facts.dat` and `facts.idx` in the current directory. `CheckFacts.txt.gz` is an external, checksum-pinned database snapshot. Its pinned SHA-256 is:

```text
ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119
```

The full dataset is large. Heavy-data workflows require explicit manual dispatch; lightweight source compilation and core tests run automatically on source pushes. Use **Actions → Factor-chain proof experiments** for a compile check or proof run and **Actions → Python LP experiments** for a selected Python experiment.

## Proof standard

A claimed unconditional bound requires all forbidden-prime branches to finish with no unresolved roadblocks, a sound endgame certificate covering the complementary case, and a review of branch completeness, factorization correctness, floating-point bounds and data provenance. See [Records/ValidationChecklist.md](Records/ValidationChecklist.md). See [Records/ExperimentLog.md](Records/ExperimentLog.md) for test status and reproduction instructions.

## V6 prototype

`Sources/Cpp/ProofTreeV6.cpp` preserves the V5 interface and adds an analytic infinite-prime-tail relaxation and overlap-safe composite accounting. Run `ProofCoreTests.cpp` before dataset-backed comparisons:

```bash
g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofCoreTests.cpp -lgmpxx -lgmp -o Build/ProofCoreTests
./Build/ProofCoreTests
```

V6 is under validation. The ALPHA assumption, probabilistic primality decisions and floating-point comparison margins still require full mathematical audits.

## Validated regression snapshot

- V5, exponent 300, all 15 roots: 13,250 branches, no failed roadblocks, 0.390215 seconds for the proof tree on a two-thread GitHub runner ([original run](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990168041)).
- V6 and earlier C++ versions compile, core regression tests print `ProofCoreTests: OK`, and Python syntax checks pass ([quality run](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990984163)).
- The next performance gate is a dataset-backed, root-matched comparison of V5 and V6 at a higher exponent.

The historical Python workflow output can be inspected in [Run 44990184125](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990184125). It reports a 3129.458561 complement-case LP value and an interval dual output agreeing to six decimals. The full independent mathematical audit remains open.

## V7 parallel roadblock prototype

`Sources/Cpp/ProofTreeV7.cpp` introduces block-parallel circular prime case checking on large roadblocks. The partition preserves the prior-prime exclusion prefix for each block. Historical V1–V6 implementations remain unchanged, and `ProofCoreTestsV7.cpp` provides a separate smoke-test entry. V7 requires dataset-backed parallel equivalence testing before any proof claims.

V7 also compiled and passed its core tests in [Run 44991317752](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991317752). The bounded 2201 candidate experiment is separately tracked in [Run 44991101998](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991101998).

The first bounded probe at exponent 2201 timed out after 120 seconds on each of roots 17 and 307. Its V5/V6 control experiment at exponent 1000, root 17, matched exactly at 2,770 branches, with elapsed times 2.28969 s / 2.25512 s respectively. These two target timeouts are inconclusive and no new lower bound follows.

## V8 diagnostic build

`Sources/Cpp/ProofTreeV8.cpp` adds 10-second progress reports, allowing bounded high-exponent experiments to expose where time is spent. Each report includes branch and circular-branch counts and the largest roadblock bound encountered. A short follow-up probe at exponent 2201 is tracked in `.github/workflows/TargetedProbe.yml`.

V8 diagnostics in [run 44991559032](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991559032) found 403,628 branches for root 17 and 412,952 for root 307 by 50 seconds of exponent-2201 search; neither root finished in 60 seconds. Their maximum observed roadblock bounds were only 3 and 29 respectively. V9 is an experimental bounded-deep-task prototype designed to address ordinary DFS load imbalance, subject to benchmark and proof audit.

The [V8/V9 bounded benchmark](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991855026) measured branch visits at 30 seconds: for root 17, V8 222,022 vs V9 245,875; for root 307, V8 233,773 vs V9 299,786. All four timed out at 35 seconds. These are non-equivalent partial traversals and do not establish a full-run speedup.

Completed-case V8/V9 comparison in [Run 44992192309](https://github.com/stormwhip/PerfectNumbers/actions/runs/44992192309): exponent 1000 root 17 completed in 2.29845s / 2.25049s (2770 branches each); root 307 in 1.15197s / 1.13924s (1531 branches each). Both versions reported zero unresolved roadblocks. These small single-run time differences do not establish a robust high-exponent speedup.

An LP-guided candidate reduction for exponent 2300 selected \(S_*=\{3,5,7,11,13,17,19,31\}\) and obtained an interval-dual output of \(2390.1110142932844\) for the complementary case. See [prime-set optimization theory](Documentation/PrimeSetOptimization.md) and [Run 44993433027](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993433027). Independent model verification and the full eight-root factor-chain proof are still outstanding.

V10 adds prime-adic obligation propagation and quotient-congruence sharpening to ordinary factor-chain DFS, without changing the root set. It is a separately versioned candidate intended for a clean V9/V10 performance and correctness comparison.

Measured reduced-root prototype: [Run 44993825296](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993825296) confirmed that at exponents 300 and 500 the eight-root tree was slightly slower than the original 15-root tree, because previously forbidden primes re-enter other branches. V10 valuation tests passed but did not reduce the number of branches on the completed regression roots ([Run 44993733799](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993733799)). These experiments motivate optimizing the root permutation and tighter state-level LP cuts.
