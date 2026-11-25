# Four partial root-3 net-base certificates, 2026-11-26

**New full exponents = 0; new closed shards = 0.** Proves the E3a all-s base >10^2120, 10^1893, 10^1855, 10^1639 at e=1108,990,970,856 respectively, and E3b >10^2089 at e=1108. Each external ordinary 3-supply unit other than the chosen Euler emitter comes prepaid at price 81. The remaining *net* auxiliary cost is missing; the bounds alone do not prove N>10^2400. No repository access needed. No LP. No network required except to obtain optional Python dependencies.

Run from this directory:

```
python -m pip install --target vendor python-flint==0.9.0
python -I -S -B NextRange.py
python -I -S -B Next.py
python -I -S -B Fast1108.py 2120 --fast
python -I -S -B InternalSupply.py
python -I -S -B InternalPrefix.py 2089 --fast
```

The last script can run without `--fast`, using Python integers only (slower). Only NextRange requires python-flint; it uses modular polynomial multiplication/evaluation, no probable-prime oracle. The other checks can use standard Python alone. The two markdown notes contain arguments for every branch. Expected outputs for NextRange and Next are supplied; InternalSupply prints `5525`, InternalPrefix prints `{'e': 1108, 'target': 2089, 'prefix': 3643356, 'order_exclusions': 1928}`. Set no Python optimization options; certificates use assertions. Original shared setup for the canonical root 3: 3^e||N, gcd(N,7·11·13·19·31)=1, σ(N)=2N, N odd and ≤10^2400; external Euler to first power q∤σ(3^e), s=v3(q+1)>0, r ordinary with q|σ(r^f). Published files extend the previous partial verifier, not the frozen proof ledger.
