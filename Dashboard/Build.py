"""Generate the public dashboard from the selected Git mainline."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LEDGERS = ':(glob)Research/*/OpenFrontier.json'
CENSUS = 'Research/FermatRootValuation/Results.csv'
GITHUB = 'https://github.com/stormwhip/PerfectNumbers'

# The milestones preceding the machine-readable OpenFrontier ledgers.
MILESTONES = [
    ('26cb81d5', 1805, '根 3、5 赋值与来源'),
    ('7cceb374', 1851, '批量来源与因子链'),
    ('af56fcd3', 1869, '指标容量'),
    ('64e830c9', 2015, 'Teichmüller 提升'),
    ('652c1f27', 2027, 'Gemini 批次并集'),
    ('3b50576b', 2192, '来源间隙与多根因子链'),
    ('f2885e86', 2646, '夜间并集'),
    ('6732a1a8', 2666, '11 月 25 日上午'),
    ('ec84fbbd', 2868, '11 月 25 日午间'),
    ('2b53c830', 2974, '11 月 26 日主线基线'),
    ('49b19bbd', 2990, '晚间增量 · PR #7'),
    ('65891c45', 3003, '夜间增量 · PR #8'),
    ('79781fc0', 3004, 'Gemini 精确键 (13,508)'),
]

# Each row is an audited contribution, with duplicate coverage listed separately.
# Register a batch after its merge, using the merge SHA and an evidence permalink.
CREDITS = [
    ('af56fcd3', 'Gemini', 18, 0, 'Research/IndicatorCapacity/Readme.md'),
    ('652c1f27', 'Gemini', 12, 0, 'Research/TeichmullerValuation/GeminiBatchAudit2400.json'),
    ('1e8f915b', 'Claude', 0, 2, 'Research/EulerOneSieve/Readme.md'),
    ('79781fc0', 'Gemini', 1, 0, 'Research/GeminiFrontier/Review.md'),
    ('bc05f4db', 'GPT 6.2 Astra', 25, 0, 'Research/FinalNight2400/Proof.md'),
    ('495c59f5', 'Kimi', 0, 0, 'Documentation/CurrentStatus2400.md'),
]
LEDGER_CREDITS = {
    'Research/AstraFinalAfternoon2400/OpenFrontier.json': ('GPT 6.2 Astra', 2, 'Proof.md'),
}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], encoding='utf-8')


def commit_info(ref):
    sha, timestamp, title = git('show', '-s', '--format=%H%x09%cI%x09%s', ref).rstrip().split('\t', 2)
    return dict(sha=sha, timestamp=timestamp, title=title, url=f'{GITHUB}/commit/{sha}')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_ledger(commit, filename, catalog):
    ledger = json.loads(git('show', f'{commit}:{filename}'))
    remainder = ledger['ShardRemainders']
    require(remainder.keys() <= catalog.keys(), 'Frontier contains an unknown canonical shard')
    keys = set()
    for shard, pairs in remainder.items():
        unique = {tuple(pair) for pair in pairs}
        require(pairs and len(unique) == len(pairs), f'Invalid remainder for {shard}')
        require(all(p == catalog[shard] and e > 0 for p, e in unique),
                f'Unexpected root or exponent for {shard}')
        keys.update(unique)
    require(len(catalog) == ledger['TotalShards'], 'Census and frontier totals disagree')
    counts = dict(ClosedShards=len(catalog) - len(remainder), OpenShards=len(remainder),
                  DistinctKeys=len(keys), SingletonShards=sum(len(rows) == 1 for rows in remainder.values()))
    for field, count in counts.items():
        require(ledger[field] == count, f'{field} disagrees with the frontier projection')
    return ledger, keys


def build(ref):
    tip = commit_info(ref)
    rows = csv.DictReader(git('show', f'{ref}:{CENSUS}').splitlines())
    catalog = {}
    for row in rows:
        shard, prime = row['shard'], int(row['p'])
        require(re.fullmatch(rf'P{prime}_I\d{{5}}', shard) and shard not in catalog,
                f'Invalid canonical shard {shard}')
        catalog[shard] = prime
    require(len(catalog) == 3072, 'The canonical census must contain 3,072 unique shards')

    # Read changes along main's first parents so branch experiments never enter the chart.
    # On merges, diff explicitly against the first parent to resolve new ledger paths.
    revisions = git('log', '--first-parent', '--format=%H', ref, '--', LEDGERS).splitlines()
    require(bool(revisions), 'No mainline frontier ledger found')
    history = [dict(commit_info(sha), closed=closed, label=label) for sha, closed, label in MILESTONES]
    attribution = list(CREDITS)
    first_publication = set()
    latest = None
    for revision in reversed(revisions):
        changes = git('diff', '--name-only', '--diff-filter=AM', f'{revision}^1', revision, '--', LEDGERS)
        candidates = changes.splitlines()
        if not candidates:
            continue
        require(len(candidates) == 1, f'Multiple frontier ledgers changed in {revision}')
        filename = candidates[0]
        ledger, keys = read_ledger(revision, filename, catalog)
        stamp = commit_info(revision)
        snapshot = dict(stamp, closed=ledger['ClosedShards'], keys=len(keys))
        signature = json.dumps(ledger['ShardRemainders'], sort_keys=True)
        if latest is None or signature != latest[0]:
            history.append(snapshot)
        if filename in LEDGER_CREDITS and filename not in first_publication:
            model, closed, proof = LEDGER_CREDITS[filename]
            attribution.append((revision, model, closed, 0, str(Path(filename).with_name(proof).as_posix())))
            first_publication.add(filename)
        latest = (signature, stamp, filename)

    require(latest is not None, 'No active frontier ledger found')
    _, snapshot, filename = latest
    ledger, keys = read_ledger(ref, filename, catalog)
    remainder = ledger['ShardRemainders']
    totals = Counter(catalog.values())
    opens = Counter(catalog[shard] for shard in remainder)
    by_root = [
        dict(root=p, total=totals[p], open=opens[p], keys=sum(q == p for q, _ in keys))
        for p in sorted(totals)
    ]
    credits = []
    for commit, model, closed, overlap, path in attribution:
        evidence = commit_info(commit)
        git('cat-file', '-e', f"{evidence['sha']}:{path}")
        credits.append(dict(model=model, closed=closed, overlap=overlap,
                            date=evidence['timestamp'], title=evidence['title'],
                            url=f"{GITHUB}/blob/{evidence['sha']}/{path}"))
    return dict(
        latest=snapshot, source=tip, ledgerUrl=f"{GITHUB}/blob/{tip['sha']}/{filename}",
        status=ledger['GlobalStatus'], total=len(catalog), open=len(remainder), closed=ledger['ClosedShards'],
        keys=len(keys), singletons=ledger['SingletonShards'], roots=by_root, history=history,
        credits=credits, shards=[dict(id=shard, root=p, exponents=[e for _, e in remainder.get(shard, [])])
                                for shard, p in sorted(catalog.items(), key=lambda item: (item[1], item[0]))],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', default='HEAD')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    data = build(args.ref)
    args.out.mkdir(parents=True, exist_ok=True)
    for source, target in [('Index.html', 'index.html'), ('Style.css', 'style.css'), ('App.js', 'app.js')]:
        shutil.copyfile(HERE / source, args.out / target)
    (args.out / 'data.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n',
                                      encoding='utf-8')
    print(f"{data['closed']}/{data['total']} closed, {data['open']} open, {data['keys']} exact keys")


if __name__ == '__main__':
    main()
