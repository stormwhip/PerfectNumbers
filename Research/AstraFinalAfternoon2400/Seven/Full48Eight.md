# Complete exact first exponent 8 at canonical (7,48)

Let \(N\le B=10^{2400}\) be odd perfect, \(19\nmid N\), \(7^{48}\Vert N\), and \(t^8\Vert N\), where \(t=6106505825833677713\). This entire first-pivot exponent is impossible. Combined with the [fourth first exponent](Full48Fourth.py) and [the frozen 27-fiber coverage](../../FinalNight2400/LowSeven/Summary.md), precisely first exponents 2 and 10 remain. This does not close the canonical exact root key `(7,48)`, nor claim a shard removal.

The fixed components force 29 and 61 by exact sigma divisibility. If 3 occurs, it is ordinary with exponent at least two. The exact rational abundancy of \(7^{48}\cdot29\cdot61\cdot3^2\cdot5\) exceeds 2, hence 5 is absent in this case. If 11 occurs, it too is ordinary and \(\sigma(11^2)=7\cdot19\) prohibits exponent 2; thus \(v_{11}\ge4\). Then the abundancy of \(7^{48}\cdot29\cdot61\cdot3^4\cdot11^4\) exceeds 2, forcing the only smaller positive even \(v_3=2\). That in turn forces 13 via \(\sigma(3^2)=13\), but the abundancy of \(7^{48}\cdot29\cdot61\cdot3^2\cdot11^4\cdot13\) exceeds 2. Therefore presence of 3 always excludes both 5 and 11, and it also forbids \(v_3=4\) since \(\sigma(3^4)=11^2\).

The [sealed package](Forest48Eight.json.gz) exhausts exactly three disjoint cases:

| Exact conditions | Scope of forest | Vertices | Strict lower bound \(\lfloor10^6\mathrm{LB}/B\rfloor\) |
|---|---|---:|---:|
| \(3\nmid N\) | Banned 19 and 3, no extra support condition | 943 | 413934265945336 |
| \(3^2\Vert N\) | Exact third component, banned 19,5,11 | 1429 | 15959829 |
| \(v_3\ge6\) | 3 a known ordinary root with lower exponent six, banned 19,5,11 | 1414 | 15961940341079 |

For the large exponent range, 3 is explicitly in the forest root set with minimum exponent 6; the evaluator includes all permitted even powers from that minimum up to its monotone size lower tail. There is no transfer of an exact 3 exponent to greater exponents. Each case verifies [the ownership and disjoint residual rule](Proof.md); a root already present by the case hypothesis is allowed even if it did not divide the fixed sigma output, but its valuation and own size are counted only once. The two integer recurrences iterate the entire ordinary / legal Euler choices and use one Euler exception across the recursively activated tree, including the possibility that it lies outside. No Hensel or optional factors are used in replay. The 443 large labels carry elliptic chains, validated to deterministic small endpoints; all are used exactly. Packet SHA-256 `55319c6bf427872e94ec6f69139e9a17c59f090c9139dfe77998d0ac9e8a5e11`.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/Full48Eight.py
~~~

The isolated author run exited zero in 9.746 s. The two >2 comparisons proving 11's absence and the comparison proving 5's absence are made as strict integer products in the checker, not from rounded decimal abundance.
