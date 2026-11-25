"""Bounded discovery against the fixed Nov25 frontier; never grants proof credit."""
import argparse
import json
from pathlib import Path
import sys
from time import monotonic
from functools import cache

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
WORK = R.parent
sys.path[:0] = [str(R / 'NightThree'), str(HERE.parent)]
from Ledger import load_baseline, obligations
import Verify as V

J, E = V.J, V.E


def source_candidates():
    return WORK.parent / 'upstream/Research/EveningRoot3/Candidates.json'


@cache
def source():
    return json.loads(source_candidates().read_bytes())


def roots(e):
    from sympy import isprime
    a = E.sigma(3, e)
    return tuple(sorted({r for w, _ in source()[str(e)] if (r := int(w)) > 3 and a % r == 0 and isprime(r)}))


def frontier():
    return {e for p, e in obligations(load_baseline()['remaining_shards']) if p == 3}


def run(e):
    fs = roots(e)
    one, high = J.audit(e, fs)
    out = dict(e=e, root=list(map(str, fs)), one=len(one), high=len(high),
               range_one=[min(one), max(one)] if one else [], range_high=[min(high), max(high)] if high else [])
    if not one and not high:
        out['alone'] = True
    elif not one or min(one) > 0:
        try:
            flags = dict(boost=True, reduced=True, parity=True, internal=True, exception=True)
            out['one_tree'] = V.independent(e, fs, {}, one, **flags) if one else {}
            out['high_tree'] = V.independent(e, fs, {}, high, reduced=True, high=True, internal=True) if high else {}
            out['alone'] = True
        except ValueError as ex:
            out['status'] = str(ex)
    else:
        out['status'] = 'Euler-one zero source window'
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only', type=int, nargs='+', required=True)
    p.add_argument('--write', type=Path)
    a = p.parse_args()
    if not set(a.only) <= frontier():
        raise SystemExit('requested exponent is outside fixed Nov25 frontier')
    rows = []
    for e in a.only:
        start = monotonic()
        row = run(e)
        rows.append(row)
        print(row, round(monotonic() - start, 3), flush=True)
        if a.write:
            if a.write.resolve().parent != HERE:
                raise ValueError('output must be under root-three research directory')
            a.write.write_text(json.dumps(rows, indent=1) + '\n', encoding='utf8')


if __name__ == '__main__':
    main()
