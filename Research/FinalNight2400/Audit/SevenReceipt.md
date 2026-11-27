# Independent audit: (7,882), exponent 72 at 21193

Accepted as a conditional exclusion only. The historical union leaves 1,2,4,8,12, with no complete key or shard credit. Existing [historical packet description](../../Night2400/G7/Readme.md) records 42 open mask cells at 72; the new result requires no support hypothesis. Historical G7 arithmetic is not claimed as a new cold replay here.

Audited [proof](../Root7Joint/Proof.md), SHA-256 0e996cfcb87841050c460f21b1d00450cc5567620c01eb92e2a51c68c71e34a0; [verifier](../Root7Joint/Verify.py), SHA-256 fe32b60e0b84bbdcc26686a57367a620d4407b3ca071ef3b1d2c86ad086e633f. Local submitted checker passed in 1.285 s. [Independent implementation](CheckSeven.py) passed in 13.993 s using repeated Frobenius exponentiation on primitive cube roots instead of the submitted Newton lifts and the opposite CRT reconstruction. It tested 252395 representatives, allowing composites and discarding no possible prime bases, and independently obtained 33 exceptional odd bases, product numerator/denominator bit lengths 36048/35220. Both cutoff inequalities are strict. Commands from the checkout root:

~~~sh
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Root7Joint/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Audit/CheckSeven.py
~~~

Soundness review: the odd component of the Euler index is accounted for by factoring its geometric sum at base q²; this unique square atom cannot equal any prime-base atom. Its possible deficit is included without a primality filter. The even index and actual-size cutoff imply the odd orders at t are 3,883,2649 when it supplies. At high order, the reserved 32 powers pay the *entire* 7-coordinate even with the index valuation included. At order one for 7, value is bounded by h+1, and a t order three imposes h≥20. In the remaining cubic case the increase h−2≥18·v7((h+1)/3) pays the extra supply; no t increment is possible. Thus the enumeration and the one maximum charge per base are valid. In the large Euler window, q≡−1 mod 7, q≡1 mod 4 gives (7/q)=−1; an odd-order divisor of q−1 would make 7 a square. This excludes q|A. Also q>C and q is neither 7 nor t, so q multiplies XD without recharging any existing factor. The small window only uses q≥m, not independence from D. This handles all Euler exponents, including 1 and ≥5.
