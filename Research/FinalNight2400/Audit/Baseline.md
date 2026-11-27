# Baseline 1447d41b regression (independent audit)

All five requested baseline commands passed directly on the canonical-byte checkout. For the two raw-byte-sensitive Gemini commands, the lead restored exactly the pinned LF file content; [the timed rerun](DirectGemini.py) sampled the sum of parent/descendant RSS at 0.5-second intervals. This is a sampled high-water estimate, not an OS peak or unique resident memory. Other three did not measure RSS. Not a full-history cold replay and not a 72-hour benchmark. All proof checks offline, normal (non-optimized) CPython 3.11, with no discovery or factorization. [Timing runner](RunBaseline.py).

|Command (from repository root)|Result, elapsed wall time|
|---|---|
|python Sources/Python/RepositoryStructureChecks.py|[PASS](Structure.log), 0.665 s; 20040 tracked files.|
|python -I -S -B Sources/Python/FinalSprintLedgerChecks.py|[PASS](Ledger.log), 0.120 s; 18 packet identities, prior ledger 2990/82/92.|
|python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py|[PASS](Replay.log), **3807.369 s**; all 13 accepted Night2400 complete-key arithmetic checks, regenerated 3003/69/79 projection. No older-history or conditional-packet replay inferred.|
|python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/Verify.py|[Direct checkout PASS](GeminiDirect.log) after canonical byte restoration, **472.642 s**, sampled peak tree RSS **216113152 B**. G8 and T10 dependencies and 3004/68/78/60 projection. [Initial CRLF failure](Gemini.log) in 0.086 s; [earlier private LF replay](GeminiLf.log) also passed 460.308 s.|
|python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/VerifyT10.py|[Direct checkout PASS](TenDirect.log) after canonical byte restoration, **166.313 s**, sampled peak tree RSS **194641920 B**. C10 included and 12/12 T10 leaves checked. [Initial CRLF failure](Ten.log) in 0.098 s; [earlier private LF replay](TenLf.log) also passed 153.124 s.|

The secondary [LF runner](OfflineLf.py) made a private temporary proof-input tree under this audit directory, replaced CRLF by LF in text files, copied binary packets unchanged, and executed the original scripts with all raw-byte identity checks enabled. No baseline file was changed by this workaround. All timings include subprocess wall time; simultaneous workloads may affect them. Verified projection and partial historical increments do not certify the entire global theorem.
