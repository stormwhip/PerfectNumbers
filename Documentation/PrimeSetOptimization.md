# Forbidden-Prime Set Optimization

## Research objective

Find a smaller exclusion set \(S\subseteq S_{2012}\) for the odd-perfect-number lower-bound search at exponent \(K=2300\), and find a branch order minimizing *measured* proof-tree runtime.

Let \(L(S)\) denote a **validated lower bound** on \(\log_{10}N\) for hypothetical odd perfect numbers coprime to every prime in \(S\). By partitioning cases, every odd perfect number satisfying \(N\le 10^K\) must contain a prime from \(S\) whenever \(L(S)>K\). Therefore it suffices to refute the corresponding prime-containing cases for the selected \(S\).

This gives a sound search-space reduction **provided the LP relaxation and its interval certificate are themselves correct**. The numeric objective is only a screening tool.

## Why test removal of prime 127?

The historical 2012-order V4 experiment reportedly spent around 348 seconds on root 127, more than any other root. The existing GitHub Actions LP ablation run [44990184125](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990184125) reports:

| Deleted prime | Float LP complement exponent |
| --- | ---: |
| 127 | 2945.55 |
| 307 | 3075.50 |
| 398581 | 3129.46 |
| 1093 | 3128.17 |
| 31 | 2508.39 |

These figures suggest reducing the exclusion set at exponent 2300. The proof-tree runtime for other roots **will change** when a forbidden prime is removed. Root runtime savings must be measured with the new set and ordering; historical per-root times cannot simply be subtracted.

## Prototype selection experiment

[PrimeSetSearch.py](../Sources/Python/PrimeSetSearch.py) starts with the full 15-prime set. It iteratively removes primes while keeping the float LP screening objective above \(2300.2\); it explores both unrestricted and forced-removal-of-127 paths, then computes an interval-dual lower endpoint for each final set.

The outputs will include each tested set, its LP value, selected retained set, and interval-dual lower endpoint. Passing the dual calculation is not a substitute for an independent mathematical audit of the LP model.

## New candidate deduction: prime-adic obligation propagation

For every odd prime \(q\), an odd perfect number satisfies

\[
\nu_q(N)=\sum_{p^e\parallel N}\nu_q\bigl(\sigma(p^e)\bigr).
\]

A partial proof tree stores known components \(p_i^{a_i}\) where either \(a_i=e_i\), or \(a_i+1\mid e_i+1\). In both cases \(\sigma(p_i^{a_i})\mid\sigma(p_i^{e_i})\), so

\[
r_q:=\sum_i\nu_q\bigl(\sigma(p_i^{a_i})\bigr)\le\nu_q(N).
\]

Let \(m_q=\max\{1,r_q\}\) for an already forced odd prime \(q\). Its ordinary exponent must be at least

\[
e_{\mathrm{even}}(q)=2\left\lceil\frac{m_q}{2}\right\rceil.
\]

If \(q\equiv1\pmod4\) and the unique Euler-special slot is available, the alternative lower admissible exponent is

\[
e_{\mathrm{spec}}(q)=1+4\left\lceil\frac{m_q-1}{4}\right\rceil.
\]

The special choice may be applied to **at most one** eligible prime. These bounds yield an additive log-size contradiction test that is never stronger than what the exact \(q\)-adic obligations justify. The same obligations immediately reject any exact branch assigning \(q^a\parallel N\) when \(r_q>a\).

Potential contribution: current versions mostly store forced primes as a set and lose cumulative valuations from repeated divisor-sum factors. A valuation-aware lower bound can prune ordinary DFS branches before expensive factorization lookup or additional recursive searches.

### Safety conditions for the eventual implementation

- Count valuations only from factors whose primality is independently certified, or apply validated deterministic small-integer primality checks.
- Do not count a prime-power factor twice when two incomplete factorizations overlap.
- Charge the special-prime exponent saving at most once across both known and unbranched components.
- Preserve the divisor-sum divisibility relation for every inexact branch.
- Add regression tests to compare full root coverage before and after introducing the pruning rule.

## Experimental decision criteria

1. Independently audit interval-dual LP certificates for proposed exclusion sets.
2. Compare complete root searches at the same target and actual exclusion order (not just truncated branch throughput).
3. Benchmark valuation propagation at exponent 1000, then 1500, then increasingly high targets.
4. Require all selected roots plus the complementary endgame certificate for an unconditional statement.
