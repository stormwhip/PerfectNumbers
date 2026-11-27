# Two fixed-Euler atoms: obligatory internal incoming supply or a large square divisor

Let N≤10^2400 be odd perfect with canonical v_3=12, and assume v_797161=1. Its Euler prime is therefore 797161; Q=398581 is forced by its divisor sum 2Q. Under either exact h=v_Q=102 or h=108 let D=σ(Q^h), the historically difficult anonymous cyclotomic output, X=3^12·797161·Q^h, and let b be the total v_Q(σ(r^f)) over all components with r|D. Let s be the positive integer for which s² is the largest square divisor of D. Without assuming a factorization, write D=s² k with k squarefree. Since D is coprime to X, every r|D is ordinary; their product of final full powers costs at least s²k²=D²/s². This remains valid even if D itself contains high powers.

The components outside XD have total Q-supply exactly h−1−b. Compute the per-base uniform square discounts E_r≥max(1,Q^(2v_Q(σ(r^f)))/r^f) over all possible ordinary unassigned r and all 1≤v≤107 by the same exact scalar Hensel progression enumeration as in [the root-six price proof](ProofSix.md), now with q=398581, fixed Euler, and 3,797161,398581 reserved. There is one discounted base; U=∏E_r. Pricing **only outside** XD uses at most U. Since these three factor groups are disjoint,

    10^2400 ≥ N ≥ X (D²/s²) Q^(2(h−1−b)) / U.

Thus s² Q^(2b) ≥ C = X·D²·Q^(2(h−1)) / (U·10^2400). The exact vertex tradeoff has floor(log10 C)=451 for h=102, 619 for h=108. In particular:

* If D is squarefree, at least 41 internal Q-units are required for h=102 and at least 56 for h=108.
* If h=102 and b=0, then D contains a square s² with s>10^225.
* **If h=108, at least two incoming Q-units must come from prime factors of D** via their final ordinary components (possibly both from one component). Even s²≤D suffices since C>D·Q² from the integer floors 619 vs <617; moreover the checker verifies D is nonsquare and all its prime factors exceed 20 million by direct trial of their order class 1 mod 218. Hence s²≤D/20000001, and in particular C·20000001>D·Q². (The bound actually gives the exact continuous lower threshold for b once s is known.) This is an unconditional necessary structural feature of this remaining exact fiber, not an exclusion of the entire fiber.

    python -I -S -B Research/FinalNight2400/Three/AtomTradeoff.py

No ECM trial, probable-prime test for D or assumption about squarefreeness is necessary for any of these implications. Independently the previously certified order constraints force r≡1 mod 206 or 218 respectively; an exhaustive local sieve raised the certified roughness test to 10^11 on these and the index-97 atom of 797161, without finding factors. The analytic tradeoff does not use that increase. The 80 small native ECM curves and bank-wide gcd pilot likewise have no proof significance when returning no factor.
