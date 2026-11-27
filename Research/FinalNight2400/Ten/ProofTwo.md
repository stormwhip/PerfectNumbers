# The two residual leaves at T² are abundant

Assume an odd perfect N ≤ 10^2400, with exact components 19^58, Q^1, T^2, A^2. Here Q = σ(19^58), T = (Q+1)/6, and A is the historical 81-digit pivot under T^2 (explicit in [the verifier](VerifyTwo.py)). The primality of Q,T,A and all partitions up to the two residual leaves are the reviewed [C10 premises](../../Night2400/Receipts/Review19x58Low.md). Q to the first power fills the Euler slot, hence all other exponents are even.

The three sums Q+1, σ(T²), σ(A²) have respective odd divisors 3, 3·7·61, 3·13. Since these sums come from distinct exact components their product divides σ(N)=2N; consequently 3³·7·61·13 divides N. Rounding the exponents upward to even gives m=3⁴·7²·13²·19⁵⁸·61² dividing N. By the Euler product, σ(N)/N≥σ(m)/m. Exact computation gives σ(m)−2m=7088250350624187477714863874621281538522135945090998738793737635781730949984325451>0. Contradiction.

Both historical null leaves below T² have A² (and then L² or L⁴). This argument rejects their common prefix, regardless of L. All other T² paths were historically excluded. Thus T² itself is excluded **conditional on Q¹**; not the entire key. Recheck with `python -I -S -B Research/FinalNight2400/Ten/VerifyTwo.py`, which pins the historical packet, matches the uncovered paths, and checks the arithmetic; it does not replace replaying the historical proof.
