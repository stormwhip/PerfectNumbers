"""Replay the Gemini batch and audit it against the checked-in frontier."""
import argparse
from collections import Counter
import json
from pathlib import Path

from VerifyGeminiExponents2400 import CERT_FACTORS, replay
from VerifyTeichmullerValuation2400 import B, covered_exponents, odd_part, sigma

HERE = Path(__file__).resolve().parent


def audit(baseline, proved):
    previous = {
        (shard["root"], step["exponent"])
        for shard in baseline["additions"] for step in shard["proof"]
    }
    proved = set(proved)
    additions = []
    for shard in baseline["open_manifest"]:
        p = shard["root"]
        detail = []
        for e in covered_exponents(p, shard["exponent"], shard["exact"]):
            if p**e * odd_part(sigma(p, e)) > B:
                rule = "base-size"
            elif (p, e) in previous:
                rule = "teichmuller-valuation"
            elif (p, e) in proved:
                rule = "gemini-replay"
            else:
                break
            detail.append({"exponent": e, "rule": rule})
        else:
            if any(step["rule"] == "gemini-replay" for step in detail):
                additions.append(dict(shard, proof=detail))

    counts = Counter(t["root"] for t in additions)
    return {
        "theorem_status": baseline["theorem_status"],
        "total": baseline["total"],
        "closed": baseline["closed"] + len(additions),
        "open": baseline["open"] - len(additions),
        "by_root": {
            p: {"verified": row["verified"] + counts[int(p)],
                "open": row["open"] - counts[int(p)], "added": counts[int(p)]}
            for p, row in baseline["by_root"].items()
        },
        "verified_exponents": sorted(proved),
        "additions": additions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--remaining", type=Path, help="write the open shard manifest")
    args = parser.parse_args()
    baseline = json.loads((HERE / "Audit2400.json").read_text(encoding="utf-8"))
    proved = replay(CERT_FACTORS)
    if set(proved) != set(CERT_FACTORS):
        raise ValueError("At least one submitted exponent failed replay")
    result = audit(baseline, proved)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    expected = json.loads((HERE / "GeminiBatchAudit2400.json").read_text(encoding="utf-8"))
    if json.loads(rendered) != expected:
        raise ValueError("Replayed Gemini audit differs from the checked-in result")
    if args.remaining:
        closed = {shard["id"] for shard in result["additions"]}
        remaining = [shard for shard in baseline["open_manifest"] if shard["id"] not in closed]
        args.remaining.write_text(json.dumps(remaining, indent=2) + "\n", encoding="utf-8")
    print(f"{len(proved)} exclusions, {len(result['additions'])} new closed shards, "
          f"{result['open']} open")


if __name__ == "__main__":
    main()
