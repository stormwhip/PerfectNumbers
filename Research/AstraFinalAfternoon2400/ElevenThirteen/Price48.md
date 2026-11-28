# Complete canonical (11,48), first pivot 36 (not full key)

Let `N≤B=10^2400` be odd perfect, `7,19` absent, `v_11(N)=48`. Put `t=100641220283951395639601683`. The factorization and Pocklington proof in [Coverage.py](Coverage.py) give `v_t(σ(11^48))=1`. This packet excludes **`v_t(N)=36`**, uniformly in every other exponent and Euler location. It does not use a support mask, complete factorization of `σ(t^36)`, conjectural primality, or an assumption of squarefreeness.

## Exact two-unit atom price and all Euler windows

Write `X=11^48 t^36`, `A=σ(11^48)/t`, `D=σ(t^36)`. The verifier recomputes the identities, prime tests and coprimality. In particular `gcd(A,D)=gcd(D,11t)=1`, so `XAD|N`. The deficit at `t` is 35. Put `q^a` for the Euler component. Split `q^(4k+1)` as `q` times the even-exponent square-base atom `(q²)^(2k)`; its geometric sum factors as `(q+1)σ_geom(q²,2k)`. The `q²` atom is kept even when composite. Every other component outside the prefix is an even-exponent prime-base atom. All these atom bases are distinct, because the only composite square base is the Euler one.

`3^5100>B`; thus neither LTE index shifts nor order-one length can supply `t`, and the only possible nontrivial odd orders at `t` are exactly `3,7,21,49,147`, using `t−1=294·342317075795753046393203` with the last factor certified prime. For an atom at order `o` and valuation `b>0`, the even exponent is at least `o−1` and `r^o≡1 mod t^b`. **Weight 2≤o−1**, so a strict deficit `r^(o−1)<t^(2b)` forces `r<t^b`. This certifies exhaustion by least representatives at each exact level; there is no high-weight least-lift shortcut. [PivotPrice48.py](PivotPrice48.py) exhausts exact levels 1..35 and all primitive roots, rejects only composites proved not prime and not a square, and finds no positive deficits. In particular every subset of the atoms costs at least `t^(2 * its total incoming t supply)`.

Put `i=v_t(q+1)`, `Q=max(5,2t^i−1)≤q`. All `i=0..35` are examined. The first inequality is `N≥X Q t^(2(35−i))`. If it does not suffice, test `q` external to the fixed sigma blocks: for `i>0`, quadratic reciprocity gives `(t/q)=(q/t)=(−1/t)=−1` because `q≡1 mod4`, `t≡3 mod4` and `q≡−1 mod t`; a divisor of `σ(t^36)` instead has odd multiplicative order of `t`, so gives `+1`. The other stripped block is small enough to exclude by size in these surviving `i`; the generic residue/cofactor check never assumes a single lift unless the next already exceeds the full interval. Hence some unfixed ordinary prime power `r^h` emits `q`. Keeping `q` alone is valid even when Euler has higher exponent, and all pricing still includes its square-base atom.

For each `j=v_t(σ(r^h))` up to `35−i`, `σ(r^h)≥q t^j` and `σ(r^h)<3r^h/2`. Relative to `XAD`, the already paid amount of `r^h` is at most `max(A,D)` because `A,D` are coprime. Separately price all atoms other than `r^h`. These two *independent* necessary lower bounds are

```
N > 2XAD Q² t^j / (3 max(A,D))
N > 2X Q² t^(2(35−i)) / (3 t^j).
```

Neither multiplies potentially shared mass; both may be used as tests. Using also raw `XADQ≤B`, the only relaxed pairs left are `(16,16..19)` and `(17,16..18)`. The verifier recomputes their domain rather than assuming this list.

## Emitter congruences and six lattice cells

In each surviving pair a verified `2XD Q² t^j>3B` means no emitter can be external to `D`, since then its already paid amount in `AD` would be at most `A`. Put `c=v_r(D)≥1`. The prime index 37 does not divide `D` or `t−1`, so every prime divisor `r` of `D` satisfies `r≡1 mod74`. Exhaustive division by every `1 mod74` integer in `[75,10^7]` proves `r>10^7`. Consequently every possible `c` satisfies `(10^7)^c≤D`, and `h≥c` is even. Use `XADQ r^(h−c)≤B`, `XAQ r^h≤B`, `r^h>2Q t^j/3`, and the necessary overlap `r^c≥ceil(2XAD Q² t^j/(3B))`. These give exact inclusive lower and upper endpoints via integer roots, retaining equality. Enumerate all possible orders `o` and all even `h≥c` with `o|h+1`; for each initial cubic or other root mod `t^j`, intersect with `r≡1 mod74`. Single-point intervals require genuine `r^c|D`, not just `r|D`. Remaining intervals use the lattice test; if any nonempty progression lacks a valid certificate the verifier reports the fiber unclosed.

For a remaining full progression `r=R+My`, `0≤y≤K`, set `x≡R/M mod D`. This inverse exists and is checked. A true `r^c|D` gives `r|y+x`. For a chosen integer `k≥1`, the generated basis polynomials are `Y^(l−d)(Y+x)^d D^(k−floor(d/c))`, `d=min(l,ck)`, each divisible by `r^(ck)` at `y`. Recompute two given integer combinations and require `sum |a_j|K^j < R^(ck)` for each, so both vanish at an actual integer `y`. Their reductions modulo the verified prime 65537 are coprime, which directly rules out a shared integer root. This checks all required progression intervals, six coefficient-pair certificates, and forbids unreferenced witnesses. FLINT only discovered coefficients; it is not used in replay.

```
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ElevenThirteen/PivotPrice48Depth.py
```

[Price48Depth.json.gz](Price48Depth.json.gz) SHA-256 `0e1a0db906c12ec4100ea6866193f5bb12cf34ac8915943f2655ff199f7d6f12`. The cold replay reports every Euler allocation `i=0..35` excluded and 6 lattice cells. Zero whole-key or shard credit.
