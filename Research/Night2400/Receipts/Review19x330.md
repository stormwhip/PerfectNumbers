# C2 — (19,330), exact conditional fibers

Candidate `226e6bfed96a2ea67e0846c881af9d185d6236fb`, detached clean tracked files; CPython 3.11.9. `Verify.py` SHA-256 `82538c1c02c0a241df65aa422b2acd01fdef83f581132069be468f50bb3afdff`; `PivotECPP.json` `025e9e26572d6ed4dcae4a253849f3f8ddc62ae0c78815164066a0dfc2620868`; `Split8ECPP.json` `2cc3d2affd5c380f6a6fbcf3812a834312b102a1e72f64b84ab717c81e11a721`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C2/Verify.py
```

**PASS conditional `[8,10,12]`; OPEN `[2,4,6]`.** Start 2026-11-27 00:00:57.488 +08:00, end 00:03:33.342 +08:00, elapsed 156.0206234 s, exit 0. Price receipts: `(330,8,1) (16,[0,0,0])`, `(330,8,2) (16,[1260,1388,0])`, `(330,10) (16,[2294,948,68])`, `(330,12) (16,[3831,141,0])`.

Independent geometric-sum branch enumeration: the proved 210-bit pivot `q≡3 mod 4`, `v_q(D)=1`, root raw tail first exceeds `B` at 26, and every odd exponent through 25 is inadmissible. Exact state excludes evens `[14,16,18,20,22,24]`; `[2,4,6,8,10,12]` also pass the additional partial abundancy check against old `TreeCheck.py`. At root pivot valuation 8, a fresh proved 301-bit pivot `a≡1 mod 4` is compelled with valuation 1. Its tail starts with strict overflow at 8, odd exponents 3 and 7 are illegal; 4, 5, 6 fail direct full-state bound, leaving exactly `[1,2]`. The first has a fixed valid Euler slot, the second has not fixed one. These are all the internal siblings, but first-pivot `[2,4,6]` remain open. Price targets `[0,1]` with all fixed factors retained in `X,S,C`; there is no divisibility lift or whole-shard claim.
