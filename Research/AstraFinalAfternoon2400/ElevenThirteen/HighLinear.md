# Two exact root-13 keys: high Euler supply excluded, not full keys

Let `N≤B=10^2400` be odd perfect with canonical root 13, and `v_13(N)=e∈{612,618}`. If `q^a` is the Euler component, then **`s=v_13(q+1)≤536`**. This bounds the linear supply even when `a>1`, not the total 13-supply from a higher Euler component. In the boundary cell `s=536`, `a=1` and each emitter `r^h` of `q` lies on the support of `A=σ(13^e)`; writing `c=v_r(A)`, `(h,c)` must be `(8,3)` or `(10,5)` for `e=612`, and `(10,5)` for `e=618`. Those labels are relaxed necessary conditions, not feasible constructions. No factorization or squarefreeness of either `A` is assumed.

## Exhaustive branch entry

Set `p=13`, `X=p^e`, `W=pX`, `A=(W−1)/(p−1)`, `Y=p^s`, `Q0=2Y−1`. The exact 13-valuation forces `s≤e`; only `537≤s≤e` is excluded (with `s=536` a control). For these values `2s>e`. If `q|A`, then `A=qU` and `(p−1)U≡1 (mod Y)`. Since `(p−1)U≥12`, then `(p−1)U≥Y+1` and `W−1≥(Y+1)(2Y−1)>2Y²`, contradicting `2s>e`. This argument does not require `a=1`.

Thus `XAq^a|N`, and the executable tests `XAQ0^5>B`, implying `a=1`. Since `q∤A` and `q∤σ(q)`, at least one other (ordinary) component `r^h` emits `q`. If `r∤A`, then `XAqr^h|N`; the bound `σ(r^h)<3r^h/2` yields `N>2XAQ0²/3>B`. Hence **all** emitters are internal, not just a selected one. The tested `q>5100` and `3^5100>B` imply `q>h+1`. By LTE, `r≡1 mod q` would imply `q|h+1`; otherwise `o=ord_q(r)>1` divides `h+1`. If `o<h+1`, this odd index is at least 3, and `q|σ(r^(o−1))` gives `r^h>(2q/3)^3`. The verifier checks `XQ0·(2Q0/3)^3>B`, so `N≥Xqr^h` gives a contradiction without charging any part of `A` a second time. Therefore `o=h+1`, `h+1|q−1`, and `p∤h+1`.

## Internal emitter and rigid intervals

`n=e+1` is prime, `n∤A`, and `gcd(A,12)=1`, so every prime dividing `A` is `1 mod M=2n`. Explicit division by every integer in that progression through `10^7` excludes all small factors (8,156 and 8,077 trial divisors). A base-2 Fermat failure proves `A` composite; exact integer roots for every prime degree below `bit_length(A)` prove it is not a prime power. Hence beside `r` there is another prime divisor `>10^7`, which yields `r^c≤A/10^7`. This is the only factor-count input.

For a chosen `(s,h)`, `q=2uY−1` with `u` odd, `gcd(u,13·19·7·11·31)=1`, and `uY≡1 mod(h+1)`. The search starts at the smallest positive CRT `u`, and skips at most 64 progression points whose incompatibility is proved. It uses the next candidate itself as a rigorous lower bound `Q≤q`; it does not assume any candidate prime and it does not discard the unscanned tail. Then `T=floor(B/(XAQ))`, `r^h>2Q/3`, `r^(h−c)≤T`. Along with `r>10^7`, these conditions give closed integer intervals for `r`; the two outer loops exhaust positive `c` and even `h≥c` by monotonicity.

For completeness the survivor test is as follows. Write `D=(W−1)/r^c`, `w=σ(r^h)/q`, and `d=h+1−c`. The balanced identities below are adapted from the [frozen root-seven screen](../../FinalNight2400/SparseSeven/AllSupport.md), not a new general identity. Let `S_j=σ(r^j)`. Put

```
B0 = D(w+S_(c−1))−S_(h−c)
A0 = Dw(r−1)−r^d−D.
```

Both are divisible by `Y`. For `B0`, use `r^c B0=W(w+S_(c−1))−(q+1)w`; if zero, `W|(q+1)w` contradicts `v_13((q+1)w)=s+b≤e`. Positive `B0` is strictly below `(3/2)(W/Q)T+W/(r−1)`, and negative magnitude is below `3T/2`. Thus when `3WT<YQ` and `3T<2Y`, `r>2W/Y+1` is impossible; the permitted upper endpoint can be decreased without discarding any legal value. For `A0`, use `A0=((W−1)/q−1)r^d−D(1+1/q)`. Another prime divisor of `A` divides `D` but not `r`, so `A0≠0`. Also `A0≡−1−(p−1)A (mod M)`, since `r≡1 mod M`. Hence `A0/Y` has a known residue modulo `M`. Using the current lower and upper endpoints of `r`, the checker computes conservative bounds on the positive and negative magnitudes and tests both signed residues.

When `h=c=2`, the independent [square-emitter congruence](../../FinalNight2400/AuditNext/SquareEmitter.md) works with coefficient `p−1=12`: putting `v=A/r²`, `k=(r²+r+1)/q`, the positive quantity `[(p−1)v(k+1)−1]²+(p−1)v` is divisible by `Y`; it is strictly less than `(3(p−1)A/Q)²+3(p−1)A/(2Q)`. The strict comparison to `Y` uses a denominator-scaled integer test. This reuses the lemma only for an exact square emitter and does not assume that `v` is prime.

The verifier uses **no Hensel lifting** and only the Python standard library:

```
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/HighLinear.py
```
