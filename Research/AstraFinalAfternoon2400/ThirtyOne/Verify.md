# Replay checklist

Use Python 3.11 or later with assertions, no external dependencies, from the repo root. Do not use `-O`. The object being replayed is an immutable compressed packet, never the untrusted discovery logs. The fixed code dependencies are [Replay.py](Replay.py), [ForestVerify.py](ForestVerify.py), and for the complete mixed key [GenericPrice.py](GenericPrice.py), [Joint6.py](Joint6.py), [PriceLeaf6.py](PriceLeaf6.py), plus the frozen forest recursion and primality module referenced by [Proof.md](Proof.md).

```powershell
$d='Research/AstraFinalAfternoon2400/ThirtyOne'
python -I -S -B -X int_max_str_digits=0 "$d/ForestVerify.py" --require-complete "$d/Certificate6CompleteJoined.json.gz"
python -I -S -B -X int_max_str_digits=0 "$d/ForestVerify.py" --details "$d/Certificate268Union73.json.gz"
python -I -S -B -X int_max_str_digits=0 "$d/ForestVerify.py" "$d/Certificate2More.json.gz"
python -I -S -B -X int_max_str_digits=0 "$d/HighLift.py"
python -I -S -B -X int_max_str_digits=0 "$d/NegativeTests.py"
python -I -S -B -X int_max_str_digits=0 "$d/TestsJoint6.py"
python -I -S -B -X int_max_str_digits=0 "$d/AnonymousEuler.py"
python -I -S -B -X int_max_str_digits=0 "$d/EulerCuts.py"
python -I -S -B -X int_max_str_digits=0 "$d/RoughBounds.py"
```

| Sealed packet | SHA-256 | Exact scope |
|---|---|---|
| [Certificate6CompleteJoined.json.gz](Certificate6CompleteJoined.json.gz) | `450a80c01c74b098fb858f340c17f4b3be674da4d6cbf8894080e0b5099f3130` | `(31,6)` 53/53; `open=[]` compulsory. |
| [Certificate268Union73.json.gz](Certificate268Union73.json.gz) | `015161d6cedeaa45fa5a566dc7fc690f13c3f683e934b0ad8b579ea93b663a75` | `(31,268)` 73/76, open 102,156,210. Do not pass `--require-complete`. |
| [Certificate2More.json.gz](Certificate2More.json.gz) | `e6955d8768ac33b917343eab41e0540bf8b4b73e53935b38f249fbb673cdfc9e` | `(31,2)` 117/143, 26 open. |

For the additional fourteen root-two firsts (131/143 total), see [RootTwoFollowup.md](RootTwoFollowup.md); the old 117-first packet remains immutable. The complete root6 certificate passed independent replay and both Windows CPython 3.11.9 / WSL CPython 3.14.4. Its proof is exact only: no other root exponent is thereby excluded. Historical reported but unaccepted 31^268 `75/76` is not needed or relied on. Both high exact roots remain open; only the stated subordinate conditions in [HighRoots.md](HighRoots.md) are recorded.
