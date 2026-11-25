# The 3/5/11 support theorem

For every odd perfect number `N ≤ 10^2400`, **3, 5 or 11 divides N**. The assertion is unconditional in the Euler prime, exponent pattern and canonical root class. Alongside the previously published `{3,5,7}` hitting theorem, this says that if `gcd(N,15)=1` then **both 7 and 11** divide N. Neither 3 nor 5 alone is asserted to divide N. This excludes the former entire `3,5,11`-absent seven-exponent subclass, not the canonical exponents when 11 is allowed; no additional complete root exponent or shard is counted solely from this result.

## Exact proof and dependencies

1. Under absence of 3 and 5, the old `{3,5,7}` theorem forces 7.
2. Under absence of 3,5,11, the new four-prime hitting sets `{3,5,11,q}`, for `q=13,17,19,23`, force those four primes. Each was cold-replayed from separately authenticated six-, five- and four-element forbidden/required support cases. The last three four-element conclusions come from `ReleaseAlternates.py`; the first comes from `ReleaseFour.py`. The intermediate files deliberately state their own prerequisites.
3. Therefore, if 3,5,11 are absent, all of `7,13,17,19,23` occur. The final packet assumes precisely these five presence conditions (only exponent lower bound one for each) and no other support condition. Its original size/abundancy relaxation yields integer logarithmic floor **2511**, strictly greater than 2400. This is a finite certificate, not a claim that an unconstrained LP enumeration finished.

The final packet uses the ordinary dual model described in `FiveSets.md` without any additional parity cutting planes. It includes only the ECPP chains required by its extra prime labels, checked link by link; the other optional labels have the already checked 64-bit or archival Pocklington proof. Solving and certificate discovery tools are not used in replay. The independently computed directed bound is checked before assigning support credit. The positive branch theorem from step 3 cannot be detached from step 2 and used when these primes are not yet forced.

## Cold commands

```
python -I -S -B Research/MiddayTerminal/ReleaseTriple.py --baseline
```

To verify just the last packet **after** the historical and intervening support premises have been replayed, use `--only-new` instead. Beyond the files in the immediately preceding alternate-four-prime release, the three-prime release requires only `Triple.md`, `ReleaseTriple.py` and `Pack-New-LocalTriple.json.gz`.
