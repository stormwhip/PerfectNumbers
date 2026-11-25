# Conditional proof packet manifest

These packets record conditional results. Complete-exponent counts come from the registered jobs in the Nov25 ledger.

## Portable source and tests

- [README.md](<README.md>) and this manifest.
- [Compose.py](<Compose.py>), [Replay.py](<Replay.py>), [IndependentForest.py](<IndependentForest.py>), [Terminal.py](<Terminal.py>), [IndependentTerminal.py](<IndependentTerminal.py>), [SupportRules.py](<SupportRules.py>), [Weighted.py](<Weighted.py>), [Tests.py](<Tests.py>).
- Replay uses the checkout's [ForestReplay.py](<../../NightLowRoute/Release/ForestReplay.py>) for shared exact helpers, [PrimeCheck.py](<../../RootFiveNext/PrimeCheck.py>) for primality witnesses, and [RoadblockDual.py](<../../Session20261122/Python/RoadblockDual.py>) for atanh log intervals; these existing files were not edited.
- Optional reproducibility tools are [Scout.py](<Scout.py>), [TerminalScout.py](<TerminalScout.py>), and [WScout.py](<WScout.py>). They are not needed by replay and read local histories/caches only as untrusted discovery hints. Do not stage any local `ecpp/` cache directory, bytecode, historical cache, or logs.

## Portable data

Stage the 13 positive-support forest/direct packets specifically linked from the [README](<README.md>), plus optionally the four terminal calibration packets listed there and the one weighted calibration. All 18 compressed files together use 3,709,797 bytes. Each is self-contained (compressed JSON with just its proof labels and required ECPP chains). No large shared data cache is required.

## Reproducible tests

From the checkout root, in PowerShell:

```powershell
python -I -S -B Research/Nov25/Compose/SupportRules.py 10 54 76
python -I -S -B Research/Nov25/Compose/Tests.py
$f = Get-ChildItem Research/Nov25/Compose/Branches -File -Filter 'F*.gz' | Select-Object -ExpandProperty FullName
python -I -S -B Research/Nov25/Compose/Replay.py --conditional $f
python -I -S -B Research/Nov25/Compose/IndependentForest.py $f
$t = Get-ChildItem Research/Nov25/Compose/Branches -File -Filter 'T*.gz' | Select-Object -ExpandProperty FullName
python -I -S -B Research/Nov25/Compose/Replay.py --conditional $t
python -I -S -B Research/Nov25/Compose/IndependentTerminal.py $t
```

The optional calibration packet with a `W` prefix replays with the primary `Replay.py --conditional` CLI only.
