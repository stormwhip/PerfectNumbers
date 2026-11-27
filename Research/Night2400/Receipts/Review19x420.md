# C — (19,420), exact conditional fibers

Candidate `1f20e3d284b8c8a329f6412c35a58b711b9829ef` (supersedes `2cd55912073203cfd8fdd0db25901d1515b018ae`, not replayed). Detached, clean tracked files, CPython 3.11.9. No author caches; pivot and forced-prime ECPP chains are included in the packet.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C/Verify.py
```

**PASS conditional exactly `[8,10,12]`; OPEN `[2,4,6]`.** Started 2026-11-26 23:46:17.741 +08:00; ended 23:48:22.355 +08:00; elapsed 124.720192 s; exit 0. Price outputs: `8 (16,[2549,819,0])`, `10 (17,[3490,720,0])`, `12 (17,[4985,67,0])`.

SHA-256: `Verify.py` `d5eb58acf5109f4ae94620eedff634e904857c618f6413fd795d38e30933c8de`; `PivotECPP.json` `1bbf46f3a22e4d07f9d44a910142d46832efbc25dbc09cdefdba56fe1734fae9`; `Forced8ECPP.json` `17211f68a208bf4dde6fa5f3ab930e3fba60003553189cb4b319e2afd341e57b`.

Independent split arithmetic used direct geometric sums and gcds, not the candidate modules. For `q=28174642921954703272833689609691232580811241064837460583`, `q≡3 mod 4` and `v_q(σ(19^420))=1`. Elementary budget `(19^420 σ(19^420)/q) q^f <= B` reaches `f=24` and fails at `25`, so lawful even tail is `>=26`. Children `[2,4,6,8,10,12]` meet full size and abundancy bounds and neither fixed prime's incoming valuation exceeds its exact exponent. `[14,16,18,20,22,24]` strictly fail full-state size. Comparator equality at `B` is retained throughout the bounds. The only packet covers requested are `[8,10,12]`; `[2,4,6]` remain open.

For `f=8`, an additional prime `r=18716166489844799458885230781362655242022878296316554735036307387001821111739679109236269675618028263` is certified in a separate ECPP chain. Independent calculation gave `r≡3 mod 4`, `v_r(D)=1`, and `r²` within full-state budget. At `r^4` the prefix budget still passes but the full state strictly exceeds `B`; `r^6` first exceeds the elementary even-exponent budget, with all larger powers excluded monotonically. Thus `r² || N` under this exact path. The price checker targets only indices `[0,1]`, retaining all fixed factors (including `r²` for `f=8`) in its baseline. No coverage transfers to other exact fibers or to the shard.
