# All-s external-source bases for e=1108,990,970,856

This uses the same canonical bans, odd perfect N≤10^2400, q^1 Euler, q∤A, s=v3(q+1)>0, and at least one ordinary source r∤A with q|σ(r^f). No source-supply-zero hypothesis. This covers E3a only, not full exponents. Program `NextRange.py` extends the same product-gcd test; `Next.py` replays all s and all m by integers. Take L=1+2(e+1)*32768*140000, check gcd=1; e+1 prime and A nonsquare are checked deterministically. Bounds for auxiliary net cost (as paid separately in joint terminology):

|e|L|E3a base > 10^t, t|gap to 2400|
|---:|---:|---:|---:|
|1108|10175119360001|2117|283|
|990|9092464640001|1893|507|
|970|8908963840001|1855|545|
|856|7863009280001|1639|761|

**Proof when b may be positive.** Let b=v3(σ(r^f)); when b>0, LTE gives r≡1 mod3 and b=v3(f+1). With n=(f+1)/3^b, q≡2 mod3 implies cubing is bijective mod q, hence q|σ(r^(n−1)). (If r≡1 mod q then q|f+1 and q≠3 gives q|n; otherwise use the order.) Thus r^f>(2q/3)^(3^b), using f≥(n−1)3^b and σ(r^(n−1))<3r^(n−1)/2. For q≥17 put x=2q/3>9. Then x^(3^b)/81^b≥x³/81>x for b≥1; successive ratios are x^(2·3^b)/81>1. Small q are unnecessary: s≤2 contradicts 3^e43^(2(e−2))>10^2400 by canonical minimum ordinary supply base. Normalize source volume to r^f/81^b, but elsewhere prepay 81^(e−s−i) as if the source did not supply. This exactly cancels, since the other external suppliers give e−s−i−b.

For i units internal A-supply put X_s=min_{0≤i≤e−s}81^(e−s−i)max(AL,L^(2i)); then a lower bound for the component of N left after removing the joint auxiliary net is 3^e q X_s r^f/81^b. For every s≥1, q=2m3^s−1. Integer square roots determine the largest m for which 2·3^e q² X_s≤3·10^t. For all larger m the preceding source inequality proves the target. Within the low prefix sieve m and q as in the root-1162 certificate, then for survivors either b>0, where x³/81 already suffices by direct integer comparison, or b=0. In the latter case set C=floor(10^t/(3^e q X_s)), *not* 10^2400/(3^e q A), using the negation of the desired base inequality. In each instance C<q², so enumerate all possible multiplicative orders for even f<bit_length(C), taking the smallest nontrivial root of x^d−1 in F_q as a lower bound for r. Script checks z^f>C. The conclusion is a net-price lower bound independent of the support leaf, not a proved existence of any particular auxiliary net volume. No claims for E3b.
