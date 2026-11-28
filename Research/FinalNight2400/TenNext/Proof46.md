# (19,46): exact child exclusions and a necessary external Euler condition

Assume an odd perfect N≤B=10^2400 with 19^46 || N. Put q=σ(19^46)=70169234660105574400577005075855017842743056666917902427141. This is a certified prime. Historical [C11](../../Night2400/C11/README.md) leaves the exact q-valuations 6,10,12 open. **This packet does not close any of them completely.** Instead:

|Exact q valuation|Compulsory next prime|New exclusions in its exact exponent|
|---:|---:|---|
|6|A6=2247860239402417332211|30,32,34,36,38 (all viable ≥30)|
|10|A10=4098026841288271|22,24,26,28,30,32,34,36 (all viable ≥22)|

The two next primes are 3 mod4; exact division checks them in the corresponding q-geometric sum. Complete direct domains are 2,4,…,38 and 2,4,…,36, respectively. These 13 children are shown impossible for **all** placements and exponents of the Euler prime. Some old C11 proofs were for deeper paths, not claims of complete second children. We do not treat the historical discovery tree as an exhaustive partition.

At q^12 the packet proves a different, factor-free reduction: the Euler prime π is **exterior** to C=σ(q^12) and has exponent exactly one. For a=v₁₉(π+1), j=v_q(π+1), only the following necessary levels remain:

|j|a|
|---|---|
|6|7,…,46|
|7,8,9|0,…,46|
|10|0,…,40|

These are 222 levels, not surviving perfect numbers. In 141 of them every ordinary component emitting π has its base inside C (all at j=8,9,10; also j=7 with a≥41). No factorization or squarefreeness of C is assumed.

## Price and Euler windows

For exact prefix product X, let S=σ(X)/2 if the Euler component is fixed and S=σ(X) otherwise, C=S/gcd(X,S). Thus XC|N. All listed variable-power branches have Euler free. Use weight 4 on q and weight 2 on 19; on the three-target branches add weight 2 on the next pivot. For selected p with remaining cap c_p=v_p(X)−v_p(S), write M=∏p^{w_p c_p}. For components r^f with f≥2 (even or a legal high Euler exponent), compute a per-base exceptional loss E_r≥max(1,∏p^{w_p v_p(σ(r^f))}/r^f) on admissible components with each contribution ≤c_p. A true ordinary or high Euler base never fails the one-sided Fermat, exact size, parity, or prefix LCM filters. Factors of 2 in σ never affect odd targets. [Price46](Price46.py) performs the same complete integer-weight CRT construction proved in [the prior full reduction](../Ten/ProofFull.md), with inherited lifts/CRT helpers: for f<H=Σw_p enumerate joint order/level progression terms below weighted demand; for f≥H enumerate individual exceptions with bound p^{H v_p}. LTE shift v_p(f+1) is included; for r≡1 mod p it is the entire contribution. High exponents are exhausted using X3^f≤B. Store maximum per r, then V=XM/∏E_r. All valuations and strict comparisons are integer/rational. Even if r is composite in this relaxation, it only weakens the price. Every computation verifies V>B, excluding all Euler exponents ≥5, with no earlier assumption that Euler is linear.

For linear π let u_p=v_p(π+1), m=∏p^{u_p}, k=∏p^{w_p u_p}. Its congruence is π≡2m−1 mod 4m (π≡1 mod4); write l=2m−1. Pricing all other primes gives N≥Vπ/k. Thus π≤floor(Bk/V). Every u-vector is checked including zero levels; l above the upper bound proves impossibility. To eliminate π inside a fixed σ-block Z use [the reviewed divisor-window recurrence](../../Night2400/InteriorPrice.py) on [l,min(Z,floor(Bk/V))]. It tests the Euler prime progression and complementary cofactor progression, also intersecting the exact center order condition when the geometric index is prime and absent in Z. No lattice witnesses needed: unknown or unbounded intervals make this verifier reject, never pass. Once π is exterior, XCπ divides N and XC l>B rejects. This proves all 13 indicated child exclusions without relying on a size-only search or empirical factorization.

## q^12 exterior-emitter refinement

Here the sole nontrivial stripped fixed block is C=σ(q^12), coprime to q−1. Of the 564 possible Euler-one target supply vectors, 289 fail the mixed price; for each of the remaining 275, π cannot divide C by the preceding rigorous interior check. If π is exterior, an ordinary distinct base r^h must emit π (not a fixed component). Then r^h>2π/3. When r∤C this multiplies XCπ and gives the outside-source constraint. When r|C write c=v_r(C); its *excess* beyond the mandatory r-part of C is r^{h−c}. Apply the earlier [balanced-emitter lemma and proof](../../Night2400/B/HardAtomRoute.md) via [its exact checker](../../Night2400/B/Balance.py): with W=q^13,Y=q^j,δ=W/Y, we have r^{h−c}≥Yl/(max(W,l)(δ+4)). The prerequisites hold: q^j|(π+1), q^12 || N, v_q(σ(r^h))≤12−j, gcd(C,q−1)=1, and r,π are distinct from q. This bound is used only for internal emitters, so no already-paid mandatory mass is counted twice. For 53 vectors neither location is possible. Of the 222 remaining, only 81 admit an outside emitter under this bound. The verifier checks the precise level set as well as these counts.

## Offline replay

~~~text
python -I -S -B Research/FinalNight2400/TenNext/Verify46.py
~~~

[Verifier](Verify46.py) pins the baseline C11 prime book; all large primes used are checked with its elliptic certificates, small ones with the deterministic 64-bit kernel. A clean stdlib run on the final code exited 0 in 250.949 s. This is a new conditional proof, not a replay of all historical non-claimed cells or a change to the shard ledger.
