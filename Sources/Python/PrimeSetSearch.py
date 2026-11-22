"""Find smaller certified forbidden-prime sets for OPN lower-bound searches.

A numerical LP estimate is used only to screen candidate sets. Any accepted
candidate is confirmed by IntervalCertificate.solve_and_certify(certify=True).
This does not prove the associated prime-containing branches.
"""
import json
import math
import time
from functools import lru_cache
from IntervalCertificate import S_2012, solve_and_certify

TARGET = 2300.0
PRIME_SET = frozenset(S_2012)
MAX_SOLVES = 55
calls = 0

@lru_cache(maxsize=None)
def model_bound(primes):
    global calls
    if calls >= MAX_SOLVES:
        raise RuntimeError("LP evaluation budget exhausted")
    calls += 1
    t0 = time.perf_counter()
    approx, _ = solve_and_certify(set(primes), P_max=4000, a_cut=16, certify=False)
    if not math.isfinite(approx):
        raise RuntimeError("Non-finite LP objective")
    print("LP", calls, "size", len(primes), "bound", f"{approx:.6f}",
          "seconds", f"{time.perf_counter()-t0:.2f}", "set", sorted(primes), flush=True)
    return approx

def greedy(initially_removed, label):
    selected = PRIME_SET.difference(initially_removed)
    start = model_bound(frozenset(selected))
    print("\nRUN", label, "INITIAL", sorted(selected), "bound", f"{start:.6f}", flush=True)
    if start <= TARGET:
        return {"label": label, "error": "seed fails bound", "floatBound": start}
    history = []
    while len(selected) > 1:
        options = []
        for p in sorted(selected):
            subset = frozenset(selected - {p})
            val = model_bound(subset)
            if val > TARGET + 0.2:
                options.append((val, p))
        if not options:
            break
        # Preserve as much certified margin as possible for additional removals.
        val, chosen = max(options, key=lambda x: (x[0], -x[1]))
        selected.remove(chosen)
        history.append({"remove": chosen, "floatBound": val})
        print("REMOVE", chosen, "remaining", sorted(selected), "bound", f"{val:.6f}", flush=True)
    fval, certified = solve_and_certify(
        set(selected), P_max=4000, a_cut=16, certify=True
    )
    if not (math.isfinite(certified) and certified > TARGET):
        raise RuntimeError("Final candidate did not certify target bound")
    result = {
        "label": label,
        "retainedPrimes": sorted(selected),
        "removedPrimes": sorted(PRIME_SET - selected),
        "floatLog10Bound": fval,
        "intervalDualLog10Lower": certified,
        "removedSequence": history,
    }
    print("CERTIFIED_FINAL", json.dumps(result), flush=True)
    return result

if __name__ == "__main__":
    t0 = time.perf_counter()
    results = [
        greedy([], "PreserveMaximumMargin"),
        greedy([127], "ForceRemoveExpensiveRoot127"),
    ]
    print("COMPLETE", json.dumps({
        "targetExponent": TARGET,
        "lpEvaluations": calls,
        "durationSeconds": time.perf_counter() - t0,
        "results": results,
    }, indent=2), flush=True)
