# Two elementary low-seven progression obstructions

Keep the fixed canonical rows from Tertiary.md. Write a(p,h)=σ(p^h)/p^h. This increases with h, and the product for any subset of actual rows is at most 2.

* For T², primes 3,13,L=3453283 are compulsory. If 5|v_L(N)+1 the geometric divisor sum σ(L^4) divides σ(L^v_L), forcing both 11 and 151. Since 3,11,151 are 3 mod 4 their exponents are at least two. Even allowing 13 as Euler of exponent one, a(7,12)a(3,2)a(11,2)a(13,1)a(151,2)>2. Thus all fourteen directly live powers 4,14,...,134 are excluded. Five (94,104,114,124,134) were already in the tertiary packet; **nine additional**.
* For T⁶, S=62936242392988051361 is compulsory. If v_S is odd then S is Euler and 13 is ordinary. The factor S+1 divides σ(S^v_S), forcing 3 and 11. Now a(7,12)a(3,2)a(11,2)a(13,2)>2. This eliminates all four viable odds 1,5,9,13, of which the previous packet included 13; **three additional**.

    python -I -S -B Research/FinalNight2400/SevenNext/Abundance.py

The verifier authenticates every prime (using the compact tertiary ECPP bank for the two large labels), divisibility statement and rational comparison. After union with Tertiary.md and Four.md the low-two branch has 46/68 still live; the low-six branch has just **2,6,8,10,12** of the 14. The combined unique tertiary exclusion count is 31, not 37. Neither secondary fiber is closed.