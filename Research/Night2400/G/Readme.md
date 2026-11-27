# Strict pivot subdomains at (11,358)

This is a **partial** result for the canonical root 11 under `19,7 ∤ N` and `11^358 ∥ N`, with `N` odd perfect and `N ≤ 10^2400`. It does not close [P11_I00070](../../FinalSprint/Delta.json#L1133-L1142), nor does it close a whole projected support mask. No ledger is changed.

```powershell
python -I -S -B Research/Night2400/G/Verify.py
```

The [checker](Verify.py) uses Python standard library and the existing [Compose forest implementation](../../Nov25/Compose/Compose.py). It separately recomputes every accepted forest by a second exact one-Euler recurrence using different legality arithmetic. No archived verdict, probable-prime outcome, factor dictionary or exploratory witness is proof input. [Eleven358.json.gz](Eleven358.json.gz) provides the forests and the checked ECPP chains.

The pivot `Q=2471107084783904470093` is prime, `v_Q(σ(11^358))=1`, and `19 | Q+1`; thus Q cannot carry the Euler exponent. There are 32 root-order support masks (19 and 7 absent, 11 present), of which 17 appear in the frozen [projection](../../Session20261126/OpenSupport.json). The verifier checks all 32, and certainty of partial results does not require the projection to be comprehensive. For each, the monotone root size bounds cover `v_Q ≥ 79`, while exact arithmetic (including Euler parity, forbidden sigma factors, known incoming capacity, size, and partial abundancy) tests all `1 ≤ v_Q < 79`. The exact next-level exponent tails inside each forest are likewise charged by component size.

The union of all compatible first-pivot exponents is `2,4,8,10,12,14,16,18,22,24,26,28,30,32,36,38`. Before the new leaves there are 416 compatible pairs of support mask and pivot exponent, and 224 in the frozen projection. Separately, seven masks are rejected from the fixed root abundance bound, irrespective of the pivot exponent: `108,116,124,228,236,244,252`. Those seven masks are outside the frozen projection. Fixed abundancy uses the least compatible exact abundance per compelled prime and allows one Euler position, possibly exterior.

The packet closes the complete pivot fibers `8,12,14,16,24,26,32,36,38`, with 205 forest leaves and eight branch abundancy leaves beyond the seven root masks. There remain 91 compatible cells over 25 masks, including 69 cells over the 17 projected masks. The remaining cell counts by pivot exponent are `2:9, 4:14, 10:24, 18:21, 22:1, 28:5, 30:17`. Packet SHA-256: `0b4c763e6680587d1136852e538f08ccd66809331de0cdd0929439915cb94f7e`.

At `v_Q=8`, [the ECM run](EcmLow.sh) split the 418-bit unresolved factor of the ninth cyclotomic block into prime factors of 46, 69 and 304 bits. Direct integer root validation and ECPP replay cover these labels; the ECM output itself is not trusted. At `v_Q=12`, the entire thirteenth cyclotomic value is a single prime and is a strong mandatory root. The lowest unresolved valuation `v_Q=2` has the completely factored sigma value `3·127·773713·23140498320221407·895170073833184333`, but the proper size bound of the mask-36 prefix is only floor 809. A selected two-row price targeting Q alone fails the high-Euler inequality; this is a failed proof attempt, not a surviving candidate N. The 1168-bit cofactor of the root sigma remained unsplit in the bounded ECM trial.

[Domain.py](Domain.py), [Search.py](Search.py), and [BuildPacket.py](BuildPacket.py) are optional discovery scripts. Search uses bounded witness expansion from old packet edges and the read-only factor index; raw trials are not included. The exploratory floor at `(mask=36,v_Q=2)` reached 2256 without a certificate, still below 2400. No network discovery is needed. Do not use discovery in place of the cold proof command.
