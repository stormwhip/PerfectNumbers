# Strict pivot and support coverage at canonical (7,882)

Assume an odd perfect `N ≤ 10^2400`, with `19 ∤ N` and `7^882 ∥ N`. The [packet](Seven882.json.gz) is a partial certificate for `P7_I00152`, not a closure of the exact exponent. Its forced prime pivot is `Q=21193`.

```powershell
python -I -S -B Research/Night2400/G7/MaskedVerify.py
```

The [cold checker](MaskedVerify.py) uses the standard library and frozen public proof arithmetic, without the root-factor file, ECM, PARI, or the factor bank. It certifies `v_Q(σ(7^882))=1`, and re-enumerates every exact first valuation until the monotone raw-size tail at 212. Euler parity, forbidden factors, exact incoming capacity, partial abundancy and divisibility size leave 70 compatible first values under the canonical root condition. Across all 64 exact root-order masks there are 3488 raw mask–first-valuation pairs. The mask order is `(19,7,11,31,13,3,5,17)`; every mask considered has `m ≡ 2 mod 4`.

The certificate closes **64 of the 70** first-pivot values and **22 of the 64** masks. Exactly one of the 26 historical projected masks is fully excluded: `46`; the other 21 closed masks are outside that projection. The six live first values are `1,2,4,8,12,72`; the respective numbers of unresolved mask–first-value cells are `40,5,40,5,40,42` (172 total, 104 in the historical projection). Packet SHA-256: `0c2126c026c9aec5fd86f2dde96a8fedae3f8498dd274f57a0052d20630a302f`.

The verifier checks every mask and every live child. At each nested split it verifies a compelled prime and rebuilds all siblings up to the monotone size tail. Forest leaves use independent exact recurrences and require an integer bound strictly larger than `10^2400`. An exact forest verified without support restrictions may be reused under several masks. An `open` marker is not a contradiction. The rational abundance leaves minimize over all compatible locations of one Euler component, including an exterior Euler prime.

## Lowest remaining branches

At `v_Q=2`, complete factorization of `σ(Q²)` forces `3,13,1645291`; five masks survive, namely `50,54,58,178,186`. At `v_Q=8`, the same five masks survive initially, and each now has just one open exact secondary assignment, `v_30201838022902600352247769(N)=4`. The latter sigma sum has a 339-bit unfactored block; the short targeted ECM trial did not split it. The 2462-bit root cofactor also remained unsplit in the bounded root trial. These do not limit the direct proof, which charges every untracked composite as a divisor, not as a prime.

The completed `v_Q=10` fiber splits on `9867734838348471700969`. The last of its nine compatible exact secondary leaves had that prime at exponent 1. Short ECM of recurring forced witness emissions found `109316483,458535991` and `2362749121,6872392507,93561411512143`; refreshing the forest with those factors gave a strict cutoff. Mask 46 needed only the final values `v_Q=1,72`; [short witness ECM](EcmWitness.sh) made both bounds strict. For discovery only, use the [domain utilities](Domain.py), [forest search](Search.py), [sealer](Seal.py), and [root ECM](Ecm.sh). No total ledger is modified.
