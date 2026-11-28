# Complete canonical exact exponent (13,262)

Claim: no odd perfect N≤B=10^2400, avoiding the earlier canonical primes 19,7,11,31, has p=13 to exact exponent E=262. The historical forced pivot is t=231050784610489. Frozen exact-domain replay has 29 live exponents, with first strict size tail 128. The disjoint union is: historical Fibers13x262 (22); historical G6 (1); new Thirteen262 (12,28,42,60); new Thirteen262Direct16 (16); the new simultaneous-price proof below (46). Parentheses name first valuations except where a count is explicit. **One key, one shard P13_I00055.** No divisibility lift.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/Full13.py
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Others/Verify46.py
~~~

## Final fiber f=46: compulsory output and remaining demands

Let X=p^E t^46, A=σ(p^E)/t, C=σ(t^46), D=AC, M=p^E t^45. The checker verifies integrality, gcd(D,X)=gcd(A,C)=1. Since σ(N)=2N, XD divides N. The two exact sigma blocks have supplied only a single t, leaving p,t multiplicity M to be supplied externally. Write the unique Euler component as q^(4k+1); q differs from p,t. Factor its size into q and (q²)^(2k), and its sigma into (q+1) times σ_base(q²,2k). Unfixed ordinary prime powers and this last square-base factor are called atoms. An atom has odd base r, even exponent h, and odd length L=h+1≤8000 (since 3^8000>B); distinct atoms have distinct bases. Supply means the p,t prime-power contribution to the corresponding geometric sum. Euler exponent one is included, as then the square atom is the unit.

## Uniform square price for every subset of atoms

We establish that the product of sizes of any subset, times U=2247129787084402954, is at least the square of the subset's supply. For prime s=p or t, if r=1 mod s the supply is v_s(L) by LTE. Otherwise if the geometric sum is divisible by s, o=ord_s(r)>1 divides L, and supply is v_s(r^o−1)+v_s(L). Here t>L; its order-one case supplies no units. The only nontrivial odd p-order is 3. The odd t-orders divide 3·263·401·877·104087 (product squarefree). Divide a component's exponent budget into these charges:

* For any p supply arising from k'=v_p(L), reserve at most p^k'−1 powers. They pay p^(2k') with no loss because r≥3 and 3^(p−1)≥p².
* For order three, simultaneously charge the p-order-three units from r³−1, if present, and the analogous t units when ord_t(r)=3. Two powers suffice modulo the loss below. If a target has no such charge use modulus 1.
* For t-order o>3 reserve o−3 powers for the t supply, leaving two for a possible p-order-three charge. If t does not supply, only the p charges are needed. These reservations fit in h: when o>3 divides L and k' units derive from its length, (o−1)+(p^k'−1) ≤ o p^k'−1 ≤ h since p and o are coprime. The analogous bound with o=3 covers joint cubic charges; when there is no base-order charge the length charge alone fits. Reserving unused powers is harmless.

For fixed positive base-order exponents a,b, put m=p^a t^b, allowing zero exponents at either target. Only r<m can have loss m²/r²>1. A primitive cubic root is nonzero and simple mod its target, and has a unique lift at each higher level by the displayed Hensel digit in PriceThree.py. An element of order three and its square exhaust the two primitive roots modulo a prime. CRT enumerates at most four residue classes, using the smallest nonnegative representative r mod m. The scans include every possible a≤E,b≤45, even if the representative has extra supply; each physical atom is charged at its actual levels. The separately reserved length increments cover the rest. In the high t-order test the possible loss t^(2b)/r^(o−3)≤1 if 3^(o−3)≥t^90; the finite remaining cases exhaust odd bases with r^(o−3)<t^90 and pow(r,o,t)=1. For this test gcd(r^o−1,t^45) is an upper bound for t supply of an actual order-o atom. All possible orders are rechecked from the factored t−1; smaller-order false positives in this test could only enlarge its loss bound.

**Mandatory net-cost sieve.** For a positive conditional charge reserving h' powers, r^h' divides the size of the true atom even if r=q². Hence X·lcm(D,r^h') divides N (r is coprime to X), so r^h'/gcd(r^h',D) ≤ floor(B/(XD)). Failure therefore rigorously excludes the label even in a price applied to just a subset of atoms. The cheap factor and Fermat tests eliminate only proven composites from the possible prime-base labels: a survivor is allowed without claiming primality. If r fails as a prime label, the checker still allows it as an Euler square when its exact integer square root passes the same necessary prime tests. The canonical banned primes and fixed p,t cannot be roots of either type. For each distinct base take the maximum possible cubic deficit ratio (>1). Exact enumeration gives **23** such base labels; the product rounded upward is U above. The separate high-order loop gives **no** deficits; the two charges thus cannot cost more than this single U. Values U and the count are recomputed, not assumptions. Critical.py reads no cache or external data. The primality of the two fixed primes and the t−1 factors is checked below 2^64 by deterministic Miller–Rabin (the large fixed pivot also has an independent historical replay).

## All Euler allocations: no factorization of either block

Let i=v_p(q+1), j=v_t(q+1), m=p^i t^j. Since q≡1 mod 4 and m odd, q is in the class Q=2m−1 mod 4m and q≥Q. The atom price gives N≥XQ(M/m)^2/U. When this does not already exclude the window, prove q external to A,C: if q|Z, the positive cofactor n=Z/q is ≤Z/Q and n ≡ Z·Q^(−1) mod 4m. For each tested block either Q>Z, or Z/Q<4m and the sole possible residue fails divisibility or the interval bound. All windows reaching this check pass. Then N≥XDQ. For the remaining windows, q must divide σ(r^h) for a distinct unfixed ordinary prime r: neither of the two fixed sigmas nor the Euler prime's own sigma supplies q. Let y be the p,t contribution of this emitter. Its sigma is at least qy and strictly less than (3/2)r^h. Its overlap with D is at most H=max(A,C), since gcd(A,C)=1. Two independent bounds follow, each reserving this emitter once:

- 3N > 2XD Q² y/H, from combining XDq and the net multiplicity of the emitter.
- 3NU > 2X Q² (M/m)^2 / y, from applying the subset atom price to all other atoms.

Multiplication cancels y. Thus 4X²D Q⁴(M/m)^2 > 9B²UH excludes a window (the checker uses strict comparison). All 263·46=12098 allocations among i=0..262,j=0..45 are excluded: **4984** basic price, **5320** mandatory size, **1794** emitter. No assumptions about possible factors of A,C, or about q having exponent exactly one, are used.

## Packet integrity

* Four new complete firsts: Thirteen262.json.gz, SHA-256 23e91a724829cac6f849993452067010df3bb66d9d4bc8b4f07ad105b08b7f21 (1779 ECPP chains). The packet includes a still-open marker under first 16; it does not claim first 16.
* Complete first 16: Thirteen262Direct16.json.gz, SHA-256 81885a1ec74ac13fd07323c0fb475b5ec4774d551487cb45b45637f8d3eb375d (1020 ECPP chains; 91 strict forest leaves). The central forest uses compelled prime 419 but need not branch on its exponent. The longer, separately cold-checked 40-sibling alternative is not needed in the union. Forest thresholds are strict even when the decimal floor is 2400.
