# 2026-11-28 Gemini frontier review

Baseline: main e970138365ef8928c93153a57ea9dcd909ff09e4 (3029/3072 closed, 43 open shards, 53 open keys, 35 singleton shards). Status: VERIFIED_CONDITIONAL, no complete key or shard closure. The eight submitted keys all remain in the current canonical frontier. The original four files are preserved as Submitted.py, SubmittedProof.md, SubmittedValidation.md and Certificates.json. The authoritative local acceptance entry is ReviewVerify.py, not the original status labels.

## Independent replay

On the uploaded LF files, Python isolated standard-library replay returned 0, certified 57 primes, checked 40,943 arithmetic conditions, and reproduced the certificate SHA-256 ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8 in 4.571 s. The eleven supplied negative tests also returned 0; several are demonstration tests rather than full mutated-input replay. The supplementary verifier pins the submitted verifier and certificate hashes, rechecks their prime certificates and reruns all accepted arithmetic with a complete joint-order audit. All eight entries passed the supplementary local replay. No full historical cold replay or 72-hour benchmark was performed.

## Accepted conditional domain

|Key|Exact additional prefix after root|Accepted exclusion|
|---|---|---|
|(7,16)|2767631689^h|h=85,102,108|
|(7,18)|4534166740403^h|h=66|
|(19,222)|7579985624053^1,3705121363^g|g=58|
|(19,222)|7579985624053^1,3705121363^16,3789992812027^j|j=40,42|
|(19,276)|1176672733^1,1109^h|136 of 138 live h, exactly those h>=6; raw tail 555; h=2,4 remain open|

All prefixes denote exact valuations, under the canonical bans and the hypothesis of an odd perfect N<=10^2400. There are 143 accepted local exclusions in the submitted domain. Their overlap with any other historical conditional certificates is not counted as additional complete keys. All global projections remain unchanged.

## Mathematical audit

Write G(b,h)=sigma(b^h), X for the fixed prime-power product, S for the odd part of its sigma, D=S/gcd(S,X), and c_s=v_s(X)-v_s(S). Under a consistent exact prefix, remaining sigma sources supply exactly c_s. For an even exponent h, L=h+1 is odd and at most 5031. If b is coprime to s and ord_s(b)=o>1, then a positive supply requires o|L and LTE gives v_s(G(b,h))=v_s(b^o-1)+v_s(L/o); order 1 gives v_s(L). A source b=s gives zero. The bound on L and the certified factorizations of s-1 exhaust the possible odd orders. Deficit factors per distinct prime base can safely be multiplied; overinclusion of probable primes and lower-order roots only weakens the bound.

For H and G, when Euler is unfixed, use G(q,4k+1)=(q+1)G(q^2,2k), with the residual square atom q^2 distinct from all ordinary prime bases. Its price is q^(4k), while q is paid once separately. The single-target weights 2 or 12 are no larger than the minimum permitted o-1. A positive deficit at valuation z implies b<s^z, and when using the truncation depth Z=ceil(w*c_s/(o-1)) also b<s^Z. Thus the least positive Hensel residues suffice, with the true capped valuation at the terminal depth. Order one and LTE are excluded by L<=5031 in these large-target cases. The supplied primitive roots match the certified roots. H fixed Euler is a direct product inequality; in H and G unfixed Euler, i=v_t(q+1) ranges from 0 to c_t, q>=max(5,2t^i-1). For H the inner congruence q=2t^i-1 mod 4t^i yields the exact cofactor test in the submission. For outer q^1, some ordinary r^h not already fixed supplies q, since q does not divide D; writing u=v_t(G(r,h)), the strict inequality G(r,h)<3r^h/2 yields r^h>2qt^u/3. Removing that supplier from the ordinary price product gives N>2Vq^2/(3t^(2i+u)); independently gcd(D,r^h)<=K_max since the two D blocks are coprime, and N>2XDq^2t^u/(3K_max). Multiplication yields the submitted same-supplier inequality. Outer q^5 or higher is covered directly by XDq^5. For G, quadratic reciprocity excludes q|G(t,h_t) when i>=1, and q exceeds the other block. All integer endpoints replay successfully.

### Correction of the B joint pricing proof

