# Complete first fiber f=12 at (19,618)

This is another full application of the [nested-anchor theorem](ProofNested.md), with all earlier fixed-prefix arithmetic, square/no-square inverse criteria, and price comparisons unchanged. It is *not* reliant on a separately registered partial f12 case: the verifier independently begins at (19,618),(2477,12), then enumerates all new live valuations and size tails.

    python -I -S -B Research/FinalNight2400/Nineteen/VerifyTwelve.py

Set z=3321227264918952026382327955981619089, the largest certified factor of σ(2477^12). At z^4 the extra factor 1464917891 divides σ(z^4); it is a proved prime ≡3 mod4, hence ordinary. Its valuation must be even and positive, with monotone tail from X D/r^v·r^k as for all nested splits. The sealed optional factor lists of its emissions through manageable exponents contain only deterministically certified <2^64 bases; e.g. σ(1464917891²)=2145984428836805773 is prime. For any exponent without a supplied factor row we simply add no extra hints: no unknown factorization is assumed. Every child is rejected by the same direct bounds or the generic compulsory-credit Euler-supplier comparisons. Total 37 visited nodes. The scope is f=12 only. Combined with other audited and reported packets six outstanding first values reduce to five: 2,4,6,8,10.
