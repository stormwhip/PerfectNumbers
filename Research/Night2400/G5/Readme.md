# New pivot subdomains at canonical (7,430)

Assume an odd perfect number `N ≤ 10^2400` with `19 ∤ N` and `7^430 ∥ N`. This is a strict partial certificate for `P7_I00082`. It does not replay the earlier C3 results for pivot valuations 14 and 16 or claim the whole shard.

```powershell
python -I -S -B Research/Night2400/G5/MaskedVerify.py
```

The [cold checker](MaskedVerify.py) requires only the public proof arithmetic, standard library, and [sealed packet](Seven430.json.gz). Packet SHA-256: `8d8cd83e60e94f01cea543a1ed2ff7b04b49996c264c065343b20f303cb4f6de`. Negative/exploratory results, third-party libraries, the C3 data, and the factor bank are not required. Every size leaf must strictly exceed `10^2400` in both recurrences; the paper decimal floor is not the acceptance test.

The certified `Q=3602407438103418087310110702859943140744217508967` divides `σ(7^430)` to exponent one. Its exact live canonical valuations are `2,4,6,8,10,12,14,16`; the monotone tail starts at 36. The verifier enumerates all 64 S8 masks under the root condition (`mask ≡ 2 mod 4`) and exhausts the six requested fibers `2,4,6,8,10,12`, pruning by parity, forbidden-prime divisibility, incoming valuations, prefix size and abundancy. The support order is `(19,7,11,31,13,3,5,17)`. Exact splits enumerate every compatible sibling and monotone tail; `open` markers never earn credit. Abundance checks minimize over at most one Euler position among the compelled factors, permitting it to be elsewhere.

The lowest two tested fibers `v_Q=2,8` share the certified 289-bit forced prime `U=2719475404574062750177556064626770984612172161050693998086064689414615488121825606606912057`. The exact support/abundancy check leaves only masks `50,58,178` before the `U` split. After the split `v_Q=8` is fully excluded, with the surviving size leaf at `v_U=2`. For `v_Q=2`, `v_U=8` is excluded by a strict forest, and `v_U=4` by direct/support checks. The `U^2` divisor sum still has an unfactored 566-bit cofactor; a short deterministic [ECM attempt](Ecm.sh) found no split. The complete `v_Q=6` fiber uses a shared ordinary size leaf. The complete `v_Q=10` fiber uses masked strict forests, direct contradictions and minimum abundancy.

The five explicit lowest holes are `(mask,v_U)=(50,2),(50,6),(58,2),(58,6),(178,2)`. The complete fibers covered here are `6,8,10`. In the six targeted fibers this leaves 85 first-level mask–valuation cells, of which 53 occur in the 27 historical projected masks; none of those 27 complete masks is excluded. Combining the result with the separate C3 closure for `14,16` leaves first values `2,4,12`.

For the three nearest projected support closures (`46,54,186`), all remaining work is at `v_Q=4`, where the exact split prime `W=62619225867394162638521` exposes the common unresolved assignment `v_W=6`; its odd sigma remainder is 431 bits. The short discovery attempts in [Ecm.sh](Ecm.sh) did not split this remainder. The supplement makes no claim for an unverified branch. [Domain.py](Domain.py), [Search.py](Search.py), and [Seal.py](Seal.py) are optional discovery and serialization utilities, not proof dependencies.
