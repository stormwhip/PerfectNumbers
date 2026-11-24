# Five-root exact-exponent packet — offline replay

**Frozen result.** Against the archived Gemini frontier (2,027 closed and 1,045 open out of 3,072), this packet excludes **341** previously untreated actual exponents and closes **64** additional original shards. Considered by itself, that gives 2,091 closed / 981 open; status remains `INCOMPLETE_FRONTIER`. There are 689 ECPP certificates in the exact compressed witness set. Concurrent research is deliberately not included in these totals.

| Root | New actual exponents | New completed shards |
|---:|---:|---:|
| 7 | 49 | 15 |
| 11 | 44 | 14 |
| 13 | 119 | 16 |
| 19 | 72 | 7 |
| 31 | 57 | 12 |

The chosen proofs are: chain 124, hybrid 72, multiple anchors 70, fast price 69, forbidden-order price 3, Gemini emitter 2, parity alone 1. Five of the 64 closures require two different untreated actual exponents. For example, `P31_I00038` requires 172 and 518, not just the representative 172. The cofactor nonsquare-premium method was also screened but produced no additional full exponent and is not counted.

## Files and baseline

In `upstream/Research/OrderSupplyNext`, take **only** [`VerifyOrderSupply.py`](VerifyOrderSupply.py), [`Accepted.json`](Accepted.json), [`OrderPrimeProofs.json.gz`](OrderPrimeProofs.json.gz), [`Audit.json`](Audit.json), [`ReleaseTests.py`](ReleaseTests.py), and this document. Discovery caches, per-prime certificates, tools, exploratory scripts and interim audits are not dependencies. The Python-only entry point needs Python 3.10+; no PARI, internet, database, SymPy, or local paths are needed. From this directory run:

```sh
python -I -B VerifyOrderSupply.py --workers 8 --output replay.json
python -I -B ReleaseTests.py
# Optional faster independent backend for checking the identical ECPP bundle:
python -I -B VerifyOrderSupply.py --gp /usr/bin/gp --output pari-replay.json
```

The verifier reads two **existing** mathematical modules: [Gemini](../TeichmullerValuation/VerifyGeminiExponents2400.py) and [Teichmüller](../TeichmullerValuation/VerifyTeichmullerValuation2400.py). For frontier comparison it reads exactly these five checked-in baseline receipts: [Teichmüller](../TeichmullerValuation/Audit2400.json), [Gemini](../TeichmullerValuation/GeminiBatchAudit2400.json), [SupplierBatch](../SupplierBatch/BatchAudit2400.json), [IndicatorCapacity](../IndicatorCapacity/Audit2400.json), and [EulerOneSieve](../EulerOneSieve/ActualExponentRecords.json). Those archived receipts are the baseline, not re-asserted as new proofs. Applications needing a pristine zero-trust full-archive replay should first run their original verifiers.

## Theorem, counting, and limitations

Assume an *odd perfect* `N≤10^2400`, `p^e || N`, and that every prime preceding `p` in `(19,7,11,31,13,3,5,17)` is absent from `N`. No such `N` occurs in the pairs listed by the verified output `new`. These are complete actual-exponent exclusions, **not** just failures for a single Euler prime or source. `closed` lists newly completed original representative shards; its final field lists **all baseline-open actual exponents** within that shard. The two counts are not interchangeable. The verifier directly enumerates every legal `e` covered by the shard (including the exact-shard convention) and checks size, predecessor prohibitions, earlier receipts or new certificates. Separate proofs can overlap; sum other research batches only after set union. No conclusion is claimed for uncovered exponents.

## Exact inequalities and case splits

Let `B=10^2400` and `A=σ(p^e)`. In these records `e` is even, so `A` is odd and divides `N`. For distinct checked odd primes `r|A` the verifier recomputes `c_r=v_r(A)`. Except for the unique Euler prime `q≡1 mod 4`, all exponents in `N` are even. If `c_r` is odd and `r≠q`, the factor `r^(c_r+1)` is compulsory. Explicitly enumerate the single eligible Euler exception; do not feed a maximum-discount *numerical* bound into an LCM as if it divided `N`.

