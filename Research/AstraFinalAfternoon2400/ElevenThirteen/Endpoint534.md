# Verified endpoint: (13,618), s=534

Retain the exact canonical hypotheses and notation of [HighLinear](HighLinear.md) and [Thin618](Thin618.md). For `s=534`, the prior internal ordinary-emitter arithmetic leaves `(h,c)=(8,3)` or `(10,5)`. In either shape `q=2uY−1`, `Y=13^534`, `u` odd with `uY≡1 mod (h+1)`, `gcd(u,13·19·7·11·31)=1`. The two signed bounds for `A0/Y` are already too small at `u=52360`, hence at every larger `u` by monotonicity. At lower `u` we must cover the entire two progressions, not just observed probable primes. The verifier uses a failed Fermat congruence in base 2, 3 or 5 as a compositeness certificate; passing bases do not prove primality and do not remove the candidate.

For a remaining candidate, select any emitter `r^h` of `q` with `r^c|A` and define `a=A0/Y`. The signed bounds exclude negative `a`. The positive values are in the full progression `a≡−13Y^(-1) mod 1238`, starting at 547 with stride 1238. From the original integer identity

```
A0 = ((W−1)/q−1) r^(h+1−c) − ((W−1)/r^c)(1+1/q)
```

multiply by `q r^c` to obtain the exact sparse polynomial equation

```
F(r)=(W−1−q)r^(h+1) − Y a q r^c − (q+1)(W−1)=0.
```

Here `F(x)/x^c` is strictly increasing for real `x>0`: its first term is a positive coefficient times `x^(h+1−c)`, its second term is constant, and its third term is a negative constant times `x^(−c)`. The complete inclusive emitter range is the one from the parent proof. Every possible `r` is `1 mod 1238` by prime cyclotomic index. Exact integer sign bisection on that progression rules out a zero for each enumerated positive `a`, or else checks the found integer directly for `r^c|A`. No LLL, irreducibility, unsigned rounded floatingpoint root tests, or actual factorization of `A` are used. In particular the large value `q` does not need primality certification to prove that no admissible emitter works for it.

```
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/Endpoint534.py --full
```

The `--full` cold replay exited 0: 1,917 and 1,727 candidates, five surviving each after Fermat filters, and 2,525 and 314 exact signed polynomial cells checked. The short mode is diagnostic only. Independently, [ThinGeneral.py](ThinGeneral.py) uses a different sieve and an exact full cyclic subgroup restriction rather than sparse-polynomial bisection; its standard-library cold pass took 46.47 s with 320+224 Fermat candidates, 5+5 subgroup survivors, and zero possible emitters. Therefore `(13,618)` has `s≤533` when combined with the earlier windows. Exact-key and shard credit are zero.
