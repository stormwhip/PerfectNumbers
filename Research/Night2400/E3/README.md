# (7,490): complete first-pivot exclusion for P7_I00093

The research tree was built in stages: 11 fibers, then 12 after closing 18,
then 13 after closing 12. Only the final complete packet is carried here;
it also closes 16. No conditional result is counted separately.

The first pivot `6644251020606657127` is forced by `σ(7^490)`. The
monotone size tail begins with exponent 85. Before the tail, the exact
legal branches are `4,6,10,12,16,18,22,24,28,30,34,36,40,42`. Direct
rejections are `46,48,52,54,58,60,64,66,70,72,76,78,82,84`; all other
exponents from 1 through 84 are inadmissible by parity or forbidden
emissions. The floor log10 at the first size-tail exponent is 2409.

The `18` fiber splits on `7197353`, which initially has valuation one.
Its live second exponents are `1,2,4,5,6,8,9,10,12,13,14,16,17,20,21,22,24,
25,26,28,29,30,32,33,34,36,38,40,41,42,44,45,46,48,49,50,52,53,54,57,58,60,61,62,64,65,66`.
Every other exponent below 135 fails admissibility or the exact-state
bound. The monotone tail starts at 135 (floor 2405). All leaves are evaluated
by both existing exact integer forest algorithms. The discovery factor
bank and PARI are not proof dependencies.

## Complete packet

The [complete certificate](Fibers7x490Complete.json.gz), SHA-256
`caeabb5d0ddedfa7fffb071404e712ad0a8233a47b8131c68d2f570df34a226d`, includes
all fourteen first fibers: 277 forest leaves, ten internal splits after
selecting the first pivot, 1,588 ECPP chains, and no open paths.
The `12` fiber uses 84 forests beneath four splits. Its
second pivot `401819947527959273` has initial valuation one; the live
second exponents are `1,2,4,5,6,9,10,12,13,14,16,18,20,21,22,24,25,28,29,30,32`,
and the monotone tail starts at 66 (floor 2405). The `16` fiber uses 135
forests beneath five splits. Its second pivot `696239` has initial
valuation one. All even exponents from 2 through 84 are live; even
exponents 86 through 170 are excluded directly, odds are inadmissible,
and the monotone tail starts at 171 (floor 2405). The tightest late
subtree, at second exponent 10, is replaced by one forest (floor 2417).

```powershell
python -B -I -S -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E3/Fibers7x490Complete.json.gz
```

Discovery-only: the targeted ECM run on `f=12,16,18` used `B1=250000`, at
most 500 curves and 180 seconds per input, and recovered the 59-bit
factor for fiber 12. The 1001-bit and 1103-bit inputs were not factored by
that run. Final fiber 16 work used two separate ECM probes on the smallest
open descendants; the stronger probe used `B1=375000`, up to 700 curves
and 110 seconds per input. It yielded factors for the 195-bit and
466-bit descendant residuals. PARI factored the 125-bit residual
`25310786732075498293467630602217479059` under a 90-second cap. The final
forest at second exponent 10 used smoothing parameter 31 and head 256.
Neither incomplete factorization nor any search result is taken on trust
in replay. No divisibility lift or ledger edit is made here.
