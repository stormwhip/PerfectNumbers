# PerfectNumbers: certified terminal LP and fixed-multiplier roadblock sweep

The target remains \(N>10^{2400}\) for every odd perfect number. An independent integer verifier now establishes the mutual-coprimality case for each of two candidate eight-root sets. The eight divisibility classes, reachable-node replay, and a full 72-hour experiment remain open.

## Conditional terminal results

| Roots whose divisors are excluded | Certified lower bound on \(\log_{10}N\) | Factor relations |
| --- | ---: | ---: |
| \(S=\{3,5,7,11,13,17,19,31\}\) | \(4183.209493\) | 8,616 |
| \(S'=\{3,5,7,11,13,17,23,31\}\) | \(3954.197016\) | 8,214 |

Both use the basis cutoff \(P=5000\), exact exponent cutoff \(22\), and a bounded factorization parameter of 5000. These are independently generated certificates for a stronger model instance. The generator splits each geometric sum into cyclotomic components, attempts partial factorization, and keeps only prime divisors with recursive Pocklington witnesses. Missing factors omit rows. Every retained divisor is rechecked by exact modular arithmetic. The verifier was run with Python's external site packages disabled, and it rejected a modified factor exponent.

Given a hypothetical odd perfect number coprime to the root set, send each prime power to its unique basis option, induced prime option, or generic tail. The exact basis options incorporate the factor-sum restrictions. Beyond the exact cutoff, the smallest allowed exponent is used as a cost lower bound, separately for even exponents and Euler exponents. The search for this exponent terminates: taking \(e+1\equiv1\) modulo every forbidden prime and every multiplicative order arising in the modular test gives a legal exponent. For a special exponent, the obstruction is divisibility of \(e+1\) by a forbidden prime or by a multiplicative order modulo one of those primes. \(e+1=2(1+2kL)\) has no odd factor shared with \(L\), and its valuation at 2 is exactly one. Any forbidden divisor of 2 in this test would also forbid exponent 1. Choose a sufficiently large \(k\). Each ordinary generic tail component contributes its actual logarithmic abundance at cost at most \(e\log p\). There can be at most one generic special component. An implication from a present exact source is satisfied because every retained \(q^k\) divides the source factor sum and hence divides \(N\). Explicit induced primes and the generic tail use disjoint supports.

The verifier reconstructs the LP using lower cost and upper abundance endpoints. For nonnegative dyadic multipliers \(\lambda\), it computes \(r=c+A^\top\lambda\), checks the unbounded tail reduced cost is nonnegative, and uses \(-\lambda^\top d+\sum_{i\text{ bounded}}\min(0,r_i)\) as a lower bound. It compares the integer numerator against \(2400\) times an upper endpoint for \(\log 10\), so the numerical optimizer need only propose multipliers.

~~~bash
cd Research/2026-11-22
python -S Python/TerminalCertificate.py verify Certificates/TerminalOriginal.json.gz
python -S Python/TerminalCertificate.py verify Certificates/TerminalReplacement.json.gz
python Python/TerminalCertificate.py generate Replacement.json.gz --limit 5000 --cutoff 22 --factor-limit 5000
~~~

The first two commands need only Python. The last command uses SciPy and SymPy. The archived gzip SHA-256 digests are:

~~~text
2ad27ba74c52bb3298c034a312d2c4f33f67bc0134152c1c4d6cc9f10114383c  TerminalOriginal.json.gz
790203f736318296e93c1e2020699d143111c5497ae688a370222ec2d4bbadaa  TerminalReplacement.json.gz
~~~

## Roadblock boundary sweep

The prior routine rebuilt its two exponent streams for each trial boundary. For fixed \(\mu\), each candidate \(q\) is now represented by at most two half-open boundary intervals for its even options and two for its special gain. A forbidden factor already in \(F_s\) acts from the start. A first non-expanded factor \(r\) activates the relevant restriction at \(r+1\). The candidate disappears at \(q+1\). A difference sum gives the even reduced-cost contribution, while a heap with expirations gives the best special adjustment. The table of small factors is built once by marking modular roots: \(q^2+q+1\) has the nontrivial cube roots modulo primes \(r\equiv1\bmod3\), and has root \(1\) modulo \(3\). For \((q+1)/2\) use residue \(-1\) for every odd prime. Explicit forbidden factors above the table are tested directly when relevant.

Before flooring, the witness bound is the minimum over choices of the special option, including choosing none or the generic tail special option. The even contribution in each alternative uses the even reduced-cost minimum for each remaining ordinary candidate. Increasing \(b\) removes alternatives or raises their even costs. This proves monotonicity for the same \(\mu\) and fixed tail. Directed integer rounding preserves it. The first strictly valid boundary is obtained by binary search in the completed profile. The code also stops scanning once \(\log_{\rm lo}q\ge\mu h_{\rm hi}(q)\): all later finite reduced costs are nonnegative.

For a shared table and fixed node, a profile takes \(O(k\log k+k|F_{>P}|)\) plus the small-factor checks, where \(k\) is the scanned prefix. It uses \(O(k)\) memory, then permits \(O(\log k)\) queries by boundary or budget. In the synthetic 300,000-cutoff example, table precomputation took 1.207 seconds and the known multiplier's entire profile took 0.121 ms. This measurement excludes multiplier selection and search-tree work. The randomized test compared every integer boundary on 80 synthetic inputs and tested strict budget equality and an explicit factor above the table.

~~~bash
python Python/RoadblockBoundaryProfileTests.py
~~~

## Remaining verification and performance work

- Replay reachable V21 roadblocks and test how to select good multipliers when the boundary is unknown. Candidate multipliers may be proposed heuristically, with a bounded retry strategy and a conservative unresolved result if none certifies the node.
- A node may account for a residual's size while its constituent primes are still unknown to the search. In the actual \(N\), define the new support as the primes outside the expanded components and all recorded residual supports. Accounted residuals must individually divide \(N\) and the residuals used for the size sum must be pairwise coprime and coprime to the expanded components. Their abundance upper bound covers their entire support. This ensures the budget holds for the new support. The candidate enumeration can still cover every admissible unexpanded prime \(q<b\), including those in residuals.
- Measure certificate quality, total wall time, and remaining failures on real shard pairs. Then compare the two root sets across their complete eight-class partitions. The replacement changes the root-\(7\) exclusion involving \(19\mid\sigma(7^2)\). The terminal bound alone gives no runtime comparison.
