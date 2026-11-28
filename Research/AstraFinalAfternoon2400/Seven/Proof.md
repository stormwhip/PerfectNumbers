# Canonical root 7: exact-prefix factor forests

Work against frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. Assume an odd perfect number \(N\le B=10^{2400}\), with \(19\nmid N\). All component exponents below are exact. No result is a whole key or shard. No Hensel calculation or prime-order price is used in the packets covered by the main verifier below. In particular the unrestricted new forest cuts at `(7,438)` do **not** assume the inherited Euler-prime location or exponent; both are unrestricted in that checker. The [separate Euler-reserved packets](Reserved438.md) re-prove the restriction that they need.

## Covered exact prefixes

Let \(t=572749682520506652634407616247\), \(Q=16148168401\), and \(T=(1+Q+\dots+Q^{12})/13\). New results are relative to the [frozen root-seven report](../../FinalNight2400/Report.md) and its [exact ledger](../../FinalNight2400/Results.json).

| Sealed packet | Required exact components | Newly excluded exponents |
|---|---|---|
| [48a](Forest48a.json.gz) | \(7^{48},6106505825833677713^4\) | \(v_A\in\{8,10,12,14,16,18\}\), \(A=5913168485260377611579965807967983090512568398832018674784831\) |
| [48b](Forest48b.json.gz) | same | \(v_A\in\{4,6\}\) |
| [438a](Forest438a.json.gz) | \(7^{438},t^{10}\) | \(v_{67}\in\{130,132,134,136,138,140,142,144,146,150,152,154,156,158\}\) |
| [438b](Forest438b.json.gz) | \(7^{438},t^{10}\) | \(v_{67}\in\{36,38,42,50,52,54,58,64,66,68,70,72,74,76,78,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,126,128\}\) |
| [438c](Forest438c.json.gz) | \(7^{438},t^{10}\) | \(v_{67}\in\{12,16,22,28,30,34\}\) |
| [12a](Forest12a.json.gz) | \(7^{12},Q^{12},T^2\) | \(v_{3453283}\in\{10,16,22\}\) |
| [12a](Forest12a.json.gz) | \(7^{12},Q^{42}\) | \(v_{173}\in\{160,162,164,168,170,174,178,186,188,194\}\) |
| [12b](Forest12b.json.gz) | \(7^{12},Q^{42}\) | \(v_{173}\in\{64,66,68,70,72,74,76,84,86,88,90,92,94,98,100,102,104,108,110,112,114,116,118,122,128,132,134,140,142,144,146,152,154\}\) |
| [12c](Forest12c.json.gz) | \(7^{12},Q^{42}\) | \(v_{173}\in\{14,20,28,34,38,44,46,50,52,54,56,60,62\}\) |
| [12d](Forest12d.json.gz) | \(7^{12},Q^{12},T^2\) | \(v_{3453283}\in\{26,46,48,52,58,108,112\}\) |
| [12d](Forest12d.json.gz) | \(7^{12},Q^{42}\) | \(v_{173}\in\{26,32,80,120,124,148\}\) |
| [12e](Forest12e.json.gz) | \(7^{12},Q^{42}\) | \(v_{173}\in\{22,82,96\}\) |

