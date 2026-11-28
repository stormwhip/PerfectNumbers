# T⁶: five historical null paths excluded by forced-component net prices

Assume an odd perfect N ≤ B=10^2400 with exact prefix (19⁵⁸,Q¹,T⁶), Q,T as in [the C10 proof](../../Night2400/C10/README.md). Among the eight historically unresolved T⁶ paths, the following five are impossible. U=3291622576015727423, W=397752239, V=804577.

|Exact continuation| witness | number of explicit terminals / split nodes / tails | smallest floor(log10 bound) |
|---|---|---:|---:|
|U¹²,W¹⁰|[4](Tree4.json)|6/4/4|2404|
|U¹²,W¹²|[5](Tree5.json)|1/0/0|2411|
|U¹²,W⁶|[6](Tree6.json)|3/3/3|2402|
|U¹⁶,V²|[7](Tree7.json)|3/2/2|2408|
|U¹⁶,V⁴|[8](Tree8.json)|1/0/0|2418|

**Price.** Set X equal to the product of the exact components, S=σ(X)/2, C=S/gcd(S,X). Then XC divides N and gcd(X,C)=1. Targets are all fixed primes except Q. Write c_p=v_p(X)−v_p(S), M=∏p^{c_p}. For an unseen exact component r^f, define m(r,f)=∏p^{v_p(σ(r^f))}, where the product runs over targets. Euler is fixed, so f is even and positive. The product of all m is M. In particular

N = XM² ∏ (r^f/m(r,f)²).

For each possible unseen r write E_r ≥ max(1, m(r,f)²/r^f) over admissible f. Only finitely many E_r>1 are needed. With V0=XM²/∏E_r, each **distinct compulsory** r can improve V0 by the factor E_r times a lower bound on r^f/m². Unknown non-compulsory primes retain factor 1 (nonoccurring bases with E_r>1 also give nonnegative slack). This is an improvement on the raw mixed price, not a multiplication by a full outgoing divisor already paid for.

**Completeness of exceptional bases.** [PriceCore](PriceCore.py) uses the reviewed C10 exact LCM prefix price, unchanged through formation of V0, returning its per-base exception factors. Briefly, n is the target count. For f<2n enumerate all choices of exact target orders dividing gcd(p−1,f+1), and all valuations up to c_p. For nontrivial order o, lift roots of exact order o mod p^j by the simple Hensel formula and include the additional LTE shift v_p(f+1); the trivial order has the shift alone. Include absent-target choices. CRT gives the progressions for each combination, and all r^f<m² are tested, including repeated progression terms. For f≥2n a deficient r must satisfy r^f<p^{2n v_p(σ(r^f))} for at least one target: enumerate these individual progressions instead. Both f and r are bounded by Xr^f≤B. Remove incompatible candidates, including those with X lcm(C,r^f)>B. Unproven primality is never used to remove a real prime. Over-inclusion of composite bases only weakens V0. This gives a safe E_r; absent keys mean 1.

**Forced gains.** If r is forced with f≥h then enumerate even f starting at the least even ≥h; discard impossible f whose contribution exceeds any cap. Define G_r(h) as E_r times the minimum of r^f/m(r,f)². Once r^f/M² exceeds the current minimum, every further f is bounded below by it and the scan is complete. [VerifySix](VerifySix.py) checks r≡1 mod p contributions by LTE; otherwise it computes ν_p(r^{f+1}−1) capped at c_p+1 via modular exponentiation. Roots are distinct primes dividing C, charged at h=v_r(C), all certified in the historical ECPP book or by the deterministic 64-bit checker.

At a split q, other outstanding primes keep their gains. For each exact even f (beginning at least even ≥h), replace G_q(h) by its exact net factor; also verify and add any fresh prime divisors of σ(q^f). No divisor may be counted twice: split, pending, fixed and freshly introduced bases are tracked separately. If the other prices times G_q(f) exceed B, that entire f-and-larger tail is impossible. All explicit terminals and tails must give a strict rational bound >B. The verifier checks split dictionaries against the complete list of exponents it derives itself, including rejected cases. No heuristic factoring is involved in replay.

From repository root: `python -I -S -B Research/FinalNight2400/Ten/VerifySix.py`. The proof pins the old C10 packet, confirms every claimed path was a null terminus, and rechecks primality of every arithmetic base. It does not claim a full replay of the historical non-null forest leaves. The other three historical T⁶ nulls are not excluded by this five-case proof.
