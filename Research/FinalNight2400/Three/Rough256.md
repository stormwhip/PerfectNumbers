# Factor-free internal-supplier lower bound for (3,6), v1093=256

Let p=1093, X=3^6 p^256, D=σ(p^256), M=p^255. The fixed sums give XD|N and gcd(X,D)=1. No nontrivial factor of this 778-digit composite was needed in the proof. Define s² as the largest square divisor of D. Choose the case of an **Euler prime exterior to D**; the case Euler inside D is not excluded by the following claims. Every prime in D must then receive an even total exponent, and the product of its final ordinary components is at least D²/s², as follows from writing D=s²k, k squarefree. Let b count the total v_p(σ(r^f)) supplied by r|D. Other outside ordinary rows of joint demand p^v cost at least p^(2v)/U, for the single-target uniform deficit U computed over all h≥2, even or legal Euler exponent. Its Hensel/size enumeration is the scalar argument in [the atom note](ProofAtoms.md); in this variant all possible h≥2, not only even h, are included. Only one base incurs any loss; failure of Fermat or divisibility tests excludes only composites. Put C=XD²M²/(BU); floor(log10 C)=1486.

* If every exterior component exponent is ≥2, all exterior components are already eligible for the uniform price, including a possible Euler exponent ≥5. Then s² p^(2b)≥C; even granting s²≤D, this requires b≥117.
* If Euler e has exponent one and i=v_p(e+1), all ordinary components outside D have total residual supply p^(255−b−i). Reserving e independently gives s² p^(2b+2i)≥C e. Here e≥max(5,2p^i−1). In particular, b≥117,109,101,85,67 respectively for i=0,16,32,64,100. The complete exact formula, not an interpolation, applies at any i≤255. Bounds weaken when more Euler contribution is allowed. The case i=0 has an even larger right side due to e≥5.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Rough256.py

## Inverse-order prohibition for a single internal supplier

Suppose r^t|D and r^g||N is ordinary with u=v_p(σ(r^g)). Every r|D has ord_r(p)=257, hence r≡1 mod514. If ord_p(r)=1 then u=v_p(g+1)≤1 because 3^(p²−1)>B. Otherwise, at positive u the order o>1 is an odd divisor of p−1. By LTE u=v_p(r^o−1)+v_p(g+1), and v_p(g+1)≤1 by the same budget. For each pair (t,L) below the checker enumerates all 272 nontrivial odd-order roots of x^273=1 mod p^L using unique simple Hensel lifts. For each combine with r≡1 mod514 to get the least positive representative R modulo K=514 p^L. If r^t|D, the least positive residue J0 of D/R^t mod K is a lower bound on D/r^t. R^t J0>D in **every** class at each indicated L. Thus u≤L for an internal ordinary component of that compulsory multiplicity.

| t (minimum multiplicity in D) | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 16 |
|---|---|---|---|---|---|---|---|---|
| upper bound on u |128|86|64|52|37|29|24|15|

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Three/Inverse256.py

For example, if the total internal supply b≥117 comes from a single internal emitter, that emitter must occur to **exactly one power in D**, not twice or more. It must pay at least one entire further copy for its ordinary exponent. This conclusion remains valid without identifying a single factor of D. It does not force b≥117 when the Euler assumptions of that bound fail.

This is a real **conditional mass-and-target reduction**, not an exclusion of the whole first fiber. It quantifies the substantial internal supply owed by the anonymous block at many exterior Euler windows. It is not a claim that D is squarefree or that b counts distinct primes.
