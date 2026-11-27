# Fixed batch one: independent projection audit

**PASS** for the detached LF checkout identified by the lead as 4ebbccc78135cc7dfbd20ed732564cca7643ddea. The projection audit tests bookkeeping and references. Separately the lead completed the integrated arithmetic run described below. The [independent checker](ProjectBatchOne.py) starts from both original frozen Gemini incidence maps (68 shards, 78 distinct pairs, 60 singleton shards) rather than importing the candidate projection. It asserts the exact old-minus-new triples from a separately specified five-key acceptance list, all remaining row sequences and all per-root lists, and checks the five complete verifiers appear in the integrated entrypoint. All 27 tagged results refer to the same 1447d41b baseline; precisely five full records with distinct keys; **22 conditional records, zero ledger credit**.

|Full exact pair|Deleted singleton|Independent arithmetic receipt|
|---|---|---|
|(19,58)|P19_I00015|[Ten](TenReceipt.md)|
|(31,310)|P31_I00062|[Thirty-one](ThirtyOneReceipt.md)|
|(13,262)|P13_I00055|[Thirteen](ThirteenReceipt.md)|
|(13,310)|P13_I00063|[Next](NextReceipt.md)|
|(31,352)|P31_I00069|[More](MoreReceipt.md)|

No row is partly changed or newly added. Five unique exact keys removed, all from separate singleton shards. Counts **3009/3072 closed, 63 open, 73 distinct residual keys, 55 singleton shards**; status remains INCOMPLETE_FRONTIER. SHA-256 (LF): Results 1212291dc757ba71cefd3f520e2b97c3772a38415f6cbeed9b9ba4c22cff130c; OpenFrontier 41f67982150be6e95bd69efb282ee2dc82baa88f2e99aebf959d2270cdd925a5; integrated Verify a801932fa0937184e0aec102a5c521fe226a367721f18e8c7f8e899454ad56f0. Later work is not covered by this snapshot. Replay with the checker followed by an optional checkout-root argument pointing to this exact batch.
