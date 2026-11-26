# Two exact fixed-Euler support leaves

Assume `v_7=12`, `19` absent, odd perfection and `N<=10^2400`. The first packet excludes `v_16148168401=1`, `v_110563=2`, `v_226741=2`; the second excludes `v_16148168401=2`, `v_200741603328100897=1`. The unique Euler prime is fixed in both leaves, and every named non-root base is forced by the preceding divisor sum. This is **not** a closure of either first-pivot fiber or of the root exponent/shard. These packets are kept separate from the [first-pivot ledger](README.md).

The proof partitions by exact presence or absence of `(3,5,11,13,17,31)`, with no conditions on other primes. Of the 64 cases, 32 conflict with a fixed exact exponent or forbidden divisor. Of the other 32, 23 are strictly abundant using the least allowable even exponents of the required support primes; none of these primes can be Euler. Abundancy of a prime component is monotone in its exponent. All nine surviving support masks have individually validated integer forests. A required support prime need not divide the fixed divisor-sum block: in that event its root valuation lower bound is one, its own minimum even exponent is charged, and its label is stripped from every other charged divisor sum. Both recursions verify the same disjoint charge accounting and include the entire exponent tail. No unknown support prime or heuristic assumption is added.

Run from the repository root without external dependencies:

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/SupportLeaf12.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/SupportLeaf12.py Research/Night2400/A/SupportLeaf2.json.gz
```

The [first packet](SupportLeaf12.json.gz) has SHA256 `2f6e8e114b04c9f35c3f52ead54345cb28e5091b314b2575dbf8d36b82f7c116` and 839 ECPP witnesses. The [second packet](SupportLeaf2.json.gz) has SHA256 `84d1fb5287dfd609e3707134d369a96c0f816bbf5d936a7b13fee27c75d6f87d` and 969 ECPP witnesses. Each covers the same nine mask numbers in the stated order: `1,5,9,17,25,33,37,41,49`.
