#!/usr/bin/env python3
"""Lightweight CI check of the FinalSprint ledger, not a proof replay."""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPRINT = ROOT / 'Research' / 'FinalSprint'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    baseline = ROOT / 'Research' / 'Session20261126' / 'Delta.json'
    raw = baseline.read_bytes().replace(b'\r\n', b'\n')
    require(sha256(raw).hexdigest() == 'ff47c354d6e5c47f6daff26bdd37b3b2922ff1cfcc0ce6af91487432f9a0c4e2', 'baseline digest')
    old = json.loads(raw)
    ledger = json.loads((SPRINT / 'Delta.json').read_bytes())
    require(ledger['baseline'] == '2b53c830dd903b460a315df04fa3a4a410fb8357', 'baseline commit')
    rows = old['remaining_shards']
    live = {(s['root'], e) for s in rows for e in s['remaining_actuals']}
    require(len(rows) == old['open'] and len(live) == old['open_actuals'], 'baseline counts')
    hits = set()
    packets = set()
    for receipt in ledger['proofs']:
        key = tuple(receipt['actual'])
        name = receipt['packet']
        require(key in live and key not in hits, f'invalid or duplicate exponent: {key}')
        require(Path(name).name == name and name not in packets, f'invalid packet name: {name}')
        require(sha256((SPRINT / name).read_bytes()).hexdigest() == receipt['sha256'], f'packet digest: {name}')
        hits.add(key)
        packets.add(name)

    left, closed = [], []
    for s in rows:
        exponents = [e for e in s['remaining_actuals'] if (s['root'], e) not in hits]
        if exponents:
            left.append(dict(s, remaining_actuals=exponents))
        else:
            closed.append(s['id'])
    expected = dict(total=old['closed'] + len(rows), closed=old['closed'] + len(closed),
                    open=len(left), open_actuals=len(live - hits),
                    singleton_shards=sum(len(s['remaining_actuals']) == 1 for s in left),
                    new_actuals=sorted(map(list, hits)), new_shards=closed, remaining_shards=left)
    for field, value in expected.items():
        require(ledger[field] == value, f'projection mismatch: {field}')
    print(f"PASS: {len(packets)} packet hashes; {expected['closed']} closed, "
          f"{len(left)} open shards, {expected['open_actuals']} open actuals")


if __name__ == '__main__':
    main()
