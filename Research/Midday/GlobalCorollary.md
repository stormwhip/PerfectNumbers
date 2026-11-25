# A support consequence of exhausting the canonical root-five class

Write `B=10^2400` and let `N` be an odd perfect integer with `N<=B`. The historical three-root theorem states that at least one of 3, 5, 7 divides `N`. The first-root order of the canonical ledger is `(19,7,11,31,13,3,5,17)`. Thus an odd perfect `N<=B` divisible by 5 but by none of `3,7,11,13,19,31` belongs to the **canonical root-five class**, independent of whether 17 divides it.

Provided all the 14 remaining root-five exponents have passed their exact terminal verification in addition to the 468 previously closed canonical shards, no such `N` exists. Indeed the exhaustive canonical partition has 481 root-five shards; the remaining 13 consist exactly of the 14 obligations in the frozen terminal input. This gives the following implication:

`3∤N and 7∤N  =>  5|N and (11|N or 13|N or 19|N or 31|N)`.

In particular `{3,7,11,13,19,31}` hits every hypothetical counterexample. This set does **not** replace the stronger cardinality-three hitting set; the point is that the new set omits 5 and 17. This implication uses the historical proof for excluded exponents as well as the new terminal results. It does not assert that arbitrary `5|N` is impossible, nor is it counted as an additional exponent or canonical shard.

Independent terminal replay: `python -I -S -B Research/MiddayFive/Replay.py --audit`. The baseline input is [the Nov25 difference ledger](../Nov25/Delta.json); arithmetic and proof of the terminal inequalities are given in [the root-five proof](../MiddayFive/README.md).
