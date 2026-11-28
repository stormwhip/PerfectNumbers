# Independent audit: (11,462), exact t-exponents 70 and 72

**PASS, conditional only.** Reviewed the [proof](../Fifth/Proof.md) and [verifier](../Fifth/Verify.py), then ran the frozen default command from repository root under CPython 3.11.9 on 2026-11-27 (Beijing). No historical corpus replay or full-key closure is claimed.

    python -I -S -B Research/FinalNight2400/Fifth/Verify.py

Exit 0, 11.3629696 s. Both f=70 and f=72 report 27 low-order exceptions, zero high-order exceptions, and a strict passing window bound. SHA-256 verifier before and after run: 754faff6a085c86c286d0a218af2d376d5c53d2838725231288bc2bfd272243b; proof: bd7ae24622dae977329706aa672ae46160522a74767760499be376e257bcfe82.

I checked the odd orders at 879701 are among 1,5,19,25,95,463,475,2315,8797,11575,43985,219925; generators 2 and 10 at 11 and 879701. Both fixed-block gcds equal exactly 879701. The two fifth-order coordinates occupy the same four powers and are priced by one CRT maximum, not the product of separate overlapping prices. For larger t-order o the o−5 allocation is disjoint from the four powers reserved for 11; 11-adic length multipliers have disjoint support from o and the unused length pays every LTE increment. Every admissible prime base or Euler square survives the short composite sieve: divisibility by sieve prime s discards neither s nor s². Positive even-exponent atoms and the separate q+1 exhaust the Euler row even at a>1. For Euler m above the cutoff, reciprocity excludes q in the root block and size excludes q in the pivot block; below it the verified fifth-power comparison is sufficient. No assumption about f=46 or any other pivot value.
