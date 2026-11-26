# B — stronger parity completion on the hard exact valuation-66 path

Candidate `8247700901b504856f5fc2ae578808993fd6f5c0`, detached clean tracked files; CPython 3.11.9. Only `EulerRoute.py` and its explanation changed from the prior audited `a9f27a8a`. The historical and fiber packets were not rerun.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/B/EulerRoute.py
```

**PASS diagnostic; 154 windows remain OPEN.** 2026-11-27 02:48:00.847–02:48:59.901 +08:00, elapsed 59.2357535 s, exit 0. Of 168 windows after balance, 14 are now excluded by parity, zero further by the small-rest fallback.

Independent review of the new bound: the two forced blocks `A,T` are coprime to each other and to the assigned prime product. Exact integer square-root checks show each nonsquare, so each contains a prime of odd valuation in `D=AT`, and the two primes are distinct. The trial roughness bound applies to both because every prime factor is in its proved cyclotomic order class. In the exterior Euler-one windows neither prime can be the Euler component. Their final ordinary valuations are even, so both supply a separate additional factor beyond `XD·e`. The exact necessary divisor gives `N >= XD·e·rough² >= XD·a·rough²`. The filter rejects only when this conservative bound is strictly above `B`; equality is retained. It does not multiply with the separate emitter-growth estimate (which could charge one of the same primes). The prior small-rest test is a separate fallback, not multiplied into the parity bound. This is only a necessary-window diagnostic, not a closure of a hard path, primary fiber, exact key, or shard.
