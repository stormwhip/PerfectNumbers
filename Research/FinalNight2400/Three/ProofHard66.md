# Complete closure of the hard (66,6,2,12) exact prefix

Under odd perfection, N≤10^2400=B and absence of 19,7,11,31,13, the following simultaneous exact valuations are impossible:

    (3,12), (797161,66), (5897,6), (42059143035592870990447,2), (589657170962820100934139512775879733212083419,12).

This closes the entire named hard path, **not every sibling** under 5897^6 or the entire 797161^66 fiber. This theorem supersedes the earlier eight-window sharpening. The last argument uses neither roughness nor support masks nor an assumption of squarefreeness.

**Setup and historical price kernel.** Let X be the product of these exact powers, Q=797161, P=the last prime, S=σ(X), D=S/gcd(S,X), A=σ(P^12), T=σ(Q^66)/5897. The verifier rechecks D=AT and gcd(A,T)=gcd(D,X)=1. All are integer identities, so XD|N. The residual amounts of Q and P which σ of the remaining components must supply are 65 and 11: write M=Q^65 P^11. For any unseen component r^h with h≥2 let w(r,h) denote the product of its Q and P supplies (Q^u P^v dividing σ(r^h) exactly on these two primes). The historical cap_two routine computes an upper bound U_r≥max(1,w(r,h)^2/r^h) at each base r; omitted bases have U_r=1. Set U=∏U_r and V=X M²/U. All comparisons use rational or integer arithmetic. For **any subset** of actual unseen h≥2 components, of total target supply w, their product costs ≥ w²/U: each base is used at most once and every U_r≥1. This subset version is important.

For completeness, the price kernel enumerates exceptional bases with r^h<w(r,h)^2 and Xr^h≤B. When h=2 it enumerates the two target residue systems jointly by CRT. For h≥4 an exception must satisfy r^h<q^(4v_q(σ(r^h))) for one of the two targets. It enumerates exact orders dividing gcd(q−1,h+1), lifting each nontrivial simple root modulo q^k; for order 1 the valuation is v_q(h+1), whereas for nontrivial order it is the root lift depth plus v_q(h+1) by LTE. All candidate representatives up to the strict size threshold are tested. h=3 is not Euler-compatible; other odd h require r≡h≡1 mod4. Small divisors and failed Fermat tests only exclude composites, not primes. The least possible unassigned base is 5 since 3 is fixed. The kernel may retain composite bases as extra losses; this only weakens the result. It returns V>B, ruling out Euler exponent ≥5.

**Euler windows.** The unique special prime e therefore has exponent one. For m=Q^i P^j (0≤i≤65, 0≤j≤11) its exact target supply from e+1 is m, hence e≡a=2m−1 mod 4m (as e≡1 mod4 and m odd), e≥a. The subset price first gives N≥V a/m². When this doesn't exceed B, for each block b=A,T the cofactor if e|b must be the unique class b/a mod 4m within [1,b/a]; every candidate in this interval fails exact division. Therefore e∤D. If XD a>B, exclude outright; 184 windows remain. The 1-mod-4 congruence equivalently follows since (e+1)/(2m) is odd (not an assumption that this quotient is 1).

**Same-emitter product.** As e cannot appear in the fixed sums (e∤D and e is not fixed), some unseen ordinary prime power r^h emits e. Let t=w(r,h). The distinct e,Q,P factors imply σ(r^h)≥e t, while σ(r^h)<3r^h/2; hence r^h>2e t/3. Consider two separate lower bounds on N:

1. The other ordinary rows have total target supply M/(m t), so their product is ≥(M/(mt))²/U. Including X,e,r^h gives N>2 V e²/(3 m² t).
2. Because D=AT has coprime blocks, gcd(r^h,D)≤max(A,T), even if the whole emitter lies inside one anonymous block. Thus X·D·e·r^h/gcd(r^h,D) divides N and N>2 X D e² t/(3 max(A,T)).

Multiplying these two inequalities concerns **N²**, not N; it is valid even if they bound the same factors. The unknown t cancels. Therefore N²>4 V X D a⁴/(9 m² max(A,T)). Over all 184 windows the **minimum decimal floor is 4844**, strictly above 4800. This proves the claim. No factoring of A or T is required. The stock isolated verifier is:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Hard66.py

Expected: direct product exclusions 184 of 184, minimum joint lower N² floor 4844.
