# Complete canonical key (19,330), P19_I00065

Assume an odd perfect N<=10^2400 with exact 19 exponent 330. The historical [C2 proof](../../Night2400/C2/README.md) verifies that the direct domain at forced prime t=1214428680506010004551311201724184433986966434253654794712076383 is {2,4,6,8,10,12}; 8,10,12 are historically certified. The [new first-six proof](DeepProof.md) and [new first-four proof](Four330.md) discharge 6 and 4 with unrestricted Euler forests. It remains to handle exactly t².

1. [Explicit domain and three secondary leaves](DeepProof.md): compulsory r=2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541, exact r-exponents 1,2,4,5,6,8. Exclude 1,5,8. [Abundance trees](Ab330.md) exclude 4 and 6, hence only r².
2. [Exact r² sister partition](Remaining330.md): a=541060314202200985634836209806257 is also forced by sigma(t²), 13 exact viable exponents. Exclude all but 1 and 6; [Euler one proof](EulerOne330.md) excludes a¹ as well.
3. [The final a⁶ checker](LastSix330.py) and [small packet](LastSix330.json.gz) give strict forest overflow with decimal floor 2401. The 195-digit residual factor in sigma(a^6) splits as the product of 34964781683777604014242271896001 and 3534656567580033337992379213961046503307673007087613912884719332240087361776512320201661601519143478409376436360299487240696387991932360005034708010487790700240069. Native free GMP-ECM found them; the proof verifies divisibility and ECPP chains. Compulsory 3,7,29 and these two large vertex roots support the 45-edge free-Euler forest. Local bans 5 and 11 are not global assumptions: each is re-derived by exact rational minimum abundance over all Euler placements under the current forced exponents. The standard integer forest uses these bans only after their proof. Both possible Euler allocations in the tree and Euler outside it are covered. No unproved cofactor primality needed.

**Conclusion: all six exact first valuations are closed.** Replay just this complete key and dependencies (no full-repository regression claim):

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/ShortNineteen/Full330.py
