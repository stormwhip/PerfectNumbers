# FULL canonical key (31,16), singleton P31_I00005 — cold pass

The complete isolated command returned exit 0 in 269.940 s (job start/end UTC milliseconds 1795793842498, 1795794112438). No native binaries, network, or third-party Python packages are required. Historical packet plus the two new firsts exactly covers all 16 first exponents.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/ThirtyOne/Full31x16.py
~~~

~~~text
PASS 31^16 exact t^16. Euler-on-vertex restricted via t-price; absent via ordinary forest. 1855 vertices 540 ECPP, floor 2402 price floor 4703
Final 37 domain 112 [109, 1, 2] left {}
FULL checked canonical exact 31^16: 14 historical + firsts 16 and 22. P31_I00005.
~~~

The standalone 47-layer check also passed (127.284 s wall): 139/140 excluded, residual h=2 and j=16,17,18,19,20. The last 112 live h' for prime 37 (range 6 to 420, not every even) split 109 ordinary forest, one pure price/window cut, two reserved-Euler forests. No residual. The 140 live h for 47 range from 2 to 396.

Integration inputs in this directory: **First16.md, First22.md, Verify16.py, AtomPrice.py, Forest16.json, Cert16.json, Window.py, EulerForest.py, Verify22.py, Packet22.json, Cert22.json, VerifyDeep.py, DeepPacket.json, CertDeep.json, DeepExtras.json, Full31x16.py**. All historical imports already tracked. For SHA-256s run AuditInventory.py. The new geometry packets hash as follows: Forest16 b334ebb392272e84f5bd5ab78ade7534fa37f3dfe7219b54a088b1f5584bade1, Packet22 65016c908e8c2bde220efc4ec60fbc72821e280d084adcc4ca4e8e04fdea65fe, DeepPacket d6bf0eb8c376add8d1ff2c6d71dec92bd12eded724f9a8ca8359de8e209310cf. Cert16 9c45f8a41a3a387d6a1b7099c78caa93670a0b9fa37b97f688725bbf05ecd3e5; Cert22 520c6e4ee17bdeb558c6ee219a344d54e32d5697e9704bdb84d51795668cfd45; CertDeep d3d3ac3358dbe0129a0b08db5281319748b688469819b3c94ffc6687a0a88b40; DeepExtras 7714e1fec9e68f9ad1db5d13697ed2f5cb231e0b2061b4e64e02a02dbeec267f.

This establishes one canonical exact exponent under N≤10^2400, not a statement for other exponents, primes or projections. Separate auxiliary 19,618 factorizations are discovery support for the corresponding owner, not part of this proof.
