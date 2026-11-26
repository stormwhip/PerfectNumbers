# P19_I00059 — exact key (19,282)

This additive packet covers only exact root `(19,282)` against baseline `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. It is not a full-key closure and is not lifted to any other exponent.

- First pivot `q = 1735317810514627`, `v_q(D)=1`, `q ≡ 3 (mod 4)`. The 27 live exponents are even `2..54`.
- This packet covers `4,8,16,28,30,36`; the lead's disjoint remit covers `6,12,14,18,20,22,24,26,32,34,38,40,42,44,46,48,50,52,54`. The union leaves `2,10` open.
- Odd `1..111` fail Euler parity, even `56..110` fail the exact-state base bound (decimal floor 2412 already at `56`), and the monotone size tail begins at `112`.
- Packet: [Fibers19x282.json.gz](Fibers19x282.json.gz) — SHA-256 `4cde99ecee143874fa6609c5858bb9c5f83673ee213c619c452ddd433beeefde`.
- Cold receipt: `[3554,130,3903,0]` (forest, inner split, direct child exclusion, price). No joint-price leaves appear in this additive packet.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/F4/Fibers19x282.json.gz
```

Discovery repaired only holes in the lead's scout. The last leaf of `4` used fully separated remainders of `Phi_3(65564877023808514086956556442714245281943976141)` and `Phi_11(124488945131)`. The lead's ECM returned root-emission factors `2485015031593` and `1356123638694434236741701011417065781518553882490519056789050640655601813387` at `8`, and `6851056278827` at `30`; subsequent forest/split repair closed both. The two misses at `36` closed by ordinary trees without repeating the failed root-level price trial. Replay uses no discovery data or network.
