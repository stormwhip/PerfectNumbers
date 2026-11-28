# Frozen baseline replay — 495c59f55456a70994ce7848487e0c4e262c1984

Executed in PowerShell from `E:\PerfectNumbers`, with assertions enabled. These are a frontier/accounting check and a targeted replay of the already-accepted Gemini November 28 overlay; neither is a cold replay of the mathematics behind all historical shards.

```powershell
python -I -S -B Research/FinalNight2400/AuditCoverage.py
python -I -S -B Research/FinalNight2400/ReportChecks.py
python -I -S -B Research/FinalNight2400/Project.py
```

All three exited 0, respectively:

```text
PASS 3072 canonical root-exponent representatives; old/new exact incidences 82 57
PASS independent exact set difference, per-key singleton and proof links, Chinese per-root table: 25 new full keys; counts (3029, 43, 53, 35)
{'ClosedShards': 3029, 'OpenShards': 43, 'DistinctKeys': 53, 'SingletonShards': 35}
```

```powershell
python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/November28/ReviewVerify.py
```

First attempt exited 1 at the unchanged line-20 SHA-256 check: `ValueError: submitted verifier hash mismatch`. The worktree had CRLF checkouts. Exact repair for the replay, **not touching the tracked originals or weakening hashes**:

```powershell
$dst='Research/AstraFinalAfternoon2400/Audit/FrozenGemini'
New-Item -ItemType Directory -Force $dst | Out-Null
python -I -S -B -c "from pathlib import Path; from subprocess import check_output; from hashlib import sha256; dst=Path('Research/AstraFinalAfternoon2400/Audit/FrozenGemini'); src=Path('Research/GeminiFrontier/November28'); names=('ReviewVerify.py','Submitted.py','Certificates.json'); [(print(n, sha256(data).hexdigest(), sha256((src/n).read_bytes()).hexdigest(), data==(src/n).read_bytes().replace(bytes([13,10]),bytes([10]))), (dst/n).write_bytes(data)) for n in names for data in [check_output(['git','show','495c59f55456a70994ce7848487e0c4e262c1984:'+str((src/n).as_posix())])]]"
if ($LASTEXITCODE) { exit $LASTEXITCODE }
python -I -S -B -X int_max_str_digits=0 "$dst/ReviewVerify.py"
```

Second replay exited 0. Output (blob hash, worktree hash, equality after CRLF→LF, then actual verifier output):

```text
ReviewVerify.py 86482435ee15ba6a4fe1ecc34f5310e223fc1e84274f1bdb1c53871b65154eed e2a3edb961389390c8556701c7d14d6aa862436cb1e02dc2a0ffd151869a1741 True
Submitted.py 8ba69b99be28e0ef11968dac1afc24e5e187b432b4298c0c035dba09be7daa99 5ff36962fd7cdd042f7a9bb67317389ac1ec7f1c274c6e612dba962906e890f1 True
Certificates.json ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8 c6b5704a567a1a268fb036b2adaf9adc5cb105e18476c286ecf464e739a15ae8 True
[ACCEPTED] H_h85 CLOSED (exc_bases=1, log10_lb=2401.83 > 2400)
[ACCEPTED] H_h108 CLOSED (windows=108, inner_div_checked=38, exc_bases=1)
[ACCEPTED] H_h102 CLOSED (windows=102, inner_div_checked=50, exc_bases=1)
[ACCEPTED] G_h66 CLOSED (windows=66, QR outer-Euler for i>=1, exc_bases=1)
[ACCEPTED] B_f1_g58 complete joint order audit: 3 deficit bases, log10 lower bound 2423.528463
[ACCEPTED] B_f1_g16_j42 complete joint order audit: 3 deficit bases, log10 lower bound 2493.516199
[ACCEPTED] B_f1_g16_j40 complete joint order audit: 3 deficit bases, log10 lower bound 2420.560096
[ACCEPTED] E_t1_split_1109 PARTIAL_CLOSED (136/138 closed, tail=555, OPEN=[2, 4], U19_exc=4, U1109=1)
```

The three temporary extracted files were removed from the audit tree after replay. See the historical [validation boundary](../../FinalNight2400/Validation.md) and the [corrected Gemini mathematical proof](../../GeminiFrontier/November28/Review.md); the command output does not replace the all-orders coverage proof.
