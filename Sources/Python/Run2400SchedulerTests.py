"""Synthetic integration test of 2400 restartable scheduler without factor data."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).resolve().with_name("Run2400Scheduler.py")
FILES = (
    "facts.idx", "facts.dat", "PrimeCutoffProduct.bin",
    "PrefixDualBounds.csv", "PrefixDualVariableGains.csv",
    "PrefixDualForcedGains.csv",
)

def run(cmd, expected=0):
    p = subprocess.run([sys.executable, str(SCRIPT)] + cmd,
                       text=True, capture_output=True)
    assert p.returncode == expected, (cmd, p.returncode, p.stdout, p.stderr)
    return p.stdout

with tempfile.TemporaryDirectory(prefix="opn-scheduler-test-") as tmp:
    base = Path(tmp) / "Build"
    base.mkdir()
    for filename in FILES:
        (base / filename).write_bytes(b"test-data")
    app = base / "ProofTreeV21"
    app.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        "p=sys.argv[2]\n"
        "if sys.argv[3]=='list':\n"
        " print(f'SHARD_COUNT root={p} count=1')\n"
        " print(f'SHARD root={p} index=0 exponent=2 exact=1')\n"
        "else:\n"
        " print(f'Forbid p={p} branch=0/1 -> PROVEN | branches=1 | failed_rb=0')\n",
        encoding="utf-8",
    )
    app.chmod(0o755)
    out = base / "Results"
    common = ["--base", str(base), "--out", str(out)]
    assert "MANIFEST_COMPLETE tasks=8" in run(["prepare"] + common)
    assert "ALREADY_PREPARED" in run(["prepare"] + common)
    run(["verify"] + common, expected=1)
    txt = run(["run", "--jobs", "2", "--threads-per-job", "1",
               "--max-hours", "0.05"] + common)
    assert "TREE_SEARCH_COMPLETE_UNAUDITED" in txt, txt
    assert "proven=8 total=8" in run(["status"] + common)
    assert "proven=8 total=8" in run(["verify"] + common)
    # A corrupted result log must invalidate the saved PROVEN flag.
    bad_log = out / "Logs" / "P19_I00000.log"
    bad_log.write_text("FORGED COMPLETION", encoding="utf-8")
    run(["verify"] + common, expected=1)
    assert "TREE_SEARCH_COMPLETE_UNAUDITED" in run(
        ["run", "--jobs", "2", "--threads-per-job", "1",
         "--max-hours", "0.05"] + common
    )
    assert "proven=8 total=8" in run(["verify"] + common)
    manifest = json.loads((out / "Manifest.json").read_text())
    assert len(manifest["tasks"]) == 8
    assert manifest["root_order"] == [19, 7, 11, 31, 13, 3, 5, 17]
    run(["prepare", "--root-order", "3,5,7,11,13,17,31,19"] + common, expected=2)
    run(["verify", "--root-order", "3,5,7,11,13,17,31,19"] + common, expected=2)
    # A modified input invalidates completion and requires a fresh manifest.
    (base / "facts.dat").write_bytes(b"corrupted-test-data")
    run(["verify"] + common, expected=2)
print("Run2400SchedulerTests: OK")
