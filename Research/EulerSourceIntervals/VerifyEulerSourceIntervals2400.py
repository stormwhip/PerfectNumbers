"""Reproduce the exact Euler-source interval experiment for roots 3 and 5."""
import argparse
from heapq import heapify, heapreplace
import json
from math import prod
from pathlib import Path
import sys

RESEARCH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH / "FermatRootValuation"))
from Verify import B, covers, forbids, primes, sigma, tables

ROOTS = (3, 5)
CUTOFF = 100_000


def read_audit(relative_path):
    return json.loads((RESEARCH / relative_path).read_text(encoding="utf-8"))


def open_exponents():
    supplier = read_audit("SupplierBatch/BatchAudit2400.json")
    indicator = read_audit("IndicatorCapacity/Audit2400.json")
    valuation = read_audit("TeichmullerValuation/Audit2400.json")
    gemini = read_audit("TeichmullerValuation/GeminiBatchAudit2400.json")
    excluded = {
        (row["root"], row["exponent"])
        for audit in (supplier, indicator)
        for row in audit["exact_exponents"]
    }
    excluded.update(map(tuple, gemini["verified_exponents"]))
    closed = {shard["id"] for shard in gemini["additions"]}
    open_shards = [shard for shard in valuation["open_manifest"] if shard["id"] not in closed]
    if len(open_shards) != gemini["open"]:
        raise ValueError("Inconsistent merged open shard counts")
    _, actuals = tables()
    return {
        p: sorted({
            e for root, e, status, _ in actuals
            if root == p and status == "OPEN" and (root, e) not in excluded
            and any(shard["root"] == p and covers(e, shard["exponent"], shard["exact"])
                    for shard in open_shards)
        })
        for p in ROOTS
    }


def marginal_costs(p, units, prime_table):
    """Return prefix products of the least possible valuation increments."""
    heap = [(r, r) for r in prime_table if r % p == 1 and r not in forbids(p)]
    heapify(heap)
    costs = [1]
    for _ in range(units):
        base, prime = heap[0]
        if base > CUTOFF:
            raise ValueError("Prime cutoff does not certify the marginal tail")
        costs.append(costs[-1] * base**(p - 1))
        heapreplace(heap, (base**p, prime))
    return costs


def intervals(values):
    result = []
    for s in values:
        if result and s == result[-1][1] + 1:
            result[-1][1] = s
        else:
            result.append([s, s])
    return result


def analyze_exponent(p, e, costs):
    root_power = p**e
    direct, extended, higher = [], [], []
    extra = 0
    y = 1
    for s in range(e + 1):
        q_min = max(5, 2*y - 1)
        size = root_power * costs[e - s]
        direct_close = size * q_min > B
        source_close = (
            not direct_close and s > 0 and (p == 3 or 2*s > e)
            and root_power * 2**p * q_min**(p+1) >= 3**p * B
            and 2 * size * q_min**2 >= 3 * B
        )
        if direct_close:
            direct.append(s)
        if direct_close or source_close:
            extended.append(s)
        extra += source_close
        if size * max(5**5, p**max(0, 5*s - 5)) > B:
            higher.append(s)
        y *= p
    return {
        "root": p, "exponent": e, "direct_euler_one": intervals(direct),
        "extended_euler_one": intervals(extended), "extra": extra,
        "higher_euler_exponents": intervals(higher),
    }


def internal_example(prime_table):
    p, e = 3, 1330
    a = sigma(p, e)
    witnesses = [23, 2663, 3851, 11617, 15973, 513767]
    if not all(a % r == 0 and a % (r*r) != 0
               and all(r % z for z in prime_table if z*z <= r) for r in witnesses):
        raise ValueError("Invalid witness for an exact first power")
    premium = prod(witnesses)
    root_power = p**e
    same_exponent, single_in_a = [], []
    for s in range(1, e + 1):
        q_min = 2*p**s - 1
        if 3 * (a // premium) <= 2 * q_min:
            same_exponent.append(s)
        if (3 * max(witnesses)**4 <= 2 * q_min
                and 8 * (root_power * a * premium)**4 * q_min**7 >= 27 * B**4
                and 32 * (root_power * a)**6 * q_min**11 >= 243 * B**6):
            single_in_a.append(s)
    return {
        "root": p, "exponent": e, "witnesses": witnesses,
        "excluded_f_equals_c": intervals(same_exponent),
        "excluded_c_equals_one": intervals(single_in_a),
    }


def run():
    frontier = open_exponents()
    prime_table = primes(CUTOFF)
    rows = []
    summary = {}
    for p, exponents in frontier.items():
        costs = marginal_costs(p, max(exponents), prime_table)
        active = [analyze_exponent(p, e, costs) for e in exponents]
        rows.extend(active)
        summary[p] = dict(
            open_actual_exponents=len(active),
            improved_actual_exponents=sum(row["extra"] > 0 for row in active),
            extra_euler_one_values=sum(row["extra"] for row in active),
            all_higher_euler_values_excluded=sum(
                row["higher_euler_exponents"] == [[0, row["exponent"]]] for row in active
            ),
        )
    return {"summary": summary, "internal_example": internal_example(prime_table), "results": rows}


def main():
    if not __debug__:
        raise SystemExit("Run without -O.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the per-exponent interval audit")
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("summary", "internal_example")}, indent=2))


if __name__ == "__main__":
    main()
