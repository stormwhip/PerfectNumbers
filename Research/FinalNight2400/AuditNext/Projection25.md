# Final 25-key frozen projection: all incidence and overlay-link checks pass

Independently checked the **detached LF checkout 86b83705be550cb53cfcf8d7ea262a689bf00494** in Build/Final25Audit. [No-import projector](Projection25.py) compares the entire old and new incidence multiset using the verified baseline forward/reverse blobs; it never imports project code or counts certificate presence as a proof. The 25 complete keys were separately identified from accepted component reviews, including the final independent [(11,12) receipt](../LowSeven/ReviewSmallEleven.md). Each full result is unique, each key drops exactly one original **singleton** shard, and every unaffected remaining row retains exactly its old array. No secondary-fiber, new support mask or conditional row was credited as a closure. Original 3004/68/78/60 → **3029/3072 closed, 43 open shards, 53 distinct keys, 35 singleton shards**. The 93 result rows divide into 25 VERIFIED_FULL and 68 VERIFIED_CONDITIONAL; global status remains **INCOMPLETE_FRONTIER**.

| Canonical root | Exact exponents removed | Distinct residual keys |
|---|---|---:|
|19|58,82,280,282,292,312,330,372,420,618|18|
|7|36,430,882|16|
|11|12,358,396,456,462|5|
|31|16,240,310,352|5|
|13|262,310,388|6|
|3|none|3|
|5,17|none (already excluded in baseline)|0|

All 25 complete verification entrypoints occur once in the real dispatch list. All 182 listed command paths and 59 distinct proof/receipt references from verified-full rows exist. All **773 local Markdown link occurrences** in the overlay resolve to existing files in the checkout. An earlier check while the detached worktree was still populating lacked five historical path targets; once files materialized the same unmodified checker exited 0 with no missing links. The old development-link defect in the [24-key snapshot](Projection24.md) is resolved. This is a ledger, dependency-reference and link check, **not** a retrospective run of every one of the 182 commands or full historical proof replay.

Frozen SHA-256: Results 1e0d318efe5a0fb192135369d120de760f85d8b63714d254c930a5b0ed48f872; OpenFrontier c05c97f44cb8db2b9daf85a325f729b4ee74de79bd31edc690252d1f95c15919; Verify ec8387493ce60b678c010a3482da793e877870f8fe3a253aa4939c380cf55f80; Project 3993ee55c69d72bbba107af979d5ee7b4ffe159f7290906f38c36232e6eed708. Re-run: python -I -S -B Research/FinalNight2400/AuditNext/Projection25.py PATH_TO_86b83705_CHECKOUT.
