# Second tranche of complete (3,6) first-pivot exclusions

Under the hypotheses of [the first tranche](ProofFullSix.md), these twelve additional exact valuations v1093 are impossible. Stock isolated replay completed successfully, including all checks of strict bounds, not accepting rounded floors for proof.

|v1093|first pivot|upper tail|live|splits|forest leaves|paired leaves|ECPP|min forest floor|
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
|5|1193557|391|76|80|3673|0|4149|2400|
|102|359087761879729044748645493970102119407|48|9|15|427|0|1441|2400|
|106|64029227661110311466520922008445357|52|6|20|392|0|696|2400|
|130|21727661|221|36|36|834|0|2014|2400|
|148|317633006248891|105|14|9|141|2|499|2400|
|180|80031962871769|95|15|2|31|0|260|2403|
|190|44448554402939|93|16|4|95|0|397|2401|
|192|619939100150929398024401|53|10|3|20|1|146|2400|
|196|4784187024041|97|23|33|859|4|954|2400|
|226|1412993744646848738480685164110162730941|28|6|40|1086|25|1465|2400|
|240|9616400017587385400438896773389435561|27|6|9|80|6|258|2400|
|250|384533|159|36|28|589|12|1722|2400|

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Full.py 5 102 106 130 148 180 190 192 196 226 240 250

Each Full{f}.json.gz is complete and stands alone for its f with the arithmetic verifier and referenced library, no discovery factor data. For all-forest packets the complete proof is the exact two-recursion argument already given in the first tranche. For the paired terminals: with X the chosen exact prime powers, S=σ(X)/2^ε and D=S/gcd(X,S), choose two distinct targets p,q in X. Let c,d be their residual exact deficits and M=p^cq^d. For each unassigned prime-power r^h, h≥2, with m=p^u q^v its contributions to the targets, an exception is r^h<m². At h=2 combine via CRT the choices of exact orders of r modulo p and q and all simple Hensel roots lifted through conservative upper valuation caps. At h≥4 at least one single-target condition r^h<p^(4u) or r^h<q^(4v) is necessary, so enumerate their union. h=3 violates Euler, and other odd h are allowed only if h≡r≡1 mod4. A failed Fermat or proper small divisor only excludes non-primes. The enumerated table is a superset reused under smaller caps; the leaf further removes incompatible fixed labels, forbidden/overflow rows, and anything with X·lcm(D,r^h)>B. U is the product of maximal per-base loss factors (all at least one); then V=XM²/U. These steps are implemented in [FastPair](FastPair.py). Integer and rational arithmetic throughout.

With fixed Euler, all remaining components are ordinary and V>B suffices. Otherwise this same test excludes all Euler exponents ≥5 (all h≥2 have been priced); for Euler exponent one enumerate m=p^i q^j|M, lower endpoint a=2m−1, progression e≡a mod4m. The basic price is V a/m². For other windows use the fixed-σ block cofactor progression: the cofactor of e in any emitting block must lie in b/a mod4m and ≤b/a, where first b/a indicates modular division. If not proved external, the verifier refuses the branch. If external and XD a>B it is impossible. In remaining cases employ the **two opposite bounds on a common emitter** from [the hard product proof](ProofHard66.md): an unassigned ordinary r^h emitting e also contributes t to the targets, so r^h>2et/3. Charging all other ordinary rows yields N>2V a²/(3m²t); independently, charging the mandatory divisor yields N>2XD a²t/(3 max_block), where blocks have first been clustered by common factors so r divides at most one cluster. Multiplying gives a valid N² bound without double-counting or assuming that r is exterior. Every terminal must meet one of these strict criteria. This proof requires no per-base Euler-square assumptions.

In union with [the first tranche](ProofFullSix.md), 17 formerly open firsts are now closed by the two tranches, and all 17 were cold replayed. Together they give 176/182; only **1,2,8,156,166,256** lie outside these two tranches. The independently sealed [full first-1 proof](F1Handoff.md) excludes 1 as well (177/182 including it). That leaves 2,8,156,166,256; no complete key or shard yet. [Rough256](Rough256.md) derives a strong conditional source constraint but not a 256 exclusion.