1. **Chain / parity.** Fix the entire power `R^f || N` at a mandatory prime `R`. Enumerate `f` from `v_R(A)` until `p^e R^f>B`. Odd `f` must be `1 mod 4` and puts `R` in the Euler slot. `Z=odd(σ(R^f))` divides `N`; let `b=v_p(Z)≤e`. Any forbidden prime in `Z`, or an LCM of compulsory sizes exceeding `B`, prunes the branch. Independently check the Euler-slot choices when constructing that LCM. If `R` is Euler, all other powers together must supply the remaining `e-b` units of p-valuation.
2. **Fast / order.** The archived Teichmüller inequality bounds the product of non-Euler prime powers supplying total valuation `j` below by `p^(κj)/U_e`, with `κ=4` at 11 and `κ=2` otherwise. For each compulsory `r^c`, multiply by any certified surplus above one: the minimum of `r^f/p^(κ v_p(σ(r^f)))` for eligible even `f≥c`. If `r=q`, remove its **entire** surplus. The `Order` refinement removes `f` whose divisor sum has a forbidden factor, prices the minimum over surviving `f` and supplies additional compulsory parity/size powers. Its tail uses `v_p(σ(r^f))≤t+log_p(f+1)`; thereafter `r^f/(p^(κt)(f+1)^κ)` is monotone once the displayed integer ratio test passes. Root-size and valuation bounds are separate necessary inequalities, not assumed independent products.
3. **Euler branch.** Euler exponent `a≥5` has the archived price `q^a≥p^(5s)/D_e≥p^(κs)/D_e`, `s=v_p(σ(q^a))`. For `a=1`, enumerate `0≤s≤e` and split into the witnessed `q` (then `v_q(A)=1`), unwitnessed `q|A`, and `q∤A`. When `s>0`, `q≡2p^s−1 mod 4p^s`; for every component `x` divisible by `q`, its complementary integer is `−x mod p^s`. Short progressions can be exhausted, long ones stay open. The `Emit` fallback uses the archived Gemini internal/external emitter proof at only the values not already excluded; no probabilistic assumption is added.
4. **Hybrid and multiple anchors.** Fix distinct mandatory primes at their actual powers `R_i^f_i || N`; enumerate each legal exponent up to the current compulsory size limit. The LCM of `p^e`, `A`, these powers and their odd divisor sums divides `N`. Recompute every remaining compulsory valuation from this LCM, not from `A` alone. Distinct fixed prime powers contribute **additively** `Σ_i v_p(σ(R_i^f_i))` to the total exactly `e`. Remove the fixed primes from the surplus list and cap every remaining branch at the residual budget. If any fixed exponent is odd there is no other Euler prime. For a free Euler exponent one, an unknown `q` inside the LCM must divide one of the explicitly enumerated stripped cyclotomic blocks of the root or the fixed powers (unless already handled as witnessed). If `q` is outside, it multiplies the entire compulsory size. The bounded search never assumes an unsplit cofactor is prime. The `Pair` rule accepts lists of two or more anchors by the same induction on the number of unassigned mandatory primes; the ordering changes speed only.

## Primality independent of PARI

All witnesses `r<2^64` use deterministic Miller–Rabin at the seven standard bases; larger witnesses require a bound-to-`r` ECPP chain in the compressed file. Each node `[n,t,s,a,[x,y]]` has prime child `q=(n+1−t)/s>(n^(1/4)+1)^2`. Derive `b=y²−x³−ax mod n`, prove the discriminant a unit, and verify `S=sP` is finite at every prime divisor of `n` and `qS=O`. The projective arithmetic checks the product of intermediate nonzero denominators is a unit; mixed reductions are rejected. The integer bound on `q` and Hasse's inequality contradict every prime divisor `ℓ≤√n`. Downward induction proves `n` prime. A truncated or altered ECPP proof does not become a PRP acceptance. PARI's separate `primecertisvalid` backend provides an independent replay. See the [PARI arithmetic reference](https://pari.math.u-bordeaux.fr/dochtml/html-stable/Arithmetic_functions.html#primecert) for the encoding.
