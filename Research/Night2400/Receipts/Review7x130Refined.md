# E refined — (7,130), five complete conditional first-pivot fibers plus partial descendants

Candidate `a495ca47cf3930f32bf951371ffe8f7e0ba97769`, detached clean tracked files; CPython 3.11.9. This candidate renames (but does not change the bytes of) the refined packet from `100f8971d42e8d5dedd2182541b04efbd7f53d0a`. Compressed SHA-256 `c3215e5a7456cee4ba8c266b0103c1316cbc18aa369813429f112e396161b8f6`.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/E/Verify130.py Research/Night2400/E/Conditional7x130Refined.json.gz
```

**PASS conditional `[1,2,8,9,10]`; OPEN first-pivot `[4,6]`.** Start 2026-11-27 00:04:11.730 +08:00; end 00:05:36.737 +08:00; elapsed 85.1291239 s, exit 0.

Independent direct arithmetic rebuilt all 17 split domains (including the root), requiring exact equality of the live children at every split. Raw tail exponents in depth-first order: `21,52,28,126,90,44,49,68,61,44,25,17,23,4,18,25,14`. All split pivot source valuations are 1. Root domain remains `[1,2,4,6,8,9,10]`, with `[4,6]` not fully closed; neither carries over a root-level exclusion. The deep packet has 44 explicit OPEN paths (22 under first valuation 4 and 22 under 6), 114 forest leaves, 8 price leaves, 626 embedded ECPP entries. Appending a deeper exact branch does not lift back across its open siblings. Strict integer `>10^2400` remains necessary for a size exclusion; the single Euler choice is checked on each fixed path and canonical root 7 rules out 19 throughout.
