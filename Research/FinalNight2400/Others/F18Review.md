# Conditional 19^432, t^18 — independent review PASS

Scoped to **exact** valuations at both primes (t=11842464881317660217), no support-mask assumption and no full-key credit. The common dual allocation and additional retained-block argument were inspected. For C=Phi_19(t), every prime ell|C is 1 mod 19 because 19 and t-1 are coprime to C. If q is external, these are ordinary primes: for v_ell(C)<=h, u=v19(h+1), h>=18u, ell>=39 and ell^h >= 19^(2u) ell^(7 v_ell(C)/8). This charges only the 19-target on retained primes. Removing a supplier r outside C does not spend the retained C; if r divides C it supplies at most two units of 19 since 3^(19^3-1)>B. Nontrivial 19-adic ninth roots used to bound overlaps are necessary conditions, not primality assumptions. The distinct bases, disjoint length divisors, and one Euler atom of square base in the common proof avoid double counting. Strict thresholds only.

Cold CPython 3.11 replay of `Explore.py` SHA256 5533c5df69c1c5b26429b5c0a0f632bf2cb557d3222b3f0fac941ecc4df42ee3 (proof SHA256 85d6628eb518bc14d8aa37c00c3e8ce10c1d08e84e5ac578d07ce48f7b6d9ca6): counts 6447 simple, 985 mandatory/retained block, 362 supplier, 0 unresolved. Additional `Audit18.py` uses the original common deficit functions and lifted roots but tests *every* (u,v) supplier allocation, rather than binary search or endpoint interpolation. 179907 supplier comparisons; all 7794 Euler windows confirmed. Both commands exited 0:

~~~powershell
python -I -S -B Research/FinalNight2400/Dual/Explore.py
python -I -S -B Research/FinalNight2400/Others/Audit18.py
~~~
