# PascalCase release of the full exact (19,280) proof

[Mathematical proof](Full280.md) · [Full replay](Full280.py) · [Release content manifest](Manifest280.txt) · [Invertible original-blob map](Equivalence.json) · [Equivalence checker](CheckEquivalence.py) · [Independent original arithmetic audit](../../../FinalNight2400/AuditNext/Full280.md).

The source candidate was produced **on baseline 1447d41b, not contained in that baseline commit**. Frozen original 161-file manifest SHA-256 b7d6464b6da32f4f01da9f35a2c9a7f4527a90ae69b51127ee4970b3494362ec. Individual originals are identified by both SHA-256 and Git-compatible SHA-1 blob IDs, without asserting an original working-tree commit. The independent full original proof replay was accepted after 4569.877 s. The translated release content manifest is 0a97a39b24f0d3c4545ac39b43b695d5500a79b9addd96e5fc3f9227e5b22309.

All 161 released proof files have PascalCase stems (66 renamed); 153 have byte-identical payloads including every certificate and forest, with no recompression. Four source programs have only filename-template and/or parent-path literal changes to resolve the extra folder depth, and four Markdown notes have only file/command reference changes. The checker reconstructs the original bytes in memory, verifies both original hash identities and the original manifest hash, checks the allowed edits, checks the new manifest, and validates all local proof-note links. The historical audit link above refers to the original acceptance, not to a new cold full replay of this renamed package.

From the repository root:

~~~text
python -I -S -B Research/FinalNight2400/Ten276/Release280/CheckEquivalence.py
python -I -S -B Research/FinalNight2400/Ten276/Release280/Full280.py
~~~

The first command does not require an original candidate checkout. In a workspace retaining the original 161 files, append `--with-original` to require direct byte comparison; this mode passed on all 161. Smoke tests using the new location exercised compact, explicit-tree and hybrid filename schemas and their relative baseline imports. The 161-file manifest excludes these explanatory release notes, the reversible mapping, the equivalence checker, and the manifest itself. This release changes no mathematical claim.
