"""Replay overnight releases in isolated interpreters; union complete exact exponents only."""
from pathlib import Path
import argparse,json,subprocess,sys
from collections import Counter
H=Path(__file__).resolve().parent; R=H.parent

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def merge(base,pairs):
    remaining=base['remaining_shards']; keys={(s['root'],e) for s in remaining for e in s['remaining_actuals']};pairs=set(pairs)&keys
    closed=[];left=[]
    for s in remaining:
        orig=s['remaining_actuals'];rem=[e for e in orig if (s['root'],e) not in pairs]
        if not orig:raise ValueError('empty baseline obligation')
        if not rem:closed.append(s)
        else:left.append(dict(s,remaining_actuals=rem))
    return dict(baseline_main='3b50576bc6af2a8fa3e6ed1bee077039b1ed86ce',theorem_status='INCOMPLETE_FRONTIER' if left else 'REQUIRES_GLOBAL_REPLAY',baseline_closed=base['closed'],baseline_open=base['open'],new_actuals=sorted(pairs),new_shards=len(closed),by_root=dict(sorted(Counter(x['root'] for x in closed).items())),closed=base['closed']+len(closed),open=len(left),closed_shards=closed,remaining_shards=left)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--manifest-only',action='store_true',help='aggregate only; not proof verification');a=ap.parse_args();
    def replay(*args):
        if not a.manifest_only:subprocess.run([sys.executable,'-B',*map(str,args)],check=True)
    base=read(R/'EveningMerge/Audit.json');rows=read(H/'Pilot.json')
    if [(r['p'],r['e']) for r in rows]!=[(11,306)]:raise ValueError('pilot scope')
    replay(R/'EveningTree/IndependentTree.py','--allow-overlap','--valuation','--input',H/'Pilot.json')
    pairs={(r['p'],r['e']) for r in rows}
    for packet in (R/'NightOrder'/n for n in read(H/'Batches.json')['order']):
        replay(R/'NightOrder/Replay.py','--input',packet.name)
        pairs.update((r['p'],r['e']) for r in read(packet))
    for name in read(H/'Batches.json')['five']:
        replay(R/'NightFive/Verify.py',name);j=read(R/'NightFive'/name);pairs.update((5,int(e)) for e in j.get('exponents',j))
    for name in read(H/'Batches.json')['three']:
        replay(R/'NightThree/Verify.py',name);pairs.update((3,r['e']) for r in read(R/'NightThree'/(name+'.json')))
    if read(H/'Batches.json').get('five_more'):
        replay(R/'NightFive/VerifyMore.py');pairs.update((5,int(e)) for e in read(R/'NightFive/Batch2.json')['exponents'])
    audit=merge(base,pairs); print('new complete shards',audit['new_shards'],'remaining',audit['open'])
    if a.output:a.output.write_text(json.dumps(audit,indent=1)+'\n',encoding='utf-8')
    elif json.loads(json.dumps(audit))!=read(H/'Audit.json'):raise ValueError('snapshot mismatch')
if __name__=='__main__':main()
