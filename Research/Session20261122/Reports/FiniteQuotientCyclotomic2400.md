# Finite Quotient Cyclotomic Closures for Three Hard Shards

**Research date:** 2026-11-23. **Target:** odd perfect numbers N <= 10^2400.
**Root order:** (19, 7, 11, 31, 13, 3, 5, 17).
**Status:** an exact integer exhaustion rule has been implemented in the
independent verifier for three additional top-level root tasks. A fresh
full GitHub CI audit and the remaining proof trees are still required.

## 1. Theorems

Suppose p is a prime, m=d+1 is an odd prime with m>p, and the canonical
non-exact root branch represents exponents e>=d with m | e+1.
Assume an odd perfect N<=B exists in that root class. Then

    sigma(p^d)=1+p+...+p^(m-1)=Phi_m(p)=A (odd),
    p^d*A | N.

The divisibility uses sigma(p^d)|sigma(p^e)|2N, plus
gcd(p,A)=1. Write N=p^d*A*Q, with Q a positive odd integer and

    1 <= Q <= R=floor(B/(p^d*A)).

**Cyclotomic prime restriction.** If an odd prime q divides A,
then q != m, because m>p and Phi_m(p) is 1 modulo m (Fermat).
Hence ord_q(p)=m and q=1+2mk for some integer k>=1. If the
distinct prime divisors of A are q_1<...<q_t, then

    q_i >= 2*m*i+1,
    t <= floor(log_{2m+1}(A)).

Let f(n)=sigma(n)/n. For any prime q and a>=1,
f(q^a)<q/(q-1). Therefore

    f(A)<product_{i=1}^t (1+1/(2mi)).

Set C=1+ceil(log_2 t) for t>=1. Grouping harmonic terms into
dyadic blocks shows H_t<=C. For C<2m,

    f(A)<1/(1-C/(2m))=2m/(2m-C).

This is an exact rational bound and does not require factoring A.

**Abundance exclusion.** For all positive x,y, f(xy)<=f(x)f(y).
Thus

    f(N) <= f(p^d)*f(A)*f(Q)
         < (p/(p-1))*(2m/(2m-C))*sigma(Q)/Q.

Any Q satisfying

    p*sigma(Q)*(2m) < 2*(p-1)*Q*(2m-C)

cannot appear in an odd perfect N. The program verifies this inequality
as an integer comparison.

**Other exact exclusions.** Every remaining odd Q is factored by a
deterministic smallest-prime-factor sieve. It is excluded if any of the
following necessary conditions fails:

1. Q is divisible by an earlier forbidden root.
2. p|Q: then the actual root exponent is e=d+v_p(Q), but
   m | e+1 implies m | v_p(Q). The checked range has R<p^m.
3. Euler's theorem: among all prime exponents in N exactly one
   is odd, must be 1 mod 4, and its prime must be 1 mod 4.
   Every q|Q has exact exponent v_q(A)+v_q(Q), except p
   (already handled). An invalid odd exponent or two known
   odd exponents excludes Q.
4. For any q|Q with q not dividing A and q!=p, q^v_q(Q)||N,
   so odd(sigma(q^v_q(Q))) | N=p^d*A*Q. This is tested by exact
   integer remainder.
5. If gcd(A,Q)=1, multiplicativity gives
   f(N)=f(p^d)*f(A)*f(Q). Since A>1, f(A)>1. Thus
   sigma(p^d)*sigma(Q)>2*p^d*Q excludes Q as overabundant.

The tests are conservative; each exclusion is a proved necessary
condition, and every odd Q<=R is enumerated.

## 2. Reproducible integer exhaustion

Run from repository root:

    python3 -S -O Research/Session20261122/Python/FiniteQuotientClosure2400.py
    python3 -S -O Research/Session20261122/Python/DirectRootClosuresTests.py
    python3 -S -O Research/Session20261122/Python/AuditDirectRoot2400.py

The finite quotient algorithm independently recalculates A, R,
the cyclotomic abundance envelope, all odd Q and every exclusion.
There is no reliance on a C++ solver completion flag or a heuristic
primality test.

| Root p | d | R | Odd Q examined | Below abundance | Forbidden | Bad root exponent | Euler | Sigma forcing | Overabundant | Survivors |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 19 | 936 | 1,411,815 | 705,908 | 698,028 | 0 | 901 | 6,899 | 78 | 2 | 0 |
| 11 | 1150 | 56,941 | 28,471 | 27,857 | 369 | 77 | 150 | 18 | 0 | 0 |
| 11 | 1152 | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |

For p=19,d=936, the final two Q before the lower-abundance
check are 480249 and 693693; both violate the exact lower
abundance requirement and have gcd(A,Q)=1.

This adds **three** independently re-enumerable finite-quotient
certificates to the previous **1,396** direct forbidden-factor
and sigma-divisor-size leaves. The new candidate top-level tally is
**1,399 closed / 3,072** and **1,673 still open** once the
new repository audit is run and accepted.

## 3. Scope and next experiments

This fast, unconditional integer closure works when
R=floor(B/(p^d*Phi_m(p))) is small enough for exact enumeration.
For the current implementation R<=2,000,000, and only the three
explicitly pinned production tasks are accepted by the verifier.
Other root tasks still require proof DAGs or stronger certified
conditional bounds. The terminal coprime class and the original root
partition remain unchanged.

Important distinction: the 1,396 older certificates are immediate
single-leaf integer rules, while these three are exhaustive
finite-quotient leaf proofs. A successful local enumeration alone is
not a completed 3,072-shard theorem. The repository audit must accept
all remaining tasks, as specified in Documentation/CurrentStatus2400.md.
