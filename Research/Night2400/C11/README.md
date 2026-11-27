# Night2400 C11 — exact first fiber 4 and 24 deep leaves of (19,46), P19_I00013

Cold replay from the repository root, using standard-library Python with assertions enabled:

```text
python -I -S -B Research/Night2400/C11/Verify.py
python -I -S -B Research/Night2400/C11/Verify.py --deep
```

The [proof packet](Fiber4.json.gz) (SHA-256 `5c4d1a6811127d7babfd011e8a811d85a75967861696066bdd28725d3d4b1b70`) closes **only exact first exponent 4** at `q=70169234660105574400577005075855017842743056666917902427141`, the 196-bit certified forced prime under `19^46 || N` for odd perfect `N <= 10**2400`. The first raw split has 14 compatible live exponents, 15 directly impossible exponents, 10 incompatible exponents and a monotone size tail at 40. This certificate does not assume or replay any prior closure, and no other complete first fiber is claimed.

Inside fiber 4, four exact forced-prime splits regenerate every compatible branch and its tail, excluding 54 direct branches and proving 47 forests via two integer recurrences. The remaining two exact paths share the 499-bit second prime at exponent 2 and the 57-bit last prime at exponent 2. For each path every one of the 128 support masks on `(19,7,11,31,13,3,5,17)` containing 19 is verified: 124 masks contradict direct forcing or size/abundancy arithmetic; the other four are excluded by strict rational abundancy, with minimum values above 2.475 and 2.486 respectively. This proof minimizes over the available single Euler placement, rather than assuming all additional primes have even exponent. No factorization of the shared 984-bit cyclotomic block is required.

The [deep supplement](DeepLeaves.json.gz), SHA-256 `ba8eefff35a63aa1dc0c45fb0cd29d565d4f017ed9a2caa200f5930599a5d72b`, excludes exactly the 24 full prime-power assignments printed by `--deep`: 14 within first fiber 6 (six all-mask support proofs, eight prefix price proofs) and ten within first fiber 10 (all-mask support proofs). The checker validates the forcing and exact admissibility of each step, but does **not** claim any siblings. Relative to the supplied discovery tree, 22 of 36 previously open paths in fiber 6 and 82 of 92 in fiber 10 remain open. Fiber 12 is untouched. The optional [price recurrence](PrefixPrice.py) includes the exact prefix LCM budget.

Discovery used authorized local data and PARI for primality witnesses only. All required certificates are in the packet; no generated cache, network, or other Night2400 candidate is used by the verifier.
