# Exact One-Node Root Certificates for the `10^2400` Partition

**Research date:** 2026-11-22. **Status:** exact mathematical rules and locally repeated integer experiments; new GitHub Python/CI regression awaits actual execution. The global 10^2400 theorem remains `INCOMPLETE_FRONTIER`.

Original root set `S={3,5,7,11,13,17,19,31}`, fixed production root order `(19,7,11,31,13,3,5,17)`. The existing terminal coprime-class certificate uses this same set.

## 1. The divisibility lemma

Let `p^e || N` in an odd perfect number `N`, with a canonical root branch `(p,d,exact)`. For an exact branch, `e=d`. For a non-exact branch, `e>=d` and `d+1 | e+1`. In both cases,

```text
sigma(p^d) | sigma(p^e) | sigma(N) = 2N.
```

Indeed, if `e+1=k(d+1)`, then the quotient of the two geometric sums equals `1+p^(d+1)+...+p^((k-1)(d+1))`.

Set `A(p,d)=odd(sigma(p^d))=sigma(p^d)/2^v2(sigma(p^d))`. Since `N` is odd, `A(p,d)|N`. Furthermore, `gcd(p,sigma(p^d))=1`, so `gcd(p^d,A(p,d))=1`. Together with `p^d|N`,

```text
p^d * A(p,d) | N.
```

Thus the following two one-node closure reasons are rigorous:

* `FORBIDDEN_FACTOR`: an earlier root `q` is excluded from the present root class and divides `sigma(p^d)`. As `q` is odd, `q|N`, contradiction.
* `SIGMA_DIVISOR_SIZE`: `p^d * A(p,d)>10^2400`, contradicting `N<=10^2400`.

Both reasons require only exact integer arithmetic. The second reason does **not** require factoring the potentially large `sigma(p^d)`. It is substantially stronger than using only `p^d>10^2400`.

To detect the forbidden factor `q != p`, use `p % q == 1` to test `(d+1) % q == 0`; otherwise test `pow(p,d+1,q)==1`. Every selected modular witness is then verified with an independently computed exact geometric sum.

## 2. Exhaustive canonical top-level census

Locally, a separate pure-Python integer implementation enumerated the canonical 3,072 exponent options. The same integer predicates are implemented in `DirectRootClosures2400.py`, which constructs one-node proof DAGs for `IndependentVerifierV2`. Actual end-to-end GitHub verifier/CI execution is pending.

| Root | `FORBIDDEN_FACTOR` | `SIGMA_DIVISOR_SIZE` | Combined direct closure | Root task count |
| ---: | ---: | ---: | ---: | ---: |
| 19 | 0 | 129 | 129 | 287 |
| 7 | 2 | 189 | 191 | 412 |
| 11 | 1 | 151 | 152 | 341 |
| 31 | 1 | 115 | 116 | 253 |
| 13 | 1 | 145 | 146 | 325 |
| 3 | 5 | 306 | 311 | 676 |
| 5 | 3 | 214 | 217 | 481 |
| 17 | 1 | 133 | 134 | 297 |
| **Total** | **14** | **1,382** | **1,396** | **3,072** |

The two closure groups have no overlap under the priority `FORBIDDEN_FACTOR` then `SIGMA_DIVISOR_SIZE`. The direct integer rules cover **45.44%** of canonical top-level exponent tasks. **1,676 shards remain open** before incorporating any separately verified deeper proof DAGs.

An example forbidden-factor leaf: `sigma(7^2)=57=3*19`. The root-7 partition excludes 19.

An example size leaf: root 19, non-exact exponent representative `d=940`; `19^940 * odd(sigma(19^940))>10^2400`. This rule holds for all represented actual exponents because the representative sigma sum divides each actual sigma sum.

The verifier rejects false claims, including altered source exponents and `SIGMA_DIVISOR_SIZE` at equality. It recomputes the product using integers, and has a sound bit-length precheck only when `p^d` by itself exceeds the bound.

## 3. Root-order DP experiment

Let `S` denote an already scheduled prefix of excluded roots. Set

```text
g(p,S) = number of canonical exponent options d at root p
         for which some q in S divides sigma(p^d).
DP[S union {p}] = max(DP[S union {p}], DP[S] + g(p,S)).
```

This exact subset DP takes `2^8` states. A separate oracle enumerates all `8!=40320` root orders and confirms the optimum:

| Root set | Current forbidden-factor closures | Maximum | One maximizing root order |
| --- | ---: | ---: | --- |
| Original (contains 19) | 14 | 15 | `(19,7,11,13,3,31,5,17)` |
| Replacement (contains 23) | 15 | 18 | `(7,11,23,13,3,31,5,17)` |

This maximizes **only the number of immediate forbidden-factor closures**. The full proof tree, LP certificates and runtime can change with the root order. **The production V21 order remains unchanged**.

## 4. Repository changes and reproduction

* `../Python/DirectRootClosures2400.py`: exact modular and sigma-size rules; emits independent-verifier JSON bundles and rejects tampering.
* `../Python/DirectRootClosuresTests.py`: census, positive/negative proof leaves, strict equality and audit fast path.
* `../Python/RootOrderDirectClosureDP.py`: subset DP plus all 40,320 permutation checks.
* `../Python/AuditDirectRoot2400.py`: full canonical-manifest audit using the archived original terminal certificate; expects 1396 `VERIFIED_CLOSED` and 1676 `UNSTARTED` with no external shard ledgers.
* `../Python/IndependentVerifierV2.py`: independent `SIGMA_DIVISOR_SIZE` LEAF checker.
* `../Python/AuditRunner2400.py`: returns `VERIFIED_CLOSED` only after independent proof-bundle acceptance; never trusts bare `PROVEN` solver output.
* `../../../Sources/Cpp/SigmaPrecheck.hpp`, `../../../Sources/Cpp/SigmaPrecheckTests.cpp` and `../../../Sources/Cpp/ProofTreeV21Frontier.cpp`: restore the missing G2 sigma-precheck header, fix the include, and supply GMP differential tests.
* `../../../.github/workflows/RepositoryIntegrity.yml`: adds the new regressions to its manually invoked workflow.

From repository root:

```bash
python3 -S -O Research/Session20261122/Python/DirectRootClosuresTests.py
python3 -S -O Research/Session20261122/Python/RootOrderDirectClosureDP.py
python3 -S -O Research/Session20261122/Python/AuditDirectRoot2400.py
python3 -S -O Research/Session20261122/Python/DirectRootClosures2400.py --emit-dir Build/DirectRootCertificates
g++ -std=c++17 -O2 Sources/Cpp/SigmaPrecheckTests.cpp -lgmpxx -lgmp -o /tmp/OpnSigmaPrecheckTests
/tmp/OpnSigmaPrecheckTests
```

Local C++ rebuild of the same `SigmaPrecheck.hpp` implementation passed **36,100 GMP exact-integer comparisons**. A new repository CI run is still needed to verify the pushed source artifact and its Python integration end to end.

## 5. Remaining proof gap

The original eight-root complement retains its archived certificate. For the **1,676 non-direct shards**, finish the V21-to-verifier DAG emission, deterministic primality certificates, exact roadblock/state-LP proof rules, residual accounting and full independent audit. Then measure a complete fixed-hardware `T_prep+T_search+T_verify<=72h` run. Until all shards are independently closed, status remains `INCOMPLETE_FRONTIER`.
