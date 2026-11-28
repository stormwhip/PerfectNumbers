# Large exact Euler-window arithmetic: (13,612), s=535

`(13,612),s=535` and `(13,618),s=532` can be split by the same rigorous signed-tail and primitive order lemmas as [ThinGeneral](ThinGeneral.md). The larger signed progressions require accelerating the exact modular comparison. [ModBatch.cpp](ModBatch.cpp) computes only `2^(q−1) mod q` and `3^(q−1) mod q` via GMP exact integer modular exponentiation. It reports a failing Fermat base (2 or 3), or 0 when both equal one. It does not call probabilistic primality logic. [ThinNative.py](ThinNative.py) rebuilds starting and ending residues, tiny divisor sieve and finite exact membership in Python, invokes the executable on batches in one-to-one input order, checks output frame sizes and values, independently verifies both modular powers on every retained candidate, and exhausts all primitive q-order possibilities using the verified `r<q` test.

For `(13,612),s=535` the two exact shapes `(h,c)=(8,3),(10,5)` share exclusive signed upper multiplier 31,261,892. Their first multipliers are 25 and 43, and their complete raw lengths are 1,736,771 and 1,420,994. A separate FLINT-powered exact modular replay (the optional `--fast-search` mode of [ThinGeneral.py](ThinGeneral.py), not any probable-prime function) completed with 201,919 and 134,298 deterministic Fermat tests, and 2,550/1,653 retained candidates. The exact full subgroup checks gave zero possible emitters in both cases. This result is not in [the three-profile sealed packet](CertificateThinGeneral.json). The GCC/GMP WSL cold run exited 0 in 2680.05 s; both shape counts matched, and no possible emitter remained. This is a separate implementation of the finite sieve and modular arithmetic, not a re-proof of the upstream shape identities. Combined with the previous top windows, this yields `v_13(q+1)≤534` at `(13,612)`, still only a conditional necessary bound.

From a Linux/WSL shell (or equivalent build environment with GMP):

```
D=Research/AstraFinalAfternoon2400/ElevenThirteen
mkdir -p "$D/.discovery-deps"
g++ -O3 -Wall -Wextra "$D/ModBatch.cpp" -lgmp -o "$D/.discovery-deps/modbatch"
python3 -I -S -B "$D/ThinNative.py" 612 535
```

Native accelerated runs are independent of all earlier proof data and downloaded discovery binaries. The proof method is mathematical necessary conditions, not the claim that any still open endpoint, full key or shard has actually been closed. Only completed runs count; partial native jobs have no credit.
