# Canonical `(19,222)` first 1: complete second exponents 4 and 46

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. With exact `19^222,t^1` for `t=7579985624053` and `N≤10^2400` odd perfect, the compulsory second prime `r=3705121363` cannot have exact exponent `4` or `46`. Also, at exact `v_r(N)=22`, exact `v_3789992812027(N)=18` is impossible. The `t¹` component fixes Euler throughout.

| Second exponent | Third pivot | Complete raw surviving exponents | Strict raw tail | Strict terminals |
|---:|---:|---|---:|---:|
| 4 | 12223575034313786292211 | 2,4,…,40 | 81 | 20 |
| 46 | 3789992812027 | 2,4,…,38 | 77 | 19 |
| 22 | 3789992812027 | This packet excludes exact 18 only | original domain recomputed | 1 |

The [verifier](VerifyFirst1FinishMinor222.py) binds the exact paths to the original unresolved frozen data, certifies pivot compulsion, enumerates all relevant original exponent cells and each strict monotone tail, then compares both exact forest recurrences strictly to `10^2400`. Minimum diagnostic decimal floors are 2411, 2402 and 2404, respectively. [First1Minor222.json.gz](First1Minor222.json.gz) SHA-256 `27f7e65fd61c50012452b48e8c04a99cf52175359aef61d2f2131e9f41324586`, all 159 ECPP witnesses used; fresh isolated author replay exit 0.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyFirst1FinishMinor222.py
```

In union with already accepted new overlays first 1 retains only second exponents `16,22`. Under `g=16` the tertiary remainder is `2,4,8,12,16,18,36`; under `g=22` it is `2,4,16`. This is not a whole-key, first-fiber, or shard closure.
