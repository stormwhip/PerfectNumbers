# Complementary repeated-power certificate at (7,906), at most two A-primes

**Additional structural theorem.** Under the canonical hypotheses of [the independent 906 audit](Audit906.md), suppose A=Φ_907(7) has at most two distinct prime factors. Then **no ordinary A-prime supplies 144 or more powers of 7**. Consequently the necessary Euler supply window improves to 482≤s=v_7(q+1)≤665, all emitters of q are internal, and some A-prime must supply between 82 and 143 units (inclusive). No claim about unrestricted ω(A), no global key closure.

**Arithmetic observation.** The audited earlier theorem excludes high Euler and linear zero-supply in this sparse class, so q is linear, exterior, s>0. At least one A-prime has supply ≤5. Suppose an A-prime r supplies u≥144. Its order modulo 7 is 3, and v_7(r³−1)≥u−4≥140. By the verified repeated-divisor certificate at depth 140, r²∤A. Therefore v_r(A)=1. A cannot equal r alone: that would be squarefree with ≤4 primes, already excluded. If there is another prime b, write exactly A=r b^j; j=1 is squarefree and impossible as well. Thus j≥2 and b>10^7 from the audited CRT roughness proof. Hence j≤109, as 10^770>A. We show **no** complementary b^j is possible.

The odd prime b divides Φ_907(7), so b≡1 mod1814. Moreover b^(3j)≡A³ mod 7^140, and A b^(−j) mod7 belongs to {2,4}. If 7|j then b^(3j) mod49 belongs to {1,−1} by the unit-group exponent 42; this contradicts A³ mod49=22. Otherwise 3j is a unit mod7; enumerate the possible nonzero roots b mod7 and all their unique Hensel lifts, and take their CRT intersection with 1 mod1814. For each least positive representative R, a possible b satisfies R≤b≤floor(A^(1/j)). In the 108 candidate exponents j=2..109, *only* j=2,4,5 pass this elementary initial size filter; this is checked rather than assumed.

For those remaining classes M=1814·7^140, b=R+Mx, a band lo≤b≤hi gives x≤(hi−R)//M. Directly reject x=0 by R∤A. Use c≡R/M mod A. On the hypothesis b^j|A, for any l≥0 let d=min(l,jk). The basis polynomial x^(l−d)(x+c)^d A^(k−floor(d/j)) at a candidate x is a multiple of b^(jk); this follows from b|(x+c). Two explicit integral combinations have strict coefficient-height bounds <lo^(jk), so both must vanish. Their reductions modulo prime 65537 have gcd 1, impossible for an integer x. Check a contiguous cover up through the exact integer jth root, including all 164 nonempty (j,class,band) pairs. The certificate discovery used LLL, the checks do not. Hence u≥144 is impossible, whether its would-be emitter is the same or the other prime.

**Projection.** In the sparse class every q-emitter is internal (already audited), and the two A-primes supply at most 5 and u, respectively. Suppose there were only one factor; assigning a zero for a missing second can only weaken the bounds. Write Y=7^s,Q=2Y−1,W=7^907. ∏ of compulsory 7^906,A,q, the balanced net cost of the actual internal emitter beyond A, and all genuinely *external to A* ordinary residual suppliers gives the necessary inequality

    X A Q max(1,YQ/[max(W,Q)(W/Y+4)]) · 7^(2 max(0,906−s−5−u)) ≤ B·579125.

No A factor is priced twice: the balanced net premium is for the actual emitter beyond its paid A share, and no A-prime enters the external price. Testing all s=1..710 and u=0..143 with exact integers leaves 5735 necessary pairs, with the stated s and u projections. Retention is not proof of existence.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/Sparse906.py
    python -I -S -B Research/FinalNight2400/Nineteen/SparseWindows.py
