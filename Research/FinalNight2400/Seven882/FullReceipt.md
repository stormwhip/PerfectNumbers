# FULL canonical (7,882) — P7_I00152

**PASS**: complete isolated stock CPython verifier exit 0, 670.623 s wall (epoch milliseconds 1795800854275–1795801524898). Command:

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Seven882/Full882.py
~~~

The replay reconstructed 70 compatible first valuations and all 64 canonical support masks. Historical G7 leaves open firsts 1,2,4,8,12,72; independently replayed Root7Joint excludes 72, and the earlier SevenEight supplement excludes both entire relevant masks 54,186 on firsts 2 and 8. The new results finish **all** remaining obligations; no mask projection or historical partial is promoted by itself.

| First 21193 exponent | Exact split nodes | Strict forest leaves | Additional cuts | ECPP chains |
|---|---:|---:|---|---:|
| 1 | 7 | 135 | 3 fixed-Euler prices; 1 square | 809 |
| 2, on needed masks | 32 | 875 | 11 mask gates, 41 conflict, 51 supplier-window, 1 abundance, 2 square, 2 fixed-price | 1727 |
| 4 | 11 | 429 | none needed | 763 |
| 8, on needed masks | 9 | 156 | 2 mask gates; 3 conflicts | 353 |
| 12 | 1 | 3 | none needed | 112 |

Final line: FULL canonical (7,882), P7_I00152: 70 first exponents; all 64 support masks. This certifies exactly one canonical pair and its singleton shard under N≤10^2400; no extrapolation to other 7 exponents. The verified payloads and dependencies are enumerated in Inventory.py. Proof.md gives the mathematical justification. No native factoring or network is required in replay.

The 7-price code was hardened during this run to explicitly admit Euler-square bases passing a necessary prime test on their square root. PriceAudit.py checked that the returned rational product is identical: no odd squares occur among the least primitive cubic representatives in the entire range 1..882. The final sealed first2 checker separately passed with the explicit square-aware code; the independent clean-review command loads that code from the start.
