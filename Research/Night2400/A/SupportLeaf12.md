# An exact support leaf of the `v_Q=1` fiber

This packet excludes only `v_7=12`, `v_16148168401=1`, `v_110563=2`, `v_226741=2` with `19` absent, odd perfection and `N<=10^2400`. The first non-root prime is the unique Euler prime throughout this leaf. The two subsequent bases are forced by successive divisor sums. This is **not** a closure of the `v_Q=1` fiber or of the root exponent/shard. It is kept separate from the [first-pivot ledger](README.md).

The proof partitions by exact presence or absence of `(3,5,11,13,17,31)`, with no conditions on other primes. Of the 64 cases, 32 conflict with a fixed exact exponent or forbidden divisor. Of the other 32, 23 are strictly abundant using the least allowable even exponents of the required support primes; none of these primes can be Euler. Abundancy of a prime component is monotone in its exponent. All nine surviving support masks have individually validated integer forests. A required support prime need not divide the fixed divisor-sum block: in that event its root valuation lower bound is one, its own minimum even exponent is charged, and its label is stripped from every other charged divisor sum. Both recursions verify the same disjoint charge accounting and include the entire exponent tail. No unknown support prime or heuristic assumption is added.

Run from the repository root without external dependencies:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/SupportLeaf12.py
```

The [packet](SupportLeaf12.json.gz) has SHA256 `2f6e8e114b04c9f35c3f52ead54345cb28e5091b314b2575dbf8d36b82f7c116`. Successful replay reports nine support forests and 839 ECPP witnesses. The covered masks in the order above are `1,5,9,17,25,33,37,41,49`.
