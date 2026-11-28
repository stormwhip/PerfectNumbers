# Nested first-fiber supplement (separate from the original 212-fiber packet)

Each record below excludes **all** completions of its specified first-pivot valuation, with the canonical absence assumptions only. No other first exponent or whole root key is claimed. Subtract these f values from the exact lists in [the prior receipt](ForestCoverage.json) without counting them there again.

| Root key | Compulsory first pivot | Exact exponent excluded | Forest leaves | Exhaustive splits | Minimum integer decimal floor |
|---|---:|---:|---:|---:|---:|
| `(11,16)` | 50544702849929377 | [26](Second-11-16-26.json.gz) | 57 | 2 | 2400 |
| `(11,18)` | 6115909044841454629 | [9](Second-11-18-9.json.gz) | 11 | 1 | 2400 |
| `(11,48)` | 100641220283951395639601683 | [14](Second-11-48-14.json.gz) | 60 | 4 | 2400 |
| `(11,48)` | 100641220283951395639601683 | [24](Second-11-48-24.json.gz) | 2 | 1 | 2415 |
| `(11,48)` | 100641220283951395639601683 | [26](Second-11-48-26.json.gz) | 6 | 1 | 2402 |
| `(11,48)` | 100641220283951395639601683 | [32](Second-11-48-32.json.gz) | 66 | 3 | 2400 |
| `(13,6)` | 5229043 | [124](Second-13-6-124.json.gz) | 37 | 3 | 2401 |
| `(13,6)` | 5229043 | [150](Second-13-6-150.json.gz) | 19 | 2 | 2400 |

For a fixed state with exact components and stripped compulsory remainder `D`, a split is permitted only at a certified prime `z|D`. If `v_z(D)=c`, every completion has `f≥c`. As long as `(X D/z^c) z^f≤B`, independently rebuild the state with exact `z^f`, reject any parity/forbidden/flow/abundance/size contradiction, and require a recursively checked child for **every** survivor. The first strict raw size exceedance proves the entire tail. Forest terminal arithmetic is unchanged and both frozen integer recurrences must exceed `B` strictly; displayed floors alone are not used. The checker verifies the supplied large prime chains against their exact subjects. The 25-digit split prime 2718112670273680688549131 in the `(11,48)` tree is additionally covered by the elementary Pocklington data in [Coverage.py](Coverage.py).

At this increment the exact remaining first exponents at `(11,16)` are `[1,2,4,6,8,10,12,13,16,18,22,24,25,28,30,36,40,42,46,52,60]`. The exact remaining first exponents at `(11,18)` are `[1,2,4,5,8,10,12,16,17,22,24,25,26,28,30,33,36,40,42,46,52]`. The exact remaining first exponents at `(11,48)` after these trees are `[2,4,8,10,12,16,18,22,28,30,36]`. The separate [valuation/lattice certificate](Price48.md) additionally removes 36, leaving `[2,4,8,10,12,16,18,22,28,30]`. At `(13,6)` they are `[4,10,12,16,18,22,24,28,30,36,40,42,46,52,58,60,66,70,72,78,82,88,96,100,102,106,108,112,126,130,136,138,156,162,166]`. All four keys remain open. The independent cold replay path is:

```
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ElevenThirteen/SecondTree.py --verify Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-16-26.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-18-9.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-48-14.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-48-24.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-48-26.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-11-48-32.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-13-6-124.json.gz Research/AstraFinalAfternoon2400/ElevenThirteen/Second-13-6-150.json.gz
```

The factor bank is unnecessary for replay. SHA-256 (same row order): `49d9f7a2ed23a932c6306e5cfb1fd2321c6906b19bfe70d9e0c91846ff2cdef1`, `176c08f4cfa07b1b8a584befff0aa9896a6704db93599c9f28891a5e4c1238ea`, `908928cf20efd980dde706fc84a530aa6cbb75e9d39a59c079fe255718e31e54`, `3ee3625ce0d17793a7863683a12086f21eb8d00351df28a8815ac6d0539a4dc3`, `b04ae4c4efc4f4c16cb31a9793cdd3376fc8e71f19e8962a6df019e26cb4dcd0`, `6563528ad1a8c10fb443d733c465c978e6309fafbe68ed0a950f41c56e4b4bd5`, `43ae206135da77f89f9266a40699ab6ca523a17ad510cfa1aaa1a8929c39ed68`, `b0bd453d6bca069b3921c5670e4926851cb9f1affa8ba760b179124082d8ebcb`.
