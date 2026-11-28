# Complete canonical key (11,462), P11_I00088

**Conclusion.** No odd perfect N<=10^2400 in the canonical root-11 branch (7,19 absent) has exact 11 exponent 462. The historical [audited first partition](../../Night2400/Receipts/Review11x462And13x388.md) has 58 viable values of v_t(N), with t=879701, strict raw size tail 243. The [historical arithmetic packet](../../Night2400/Fibers11x462.json.gz) excludes 49, leaving exactly {1,4,6,22,36,42,46,70,72}. All nine are now covered. None is inferred by divisibility lifting or extrapolation.

| First exponent(s) | Complete conditional branch proof |
|---|---|
|1|[Fixed Euler price with compulsory surplus](One.md)|
|4,6|[Euler membership and ordinary forests](ForestSeal.md)|
|22|Final forest below|
|36|[Complete multi-stage 36 proof](Complete36.md)|
|42|[Complete two-stage 42 proof](Six42.md)|
|46|[Five-prime 46 tree](FortySix.md)|
|70,72|[Fifth-order pricing packet](../Fifth/Proof.md)|

**Final first value 22.** Use exactly the Euler-membership disjunction and mixed fifth-order price in the [4/6 proof](ForestSeal.md), with no reserved 4-branch components needed. Recompute X=11^462 t^22, M=11^462 t^21 and the loss U. The [final forest](OrdinaryForest22.json) has 1,990 distinct vertex labels; the [prime book](PrimeForest22.json.gz) supplies 495 ECPP certificates for those >=2^64. For each of the 1,019 vertex labels q≡1 mod 4 verify (Xq)^5 (M/gcd(M,q+1))^19 > B^5 U, excluding all possible Euler exponents at q. If q is outside the vertex set, every actual forest vertex has even exponent and the standard ordinary-only forest lower bound has floor 2403. All 1,988 directed ownership edges are authenticated via the immutable baseline forest verifier. No factorization or squarefreeness of the 126-digit anonymous sigma(t^22) cofactor is required. The recorded discovery score is not trusted. The standalone arithmetic command for this final branch is:

    python -I -S -B Research/FinalNight2400/Eleven/ForestSeal.py 22

The [integrated checker](FullKey.py) cold-replays only this key's historical packet, independently reconstructs the entire first domain, and cold-replays each conditional proof with its intended exact scope. It does not claim a whole-repository regression.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Eleven/FullKey.py
