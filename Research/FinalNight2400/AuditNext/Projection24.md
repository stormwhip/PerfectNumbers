# Independent frozen 24-key projection and link audit

**Arithmetic-independent projection: PASS.** The detached LF checkout identified by lead as 3e5d9ad86e5933e12dd5f9520e9a1c16caa730f2 was read directly from Build/ColdBatchFinal. [Independent audit program](Projection24.py) takes that checkout path, uses no Git operations, imports no projection/candidate code and invokes no arithmetic replay. Both original Gemini forward and reverse maps were first pinned to raw blob SHA-1s de821605b9bb0c124ff8ca4a576f85ced96afaa2 and efad9522397f1b9a79aaf27c4ab90e65d58d1683. Their independently expanded (shard,p,e) incidence multisets matched with multiplicity exactly one. Old counters 3004 closed, 68 open, 78 distinct keys, 60 singletons.

Exactly **24 distinct VERIFIED_FULL records**, precisely the separately specified 24-key list below, no duplicates; **64 VERIFIED_CONDITIONAL records, zero closure credit**. Each full key was the sole member of its distinct former shard and occurred nowhere else. All remaining shard arrays are identical to their original arrays, no new cells, no partially edited row sequences, no extra deleted cells. Every root-specific residual list agrees with the projected union and original canonical ordering. Therefore **3028/3072 closed, 44 open, 54 distinct residual keys, 36 singleton shards**. Residual distinct counts: root 19→18; 7→16; 11→6; 31→5; 13→6; 3→3; 5 and 17→0. Global status INCOMPLETE_FRONTIER.

| Canonical root | Removed exact exponents (each clears its own frozen singleton) |
|---|---|
|19|58,82,280,282,292,312,330,372,420,618|
|7|36,430,882|
|11|358,396,456,462|
|31|16,240,310,352|
|13|262,310,388|

**Full record and link validation.** The certificate for each of the 24 full results appears exactly once in the actual integrated dispatch list; all **173** command paths exist. All **57** distinct proof and review documents cited by these full rows exist. Scanned every local Markdown link in the overlay: 759/760 valid at the frozen revision. The only stale target was the local SquareEmitter proof's link to its former development-side sparse enumeration script instead of the released sparse-pattern verifier. It does not affect any verification input or ledger cell. The lead reports the documentation corrected in follow-up 651fdbf2 and all tracked Markdown links valid there; this reviewer independently observed the corrected live link target [VerifyPatterns](../SparseSeven/VerifyPatterns.py). Do not claim the clean link result for 3e5d9ad8 or claim the broader historic repository was proof-replayed in this check. At frozen SHA the command exits nonzero **only at the last link assertion**, after every ledger/proof-reference assertion passed and fingerprints were printed.

**Frozen LF SHA-256:** Results 3fa838756c7bc63a15b808debb07f47caf80741d16fa2b1811997927a8c459cd; OpenFrontier 958a08b82f6fe8f28c3d12084ae6f1e26ec4c19db08c90e08d8a127a25d4ef32; Verify ca4e4d1e0e1a4c443ffcacbc1a6c163da699682407d2454f4645765dad6d5a12; Project 3993ee55c69d72bbba107af979d5ee7b4ffe159f7290906f38c36232e6eed708. Changes after this checkpoint require their own record. This is not a claim that the independent 173-command batch completed.
