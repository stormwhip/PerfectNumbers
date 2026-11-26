# A78 and separate support leaf — independent reviewer-a receipt

Worktree `E:\PerfectNumbers-Night2400-reviewa`; clean porcelain immediately after switching to detached `ac69476668cc98f8e5b445d39b5ec76d723c0ae2`. Sparse patterns exactly `/*` and `!/Research/NightOrder/ECPP/`, inherited from A77. The retained ECPP tree and author caches were not accessed; the packet-embedded ECPP chains were used. Python 3.11.9. Prior A77 receipts reside in local commit `6b1fe5e168dcb1250135a59cca60bbffad6812a0` so they do not pollute the candidate tree. SHA-256 as read from the candidate working files:

```text
16565e678cac8cd687d0ea4f937093b5e813f0a1d749acd9e1c773957b9b4165  Research/Night2400/A/Verify.py
27185768c900be4ab6ade1413b1f7c7586ac05954400816b291b88dd27213364  Research/Night2400/A/Fibers12.json.gz
c95016ad1822e02e76ecd0f3bfb73a09a2c81af8c44c12ff7b98e5999c06a780  Research/Night2400/A/SupportLeaf12.py
2f6e8e114b04c9f35c3f52ead54345cb28e5091b314b2575dbf8d36b82f7c116  Research/Night2400/A/SupportLeaf12.json.gz
ccaf991d8dcdff4a469f5ee52efadf6b43958a810472ddfd260f1c84efd8b10f  Research/Night2400/Receipts/Audit7x12Delta.py
```

## A78 first-level delta

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Audit7x12Delta.py delta
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
```

The independent delta reads the A77 compressed packet by Git object and establishes exact decoded equality of all 77 inherited trees and 8,656 inherited ECPP entries. One new tree, key 28, and eight new ECPP entries. Stopwatch 1.586689 s; UTC+08:00 2026-11-27 01:54:39.3855854 → 01:54:40.8404399; exit 0. The live exact suffix exponents on the new compelled pivot are `[1,2]`; 3 and 7 fail Euler form, 4–7 fail a branch-specific size lower bound, and every exponent at least 8 fails the monotone parent-size tail. The exponent-one branch fixes the Euler prime, so compelled primes 3 and 5 each must have at least exponent two. Their sigmas with the prefix give a positive exact rational excess over 2 (`floor(10^12 * lower) = 2089629629737`), irrespective of all other unknown components. The exponent-two branch is an integer forest.

Full A78 cold run: UTC+08:00 2026-11-27 01:53:00.2360831 → 02:00:15.4915203; stopwatch **435.246704 s**; Python and job exit **0**. The shell wrapper had the same corrected hash-collection issue described below; hashes were collected separately.

```text
PASS 28 2400
PARTITION live 83 covered 78 uncovered 5 forests 2139 splits 83 direct 2261 prices 2 abundance 1 ECPP 8664
UNCOVERED [1, 2, 4, 12, 42]
```

First-level credit only: 78 exact fibers; 0 actual root exponents and 0 shards.

## Separate 64-mask support packet (first committed at 839f6b05)

`SupportLeaf12.py` and `SupportLeaf12.json.gz` have identical committed blobs at `839f6b05d1f9d8f3853396253c15c100789f0cd5` and `ac69476668cc98f8e5b445d39b5ec76d723c0ae2` (`3fbff068e7e76857be2253ad2a90e2241993d78f`, `732f9f30e4074ddfc9d8fa5afdd4e22e284e24de`). At both commits its `Verify` imports `C,B,floor10` identically, and the transitive source files are unchanged. The replay runs as a separate command from clean A78, not as part of the first-level verifier:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/SupportLeaf12.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Audit7x12Delta.py support
```

Candidate Python run: UTC+08:00 2026-11-27 01:53:17.3906816 → 01:53:45.9347069; stopwatch 28.511411 s; exit 0; 32 direct, 23 abundance, 9 forests, 839 ECPP. The shell wrapper's initial attempt to pipe string paths into `Get-FileHash` raised nontermination errors unrelated to Python; hashes above were obtained separately using `-LiteralPath`. The independent audit imported no candidate code; rebuilt exact obligations, least allowable even exponents, and private-source integer forest arithmetic including all exponent tails. Candidate cold run validates large-prime certificates; independent script proves the small prefix/support primes itself by trial division. Independent UTC+08:00 2026-11-27 01:54:41.8203592 → 01:54:50.6622670; stopwatch 8.967442 s; exit 0. [Per-mask transcript](Support7x12.txt) matches all groups, including forest masks `[1,5,9,17,25,33,37,41,49]`.

This separately excludes only the exact prefix `((7,12),(16148168401,1),(110563,2),(226741,2))`, for odd perfect `N≤10^2400` with 19 absent. It gives **no** first-level closure of `v_Q=1`; no root exponent/shard credit.
