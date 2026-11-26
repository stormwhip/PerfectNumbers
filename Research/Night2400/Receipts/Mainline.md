# Frozen-main regression receipt

Input: `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec` from `origin/main`. This is a smoke/incremental regression of that GitHub baseline, not a replay of all historical dependencies. None of these checks advances the overnight ledger.

| Check | Result | Local full stdout/stderr |
|---|---|---|
| `python -I -S -B Sources/Python/RepositoryStructureChecks.py` | exit 0 | `Research/Night2400/LocalLogs/BaselineRegression.log` |
| `python -I -S -B Sources/Python/FinalSprintLedgerChecks.py` | exit 0 | same |
| `python -I -S -B -X int_max_str_digits=0 Research/Midday/LedgerTests.py` | exit 0 | same |
| `python -I -S -B -X int_max_str_digits=0 Research/SupportSplit/Verify.py` | exit 0 using the original LF blob; 11,398 cases, 4,833+9 conditional exclusions, 6,556 remaining, 0 actuals | `Build/Night2400/SupportSplit.log` |
| Independence, capacity and Teichmüller audit steps from the repository integrity workflow | all exit 0; canonical `AuditSummary2400.json` identical | `Build/Night2400/HistoricalAudit.log` |
| The integrity workflow's 12 Python smoke suites plus exact `(3,2476)` forced-prime smoke replay at 980893 | all exit 0 | `Build/Night2400/MainlinePython.log` |
| MinGW-independent C++ smoke replay in Ubuntu WSL: codec, single-flight, sigma precheck and frontier build | all exit 0 | `Build/Night2400/NativeChecks.log` |

The SupportSplit checker hashes Git's original raw `Research/Midday/Delta.json` blob. On a Windows checkout with automatic LF→CRLF conversion, the first attempt failed at the identity check. The successful run temporarily materialized the exact tracked Git blob; no arithmetic verifier or historical ledger was changed. A clean checkout with `core.autocrlf=false` avoids it. Audit-output comparison normalized transport CRLF before comparing.

Local log identities: SupportSplit SHA-256 `c74c1a9bc232bd234fe3baab7d609811293aac40d5b10bd2effdab21048521ad`; HistoricalAudit `9950a60ccdf832dbf56f8197f4506494879251bc136c9cc2f6abc1efc9f2fcf2`; MainlinePython `b6c2142bc9334729ebf2c3abbbb7b128cd968a3d46fb937ce2c621b522e6cb4a`; NativeChecks `7bd93c7d508fb36918120b9fc219c2db12ace88c5c4e966ccf161d7b0f45ce05`. Canonical generated audit JSON SHA-256 `bfd7d81a016c00d15d51c82dad7b379232f91a58c22cf1d2349061fff7e4c140`.

[Workflow commands](../../../.github/workflows/RepositoryIntegrity.yml). Arithmetic replay of [FinalSprint](../../FinalSprint/Verify.py) is reported separately when finished.
