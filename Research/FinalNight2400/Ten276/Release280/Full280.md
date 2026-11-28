# Full candidate: exact (19,280), singleton P19_I00058

**Claim.** No odd perfect N ≤ 10^2400 has 19^280 || N. This is a single exact-key claim: 19 is first in the canonical ordering so no smaller canonical prime is excluded by assumption. Its sole baseline incidence is the singleton P19_I00058; this is not the global bound. This document explains the finite proof; the full integrated replay is the acceptance criterion, not discovery output or merely the presence of certificates.

## Complete domain, including provenance

Let s=353998162545967. It is a compulsory prime with exact valuation one in σ(19^280), and is 3 mod4. The complete viable valuation list at s is the 29 even numbers 2..58 after raw tail 117, incompatible Euler exponents and direct contradictions. The [historical 25-fiber proof](../../../Night2400/Receipts/Review19x280.md) closes every value except 2,16,18,22. The [historical C13 packet](../../../Night2400/C13/README.md) independently closes exact 22; no outcome is inferred from a scout run. Thus it suffices to close three values 2,16,18.

* **2:** use the [complete first-square proof](FirstTwo280.md), which reconstructs the entire 23-value next domain, rather than closing only the old 15 scout gaps. Its elementary exact cost recurrence is described separately in [the free-Euler lemma](Proof280.md). No unsealed scout outcome participates in the argument.
* **16 and 18:** y=16208389663 divides σ(19^280), y≡3 mod4, and its exact valuation must be even. At each fixed s valuation, recompute Y=S/gcd(S,X) from the two exact prefix rows X and odd-part σ product S. After h=v_y(Y), enumerate each admissible y power while X(Y/y^h)y^g≤B; Euler restrictions, overfilled fixed components, exact partial abundancy >2 and mandatory-size failures are checked. The first strict raw exponents at s^16,s^18 are respectively 122,117, and the viable domains are independently regenerated as 2,4,…,60 (30 values) and 2,4,…,58 (29 values). Every one of the 59 exact children is represented exactly once in [the high manifest](HighManifest.json):

|first s valuation|compact forests|recursive abundance/parity trees|hybrid exact splits|total children|
|---:|---:|---:|---:|---:|
|16|18|7|5|30|
|18|17|8|4|29|

## High-fiber witnesses

All are checked from *exact prefix* state, and every newly fixed prime must be certified and forced by an earlier geometric sum. Deterministic elliptic prime certificates reduce to 64-bit deterministic primality; the original search tools are neither trusted nor required.

1. **Compact forest.** Authenticate every root/owner, require compelled root valuations, disjoint ownership, connectivity and valid head. At exact component z^g the only selected children activated are those dividing σ(z^g); checked lower bounds strip all support allocated elsewhere before the new outgoing cost is multiplied. Only one Euler placement is allowed across the whole forest, or none if occupied. Keep a monotone bare-power lower bound on the unexplored tail. Both independent baseline recurrences must strictly exceed B. See [the verifier](VerifyS2.py) and [the historical exact kernel](../../../Session20261126/PivotCheck.py). The floor(log10) may be 2400 but the raw comparison is always strict.
2. **Explicit abundance/parity tree.** The [independent recurrence](Verify280.py) validates the full child set including all possible Euler positions, the deduced absent small primes, distinct compulsory labels and their combined incoming valuation, the exact abundance and mandatory-size inequalities, and raw exponent tails. Details and proof of each rule are in [the free-Euler tree proof](Proof280.md). These witnesses supersede any numerical optimizer, and have no schema for accepting an open leaf.
3. **Hybrid tree.** A nonterminal names a single certified compulsory prime to split on. Each child shown compatible by the stock exact split routine must recurse successfully; the dictionary keys reached must equal the entire submitted scoped witness dictionary. At a forest terminal use both compact recurrences as in (1). An elementary terminal holds a list F of distinct certified primes dividing the mandatory cofactor. For h_l=v_l(Y), smallest ordinary exponent is h_l+h_l mod2 and an Euler candidate can use h_l+((1−h_l) mod4) only if l≡1 mod4 and the Euler slot is unoccupied. Compare either N's abundancy (product of geometric ratios) or its mass X·Y times the missing powers for F. Take the minimum over the all-ordinary choice and each single eligible exceptional choice, then compare strictly. Subset F need not be the complete prime factorization of Y. The [high checker](High280.py) does not use the stored discovery 'full' marker, log estimates, or depth cutoff to accept any row. In total nine hybrid trees contain **160 splits**, 3422 dual-forest terminals, 856 strict abundance terminals and 219 parity-size terminals. Their index is the entire prime/exponent path from the forced split sequence, not simply an arbitrary leaf counter.

## Isolated, local, free replay

~~~text
python -I -S -B Research/FinalNight2400/Ten276/Release280/Full280.py
~~~

[Binder](Full280.py) (a) cold replays the original 25 and C13 first-22 certificates including independent partition, (b) checks baseline singleton incidence in both ledger directions, (c) replays the entire s² union, and (d) rebuilds and verifies both high first domains, asserting no omissions. It does not modify the ledger, and the proof makes no claim for other v₁₉.

For independent parallel examination, the binder's exact components are:

~~~text
python -I -S -B Research/FinalNight2400/Ten276/Release280/Full280.py --history-only
python -I -S -B Research/FinalNight2400/Ten276/Release280/VerifyS2.py
python -I -S -B Research/FinalNight2400/Ten276/Release280/High280.py 16
python -I -S -B Research/FinalNight2400/Ten276/Release280/High280.py 18
~~~

Final 59-cell manifest SHA-256: 4a072ba0b19e3848ade38ae83d1ce45db73fec86cafb7c05885d1765f15cf156. Historical packet hashes are documented in their original receipts. Incremental prime books are deduplicated across these local proof components: include every AbBook, GrowBook and HighBook file referenced by the replay modules. They are fact data checked at use, not trusted oracles. The 12,806 extra prime chains from the high-first generation are split across a [principal book](HighBook55X12363.json.gz) and a [supplement](HighBook59X443.json.gz).
