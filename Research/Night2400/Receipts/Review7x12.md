# A — (7,12), partial exact pivot coverage

Candidate `64647233885d4a22dc60435042e06e60433fcf70` supersedes `70301aa995ae308e01a85f429eaa6c1900a0b3cd`, which was not replayed. Detached and clean tracked files, CPython 3.11.9. Packet SHA-256 `872c59c2b29a7da800338e20f6ecfd6082498135fa3c50b6be7e23339c31ac5a`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

**PASS conditional 51 of 83, 32 OPEN.** Start 2026-11-26 23:55:23.916 +08:00, end 23:57:05.381 +08:00, elapsed 101.5608621 s, exit 0. Replay counted 206 forests, 9 nested splits, 251 direct exclusions including root, 0 price leaves, 651 embedded ECPP entries.

Scope is the canonical root-7 branch, hence 19 absent; not an unrestricted exact exponent result. Independent direct geometric sums give `σ(7^12)=q=16148168401`, `q≡1 mod 4` and `q≡1 mod 19`. The pivot valuation starts at 1; the monotone exact bound is `7^12 q^f` with `f=234` included, `f>=235` strictly beyond `B`. Odd legal exponents require `f≡1 mod 4` (Euler), and `q≡1 mod 19` means `19 | σ(q^f)` exactly when `19 | f+1`, excluded. Exact arithmetic for all 234 raw valuations gives 67 illegal, 84 direct failures (state size, conflict or abundancy), 83 live. Packet subset: 51 claimed, 32 OPEN `[1,2,4,5,6,8,9,10,12,13,14,16,17,24,25,26,28,30,36,38,42,46,52,60,70,72,82,88,96,100,102,108]`.

Compared to `TreeCheck.py`, nested splits use a proved compelled fresh prime and reconstructed exact domains; all live children of an internal node are required and all finite tails use `<=B` until strict overflow. Neither forest nor joint-valuation leaves may transfer to unresolved root siblings. Each forest uses two recomputations and strict integer `>B`. Price leaves use the stock `JointValuation.excludes`; all path prime labels were established by the initial root or the split checker, with one valid Euler component allowed at most.
