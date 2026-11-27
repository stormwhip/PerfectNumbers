# Complete (11,462) first pivot 42

The [companion proof](FortyTwo.md) shows that exact 11^462 and t^42, where t=879701, force exact R^6, R=34214860794011. The [final R6 verifier](Six42.py) excludes this last case. Run both from repository root:

    python -I -S -B Research/FinalNight2400/Eleven/FortyTwo.py
    python -I -S -B Research/FinalNight2400/Eleven/Six42.py

The exact identity sigma(R^6)=1201873*a*b, with a=445781254602760137919549783164067 and b=2994389444585561163574775461704890739751087, is recomputed. The factors a,b were discovered with locally cached PARI/GP; neither PARI nor a factorization oracle is used by the checker. Complete Lucas certificates with trial division for small leaves certify a,b; both are 3 mod 4, distinct from all fixed rows, and of compulsory positive even exponent. The same exact size, mixed-price and uniform-source predicates as in the [preceding proof](FortyTwo.md) check every possible exponent at b, then at a if necessary. Depth is bounded at two: any unresolved row causes rejection. Forty leaves close, comprising 2 supplier, 3 simple-price, 5 banned, 11 mandatory, 19 raw. This removes f=42, not the full key or shard.
