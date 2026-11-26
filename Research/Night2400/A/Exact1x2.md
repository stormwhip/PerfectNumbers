# Exact descendant `v_Q=1`, `v_110563=2`

Under the [canonical root-seven assumptions](README.md), set `Q=16148168401`. This packet excludes only the exact prefix `v_Q=1`, `v_110563=2`, binding the compulsory base `110563` by `sigma(Q)`. Its split on `226741` has 110 live branches before attached proofs. The complete exact exponent tail, direct tests, and every live sibling are replayed.

The tree uses 339 forests, 8 splits, and 22 strictly abundant leaves; the 575 direct contradictions reported by replay include the ancestor partitions. Two hard branches have 3 compulsory, which excludes 5 since the lower bound for `7^12 3^2 5` exceeds 2. The 200 resulting absence-conditioned forests pass both independent integer recursions. The `v_226741=2` branch replays the [separate fixed-Euler support packet](SupportLeaf12.md), with its own witness ledger and exact-prefix binding. This appendix is not an independent first-pivot closure.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py Research/Night2400/A/Exact1x2.json.gz
```

[Packet](Exact1x2.json.gz) contains 4,449 ECPP certificates and has SHA256 `9b771704a2a84f022f2240995c6e741745d9bd28cfef50eef9c7f08064252f3e`.
