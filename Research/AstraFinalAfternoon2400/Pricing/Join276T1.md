# Parent fiber `(19,276),1176672733^1`: exact join and counting

Frozen baseline `495c59f55456a70994ce7848487e0c4e262c1984`. Bound `10^2400`. All records denote **exact** exponents. This join is independent of the withdrawn PR #11 proof and never uses its high-weight minimum-residue table.

[Verify276T1.py](Verify276T1.py) rebuilds the underlying domain in integer arithmetic separately from the baseline accepted splitter. From `19^276,1176672733^1`, `1109` has known incoming valuation exactly one. Euler is fixed at `1176672733`, so `h=v1109(N)` must be even. The necessary raw bound `X(D/1109)1109^h≤B` is strictly false starting at `h=555`; before that tail, exactly 138 exponents `2,4,…,276` pass both the necessary exact incoming and raw/abundance tests.

| Child | Complete proof covered by |
|---|---|
| `h=6,8,…,276` (136) | Exact accepted frozen Gemini branch, hash-bound to its original code and inputs; see [Review.md](../../GeminiFrontier/November28/Review.md#L35-L37). |
| `h=4` | Nine distinct order-277 supplier triples exhausted by exact combined reserve, [Proof276.md](Proof276.md). |
| `h=2` | `1,723` initial source rows, `45` raw survivors, of which 38 close by single incoming-source price and six by joint CRT price; the one exact residual `13^276` is then closed by [VerifyHard13.py](../Nineteen/VerifyHard13.py), including its only remaining exponent-2 cofactor child. See [H2LocalPricing.md](H2LocalPricing.md) and [RareTarget13.md](RareTarget13.md). |

```sh
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/Verify276T1.py --independent
```

The ordinary run includes the market proofs, the original bound accepted frozen review, the entire Hard13 subproof and the separately reconstructed parent domain. The `--independent` run additionally invokes the alternate [h=4 audit](../Audit/Check19x276x1109x4.py) and [h=2 source partition and price audit](../Audit/Check19x276x1109x2.py). Those audits are independent of the original arithmetic for their respective source partitions and do **not** on their own duplicate the entire Hard13 subproof.

**Counting:** count one first-pivot parent fiber for this union, not 138 new exclusions. Keep each nested child/subproof as traceability only; in particular the 136 baseline entries remain historical. The other first-pivot values `2,8,16,18,28` are not covered by this join; `(19,276)` and its canonical shard remain open.