The three unrestricted 438 packets are pairwise disjoint. On their own they leave 21 of the frozen 78 live exact 67-exponents on the \(t^{10}\) sibling. The separate [Euler-reserved proof](Reserved438.md) closes those final 21, so the complete first exponent \(v_t=10\) is excluded. The \(t^{12}\) sibling is not touched by this proof. The two disjoint 12 prefixes leave 20 of 30 exact \(3453283\)-exponents and 21 of 86 exact 173-exponents, respectively; 12a–12e are pairwise disjoint and disjoint from the frozen cuts. At `(7,48)` the fixed first exponent 4 forces \(A\), with exactly nine directly live exponents \(2,4,\ldots,18\) before the first strict raw size tail 37; verify this domain by `child_domain([(7,48),(S48,4)],(19,),A48)` in the checker. The forest packets cover all but \(v_A=2\). In that exact square branch, \(3,11,29,41\) are compulsory. Ordinary 11 cannot have exponent 2 because \(\sigma(11^2)=133=7\cdot19\), so \(v_{11}\ge4\). Even with 29 and 41 each charged at exponent 1 (allowing both only relaxes the lower bound), the strict abundancy of \(7^{48}11^4 29\cdot41\cdot3^4\) forces the ordinary 3's exponent to equal 2. Then \(\sigma(3^2)=13\) forces 13, and the strict abundancy of \(7^{48}11^4 29\cdot41\cdot3^2\cdot13\) is already >2. The [integrated fourth-first verifier](Full48Fourth.py) checks both packets, all nine exact branches including this elementary endpoint, both abundancy inequalities as integers, and the strict size tail. Thus the entire first value 4 at `(7,48)` is excluded; separate firsts 2,8,10 remain. It is not a whole key/shard. The separate [eighth first exponent](Full48Eight.md) is also excluded, leaving exact firsts 2 and 10.

## Integer certificate

For a prefix of distinct exact odd prime powers \(p^h\Vert N\), form \(X=\prod p^h\), the product \(S\) of the odd parts of their geometric sums, and \(D\), the part of \(S\) prime to \(X\). Then \(XD\mid N\): \(D\mid N\) follows from \(\sigma(N)=2N\), and \(\gcd(X,D)=1\). A proposed next pivot \(r\) must be certified prime, outside the prefix and not forbidden, with \(a=v_r(D)>0\). Its exact exponent \(k\) is at least \(a\), and \(X(D/r^a)r^k\mid N\). Enumerate **every** \(k\) from \(a\) through the last value for which this increasing expression is ≤B. On smaller values the checker discards only Euler-form incompatibility, a forbidden dividing prime or sigma factor, oversupply at a fixed prime, strict updated mass, or strict partial abundancy. Both size and abundance equality are retained. The checker allows at most one exact prefix exponent odd, and any odd row must have both base and exponent 1 mod 4; Euler's form for odd perfect numbers then gives precisely one factor 2 in that row's sigma. The only additional split in 438a is in exact \(v_{67}=156\): the actual split label and all three live exponents are recovered from its packet and compared with this integer domain, not trusted as a transversal supplied by discovery. The first raw exclusive tail is 23. The two additional 438c splits are at exact \(v_{67}=12,34\), with 25 and 57 live branches and first raw tails 76 and 171. 12b additionally splits exact \(v_{173}=72\) into 7 live branches before its strict raw tail 22. Every split child must be present and verified.

Each terminal stores a validated forest with selected roots dividing \(D\), and at most one owner for each non-root certified prime outside the support of \(XD\). These directed edges are acyclic and reachable strictly from the selected roots. For a possible exponent \(k\) at an activated prime \(z\), charge \(z^k\) and the odd part of \(\sigma(z^k)\) outside all bases already paid by \(X,D\) or tracked forest vertices. Activate each owned child \(r\) only if \(r\mid \sigma(z^k)\), with demand \(v_r(\sigma(z^k))\); ignore other potential inflows, which can only increase its true exponent. Each root's original part of \(D\) is removed before charging its actual power. Other stripped emissions from distinct active primes may overlap each other: their **product** divides the odd part of \(\sigma(N)\), and their collective support is disjoint from every separately paid basis. This is why neither repeated incidences nor anonymous residuals lead to double charges.

