# Integer E3b base: (3,1108), source in A

Use 3^e||N≤10^2400, q^1 Euler, q∤A, q|σ(r^f), r|A ordinary, s=v3(q+1)≥1. R=10175119360001 below every A prime (`NextRange.py`, gcd=1). Gcd with canonical bans as before. Let c=v_r(A), t=r^(f−c), Z=3^s, P=3^(e+1), b=v3(σ(r^f)), and i be all the ordinary 3 supply on A excluding r. Other ordinary factors provide U=e−s−i−b units at prepaid price 81 (4ln3). Their net is what the joint model charges in addition.

**b>0 is impossible without any source window.** The normalized hull H on A's support simultaneously exceeds A R (A nonsquare, q external) and R^(2i) r^f. By the source order/Cauchy lemma, r^f>(2q/3)^(3^b); also f≥3^b−1, so r^f>R^(3^b−1). For b≥6 this alone exceeds B. Sweep the 5525 pairs 1≤b≤5, 1≤s≤e−b. At each pair set M=max(floor(2(2Z−1)/3)^(3^b),R^(3^b−1)). Compute

    3^e (2Z−1) min_{0≤i≤e−s−b} 81^(e−s−b−i) max(AR,R^(2i)M)>B.

Only the two integer neighbors of the unique crossing R^(2i)M=AR need checking; R²>81. This proves all b>0 impossible.

**b=0.** Write Y=3^s, δ=P/Y and D1,D2,H0=max(1,P/q) as in Proof2400 §3.3. The usual estimate t>Y/[H0(δ+4)] applies. If R≥2δ+1 then r−1≥2δ, and the D2-positive upper bound gives D2 <(3/2)H0 t + P/(r−1) ≤(3/2)H0 t + Y/2; because D2 is a positive multiple of Y this gives t>Y/(3H0). D2<0 gives the same via |D2|<3t/2. Thus use improved D2 whenever allowed. Here P/(r−1) follows explicitly from `U σ(r^(c−1)) < P/(r−1)` in D2. Let z be the lower estimate on t, rounded down, at least 1. Then H ≥ max(AR,A z,R^(2i)max(z,2q/3)), since f≥f−c and r^f>2q/3. Minimizing with 81^(e−s−i) preserves the crossover structure. This monotone function of q permits bisection over q=2m3^s−1. Test all s, all m up to the rigorous per-s cutoff; sieve m by Euler and forbidden conditions and q by small factors/Fermat.

For conditional prime q surviving this sieve, if r≥q then q²>A (checked), hence c=1, t≥q and r^f≥q²; direct sweep exceeds the target. Otherwise 1<r<q, and ord_q(r)|d=gcd(f+1,q−1). Here f<200 since R^200>B. Generate all order-dividing-d residues by exhibiting an exact-order-d element (loop until first return to 1). For every nontrivial residue z compute gcd(A,product z)=1, impossible for r|A. There is no need to prove any surviving q prime. All prices are disjoint; no internal incoming Φ3 factors credited in this base.

Replay `python -I -S -B parity-lab/InternalSupply.py`, then `python -I -S -B parity-lab/InternalPrefix.py 2086` (optional `--fast` uses python-flint modular powers, identical exact computation). At 2086, s=964..1082 contribute 115160 total m before sieving, 61 conditional primes; no r. The stronger run `InternalPrefix.py 2089 --fast` succeeded with 3643356 prefix entries, 1928 conditional prime order exclusions; therefore base>10^2089 throughout E3b, not a complete N exclusion. The older baseline 2070 digits used only R=10^11 and no improved prefix. Increasing generic 81 pricing does not help those envelope cells where U=0.
