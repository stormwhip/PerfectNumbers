# First integrated cold replay

Clean detached checkout at 4ebbccc78135cc7dfbd20ed732564cca7643ddea, Git LF bytes, stock CPython 3.11.9 on Windows (i9-14900HX). Executed the frozen default overlay command with assertions enabled and no discovery cache. Exit 0; **3124.604 s wall**. Parent plus descendants sampled every 0.5 s: observed peak summed RSS **578453504 bytes**, sampled process CPU total **2914.156 s** (5922 samples). RSS is not an OS peak or unique memory, CPU of brief processes can be missed. Start 2026-11-27 23:26:03.298 Beijing. Concurrent research load present. Reproduce by checking out that exact commit in an empty worktree and running:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Verify.py

This tested the integrated overlay as frozen with its **five** complete keys and targeted historical dependencies, not later additions, not every pre-baseline closure, and not a global 72-hour benchmark. [Independent incidence audit](Audit/BatchOne.md) and [historical regression receipt](Audit/Baseline.md).