Each recursion minimizes the terminal product over all legal parity/exponent possibilities, including at most **one** special exponent at any forest vertex and the possibility that the actual Euler prime is outside the forest. If the prefix already has an Euler row, all descendants are ordinary. In the finite scan each rejected exponent would emit a forbidden prime, and the remaining monotone exact tail is bounded by \(z^k\) alone, without requiring a factorization of its emission. The [Compose evaluator](../../Nov25/Compose/Compose.py#L54) uses distinct ordinary/optional/special/below states; the [second evaluator](../../Night2400/A/MaskedForest.py#L6) computes a pair of minima and independently reconstructs geometric sums, stripping, valuations, and the tail. Both must return a strict integer lower bound >B per terminal; printed integer ratios are diagnostics only.

The 12a left prefix uses two absences, re-proved inside the verifier. \(3,13\) are forced from the listed geometric sums. Since \(3\equiv3\pmod4\), it has at least exponent 2, and adding \(5\) would already make the product of abundancies of \(7^{12},3^2,5\) exceed 2. If 11 occurs it is ordinary, so its exponent is ≥2. The strict abundancy tests for \(7^{12},11^2,3^4,13\) and for \(7^{12},11^2,3^2,13^2\) force \(v_3=2,v_{13}=1\), but both \(\sigma(3^2)\) and \(\sigma(Q^{12})\) contribute a 13. Thus 5 and 11 are absent only on this exact prefix. This argument does not presume the exponent of \(3453283\).

## Replay

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyForest.py Research/AstraFinalAfternoon2400/Seven/Forest438a.json.gz Research/AstraFinalAfternoon2400/Seven/Forest438b.json.gz Research/AstraFinalAfternoon2400/Seven/Forest438c.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12a.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12b.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12c.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12d.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12e.json.gz Research/AstraFinalAfternoon2400/Seven/Forest48a.json.gz Research/AstraFinalAfternoon2400/Seven/Forest48b.json.gz
~~~

The [verifier](VerifyForest.py) requires every ECPP chain to be used and every large label verified as prime; small labels use the frozen deterministic 64-bit primality routine. The factor index, local ECM and PARI are discovery/sealing tools only, with no proof-time dependency. Private explorations with missing leaves are not included. Proof packets and author cold verification:

| Packet | SHA-256 | ECPP | Split / terminals | Minimum \(\lfloor10^6\,\mathrm{LB}/B\rfloor\) |
|---|---|---:|---:|---:|
| 48a | `65361a2a06a7aabecfbe2e6d54bea1468554b5a10c61bc3fd40f9c9a9ec4c44e` | 152 | 0 / 6 | 840627870388672 |
| 48b | `92d1684d24a071b2f9e3636c55760ef1f63b6c91c024e5144846d72fbb897fdf` | 249 | 0 / 2 | 55266246460 |
| 438a | `ed862b6cc0f6a3a13fd4b7740825d3bed0f41861eb88a88353aae1d12a3f5b6d` | 125 | 1 / 16 | 199604667 |
| 438b | `84283ffbe0884a019647faa7ddb0746a1623e50a200b5d625ddfbd1e1dc40777` | 515 | 0 / 37 | 3227368 |
| 438c | `d7ac09f97d59087aa08e9ae5dff07ae158108552d79606b63e159af9a6b429f3` | 583 | 2 / 86 | 1025350 |
| 12a | `393ed361ee148eb28cd618271ba3adb7ff21833c4704818fbd3eda375bbfe675` | 253 | 0 / 13 | 2475189206 |
| 12b | `1b235c54fd29601e6ce1945df11d1a6c114602ed84faf00d21909d784158b91e` | 584 | 1 / 39 | 2047195 |
| 12c | `be38d3fa519ded27b8306fc0634e0a8aceb6d870a1d2fbad17e446bab2f958e1` | 613 | 0 / 13 | 4814183 |
| 12d | `f80f410cd157798ba21a9c15236794f9792e406484917f78b334cc5c968e9d0b` | 521 | 0 / 13 | 12542128 |
| 12e | `c9d915fd14c48ea4c35be188799f39d0547fccd92e6fda81d766b81df94d07f2` | 286 | 3 / 65 | 25094692 |
