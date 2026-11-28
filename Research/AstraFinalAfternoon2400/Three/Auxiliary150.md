# Sixteen additional complete Euler-one supply cells by joint abundancy

Same exact `3^6·1093²·398581^150` prefix as [NoteLow](NoteLow.md), Euler prime `e` **to exponent one**. Put `p=398581` and `j=v_p(e+1)`. The independently certified scalar price at weight 2 has no baseline losses. Beyond the 779 complete cut cells of the three-coordinate table, [AuxiliaryTriple150.py](AuxiliaryTriple150.py) excludes precisely these additional cells `(v1093(e+1),j,v3(e+1))`:

```text
(0,22,0..5); (0,23,5)
(1,22,0..3); (1,23,0,2,3,4,5)
```

This secondary result does not assume `e` is outside `D`, and none of these exact cells is one of the earlier 779 rejected cells. Thus 795/1800 Euler-one supply cells are excluded, not a complete secondary fiber.

Let `X` be the fixed prefix product, `S=σ(X)`, `D=S/gcd(S,X)`, and `V=X p^298`. Every unassigned ordinary row is `r^h` with even `h≥2`; its target supply `u=v_p(σ(r^h))`. Set `λ=200`. For each possible base charge at most the maximum loss factor

```text
L_r = max(1, max_h (r/(r−1))^λ p^(2u)/r^h),   U=Π_r L_r.
```

The maxima are upper bounds, computed over a permissible superset of each actual support; distinct ordinary bases use each loss at most once. For `r<1000` use exact trial primality, all even exponents through the exact lcm/size and strict loss tails, keeping compatible caps and canonical bans. For `r≥1000`, `C=(1000/999)^200<2`. Zero supply is never lossy (`r²≥1000²>C`). For positive supply there is no LTE length shift since `p` exceeds every possible length; order 1 cannot supply. The actual odd order `o>1` forces `o|h+1`, and necessarily `r^(o−1)<C p^(2u)`. Because `o−1≥2`, this yields `r<2p^u`. Enumerate each exact root mod `p^u` and the root **plus** `p^u`, not just the least representative. Every tested row uses the conservative exponent `o−1`, and any forbidden factor at that exponent divides its actual geometric sum. The safe Hensel-depth tail stops only when all current least roots already exceed the true full-size cap even at `o−1`, which persists for deeper levels. A retained composite only weakens the bound. The `r≥1000` part yields no discounted bases once the fixed `r=1093` is correctly reserved rather than treated as an unassigned ordinary source. Crucially the auxiliary price does not presume its positive deficits share the old scalar representative-only limit; the factor `C>1` necessitates the additional representative.

For the actual ordinary primes, multiplying the row inequalities gives

```text
N ≥ V e / (U p^(2j)) · Π_r (r/(r−1))^λ
  ≥ V e / (U p^(2j)) · [2X/S · e/(e+1)]^λ.
```

The second line follows from `σ(N)=2N` and the Euler ratio `(e+1)/e`; A-support and exterior ordinary primes are each counted once only. The right hand side increases in `e`, so the same exact lower endpoint for each Euler congruence class suffices. All rejection tests compare exact fractions strictly with `10^2400`. Replay `python -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Three/AuxiliaryTriple150.py`.
