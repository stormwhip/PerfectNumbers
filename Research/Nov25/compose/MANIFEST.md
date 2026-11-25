# Review / staging manifest

**No git reference, index, or push changes were made by this work.** Stage only the named portable subset if accepting the exploratory deliverable. Do not register any of these packets as complete exponents in the Nov25 ledger.

## Portable source and tests

- [README.md](<Research/Nov25/compose/README.md>) and this manifest.
- [Compose.py](<Research/Nov25/compose/Compose.py>), [Replay.py](<Research/Nov25/compose/Replay.py>), [IndependentForest.py](<Research/Nov25/compose/IndependentForest.py>), [Terminal.py](<Research/Nov25/compose/Terminal.py>), [IndependentTerminal.py](<Research/Nov25/compose/IndependentTerminal.py>), [SupportRules.py](<Research/Nov25/compose/SupportRules.py>), [Weighted.py](<Research/Nov25/compose/Weighted.py>), [Tests.py](<Research/Nov25/compose/Tests.py>).
- Replay uses the checkout's [ForestReplay.py](<Research/NightLowRoute/Release/ForestReplay.py>) for shared exact helpers, [PrimeCheck.py](<Research/RootFiveNext/PrimeCheck.py>) for primality witnesses, and [RoadblockDual.py](<Research/Session20261122/Python/RoadblockDual.py>) for atanh log intervals; these existing files were not edited.
- Optional reproducibility tools are [Scout.py](<Research/Nov25/compose/Scout.py>), [TerminalScout.py](<Research/Nov25/compose/TerminalScout.py>), and [WScout.py](<Research/Nov25/compose/WScout.py>). They are not needed by replay and read local histories/caches only as untrusted discovery hints. Do not stage any local `ecpp/` cache directory, bytecode, historical cache, or logs.

## Portable data

Stage the 13 positive-support forest/direct packets specifically linked from the [README](<Research/Nov25/compose/README.md>), plus optionally the four terminal calibration packets listed there and the one weighted calibration. All 18 compressed files together use 3,709,797 bytes. Each is self-contained (compressed JSON with just its proof labels and required ECPP chains). No large shared data cache is required.

## Reproducible tests

From the checkout root, in PowerShell:

```powershell
python -I -S -B Research/Nov25/compose/SupportRules.py 10 54 76
python -I -S -B Research/Nov25/compose/Tests.py
$f = Get-ChildItem Research/Nov25/compose/branches -File -Filter 'F*.gz' | Select-Object -ExpandProperty FullName
python -I -S -B Research/Nov25/compose/Replay.py --conditional $f
python -I -S -B Research/Nov25/compose/IndependentForest.py $f
$t = Get-ChildItem Research/Nov25/compose/branches -File -Filter 'T*.gz' | Select-Object -ExpandProperty FullName
python -I -S -B Research/Nov25/compose/Replay.py --conditional $t
python -I -S -B Research/Nov25/compose/IndependentTerminal.py $t
```

The optional calibration packet with a `W` prefix replays with the primary `Replay.py --conditional` CLI only.
