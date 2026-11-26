# B — canonical (3,12), exact valuation-2 first fiber

Candidate `6b6e2a699aadabbef239d8411c77a890926c22ef`, detached clean tracked files; CPython 3.11.9. Packet `Fiber2.json.gz` SHA-256 `af0771bb9e32df928bd40ae770e0c172ee6b7db376b44bf5d4c3c77612a2aac3`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/B/DomainAudit.py Research/Night2400/B/Fiber2.json.gz
```

**PASS full first-pivot `f=2`; canonical exact `(3,12)` still OPEN on `[1,66,96]`.** Started 2026-11-27 00:24:35.773 +08:00, ended 00:28:42.304 +08:00, elapsed 246.623228 s, exit 0. Verifier confirms 71/71 children, 325 forests, 2 nested splits (excludes initial secondary split), min forest floor 2400, 2585 ECPP.

Independent split enumeration from the packet only confirms canonical banned `(19,7,11,31,13)`, `σ(3^12)=797161`, first budget overflow 406, and `[1..405]` partition 205 incompatible, 100 direct, 100 live. Five frozen archive hashes checked; for this key the archive adds 96 disjoint entries (90+2+4+0+0), leaving original gaps `[1,2,66,96]`. The archive paths are checksum-scoped branch accounting in this command, not a fresh replay of all historical proofs.

At the new first-pivot `f=2`, the compelled secondary pivot `22996651` has raw tail 324 and all 71 live secondary children represented, 181 incompatible and 71 direct. At its exact exponents 58 and 78, the remaining internal pivot `61` has raw tails 855 and 690, with live child counts 142 and 114 (all present), incompatibilities 570 and 460, direct exclusions 142 and 115. All leaf certificates are exact, with two forest computations strictly exceeding `10^2400`. Counter: 325 forests, 3 total secondary/nested splits including top secondary split, 2585 embedded ECPP. No other first-pivot fiber is claimed here: remaining `[1,66,96]`; whole exact key remains OPEN.
