# Strict pivot coverage at canonical (13,508)

Assume an odd perfect number `N ≤ 10^2400`, `19,7,11,31 ∤ N`, and `13^508 ∥ N` (`P13_I00096`). The [packet](Thirteen508.json.gz) is an incremental exact proof, not a closure of the exponent. The first pivot is the certified prime `4073`, dividing `σ(13^508)` to exponent one.

```powershell
python -I -S -B Research/Night2400/G8/MaskedVerify.py
```

The [offline checker](MaskedVerify.py) only uses the standard library and published proof arithmetic. It enumerates every compatible first-pivot valuation until the monotone size tail starts at 353. After parity, exact incoming valuation, forbidden-prime, size and partial-abundancy tests, 46 first values remain. On the eight canonical S8 exact masks (`16,48,80,112,144,176,208,240` in order `19,7,11,31,13,3,5,17`) these give 368 raw mask–first-value pairs. The frozen projection retains `48,112,176,240`, but its completeness is not used by the verifier.

The final packet closes **44/46 first values**. The only remaining first values are `6` (four mask–value cells) and `108` (eight cells); seven of those twelve cells lie in the frozen projection. No complete mask or shard is claimed. The explicit residual at `v_4073=6` is `v_3032394642737237=4` on masks `16,48,112,176`; all eight masks still have `v_4073=108` open. Packet SHA-256: `d798580b1e3e4760bcb67da93e5f9c37611ef1997d543e4a6d904a0d722c9680`.

Every proof leaf replays independently of discovery. A tree requires a certified forced split prime and all compatible exact siblings, with the whole omitted size tail. The two forest recurrences must each strictly exceed `10^2400`; a decimal floor of 2400 alone is not a proof. An `open` marker never earns coverage. Abundancy proofs use exact rational factors and take the minimum over admissible Euler placements, including an exterior Euler component.

The main progress below the shallow forest threshold came from splitting the exact `v_4073=10,12` prefixes on their largest compelled primes `159387017168296185666158069` and `284483325856762389425983276524293`, respectively. Short deterministic ECM on recurring emissions supplied useful factors in the last forest leaves. The first-exponent 10 Euler subcase at secondary exponent 1 is excluded by direct/support arithmetic and abundancy; all other eight secondary siblings have strict forests. All seven secondary siblings for first-exponent 12 have strict forests. At first-exponent 52, the nine-way split on `765692473186112212513185113` likewise gave strict leaves.

The minimum first exponent is 6. Its split on `3032394642737237` has 17 exact compatible values in the unmasked domain. After the size forests and support-specific checks, only secondary exponent 4 remains open. The corresponding 206-bit sigma block was not split in the capped trial. First exponent 108 has an unresolved 1296-bit emission with no supplied prime label; the bare joint price ran into an exterior Euler window. The 1868-bit root cofactor was not split in the bounded trial.

[Domain.py](Domain.py), [Search.py](Search.py), [Seal.py](Seal.py), and the [root](Ecm.sh), [witness](EcmWitness.sh), [low](EcmLow.sh), and [mid](EcmMid.sh) factor scripts are discovery tools only. They are not invoked in cold replay. No total ledger is modified.
