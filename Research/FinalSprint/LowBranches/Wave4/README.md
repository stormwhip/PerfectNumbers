# Final incremental wave: three more root-3^6 pivot exclusions

The canonical hypotheses are odd perfect N<=10^2400, with all of 19,7,11,31,13 absent and v3(N)=6. Then v1093(N) cannot be 162, 198, or 228. All forests are checked against two exact integer implementations. No paired leaf is used in this wave. The complete frozen packet is 425,889 bytes, SHA256 `aa9afe7863e8ba7b38006645914c683f6d8df732058c78a408af2086ec77dc59`.

```
python -I -S -B Wave4/Verify.py PATH_TO_REPO Wave4/Branches.json.gz
PASS 6 1093 162 [20, 4, 2400]
PASS 6 1093 198 [119, 12, 2400]
PASS 6 1093 228 [69, 7, 2401]
ECPP 597 sha256 aa9afe7863e8ba7b38006645914c683f6d8df732058c78a408af2086ec77dc59
```

The tuples are forest leaves, exhaustive internal splits, minimum floor of log10 lower bound. The strict size comparison is integer, including when the displayed floor is 2400. `AllDelta.py` binds this packet, three earlier incremental wave packets, and the historical LowBranches packet; it verifies that all 23 new primary fibers are disjoint. Final counts: 159/182 excluded at v3(N)=6, 96/100 excluded at v3(N)=12. Complete actuals/shards closed = 0.
