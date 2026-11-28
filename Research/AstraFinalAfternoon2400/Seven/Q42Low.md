# Further conditional subdomains of the last three Q^42 cases

Under canonical `(7,12)` with \(Q=16148168401\) at exact exponent 42, the complete known exact 173 assignments after the [second full-sibling wave](Q42Wave2.md) leave precisely \(2,6,10\). The following additional cuts are intentionally **not counted** as whole 173-assignment exclusions:

| New packet | Assumptions beyond canonical \(7^{12},Q^{42}\) | SHA-256 | Minimum strict lower bound (millionths of \(B\)) |
|---|---|---|---:|
| [Low no-3](Forest12LowerNo3.json.gz) | \(v_{173}=6\) or 10, and \(3\nmid N\) | `bbec3763c0f44646674c58ac769e2659436f9501d0f7f1e8b809fe6c6658af27` | 45230511 |
| [Six with exact 3²](Forest12Low6SquareSimple.json.gz) | \(v_{173}=6\), \(3^2\Vert N\) | `4534f4e59194c3b9db79afb1b7ac3bd1c902c137c0ee10608d4a8f1ed167ad4e` | 2266406 |

In the 3-square case, 43 is compelled by \(\sigma(Q^{42})\) and ordinary; 13 is compelled by \(\sigma(3^2)=13\). If 11 occurs it is ordinary and must have exponent at least 4, because \(\sigma(11^2)=7\cdot19\). The abundancy of \(7^{12}3^2 43^2\cdot13\cdot11^4\) would then exceed 2. Similarly \(7^{12}3^2\cdot5\) already has abundancy strictly above 2. Both bans are re-proved as exact integer inequalities, and the strict forest lower bounds in all claimed rows replay with both integer evaluators. The 3-absent rows use no extra support hypothesis. ECPP counts: 553 for the first packet and 658 for the second.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyQ42Masks.py Research/AstraFinalAfternoon2400/Seven/Forest12LowerNo3.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12Low6SquareSimple.json.gz
~~~

The additional [large-3-tail packet](Forest12LowHigh3.json.gz) excludes \(v_3\ge1200,450,900\) at exact \(v_{173}=2,6,10\), respectively, in three dual integer forests with 922 ECPP labels. Its SHA-256 is `0e245a62c9bdf459f4b4eb700ee97b48505445e2d9cf95339272f961fb6d17ea`; isolated cold replay passed in 52.751 s with the same verifier. Since 3 occurs, the same abundancy test excludes 5. At \(173^{10}\), the presence of 23 from that sigma and 43 from the Q row forces 11 absent if \(v_3\ge4\): its minimum exponent ≥4 would make \(a(7,12)a(3,4)a(43,2)a(23,1)a(11,4)>2\). The lower exponent at the known ordinary 3 root is enforced before the forest's full exponent tail.

The separate [exact 3⁴ packet at 173⁶](Forest12Low6Fourth.json.gz) excludes that exact branch. The fixed \(3^4\) forces 11, which must have exponent ≥4; fixed Q forces ordinary 43 with exponent ≥2. For each additional omitted prime, the checker re-proves its absence by multiplying the fixed lower abundancy \(a(7,12)a(173,6)a(3,4)a(11,4)a(43,2)\) by its exponent-one ratio, and verifies that 5 is absent as above. Dual integer replay passed in 2.757 s with 80 ECPP chains and minimum ratio floor 1676310099 millionths. SHA-256 `bf99f823976b39a9870338f4788579a91e669ca2695432414d168fe3dff836bf`.

The [last pair](Forest12LowLastPair.json.gz) excludes exact \((v_{173},v_3)=(2,4),(6,6)\) in 1889- and 1786-vertex dual forests. The first has its individual 3⁴ abundance bans re-certified as above; the second needs only 19 and 5 absent, with 5 excluded by the same present-3 lower abundancy. Both are strict; minimum ratio floors in millionths of \(B\) are 11690066186 and 4864909. Isolated replay took 16.328 s; 849 ECPP chains, SHA-256 `d0462a223c2552b7525fccdcfeb4778ddef4c46a339d2081007718df1b418e2d`.

Remaining on the last three assignments: at 173² either 3 is absent or \(v_3\) is positive even at most 1198, except 4; at 173⁶ it is even 8 through 448; at 173¹⁰ it is even 2 through 898. These are conservative intervals, not declarations that every value within each is individually directly viable. This is not a complete first-pivot or root-key proof.
