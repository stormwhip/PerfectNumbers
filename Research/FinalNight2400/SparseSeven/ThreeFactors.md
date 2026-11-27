# At least three distinct prime factors of Φ_907(7) are necessary, without a squarefree hypothesis

**Conditional theorem about the root.** If an odd perfect N≤B=10^2400 satisfies v_7(N)=906 and 19∤N, then A=(7^907−1)/6 has at least three distinct prime factors. This is not an assertion about the actual factorization of A independent of the hypothetical N, and is not a root-key or shard closure. It sharpens the earlier all-Euler conclusion by excluding the entire linear positive-7-supply two-prime alternative, not just the middle s=453. The high-Euler/zero-supply cases already require at least four primes, and squarefree A already needs at least five, by the separately reviewed [earlier results](../Nineteen/Audit906.md).

**Reduction to finite exponents.** Assume ≤2 A-primes. The [complementary divisor theorem](../Nineteen/ProofSparse906.md) implies q is exterior linear, 482≤s=v_7(q+1)≤665, every q-emitter belongs to A, one A-prime b contributes at most five 7 units and the other r contributes 82≤u≤143. There cannot be only one prime in this state, since the low-depth prime would then be the only one. Write A=r^a b^j, v_r(N)=h, v_b(N)=g; these are distinct bases and both actual exponents are even. Both divisors exceed C=10^7. We may assume a,j≥1, (a,j)≠(1,1) by the squarefree theorem and gcd(a,j)=1: every prime d≤109 is explicitly checked not to divide both exponents via the exact test floor(A^(1/d))^d≠A, while j≥110 is impossible by C^110>A.

Let t=v_7(r³−1). Since y=7^u enters σ(r^h), r has nontrivial order 3 modulo 7, 3|h+1, and t=u−v_7(h+1)≥u−4. The audited roughness sieve gives r>C·7^t. In addition r must lie in one of two 1-mod-1814 CRT classes of nontrivial cubic roots modulo 7^t. For either t=u−4 or its actual refined t, lower-bound r by the maximum of C·7^t and the least CRT representative. Obtain a lower bound on b by the complementary congruence b^(3j)≡A³ mod 7^t and A/b^j≡r^a mod7, b≡1 mod1814. If 7|j there is no solution mod49; otherwise Hensel lifting is unique on every initial class; take the minimum positive CRT representative or discard an empty class. Denote the resulting lower bounds R,L. Using independent minima may admit extra combinations but never rejects a true one.

Enumerate 82≤u≤143, a with (C·7^(u−4))^a≤A, j with R^a C^j≤A, and even h≥a,g≥j under their component-size budgets using lower R,L, s≥482 and q≥2·7^s−1. The loops terminate by integer monotonicity; a=12 already exceeds A for every u. For each h,g update t as above. Let Y=7^s, Q=2Y−1, v=max(0,906−s−5−u). After paying the *actual* internal rows r^h and b^g, all other ordinary suppliers are exterior; hence r^h b^g≤K=floor(B·579125/(7^906 Q 7^(2v))). Since (r^h b^g)^j=A^g r^(jh−ag), if jh−ag≥0 a necessary test is R^(jh−ag) A^g≤K^j. If the difference is negative, instead use (r^h b^g)^a=A^h b^(ag−jh) and test L^(ag−jh) A^h≤K^a. For an emitter z∈{r,b}, σ(z^H)<3 z^H/2, so z^H>2Q7^u/3 for z=r and z^H>2Q/3 for z=b. Intersect these lower bounds with R or L, and retest their power product against A and K exactly. No component previously paid as part of A enters the product twice, and a high Euler is never treated as ordinary. The finite verifier returns exactly 1490 *relaxed* labels and 633≤s≤665 with the following (a,j,h,g,emitter) patterns:

    (1,2,2,2,b), (1,4,2,4,b), (2,1,2,2,r), (2,5,2,6,b).

**Signed emitter congruence to remove 1404 labels.** For a chosen emitter z write H=v_z(N), m=v_z(A), d=H+1−m≥1, D=6A/z^m, w=σ(z^H)/q. The integer

    Z0=D w(z−1)−z^d−D

is divisible by Y, since q≡−1 modY and D q w(z−1)=(7^907−1) z^d−D. It is nonzero: the other A-prime divides D but not z^d. Set W=7^907. The identity Z0=((W−1)/q−1) z^d−D(1+1/q) gives Z0<(W−1)z^d/Q. For a negative value use −Z0≤z^d+D(1+1/Q). Bound z above using both A and the actual component budget K, and D above using the emitter lower bound; these comparisons are rational/integer strict. If both sign thresholds are <Y then this nonzero multiple cannot exist. Of 1490 relaxed tuples, 1404 fail in this way; all 86 exceptions have exactly A=w0 z² and are emitted by z², with w0 the other odd prime.

**Square-emitter end (independent congruence due to Audit).** Write qk=z²+z+1, k≥1; then wk=(A/q)(1+1/z+1/z²)<3A/(2q) where w=A/z², and w≤wk. Since 6w z²≡−1 modY we have 6w(k+1)−1≡−6wz modY. Therefore the positive integer

    Z=(6w(k+1)−1)²+6w

is divisible by Y. But Z<(18A/q)²+9A/q≤(18A/Q)²+9A/Q<Y at every remaining s (the last inequality is independently checked for each exact tuple). This contradiction eliminates all 86. The same congruence works for both patterns, regardless whether the emitter was the higher or lower 7-supplier.

**Reproduction.** Neither native software nor LLL is needed. To reuse the previously audited lemmas, run the recent complement certificate and then the two exact entrypoints:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/Sparse906.py
    python -I -S -B Research/FinalNight2400/Nineteen/SparseWindows.py
    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/SparseSeven/VerifyPatterns.py
    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/SparseSeven/VerifyThreeFactors.py

The printed 1490/1404/86 are finite labels, not proved factorizations, and do not show that the actual unknown A has more than two factors unconditionally.
