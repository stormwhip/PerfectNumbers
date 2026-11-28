# Second-cycle exact Q^42 frontier reductions

Under the canonical `(7,12)` assumptions with \(Q^{42}\Vert N\) (\(Q=16148168401\)), the following proof packets are new relative to the 21 exact 173-valuations that remained after 12a–12e. Their exact claims are disjoint; the first-pivot fiber \(Q^{42}\) is not yet entirely closed.

| Packet | Exact 173 powers | SHA-256 | ECPP labels; alternate-terminal data |
|---|---|---|---|
| [12f](Forest12f.json.gz) | 18,24 | `8bd27215bd8c81fa7e17ff430ad1b7454b2a6217403045e11270c78ca610b4b4` | 411; 1 split and 15 dual forests |
| [12g](Forest12g.json.gz) | 190 | `20ff9d8cb7d75bbdb1c94ca4ecb338e6575b70a61069cf74595d97911c651279` | 412; 3 splits, 82 dual forests |
| [12h](Forest12h.json.gz) | 166 | `48cf93f36f80e9ac5586f20e9afd1af4c983273d3723b0df11c3f856a881856f` | 331; 6 splits, 116 dual forests |
| [12i](Forest12i.json.gz) | 150 | `2a5da6d84436cd44cfa75cbb5530c2640d56eab066f160544d9c256aab04665f` | 665; 10 splits, 197 dual forests |
| [12j](Forest12j.json.gz) | 42,48 | `44875997480438adc773b8c8da17bbb1710b8d15ee4ae3fa141f4344d95a00bc` | 296; 2 splits, 12 dual forests |
| [12k](Forest12k.json.gz) | 40 | `0f9415a3c18b34a61e4caafcf8bc3c6d47f5591a6260e10f97924e66117650ab` | 225; 1 split, 10 dual forests |
| [12l](Forest12l.json.gz) | 58 | `06da885eb12d7591e449d644453a6ba16cf3a901c98bdb93d1b63aa069812b09` | 63; 1 split, 5 dual forests |
| [12m](Forest12m.json.gz) | 16 | `c6093e39a3c7805a0c2a3afb50bef69e04353b5f267573b13f8358ea06f3e3ce` | 410; 1 split, 11 dual forests |
| [12n](Forest12n.json.gz) | 36 | `1900dbd3cc1293ad307122c3437fb98b2e929d23976384caf3ce64d948487c3d` | 163; 5 splits, 43 dual forests |
| [Reserved](Q42Reserve.md) | 78,106 | `e272183658f5b408172f63f1c7a2f8a1060cc2fac8d73c6f7d194bcaf7c9e8ed` | 146; full price or congruence forest partition |
| [Masked](Forest12Mask.json.gz) | 8,12,30 | `de406c34f3cb5acb244dc2c71a242cdc50d2c1b18721f734a31f592db5cac3f4` | 619; two disjoint support cases per power |
| [Odd](Forest12Odd.json.gz) | 1 | `db65692d6a615db06052ea906f2a286bb53a59dfec9d190dbd0f377bb8c48650` | 1606; two disjoint ordinary-3 exponent ranges |

The general forests and complete exact split exhaustion use [the previously documented integer accounting](Proof.md), with no Hensel pricing. For the masked even cases split on whether 3 divides \(N\). If absent, add it to the bans; if present, it is an ordinary prime and has exponent at least two. Then \(a(7,12)a(3,2)a(5,1)>2\), where \(a(p,h)=\sigma(p^h)/p^h\), excludes 5, without requiring an Euler identity. The actual bounds use the optional 3 root at its conservative lower exponent two, covering every possible higher exponent.

For the odd case \(173\Vert N\), Euler is fixed there. Its sigma forces 3,29 while the Q row forces 43, so all three are compulsory ordinary with exponents at least two. Compare the product of their lower abundancies and the fixed components. If \(v_3=2\), its sigma additionally forces ordinary 13, and then each of 5,11,17,23,31,37 individually makes the product strictly exceed 2. If \(v_3\ge4\), then each of 5,11,13 individually makes the lower product exceed 2. The two actual forests implement precisely those respective bans, and the higher-3 branch uses 3 as a root with lower exponent four, including its entire remaining size tail. The numerical verifier tests these strict comparisons using products of exact integers, not logarithms. For every masked or odd terminal the independently implemented two-state recursion agrees on strict \(>B\) with the main four-state forest. Isolated cold runtimes for the complete masked and odd packets were 16.567 s and 83.555 s respectively.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/VerifyQ42Masks.py Research/AstraFinalAfternoon2400/Seven/Forest12Mask.json.gz Research/AstraFinalAfternoon2400/Seven/Forest12Odd.json.gz
~~~

A further [masked packet at 173 exponent four](Forest12MaskFour.json.gz) uses exactly the same two support cases and verifier. Author cold replay passed in 64.780 s (730 ECPP labels; minimum strict lower bound 2350852 millionths of \(B\); SHA-256 `d3a59d90b9503e02dd8544a20e8f0cb4e140f898c2887fa0ab0a95788e5118ed`). After all these packets, **83/86** of the originally frozen residual 173 assignments at \(Q^{42}\) are excluded. The exact open complement is **2,6,10**; the separate \(Q^{12}\) first-pivot sibling is not affected here.
