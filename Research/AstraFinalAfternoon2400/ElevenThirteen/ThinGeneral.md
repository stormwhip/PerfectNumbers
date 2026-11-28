# Full cyclic subgroup test for anonymous root-13 windows

Keep the canonical `(13,e)` hypotheses and the proven high-window entry of [HighLinear](HighLinear.md). This supplement excludes further exact values of `s=v_13(q+1)` without factoring the root sigma. The cold-verified additions here are `s=536` at `e=612` and `s=534,533` at `e=618`. The `s=534` case is separately verified by [signed sparse polynomial](Endpoint534.md).

For an exact `(s,h,c)` left by the frozen-parent style arithmetic, some ordinary `r^h` emits Euler prime `q`, and `r^c|A`. The primitive-emitter argument forces `ord_q(r)=h+1=d`, because any proper index divisor would exceed the size bound. Thus `d|q−1`, `q=2u13^s−1`, `u` odd, `u13^s≡1 mod d`, and `gcd(u,13·19·7·11·31)=1`. The starting value skips only proved-impossible lower multipliers. The top of each progression follows exactly from signed `A0/Y` bounds in [HighLinear](HighLinear.md): with increasing `u`, both signed upper bounds weakly decrease, or the emitter interval turns empty. [ThinGeneral.py](ThinGeneral.py) verifies the strict threshold and covers the entire progression below it. A resource cap fails closed, never claims a truncated scan.

For each finite coefficient candidate, a sieve through 20,000 removes `q` divisible by a smaller prime `ℓ`. The modular progression test is exact: if `q=2Yu−1` and `ℓ∤2Y`, remove exactly `u≡(2Y)^(-1) mod ℓ`; if `ℓ|Y`, `q` cannot be divisible by `ℓ`. The same progression (or all of it if stride is a multiple of `ℓ`) is represented by integer slices. Fermat failure in base 2 or 3 suffices for all remaining composite exclusions; a pass retains the candidate, not certify it.

For each further candidate q, [EmitterCRT.py](EmitterCRT.py) considers two cases without requiring a primality certificate. If q is not prime, it is impossible as an Euler base. If q is prime, cyclicity of its multiplicative group implies a verified root `g` of exact order `d` generates the unique order-d subgroup. The check enforces `g^d=1` and `g^(d/ℓ)≠1` for all prime divisors ℓ of d, and exhausts powers `g^j` for `gcd(j,d)=1`. Retain an unresolved candidate if no generator is found. The emitter's forced interval is entirely below q, or the result also stays unresolved. Otherwise every possible r is literally one of those primitive representatives. Test both inclusive endpoints and the cyclotomic `r≡1 mod 2(e+1)` for each. This is a subgroup coverage argument, not a least-Hensel-lift heuristic: the independent bound `r<q` is required.

| `(e,s)` | First `u` by shape | Exclusive signed `u` cutoff | Raw counts | Fermat tests | Partial passes needing subgroup test | Survivors |
|---|---:|---:|---:|---:|---:|---:|
| `(612,536)` | 139 / 27 | 834829 | 46372 / 37946 | 5421 / 3647 | 67 / 36 | 0 / 0 |
| `(618,534)` | 1 / 9 | 52360 | 2909 / 2380 | 320 / 224 | 5 / 5 | 0 / 0 |
| `(618,533)` | 85 / 139 | 1723551 | 95749 / 78337 | 11090 / 7377 | 137 / 85 | 0 / 0 |

Each row exhausts `(h,c)=(8,3),(10,5)` in that order. Reproduction via [the pinned verifier](ThinCertified.py):

```
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/ThinCertified.py 618s534 612s536 618s533
```

In concurrent local cold standard-library runs the three cases took about 46, 657 and 1116 seconds respectively. The fast local exploration mode uses FLINT only for speeding up modular powers. This proof relies on the standard-library replay, not on a probable-prime library result. Together with [HighLinear](HighLinear.md) and [Thin618](Thin618.md) this gives `v_13(q+1)≤535` for `(13,612)` and `≤532` for `(13,618)`. No root key or canonical shard closure follows.
