# (11,462), f=36: forced 93156840075306751 exponent six

The [first two-pivot proof](ThirtySix.md) forces U=93156840075306751 to exponent 4,6,10,12. Here the [offline checker](ForceSix36.py) removes 4,10,12. Thus U^6 is exact, and R=183172571 has exponent in {2,4,8,10,12,14,16,18}. It is not yet a full f=36 closure.

    python -I -S -B Research/FinalNight2400/Eleven/ThirtySix.py
    python -I -S -B Research/FinalNight2400/Eleven/ForceSix36.py

Use exactly the [f46 joint-price, external q, and source-cut bounds](FortySix.md) plus the [ordinary-prime and exact-tail argument](FortyTwo.md). At U exponents 4,10,12, every open recursive prefix obtains a prime label from its corresponding witness table ([4](Hints36Four.json), [10](Hints36Ten.json), [12](Hints36Twelve.json)); table entries outside the specified starting exponent are ignored. The tables supply no truth values, cutoffs, or computed lower bounds. At use, authenticate each prime via [full Lucas chains](Cert36.json) or trial division, check distinctness and membership in a fixed sigma block, prove it cannot be Euler if 1 mod4, then verify all positive even exponents until strict size overflow. Missing witness for any unsettled leaf fails the replay; every scoped table entry must be reached. The three trees use 16,95,10 splits respectively. This conditional reduction is independent of any unverified discovery label.
