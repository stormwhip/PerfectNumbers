# Exact pivot fibers and support exclusions at (19,372)

For an odd perfect `N ≤ 10^2400` with `19^372 ∥ N`, the [tree packet](Nineteen372.json.gz) excludes ten complete valuations of the certified prime `Q=1778821967075836734748678577738665121`: `1,5,9,12,13,14,16,17,18,20`. The [support addendum](Support372.json.gz) excludes all remaining possibilities under exact S8 support masks `105,113,189` in order `(19,7,11,31,13,3,5,17)`. These are three full conditional support exclusions, not three closed shards. The exact exponent remains open.

```powershell
python -I -S -B Research/Night2400/G4/Verify.py
python -I -S -B Research/Night2400/G4/Support.py
```

The first checker replays the tree and every non-open leaf. The second replays the same tree, verifies that it enumerates every live first-pivot child, and checks that every exact path marked open is impossible for each claimed mask. Both run with standard library and public proof arithmetic only; they do not load the handoff, factor dictionary, or historical support ledger. Tree SHA-256: `7b9195e39ec013badb2d180b5e14fa3daa7f67a1acb8afa91b2e35ba9a6fd323`. Support SHA-256: `a4b928d9d5662892965797ea0eb987df7a4c9ff3505b85e61156a61d9dc8e3e4`.

## Coverage and remaining paths

The checker proves `v_Q(σ(19^372))=1` and exhausts every exact first-pivot exponent up to the monotone size tail, which starts at 41. Quadratic parity, incoming divisor valuations, partial abundancy and the divisibility-size bound remove all but `1,2,4,5,6,8,9,10,12,13,14,16,17,18,20`. All remaining first-pivot values branch on `U=2596142207347868442596070019`. Each forest uses two exact arithmetic recurrences and must strictly exceed `10^2400`; a printed floor of 2400 alone is not accepted.

| Unclosed `v_Q` | Compatible `v_U` still open without additional support |
|---:|---|
| 2 | 2,4,6,8,10,12,16,18 |
| 4 | 2,4,6,10,12,16,18 |
| 6 | 2,6,10,12 |
| 8 | 2,6,10,12 |
| 10 | 6 |

The open markers are explicit and are not accepted as proofs. For the three exact masks in the addendum, every marker is excluded either because a forbidden prime already divides the assigned components' divisor sums, or because an exact rational lower abundancy exceeds 2 even after choosing the best permitted Euler position.

## Discovery

The handed-off ordinary tree already supported nine complete first-pivot values. For `v_Q=1`, its two deepest gaps were `v_U=4,6`. Deterministic short [ECM](Ecm.sh) found the 95-bit prime `20063843702907083024413624361` and a 172-bit prime cofactor in the former. [Witness ECM](EcmWitness.sh) found new useful prime labels in recurrent forced emissions, closing both paths without a support restriction. The final `v_Q=1` tree has 13 forest leaves, with minimum lower-bound floor 2403, and one `U` split with first size-only tail 53. `v_Q=10` still has one gap at `v_U=6`; the separator prime 443607247 can pay its minimum at exact exponent 10, leaving a 281-bit composite emission not split by the short runs. Other new forest leaves tighten `v_Q=2,4,6,8,10` without claiming the whole fibers.

[Domain.py](Domain.py), [Search.py](Search.py), [Seal.py](Seal.py), and [SealSupport.py](SealSupport.py) are optional discovery and serialization scripts. The proof checks every prime label it uses; a guessed or unfactored remainder is never charged as a prime.
