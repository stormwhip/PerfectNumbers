#!/usr/bin/env bash
# 2400 odd-perfect-number search, reproducible WSL2 preparation & manual run.
# No third-party paid API is accessed. The long job only starts with "run".
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$ROOT/Build"
OUT="${OPN_OUTPUT_DIR:-$ROOT/Run2400Results}"
REPO="stormwhip/PerfectNumbers"
ROOT_ORDER="${OPN_ROOT_ORDER:-19,7,11,31,13,3,5,17}"
TASK="${1:-help}"
mkdir -p "$BUILD"
cd "$ROOT"
PYTHON="$ROOT/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then PYTHON=python3; fi

case "$TASK" in
  selftest)
    "$PYTHON" Sources/Python/CertificateTests.py
    "$PYTHON" Sources/Python/Prime61FactorChecks.py
    "$PYTHON" Sources/Python/Run2400SchedulerTests.py
    ;;
  prepare)
    command -v g++ >/dev/null
    command -v gh >/dev/null
    command -v sha256sum >/dev/null
    command -v python3 >/dev/null
    if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
      python3 -m venv "$ROOT/.venv"
    fi
    PYTHON="$ROOT/.venv/bin/python"
    "$PYTHON" -m pip install -r Requirements.txt
    g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofTreeV21.cpp -lgmpxx -lgmp -o "$BUILD/ProofTreeV21"
    g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofCoreTestsV21.cpp -lgmpxx -lgmp -o "$BUILD/ProofCoreTestsV21"
    "$BUILD/ProofCoreTestsV21"
    g++ -std=c++17 -O2 Sources/Cpp/BuildIndex.cpp -lz -o "$BUILD/BuildIndex"
    g++ -std=c++17 -O2 Sources/Cpp/PrimeCutoffCert.cpp -lgmpxx -lgmp -o "$BUILD/PrimeCutoffCert"
    (
      cd "$BUILD"
      if [[ ! -f checkfacts.txt.gz ]]; then
        gh release download data-v1 --repo "$REPO" --pattern checkfacts.txt.gz ||           curl --fail --location --retry 2 --max-time 300             --output checkfacts.txt.gz 'https://www.lirmm.fr/~ochem/opn/checkfacts.txt.gz'
      fi
      echo 'ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119  checkfacts.txt.gz' | sha256sum --check
      if [[ ! -f facts.dat || ! -f facts.idx ]] ||
         [[ "$(stat -c %s facts.dat)" != 745826778 ]] ||
         [[ "$(stat -c %s facts.idx)" != 1322332128 ]]; then
        ./BuildIndex checkfacts.txt.gz
      fi
      test "$(stat -c %s facts.dat)" = 745826778
      test "$(stat -c %s facts.idx)" = 1322332128
      if [[ ! -f PrimeCutoffProduct.bin ]]; then
        ./PrimeCutoffCert 100000000 | tee PrimeCutoffBuild.log
      fi
      echo '70ba114b47e7539480c418094606b0f39b2bc230337212426872d7f7adb400ec  PrimeCutoffProduct.bin' | sha256sum --check
    )
    if [[ ! -f "$BUILD/PrefixDualBounds.csv" ]] ||
       [[ "$(($(wc -l < "$BUILD/PrefixDualBounds.csv") - 1))" != 256 ]] ||
       [[ ! -s "$BUILD/PrefixDualVariableGains.csv" ]] ||
       [[ ! -s "$BUILD/PrefixDualForcedGains.csv" ]]; then
      OPENBLAS_NUM_THREADS=1 "$PYTHON" -u Sources/Python/PrefixDualCertificates.py "$BUILD/PrefixDualBounds.csv" |
        tee "$BUILD/PrefixCertificateLog.txt"
    fi
    test "$(($(wc -l < "$BUILD/PrefixDualBounds.csv") - 1))" = 256
    "$PYTHON" Sources/Python/Run2400Scheduler.py prepare --base "$BUILD" --out "$OUT" --root-order "$ROOT_ORDER"
    echo "PREPARED: $OUT"
    ;;
  run)
    "$PYTHON" Sources/Python/Run2400Scheduler.py run --base "$BUILD" --out "$OUT"       --root-order "$ROOT_ORDER"       --jobs "${OPN_JOBS:-16}" --threads-per-job "${OPN_THREADS_PER_JOB:-2}"       --max-hours "${OPN_MAX_HOURS:-72}"
    ;;
  status)
    "$PYTHON" Sources/Python/Run2400Scheduler.py status --base "$BUILD" --out "$OUT" --root-order "$ROOT_ORDER"
    ;;
  verify)
    "$PYTHON" Sources/Python/Run2400Scheduler.py verify --base "$BUILD" --out "$OUT" --root-order "$ROOT_ORDER"
    ;;
  *)
    echo "Usage: bash Scripts/Run72hWSL.sh {selftest|prepare|run|status|verify}"
    echo "The 72-hour computation starts ONLY with 'run'."
    echo "Environment: OPN_OUTPUT_DIR, OPN_ROOT_ORDER, OPN_JOBS (default16), OPN_THREADS_PER_JOB (default2), OPN_MAX_HOURS (default72)."
    exit 2
    ;;
esac
