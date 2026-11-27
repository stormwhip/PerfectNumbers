# Complete first 22 at (19,222)

[Earlier direct](Firsts.md), [second](Two.md) and [third](Thirds.md) arguments leave two secondary exponents g at 3705121363 when t=7579985624053 has exact g_t=22. At g=2 only v_371183958661=12 survives. At g=16, the 11 possible exponents of 1355978893 are 1,2,4,6,10,16,22,24,28,30,36. The [checker](TwentyTwo.py) discharges these exact prefixes using strict unrestricted-Euler forests (148 leaves, 1,074 ECPP). Where the forest is not direct, all legal exponents at compulsory prime 2677 are re-enumerated through the actual strict tail; no depth limit or sparse output is accepted. The [packet](TwentyTwo.json.gz) verifies all prime labels and owner lists, not their discovery timing or empirical bounds. In combination this leaves only f=1,2,16,18 in the whole key; 49/53 are closed.

    python -I -S -B Research/FinalNight2400/Root222/TwentyTwo.py
