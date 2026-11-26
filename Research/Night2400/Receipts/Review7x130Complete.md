# E complete — canonical exact (7,130), P7_I00031

Candidate `8ebfc3058ac351c68c9bcbee5191fe9c37bb303a`, detached clean tracked files, CPython 3.11.9. Compressed packet SHA-256 `73b84393b60962ccde065b46f30abaf2be5394862956c51537bb694bd9510ea6`; verifier SHA-256 `51ac22a6876285404da94457058be50eb0d41d15f4fba0e477a68f3205df2e57`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/E/Verify130.py Research/Night2400/E/Tree7x130.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/E/Tree7x130.json.gz
```

**PASS complete, verifier `EXACT_COMPLETE`.** Clean repeat with a stdlib JSON summarizer exit 0 at 00:21:06.346–00:21:53.308 +08:00, elapsed 47.0397013 s: closed `[1,2,4,6,8,9,10]`, open and partial both zero; 61 splits; 769 forest / 9 price terminals; 1407 ECPP. First command cold run 2026-11-27 00:19:39.580–00:20:27.790 +08:00, elapsed 48.2938984 s, Python exit 0. A PowerShell 5 result formatter then errored separately (`ConvertFrom-Json` lacks `-Depth`); this was not a verifier failure. Independent data-only enumeration (second command) exit 0 and confirmed 61 splits including root, 856 direct exclusions, 1610 illegal exponents, 769 forests, 9 price leaves, 1407 embedded ECPP entries, and zero OPEN leaves.

Root partition: compelled 366-bit pivot valuation at least 1, raw size tail begins at 21, illegal `[3,5,7,11,15,17,19]`, directly rejected `[12,13,14,16,18,20]`, and exact live branches `[1,2,4,6,8,9,10]`. Data-only audit re-enumerated every sibling in every nested split, checking first monotone overflow exactly; it confirmed set equality, not merely packet inclusion. Leaves are established by replay (two strict integer forest bounds, or the exact JointValuation price checks). No branch is rejected by rounded floors, and precisely one Euler component can occur in an actual odd perfect number; the recurrences allow that component outside their explicit scope via their all-even configuration. No author cache was used.

Frozen `FinalSprint/Delta.json` row `P7_I00031`: root 7, `remaining_actuals=[130]`, so exhausting this key exhausts that residual shard. Scope is canonical root 7 (19 absent), exact `v_7(N)=130`; neither divisibility lift nor free removal of the canonical support assumption is warranted.
