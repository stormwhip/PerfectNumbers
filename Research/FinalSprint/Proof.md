# Exact-exponent proofs of 26 November 2026

Assume that $N\le 10^{2400}=B$ is an odd perfect number. Use the canonical root order $(19,7,11,31,13,3,5,17)$; all roots before the specified root are absent. The starting point is [main at 2b53c830](https://github.com/stormwhip/PerfectNumbers/commit/2b53c830dd903b460a315df04fa3a4a410fb8357).

## Exact forest and joint valuation certificates

**Theorem.** The canonical root and its exact exponent cannot be $(7,168)$.

**Proof.** Write $A=\sigma(7^{168})$. The certificate tests primality of

```text
471014884186461786359976424959315520118992312411810290816288422077055549979204503
```

and exact division into $A$; denote this prime by $t$. Thus $t\mid N$. For $c=v_t(A)$, all candidate exponents $f=v_t(N)$ obey $f\ge c$ and $7^{168}(A/t^c)t^f\le B$. Enumerate up to this monotone endpoint. Euler parity, forbidden primes, overflow of a fixed valuation, abundance greater than two, and the integer size bound leave six nontrivial cases: $2,4,6,8,10,12$. For each the [packet](Tree7x168.json.gz) specifies a finite forest. At fixed components with product $X$, the prime-to-$X$ part $D$ of the product of their odd divisor sums satisfies $XD\mid N$. A child activates only on actual divisibility; the newly charged divisor-sum parts are stripped of all fixed and forest labels, so products from distinct sources are justified by multiplicativity. Every compatible exponent is either checked or covered by the bare prime-power bound at the start of its tail. Only one node can receive an Euler discount. Applying the [exact tree theorem and verifier](../Session20261126/TreeCheck.py) gives a lower bound strictly exceeding $B$ on each of the six leaves, independently priced by [a second integer recursion](../Session20261126/PivotCheck.py). Hence no candidate remains. The argument uses exact exponents at every node. ∎

**Two singleton closures by simultaneous valuation.** The canonical pairs $(31,388)$ and $(11,108)$ are impossible. The [joint deficit lemma and proof](JointValuation.md) applies to the full vector of incoming prime-power demands on each hard path. For $(31,388)$ the difficult leaf fixes the 85-bit pivot $29941246365965400246754591$ at exponent 18; all 7,002 Euler-one windows and the high Euler case are excluded. The other seven forest leaves and eight direct contradictions are covered by the [complete tree](JointTree31x388.json.gz). For $(11,108)$ the difficult path fixes two further primes at exponents 6 and 16. All 10,464 Euler-one windows (5,978 by price; 4,114 by block size; 372 by the remaining interior tests) and high Euler are excluded. The other 1,162 forest leaves, 54 split nodes and 1,294 direct cases are checked from the [full tree](JointTree11x108.json.gz). Thus `P31_I00075` and `P11_I00027` close: each had just the stated exponent. ∎

**Two further singleton forest proofs.** For $(7,70)$ and $(19,352)$ the [root-seven tree](Tree7x70.json.gz) and [root-nineteen tree](Tree19x352.json.gz) use the same exact splitting, valuation, Euler and disjoint-charging proof as above. Every split selects a proved prime dividing the compulsory part $D$, and enumerates every feasible actual exponent; both integer lower bounds must pass on every remaining leaf. The respective counts (forest leaves, splits, direct contradictions) are (568,40,618) and (282,13,297). The integer tail is part of every forest test. This exhausts `P7_I00019` and `P19_I00069`. ∎

**Additional complete trees.** The same exact forest theorem applied to the [7,46](Tree7x46.json.gz), [19,348](Tree19x348.json.gz), and [31,348](Tree31x348.json.gz) packets contradicts $N\le B$ on every compatible branch. Their respective (forest, split, direct) counts are (754,24,786), (1516,107,1669), and (861,53,1157). For [11,42](JointTree11x42.json.gz) the partition requires three additional price leaves: the second and third fixed primes alone suffice as valuation targets, keeping all fixed components in the mass. The first two paths fix their exponents at (16,28) and a fourth at 30 or 36, and the third fixes them at (16,46). The three window counts are 448, 448 and 736; none survives. Another 443 forest leaves, 27 splits and 491 direct cases finish the domain. All four previously singleton obligations close. ∎

The [$(7,90)$ certificate](Tree7x90.json.gz) excludes that exact exponent by 454 forest leaves, 16 splits and 469 direct cases. Both `P7_I00003` and `P7_I00005` retain open exponents. The exclusions at 90 and 168 leave 12 as the sole remaining exponent of `P7_I00005`.

The [19,478 packet](Tree19x478.json.gz) exhausts 795 forest leaves, 36 splits and 838 direct contradictions using the exact-tree theorem. Thus `P19_I00090` closes. For [19,448](Tree19x448.json.gz) the identical theorem has 3,026 forest leaves, 222 splits and 3,312 direct contradictions; `P19_I00085` closes. Partial results at root three's *low* exponents are [accounted separately](LowBranches/README.md).

The [11,10 packet](JointTree11x10.json.gz) has 5,109 forest leaves, 366 splits, 5,663 direct contradictions and two fixed-Euler price leaves. The [19,268 packet](Tree19x268.json.gz) has 3,283 forest leaves, 188 splits and 3,569 direct contradictions. The same complete-domain arguments above apply, closing `P11_I00003` and `P19_I00055`. The [support theorems](Support/README.md) give further conditional exclusions.

For [13,456](Tree13x456.json.gz), all 865 exact forest leaves, 38 split nodes and 927 direct contradictions passed the same whole-tree test; `P13_I00087` closes.

**Canonical pair $(19,232)$.** The [complete packet](JointTree19x232.json.gz) verifies 364 forests, 14 splits and 386 direct/abundance contradictions. At the special leaf the compulsory divisors 3,7,13,31,79,20333 force exponents one at 13 and two at 3 by strict abundancy. The new emission $\sigma(3^2)=13$ contradicts the 13 already owed by the fixed components. All other paths pass exact checks. This closes `P19_I00049`.

## Complete source partitions at root three

**Exponent 990.** The [complete proof](Proof990.md) combines the frozen no-five and Euler-location theorems with the newly proved five-present complement. All 64 external-source and 98 internal-source admissible five-exponents cross the strict threshold; the two minimum integer lower bounds are 5,526,917,319 and 5,526,842,626 against 5,526,208,800. The independently compiled native range sieve tested 208,105,567 candidates. The [sealed package](Root3x990.zip) and its [all-domain replay](RootThree.py) include the exact prerequisites; the fresh 162-case replay alone does not establish the frozen no-five complement. `P3_I00168` closes. Full release replay now also needs a C++17 compiler with `unsigned __int128`.

**Exponent 970.** At 970 the positive-five domain and the entire internal-source side are excluded by the [first-stage argument](Proof970.md). The [final two external cases](Full970.md) raise this to a complete proof: all 6,475 and 6,811 source atoms are covered, respectively, and both directed bounds are strict (floors 2444 and 2401). See the [full archive](Root3x970Full.zip) and [replay entry point](Root970.py). The combined argument exhausts the whole domain at 970. `P3_I00165` closes.

## Frozen ledger

Starting with 2,974 closed shards, the 18 new distinct exact-pair exclusions yield 16 additional closed shards. The frozen ledger has 2,990 closed shards and 82 open shards, with 92 distinct remaining pairs. Exactly 74 open shards have one remaining exponent. Conditional scopes contribute to these counts only through a certificate that exhausts the full pair. The [ledger](Delta.json) gives exact shard memberships. The [next proof batch](../Night2400/README.md) starts from this ledger.

| Canonical root | Closed / total | Open | New exact exclusions | Remaining exact exponents |
| ---: | ---: | ---: | --- | --- |
| 19 | 259 / 287 | 28 | 232, 268, 348, 352, 448, 478 | 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 46, 48, 58, 82, 162, 222, 238, 270, 276, 280, 282, 292, 312, 316, 330, 358, 372, 420, 432, 502, 618 |
| 7 | 389 / 412 | 23 | 46, 70, 90, 168 | 4, 6, 10, 12, 16, 18, 24, 28, 34, 36, 48, 130, 420, 430, 438, 456, 486, 490, 586, 600, 682, 732, 738, 808, 882, 906 |
| 11 | 332 / 341 | 9 | 10, 42, 108 | 4, 6, 12, 16, 18, 48, 358, 396, 456, 462 |
| 31 | 244 / 253 | 9 | 348, 388 | 2, 6, 16, 240, 268, 310, 352, 456, 466 |
| 13 | 315 / 325 | 10 | 456 | 2, 4, 6, 8, 262, 310, 372, 388, 508, 612, 618 |
| 3 | 673 / 676 | 3 | 970, 990 | 6, 12, 856 |
| 5 | 481 / 481 | 0 | — | — |
| 17 | 297 / 297 | 0 | — | — |

**Newly closed IDs.** `P19_I00049`, `P19_I00055`, `P19_I00068`, `P19_I00069`, `P19_I00085`, `P19_I00090`, `P7_I00014`, `P7_I00019`, `P11_I00003`, `P11_I00012`, `P11_I00027`, `P31_I00068`, `P31_I00075`, `P13_I00087`, `P3_I00165`, `P3_I00168`.

The eight-root coprime terminal is separate; its independently replayed lower log is 4183.209493. Root 5 and root 17 were fully closed before this sprint. Conditional supports and fixed-pivot fibers do not enter the counts above.

## Replay

Run from the repository root with Python assertions enabled and a C++17 compiler supporting `unsigned __int128`.

```sh
python -I -S -B -X int_max_str_digits=0 Research/FinalSprint/Verify.py
```

The verifier rechecks this increment and recomputes the frozen shard ledger. The 2,974 earlier closures enter as inputs to the projection. The proof at 990 also uses the earlier no-five and valuation-cap results described in [its proof](Proof990.md).
