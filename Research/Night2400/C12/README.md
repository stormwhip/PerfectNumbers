# Night2400 C12 — (31,310), P31_I00062

Offline replay from repository root using standard-library Python without `-O`:

```text
python -I -S -B Research/Night2400/C12/Verify.py
python -I -S -B Research/Night2400/C12/Verify.py --deep
```

For odd perfect `N <= 10**2400` with `31^310 || N` and inherited exclusions 19, 7 and 11, the asserted 43-bit prime `q=5691933643219` is forced. The complete first split checks every exponent below the monotone tail at 117, with 26 live, 25 directly impossible, and 65 incompatible. In this packet the only completely excluded first fibers are **6, 16, 58**. It does not replay any other initial candidates, and makes no complete key or shard claim.

- **6:** the extra forced prime has exactly two surviving exponents 2 and 4. Both are checked by two exact forest recurrences, with minimum floor 2401. Four direct siblings and the complete tail are rebuilt.
- **16:** the extra forced-prime split rebuilds 15 live children, 15 direct siblings and the complete tail. The formerly missing exponent-4 child is covered across all 16 support masks for `(13,3,5,17)`: two strict abundancy proofs and 14 dual forest proofs, with exact lower bounds all strictly above `10**2400`.
- **58:** the C7 prefix-LCM-aware price, reproduced [locally](PrefixPrice.py) for independence, succeeds at target `q` alone with receipt `(0,[21,0,37])`.
- **18, conditional only:** after `707818236468853019281602309439653890995043^2`, the forced prime `385772801143` at exact exponent 10 is fully excluded by dual forest (floor 2408). Its exponent-16 path is excluded on 12 of 16 support masks (one abundance, 11 forests). That exact path remains open at masks `8,56,72,120`. Other siblings or first fibers are not implied by this supplement.

| Packet | SHA-256 |
| --- | --- |
| [6 and 58](Minimum31x310.json.gz) | `c62dc8982aef05f8034b8b68c7734d03bb55ecd49ef719bbe0ef9df1b3d9f908` |
| [16](Fiber16.json.gz) | `ac84dd662ff3c391578743c3d0dc081d642214f221396613c7fc8d9fb4a53997` |
| [Conditional 18](Paths18.json.gz) | `0eac93df81a32ba4e8f082e302ae0ba7486972a33f99fb50007236f8181ab1ab` |

Discovery used local official data, bounded ECM and PARI. No generated cache, discovery tool, prior verdict or other Night2400 packet is loaded during cold replay.
