# Complete canonical exact key (7,438): proof composition

Assume \(N\) odd perfect, \(N\le10^{2400}\), \(19\nmid N\), and \(7^{438}\Vert N\). The exact first pivot is \(t=572749682520506652634407616247\). The [integrated verifier](Full438.py) reconstructs its entire direct exact domain and tests the arithmetic dependencies. The proofs of every first exponent are disjoint as follows:

| Exact \(v_t(N)\) | Exhaustive certificate |
|---|---|
| 4,6,14,20,24,28 | [Frozen first-pivot pack](../../Night2400/Fibers7x438.json.gz), 24 dual forests and complete splits |
| 2,16 | [Frozen additional pack](../../Night2400/G3/Seven438.json.gz), 108 dual forests and complete splits |
| 18,22 | [Reviewed Gemini arithmetic](../../GeminiFrontier/Review.md#2-接受范围的数学依据), with the frozen submitted source hash and recursive primality replay |
| 10 | [Complete second domain](Reserved438.md): all 150 directly viable even exponents of 67; frozen 72 and new 78 |
| 12 | [Complete second domain below](#exact-t12), all 55 directly viable even exponents of 27431; frozen 42 and new 13 |

The directly viable first assignments are precisely \(2,4,6,10,12,14,16,18,20,22,24,28\), with exact raw size tail starting at 57. Every first-pivot proof is conditional on 19 absence, not on any further support mask or exponent-divisibility lifting. The frozen double incidence map and final baseline projection identify the unique singleton `P7_I00084`; the integrated verifier checks both directions and that the frozen projected remainder is exactly `[[7,438]]`.

## Exact t^12

The complete direct pivot domain at \(r=27431\) is every even exponent 2 through 110; first raw size tail 221. Frozen ranges \(74..110\) (even) and \(30..72\) (even) are actually replayed by the same historical checkers within the \(t^{10}\) union. Frozen [28](../../FinalNight2400/ShortSeven/ReviewLast28.md) is independently replayed by its original verifier. Remaining \(2,4,6,8\) are covered by [the Seven packets](Twelve438.md), and \(10,12,14,16,18,20,22,24,26\) by [the propagation packets](../Propagation/VerifyReserved438x12.py) plus [the separate exact h=22 proof](../Propagation/Verify438x22.py). Their exact prefix outputs are matched, not just counted.

For the final h=2, the first forced anchor is \(a=752487193\), with all 27 positive even values 2 through 54 directly live before the raw size tail 110. Its nested forest uses the entire exact even domain for every compelled split vertex (the Euler class is shown disjoint from that vertex). Every forest terminal uses two integer calculations, reserving q first, and pruning q's possible duplicates only with complete integer cofactor intervals. Five leaves are delegated to the independently callable [propagation verifier](../Propagation/VerifyReserved438x12.py#L147): for \(a=752487193\), the bare exact prefixes \(a^{46},a^{52}\), and under \(a^{22}\) the exact \(50047294070406095227\) powers 2,10,12. The sorter uses numeric prime/exponent prefix tuples, not names or valuations alone. The set of used delegated rows must equal precisely those five, without duplication. Remaining rows in that certificate bank are alternative proofs and are not added to the coverage count. The propagated price has weights 2 and 4 with disjoint odd order-length supports; it validates their complete per-base spectrum, not the incomplete high-weight shortcut withdrawn in PR #11. New forests use no Hensel arithmetic.

## Verification

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Seven/Full438.py --historical
~~~

Use `--historical` for a full relevant cold run, not just the new intersection checks. Without it, the verified historical **secondary** domain exclusions are trusted as prerequisites, while all historical first-level packs and their relevant Gemini arithmetic still replay. Author cold receipts: historical first-level union 85.289 s, exact historical 27431 exponent 28 42.316 s, the complete new \(t^{12}\) sibling arithmetic plus all dependencies local to new files 876.773 s, and the \(t^{10}\) integrated four-historical-verifier run 2997.238 s (all exit zero). A complete key does not prove the global odd-perfect lower bound; all unrelated open keys remain unmodified.
