# Independent receipt: 212 exact first fibers under nine root-11/13 keys

**Verified conditional**, baseline `495c59f55456a70994ce7848487e0c4e262c1984`. For odd perfect `N≤10^2400`, exclude the exact first assignments listed under `accepted` in the frozen [coverage artifact](../ElevenThirteen/ForestCoverage.json), in the respective canonical classes (`19,7∤N` for root 11; additionally `11,31∤N` for root 13). These are distinct per `(root,root exponent,forced pivot,exact exponent)`; the nine canonical keys are all still open. From immutable Git blobs there are no matching conditional rows in the frozen [FinalNight ledger](../../FinalNight2400/Results.json) or [Gemini November 28 ledger](../../GeminiFrontier/November28/Results.json). The [frozen frontier](../../FinalNight2400/OpenFrontier.json) still has the target keys, including some in shared shards; this local work removes none of them.

Independent [Check11and13Forest.py](Check11and13Forest.py) consumed [Forests.json.gz](../ElevenThirteen/Forests.json.gz) SHA-256 `141fa902e99953ad720e34360ed7e456a83c90133be31b092fcbfec4029f978f`. It certifies each pivot and that it divides the root output, then independently computes geometry sums as finite series and enumerates exact `lcm(X,Sodd)`/mandatory-prefix bounds, bans, partial abundancy and Euler admissibility. Every listed exclusion is in that mandatory live set; the whole set difference equals the declared remaining values exactly. The first strict raw size tail is independently compared at both adjacent exponents and the multiplicative scale proves it covers all larger exponents. The parity-budget forest proof and its independent DP are detailed in the [earlier audit](Root31UpperReceipt.md); the implementation binds the bans for this specific canonical root. The test checks deterministic small certificates, 92 distinct ECPP chains using the [historical prime primitive](../../NightSevenForest/Release/PrimeCheck.py), and a Pocklington chain for the very large pivot in `(11,48)`. Bounds must be strictly greater than `10^2400` even when the displayed floor is 2400.

|Key|Forced pivot|Accepted / initial|Raw strict tail|Minimum bound floor|
|---|---:|---:|---:|---:|
|11,4|3221|42/211|683|2400|
|11,6|45319|21/98|514|2400|
|11,16|50544702849929377|25/47|143|2400|
|11,18|6115909044841454629|15/37|127|2401|
|11,48|100641220283951395639601683|4/19|90|2404|
|13,2|61|51/297|1343|2400|
|13,4|30941|28/122|534|2400|
|13,6|5229043|13/50|357|2403|
|13,8|1609669|13/89|385|2401|

Executed `python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Audit/Check11and13Forest.py`: exit 0. No dependency on trial/discovery records. There is no full-key claim or projection change. If a later certificate under the same pivot proves a descendant of a first already accepted here, its local progress overlaps the parent and must be deduplicated.
