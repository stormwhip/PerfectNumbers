# Canonical (13,618): exclude the Euler-supply endpoints 535 and 536

**Conditional sharpening only.** Assume odd perfect `N≤10^2400`, `19,7,11,31∤N`, `v_13(N)=618`, Euler prime `q`; then `v_13(q+1)≤534`. The previous independently audited [window proof](HighLinear.md) already excludes 537 through 618 and restricts 536 to `(h,c)=(10,5)`, where every `q`-emitter is an internal ordinary `r^h` and `c=v_r(A)` for `A=σ(13^618)`. No full key or shard closes.

Let `s=536`, `Y=13^s`. The prior proof gives exact order `h+1=11` at `q`, so `q=2uY−1` with odd `u` and `uY≡1 (mod 11)`. Its verified lower bound starts at `u=27`; every permissible `u` is therefore 27,49,71,… . The first has composite `q` by a failed base-2 Fermat congruence.

For every `u≥49` use `Q=2·49Y−1`. With `X=13^618`, `W=13X`, `A=(W−1)/12`, `T=floor(B/(XAQ))`, the same internal-emitter argument gives `r≥ceil_root(ceil(2Q/3),10)` and `r≤min(floor_root(A/10^7,5),floor_root(T,5))`. Write these integer endpoints as `L,U`, respectively, and `Dmax=12 floor(A/L⁵)`. The nonzero signed `A0/Y` from the [balanced identity](HighLinear.md) has residue 223 modulo 1238. If positive, its magnitude is at most `floor((W−1)U⁶/(QY))=187`. If negative, the bound is `floor((Q U⁶+(Q+1)Dmax)/(QY))=0`. These bounds are conservative for the whole tail `q≥Q`: `U` does not increase, `L` does not decrease, and both `1/Q` and `(Q+1)/Q` decrease. The positive minimum is 223 and the negative minimum is 1015, giving the contradiction on the entire infinite progression tail. There is no primality assumption for any surviving progression point and no Hensel calculation.

For `s=535`, complete parent arithmetic leaves exactly `(h,c)=(8,3),(10,5)`. Their first relaxed `u` values are 25 and 43, with strides 18 and 22 respectively. At `Q=2·1411·13^535−1` the same monotone signed upper bounds are both below the relevant least signed residues for both shapes, ruling out every `u≥1411`. Below 1411 enumerate the complete residue progressions, requiring exact 13-valuation (`13∤u`) and `gcd(u,19·7·11·31)=1` because every divisor of `u` would divide `(q+1)/2` and hence `N`. The remaining 51 and 46 candidates each fail Fermat base 2. Repeated candidate values across shapes, if any, are evaluated as separate shape labels, not claimed as separate root-supply windows.

```
python -I -S -B Research/AstraFinalAfternoon2400/ElevenThirteen/Thin618.py
```

The verified cells 535 and 536 are outside the previous 82-cell parent packet. This gives 84 completely excluded top `s` values for `(13,618)`; `(13,612)` is unchanged. Verifier SHA-256 `8acb243e8d0ad9e5812d48479049eea3a32e9b2ed994d6be0bb4c0b8aa106ad8`.
