# FULL canonical (11,12) — singleton P11_I00004

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/ThirtyOne268/SmallEleven/Verifier.py

**Exit 0 in 2388.036 s wall** (epoch milliseconds 1795815638392–1795818026428). The full run cold-verified both the frozen C9 input and its independent support logic, then re-enumerated all 77 compatible first valuations of forced prime 3158528101. Raw monotone tail 252. Remaining firsts: **none**. The final packet gave 41 exact nested split nodes, 1131 strict ordinary/optional-Euler forest leaves and one correctly bound historical C9 coverage at first 4. This proof directly re-verifies first 5 as a forest so it is not double-counted. The supplemental bank has 3967 verified ECPP. No unverified Internet/native factor is needed by the replay; earlier hints were checked locally for divisibility and primality.

Final stdout: canonical 11^12, 77 firsts, remaining {} {'split': 41, 'forest': 1131, 'c9': 1} ECPP 3967. Only this exact pair in its canonical branch is closed; P11_I00004=[[11,12]].

Required files: Verifier.py, Kernel.py, Forest.json.gz (6727dbd681facedd4322137608dd1a0bbb3d92663a475d7e3fa59d94694d7fdf), Primes.json.gz (c9fecb05451113cc619cbbfb88903f340a62034e0095f6af15379df1a2dee715), Proof.md and immutable repository dependencies including Night2400/C9. Release set and hashes are listed by Inventory.py.
