# Full exact key: no odd perfect N≤10^2400 with v_19(N)=618

**Theorem.** Fix an odd perfect integer N not exceeding B=10^2400 and suppose 19^618 || N. Then the compelled prime t=2477 has no possible exact exponent. This excludes the entire exact key (19,618), without any auxiliary support mask. No extension to multiples of 618 or to other root exponents is asserted. It does not establish the global 2400-digit theorem.

**Scope and exhaustion.** σ(19^618) is an odd factor of 2N and has t-adic valuation 1. For the one fixed root, X=19^618 and D=σ(19^618) outside X. Consequently (XD/t)t^f divides N for f=v_t(N). At f=243 it exceeds B (at 242 it is still ≤B), so 243 is a strict monotone tail. At every smaller f, legality of Euler, overabundance, incoming oversupply or augmented XD>B are exact rejection criteria. The verified direct live domain is 1, all even 2..120, and 5,9,...,121, exactly 91 possibilities. No closed or untested branch is extrapolated. The historical independent receipt, including its repaired a≥5 argument, excludes the 30 odds starting at 5 and the 26 evens 70..120. The remaining 35 are 1 and the 34 evens 2..68. This packet treats them all; the following stage rows are disjoint at the level of *whole initial fibers*:

|Exact f|Whole-fiber proof|
|---|---|
|48,50,...,68|[Three separate strict cost tests, full Euler repair](Proof618.md)|
|36,38,...,46|[Inverse-square supplier reimbursement](Proof618Square.md)|
|26,30,32,34|[All-Euler compound-cost and compulsory-row credits](Proof618Credit.md)|
|22,24,28|[Same bound with complete certified emissions](Proof618Factored.md)|
|1|[Complete exact Euler-one tree](ProofOne.md)|
|18,20|[Exact one-anchor proof](ProofAnchor.md)|
|16|[One-anchor extension](ProofAnchorMore.md); partial f12/f14 in this stage are *not* counted as whole fibers|
|14|[Complete two-anchor argument](ProofNested.md)|
|12|[Complete two-anchor packet](ProofTwelve.md)|
|10|[Two-anchor 26-state proof](ProofSmallTen.md)|
|8|[1384-state proof](ProofSmallEight.md)|
|6|[835-state proof](ProofSmallSix.md)|
|4|[2575-state proof](ProofSmallFour.md)|
|2|[6937-state nested ordinary-anchor proof](ProofSmallTwo.md)|

The two stronger giant-cofactor repayment lemmas used in the last three rows are [no single overlap for u≥185](ProofLattice.md) and [no repeated overlap for u≥98](ProofSquareLattice.md). Their LLL-discovered witnesses are finite integer polynomial coefficients: verification requires no lattice software, no external factorization and no trust in discovery. The frozen arithmetic checks all valuation shifts, all eligible exponent tails, equality vs strict inequalities, and the unique Euler row, potentially high, through its composite square-base atom.

**Reproducible entry.** In a clean checkout, from repository root:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyAll618.py

This entry rechecks historical (19,618) only, including the high-Euler correction that was necessary for the accepted high even values. It then runs each current disjoint verifier in a fresh isolated interpreter, asserting all 91 cases are accounted for exactly once. This is a full-key arithmetic replay, not the historical global suite. For an independent method on the last fiber, pass its sealed Solved2.json to VerifyNested.main with unoptimized BestKernel replacing the runtime's Kernel. No discovery file or native tool is required. Historical single-key arithmetic and every new component individually passed. Aggregate serial timing and final external audit are reported separately rather than inferred from component receipts.

**Aggregate receipt.** A fresh serial invocation completed all 15 stages, exit 0, 2376.360 s internal (2377.048 s process wall time under concurrent host load). Final lines: “PASS complete 618 f= 2 cumulative visited 6937”; “STAGE VerifySmallTwo.py ok; covered 91”; “FULL KEY (19,618): all 91 live assignments excluded, direct checks and entire infinite size tail replayed.” The isolated proof uses only local standard Python integer arithmetic; native tools were confined to discovery. This timing is not a global cold-suite or 72-hour benchmark.
