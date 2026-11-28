# `(19,222)`: final overlay of 12 exact tertiary cuts

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. Here `f=v_7579985624053(N)` and `g=v_3705121363(N)` following exact canonical `19^222`. Third prime `q` is `3789992812027` for `f=1` and `108501737266216818637411` for `f=18`. This packet excludes only the named exact third exponents `j` below. All five second windows remain open; first `1,18` and the exact key remain open.

| `(f,g)` | New exact `j` exclusions | Remaining `j` |
|---|---|---|
| `(1,16)` | 2,4,8,12 | 16,18,36 |
| `(1,22)` | 4 | 2,16 |
| `(18,2)` | 6 | 10 |
| `(18,16)` | 2,4,6,10 | 12,16 |
| `(18,22)` | 2,12 | 6,10 |

[VerifyLast18And1222.py](VerifyLast18And1222.py) independently builds the frozen tertiary candidate sets, confirms each live scope is in the exact preceding remainder (also documented in the earlier proof packets), and checks two strict unrounded integer forest recurrences on all 12 terminals. No extra forbidden prime is assumed. For `f=1`, Euler is fixed by the exact first component; for `f=18`, all legal Euler positions remain available in the recurrence. Diagnostic floor 2400 at `(1,22,4)` represents a still-strict comparison `>10^2400`. All 440 ECPP records are checked exactly once by subject and every graph constraint is independently recomputed before using a forest. No Hensel or withdrawn PR #11 argument is used.

[Last18And1222.json.gz](Last18And1222.json.gz) SHA-256 `15bcab2082e9d1ffd0dfb74477465629e32ba9f33e357f37601770419810b970`. Cold author replay exited 0:

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyLast18And1222.py
```
