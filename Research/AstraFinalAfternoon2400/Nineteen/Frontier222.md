# Frozen `(19,222)` coverage ledger

This ledger is an exact-scope summary, not a whole-key claim. Baseline `495c59f55456a70994ce7848487e0c4e262c1984`; first pivot `t=7579985624053`, second pivot `r=3705121363`, with respective actual exponents `f,g`. The original source certifies 50 of 53 first exponents, leaving `f=1,2,18` (raw strict tail 144). The overlays [Inert222](Proof.md), [forest I](Forest222.md), [forest II](Forest222Stage2.md), [forest III](Forest222Stage3.md) [j=4 masked](Mask222J4.md), [j=2 unmasked](Plain222J2.md), and [j=28 complete nested](Root222J28.md) are disjoint new terminal claims at the levels identified in their proofs. The final nested complement and [first-fiber composition](First222F2.md) now exclude first `f=2`, leaving only first `f=1,18`.

| f | g | Frozen third pivot if previously split | Remaining exact third exponents |
|---:|---:|---:|---|
| 1 | 4 | — | whole second window still unrefined |
| 1 | 16 | 3789992812027 | 2,4,8,12,16,18,36 |
| 1 | 22 | 3789992812027 | 2,4,16,18 |
| 1 | 40 | — | whole second window still unrefined |
| 1 | 42 | — | whole second window still unrefined |
| 1 | 46 | — | whole second window still unrefined |
| 18 | 2 | 108501737266216818637411 | 4,6,10 |
| 18 | 12 | — | whole second window still unrefined |
| 18 | 16 | 108501737266216818637411 | 2,4,6,10,12,16 |
| 18 | 22 | 108501737266216818637411 | 2,4,6,10,12 |
| 18 | 42 | — | whole second window still unrefined |
| 18 | 46 | — | whole second window still unrefined |

After the [final f=1,g=2 terminal](Root222F1G2.md), there are 12 open second prefixes. This counts a remaining second prefix once even when multiple exact tertiary values survive. Whole second prefixes newly completed by the disjoint overlay union are `(f,g)=(2,2),(2,16),(2,22),(2,46)`, all completing first `f=2`. None of these statements modifies the global shard counts.