The submitted verifier's order-3 CRT table does not cover all joint supplies with ord_19(b)=9; its higher-second-order scan also cannot substitute for a full joint residue enumeration at small second-target valuation. Replace the joint estimate by the following complete allocation. Fix w=19/10, s=3705121363 or 3789992812027, and work with the tenth power of every deficit. The certified s-1 has v_3(s-1)=1, 19 does not divide it, and s-1>=5031. Thus order 1 at s and s-LTE increments are impossible. For 19, order one costs at least 19^u-1>=18u, which pays its entire contribution since 3^180>19^19. For order a in {3,9} put k=v_19(L); the effective index a*19^k divides L and an extra a*(19^k-1)>=54k exponent units pay the LTE increment (3^540>19^19). All remaining base valuations are bounded by the capped valuation of b^a-1.

If both residual orders equal 3, remove the LTE surcharge from the exponent budget and use the complete cubic CRT table with modulus M=19^i s^j. Since 20>19, positive deficits require b<M, so the least positive representatives are exhaustive, including axes i=0 or j=0. If the 19 order is 9 and the s order is 3, allocate 6 and 2 exponent units respectively, plus 9*(19^k-1) for LTE. If s has higher odd order o>3, then gcd(a*19^k,o)<=3; putting A=a*19^k, lcm(A,o)-1 >= A-1+o-3, so allocate o-3 units to the second target and the remaining A-1 units to 19. For 19 order one its effective index 19^u is coprime to o (and to 3), so the allocation is also valid. Single-target cases use the corresponding relaxed exponent budgets. If the second target alone supplies, the budget o-3 is weaker than o-1 and remains valid.

For each b, let C be the joint cubic deficit to the tenth power, A3 and A9 the separate 19 deficits with budgets 2 and 6, B3 the second cubic deficit with budget 2, and H the maximum over all higher second orders with budget o-3. Missing entries equal 1. A valid bound is max(C,A3,A9,B3,H,A9*B3,max(A3,A9)*H). Each separate budget h satisfies 10h>=19; Hensel truncation at min(c,ceil(19c/(10h))) is exhaustive. The verifier enumerates all higher odd divisors of s-1 up to 5031, retaining nonprimitive roots conservatively. Taking the product across distinct bases proves N^10 >= X^10*(19^c19*s^cs)^19/U10. The repaired exact comparison exceeds (10^2400)^10 for all three prefixes. Diagnostic log10 bounds: 2423.528463, 2493.516199, 2420.560096, respectively. Three deficit bases in each repaired audit.

### E dual pricing justification

For each external ordinary base, its effective index for a supplied target s is s^u (order 1) or ord_s(b)*s^k (higher order, with k the LTE increment). The corresponding reduced exponent is index minus one, an even nonnegative integer; it preserves the sigma valuation of that target. The two effective indices for 19 and 1109 are coprime by the certified odd prime supports of s(s-1). Hence their product divides L and L-1 is at least the sum of the two reduced exponents. Apply each single-target estimate at its own reduced exponent, then multiply. This supplies the required non-double-counting proof absent from the terse submitted statement. For 1109 order 277 the reduced exponent is at least 276; the base-size cap 25000000 follows already from the common prefix. For z<=3, a positive deficit forces b<1109^z since 100<276; z>=4 forces b<25000000<1109^4. Thus the Hensel checks exhaust the only possible positive deficits. Order 1 is paid by 3^1108>1109^100 and higher LTE is excluded by the length cap. For 19 order 1 the bound 19^u-1>=18u pays weight 2; nontrivial orders 3 and 9 with one LTE increment are dominated by their smaller index price using the extra 18o units (3^54>19^2); two increments have exponent at least 1082 and b>=5 (3 has even order mod 19), and three exceed the length cap. The submitted U19 is computed on a superset of remaining bases. Exact split recomputes 138 live values and tail 555, and all 136 h>=6 satisfy the strict product inequality.

## Frontier and use

H retains 44 first values; G retains 13; E retains first values 2,8,16,18,28 plus (first=1,1109 exponent=2 or 4); B retains 17 second-level prefixes, including seven third-level values under first=1, second=16, subject to the inherited domain. A, C, D and F have no accepted new exclusions. In particular the reported A1 and F2 exploratory diagnostics are not accepted certificates. For A the historical 75/76 candidate remains unaccepted.

Run from repository root:
    python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/November28/ReviewVerify.py

The new overlay does not remove any exact key or alter the canonical shard incidence maps. The global theorem remains unproved.
