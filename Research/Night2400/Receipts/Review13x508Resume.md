# G8 follow-up — (13,508), full first fiber 6

**PASS 45/46; only first f108 OPEN across all eight canonical masks.** Detached clean tracked candidate `3d53a0bde2d49c92976d7e5104c87c82fac66060`, CPython 3.11.9. `Resume6.json.gz` SHA-256 `bd46c808e0a830d9f6d1e498a7daa57a2bbc55525a97491955a33e54779b4248`. Unchanged old packet SHA-256 `d798580b1e3e4760bcb67da93e5f9c37611ef1997d543e4a6d904a0d722c9680`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/G8/ResumeVerify.py
```

Full invocation (including old replay) 2026-11-27 04:51:37.736–04:54:00.431 +08:00, elapsed 142.7439069 s, exit 0. Verified source diff adds only the new replay, new packet, discovery seal and documentation; old mask checker and packet unchanged. Independently enumerated old f6 explicit holes, each exactly `[(13,508),(4073,6),(3032394642737237,4)]` in masks `[16,48,112,176]`. New forest uses canonical earlier-root bans only, no extra mask assumption, hence discharges this same exact projected prefix on all four masks. Both integer recurrences strictly exceed B (minimum decimal floor 2417); four roots, 492 owned vertices, head 384, 138 new-packet ECPP all used. Each of the eight canonical masks still has an explicit f108 gap. No complete key or shard credit, and no widening by divisibility.
