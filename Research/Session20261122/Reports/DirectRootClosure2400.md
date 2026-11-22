# Direct Root Certificates for the `10^2400` Partition

**Date:** 2026-11-22. **Scope:** original root set
`S = {3,5,7,11,13,17,19,31}` with fixed enumeration order
`(19,7,11,31,13,3,5,17)`.

## 1. Exact theorem and proof

Let `N` be an odd perfect number. Assume the current root class requires
`p | N` and excludes every earlier root `q` in the fixed order.

Every canonical exponent branch has either:

1. `exact=True`, so `v_p(N)=d`; or
2. `exact=False`, so `v_p(N)=e >= d` and `d+1 | e+1`.

In the second case, write `e+1=k(d+1)`. The identity

```text
sigma(p^e) / sigma(p^d)
  = (p^(e+1)-1) / (p^(d+1)-1)
  = 1 + p^(d+1) + ... + p^((k-1)(d+1))
```

is an integer. It is also immediate in the exact case that
`sigma(p^d) | sigma(p^e)`.

For an odd earlier root `q`, if `q | sigma(p^d)`, then
`q | sigma(p^e) | sigma(N)=2N`, hence `q | N`, a contradiction
to its exclusion. The entire top-level shard is closed by one
`FORBIDDEN_FACTOR` leaf. Its verifier independently checks the root
state, `q`'s primality witness, and exact divisibility.

For `q != p`, divisibility is checked without forming the huge geometric sum:

```text
if p % q == 1:
    q | sigma(p^d) <=> (d+1) % q == 0
else:
    q | sigma(p^d) <=> pow(p,d+1,q) == 1
```

This follows by reducing `(p-1)sigma(p^d)=p^(d+1)-1` modulo `q`.
The independent test also constructs the exact integer `sigma(p^d)`
for every selected closure and checks divisibility again.

## 2. Exhaustive experiment

Run the canonical 3,072-shard generator, test all earlier forbidden
roots for each exponent option, and independently reconstruct/verify
every resulting one-node proof bundle.

| Root | Direct closures | Total shards |
| ---: | ---: | ---: |
| 19 | 0 | 287 |
| 7 | 2 | 412 |
| 11 | 1 | 341 |
| 31 | 1 | 253 |
| 13 | 1 | 325 |
| 3 | 5 | 676 |
| 5 | 3 | 481 |
| 17 | 1 | 297 |
| **Total** | **14** | **3,072** |

Exact direct-closure task identifiers and witnesses:

| Task | Branch `(d,exact)` | Forbidden divisor |
| --- | --- | ---: |
| P7_I00000 | (2, true) | 19 |
| P7_I00001 | (8, false) | 19 |
| P11_I00000 | (2, false) | 7 |
| P31_I00001 | (4, false) | 11 |
| P13_I00000 | (1, true) | 7 |
| P3_I00000 | (2, true) | 13 |
| P3_I00001 | (4, true) | 11 |
| P3_I00002 | (8, false) | 13 |
| P3_I00003 | (14, false) | 11 |
| P3_I00004 | (24, false) | 11 |
| P5_I00000 | (1, true) | 3 |
| P5_I00001 | (2, false) | 31 |
| P5_I00002 | (4, false) | 11 |
| P17_I00000 | (1, true) | 3 |

A local independent integer experiment reproduced the 14/3,072 census and
rechecked the 14 exact geometric sums. A repository regression was added to
run the full `IndependentVerifierV2`, tamper rejection, and audit integration.
**The new repository regression has not yet been executed in CI in this session.**

## 3. Implementation

- `../Python/DirectRootClosures2400.py`: constructs externally pinned one-node
  proof bundles, verifies each through `IndependentVerifierV2`, rejects a
  mutated forbidden-prime claim and optionally exports JSON certificates.
- `../Python/DirectRootClosuresTests.py`: checks 14/3,072 counts, the root-7
  example, the audit fast path, and the non-closure of the first root.
- `../Python/AuditRunner2400.py`: before reading ledgers, attempts this
  independently verified mathematical closure for the current trusted
  `RootTaskPin`. Reports `VERIFIED_CLOSED` with
  `certificate_source=DIRECT_ROOT_FORBIDDEN_FACTOR` only after checker acceptance.

Run from repository root:

```bash
python3 -S -O Research/Session20261122/Python/DirectRootClosuresTests.py
python3 -S -O Research/Session20261122/Python/DirectRootClosures2400.py
python3 -S -O Research/Session20261122/Python/DirectRootClosures2400.py --emit-dir Build/DirectRootCertificates
```

For a complete 3,072-task audit, use the existing `AuditRunner2400.py`
with a canonical manifest and the independently verified original terminal
certificate. Missing non-direct shards remain `UNSTARTED` or their actual
ledger status, never silently closed.

## 4. Open obligations

The direct lemma closes 14 shards, or about 0.456% of the canonical partition.
**3,058 top-level shards still require independent certificates**, including
all root-19 tasks. This work does not establish the `10^2400` theorem or a
72-hour runtime.

Next, prioritize independently checkable partial sigma divisibility,
new primality witnesses and search-to-DAG export. The root-level direct
certificates demonstrate that the audit can accept mathematics rather than
C++ solver labels without requiring a complete factorization of the source sum.
