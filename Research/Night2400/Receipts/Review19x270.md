# Root 19, exponent 270 — independent partial certificate

Clean detached `45c8297ce7bca4e5191c345b70b65890280dd434` in `E:\PerfectNumbers-Night2400-reviewa`; only `Research/NightOrder/ECPP/` sparse-excluded; did not access that directory or author caches. Python 3.11.9. Verifier SHA-256 `7f652874ac1c3bef9f7da6b2c230b471f438e7163c83af583129f3db5dafe080`; certificate SHA-256 `51b237bfe95c6b0089ed7440d0ddf2a971fca85b0a0393f43ba12f0b2696b0fd`.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers19x270.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/Root19x270Audit.py
```

Cold replay 2026-11-27 03:09:33.0047854 → 03:09:46.0304501 UTC+08:00; 13.015352 s stopwatch, exit 0. Independent domain script exit 0. Pivot `107499032325771819886598832053082701603`, valuation 1; exponents 1–45 tested, monotone size tail starts at 46. Odd candidates fail Euler form; 24–44 even are directly excluded. Exactly seven of eleven live fibers covered: `[2,6,8,14,18,20,22]`; live open `[4,10,12,16]`. Both internal split domains and tails (37 and 83) independently rebuilt and key sets compared for equality. Total `forest/split/direct/price=[38,2,45,1]`, with 233 embedded ECPP witnesses. The sole price leaf is exact exponent 18 targeting both fixed bases, remaining incoming valuations `[270,17]`; stock joint replay returned `4` relaxed exceptions and Euler windows `[3242,1099,537]` (the independent script separately verifies the scope and incoming caps, not the price arithmetic). Credit is **0 actual root exponents and 0 shards**.
