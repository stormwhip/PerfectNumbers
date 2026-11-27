# Factor-free inverse nonoverlap from exact short-polynomial pairs

**Lemma.** Let A=Φ_619(19)/2477 and assume N≤10^2400 odd perfect. An external ordinary y^h attaining u=v_19(σ(y^h))≥185 must satisfy y∤A. No unproved factorization of A and no probabilistic assumption. This is a structural lemma, not by itself a case or key exclusion.

**From supply to residue.** The case y=19 contributes nothing. If y≡1 mod19 then u=v_19(h+1)≤2 since h+1<19³ by 3^(19³−1)>B. Otherwise positive supply requires o=ord_19(y)∈{3,9}, u0=v_19(y^o−1)≥u−2≥183 by LTE. Therefore y is one of the eight nontrivial ninth roots mod 19^183. If y|A then ord_y(19)=619: 619∤A and order 1 would force y|619. Thus y≡1 mod1238 and belongs to one of 8 CRT classes mod M=1238·19^183. The cofactor A/y occupies its inverse class A/R mod M. Either y or A/y, call it b, is ≤sqrt(A), is a divisor of A, and belongs to one of these 16 classes. The checks include b=1 by noting every least class representative exceeds 1. Thus it suffices to rule out b=R+Mx for these 16 least R and all integers x≥0 through sqrt(A).

**Deterministic polynomial certificates.** At x=0 check R∤A directly. Partition the possible y-sized *divisor b* interval [min R,isqrt(A)] by contiguous certified bands [lo,hi] (the lower endpoint may be below min R). Take integer X=floor((hi−R)/M). For any positive x≤X with b|A, put g(Xvar)=Xvar+c where c≡R/M mod A, balanced sign; then b|g(x), since M·g(x)≡b≡0 mod b and gcd(M,A)=1. For fixed band-specific integers k,n construct n integer polynomials

    B_l(Xvar)=Xvar^(l−j) · (Xvar+c)^j · A^(k−j), j=min(l,k), 0≤l<n.

At a candidate x, every value B_l(x) is divisible by b^k. Consequently any integral combination H is, too. The packet supplies *two* explicit coefficient vectors per class/band for combinations H1,H2 with Σ|H_i,j| X^j < lo^k. This strict integer bound precludes any nonzero H_i(x) divisible by b^k. Both H1(x),H2(x) would therefore vanish. Reduce modulo the verified prime 65537: their reductions have gcd 1, so cannot have any common root, in particular not x mod 65537. No reliance on LLL optimality or on a numerical root finder. The optional PARI LLL stage merely found vectors; the sole proof inputs are their coordinates. All 160 nonempty exact bands/classes pass. The reduced-polynomial leading check is conservative; modular coprimality alone excludes an actual simultaneous integer root.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyLattice.py

**Use.** With D=A·H, any external y^h that supplies q as well as ≥185 powers of 19 has already paid cost in D at most H, even if gcd(A,H)>1. This enables the monotone comparison base·2Q_s·19^u>3HB starting at u=185. Unlike a full factorization of A, no restriction on small-valuation factors of A is inferred.
