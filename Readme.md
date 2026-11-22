# PerfectNumbers

Computational research on lower bounds for odd perfect numbers (OPNs), combining factor-chain proof trees with endgame linear programming and interval-based certificates.

## Research status

- **Verified upstream reference:** Ochem and Rao (2012) established a published bound of \(N > 10^{1500}\). The reference paper is in [References/OchemRao2012.pdf](References/OchemRao2012.pdf).
- **Historical local results:** earlier project notes report an endgame LP certificate above \(10^{3129}\) conditional on exclusion of the 15 forbidden primes, and a complete 15-root search at exponent 1500. Those results remain historical claims until independently reproduced and audited in this repository.
- **Research target:** obtain a complete, independently checkable unconditional bound exceeding \(10^{2200}\). An endgame-only estimate is not a complete unconditional proof.

## Repository layout

| Location | Contents |
| --- | --- |
| [Sources/Cpp](Sources/Cpp) | GMP factorization index builder and proof-tree versions V1–V5 |
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

The full dataset is large. Workflows default to explicit manual dispatch to avoid silently using GitHub Actions compute quota. Use **Actions → Factor-chain proof experiments** for a compile check or proof run and **Actions → Python LP experiments** for a selected Python experiment.

## Proof standard

A claimed unconditional bound requires all forbidden-prime branches to finish with no unresolved roadblocks, a sound endgame certificate covering the complementary case, and a review of branch completeness, factorization correctness, floating-point bounds and data provenance. See [Records/ValidationChecklist.md](Records/ValidationChecklist.md). See [Records/ExperimentLog.md](Records/ExperimentLog.md) for test status and reproduction instructions.
