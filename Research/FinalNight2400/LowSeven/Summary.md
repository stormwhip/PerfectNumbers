# Low-seven conditional first-valuation certificates

**No whole key or shard is closed by these three packets.** For odd perfect N≤10^2400 with 19 absent and exact indicated valuation at 7, the listed files rule out specific first-pivot exponents. Each packet was replayed using the older stock VerifyFibers.py, not discovery code; the supplementary no-project-import TreeAudit.py independently enumerates the whole domain from geometric sums, checks the first forced prime has incoming valuation one, and prints the exact unproved complement. These are exact first values, not divisibility lifts, and the packets, not a count, specify the excluded sets.

| Key | First pivot | Excluded / live | First strict raw tail | ECPP | SHA-256 of sealed forest packet |
|---|---:|---:|---:|---:|---|
| (7,16) | 2767631689 | 44/91 | 253 | 117 | Seven16.json.gz: 4af54b1088f307019fbfe2a5b74e7faa5e6834488ae4445fee864fd56b917145 |
| (7,18) | 4534166740403 | 30/44 | 189 | 525 | Low18.json.gz: b68b20069c0c73143109afefcd4e54e999fbe24933d26e5f0963587cfdaeb7e0 |
| (7,48) | 6106505825833677713 | 27/31 | 125 | 1437 | Seven48.json.gz: 8112caf03da5792950ba2d32beded8502c8a2f5e21ebb45d105be66b5e8f9c7e |

At (7,48) the remaining exact firsts are [2,4,8,10]. At (7,18) the remaining direct-forest firsts are [2,4,6,8,12,22,28,30,36,40,42,46,58,66]. The optional experimental price/vertex addendum is separate; it is not counted here. In particular, for root-7 exponent 48 the corresponding shard contains other exact pairs even if this key were closed; do not treat it as a standalone singleton.

~~~powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/FinalNight2400/LowSeven/Seven16.json.gz Research/FinalNight2400/LowSeven/Low18.json.gz Research/FinalNight2400/LowSeven/Seven48.json.gz
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/LowSeven/TreeAudit.py Research/FinalNight2400/LowSeven/Seven16.json.gz Research/FinalNight2400/LowSeven/Low18.json.gz Research/FinalNight2400/LowSeven/Seven48.json.gz
~~~
