"""Independent structural reconciliation of the frozen audit and Nov25 result, not proof replay."""
from collections import Counter
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent
R=H.parent
BASE='3efc593b3950340cee799f0be02ee19be4c1c1caf1b8f501eefb3021dcb5d902'


def need(ok,why):
    if not ok:raise ValueError(why)


def main():
    raw=(R/'NightMerge/Audit.json').read_bytes().replace(b'\r\n',b'\n')
    need(hashlib.sha256(raw).hexdigest()==BASE,'wrong audit')
    baseline=json.loads(raw)
    result=json.loads((H/'Delta.json').read_bytes())
    universe={}; by_pair={}
    for s in baseline['remaining_shards']:
        k=s['id']; p=s['root']; es=s['remaining_actuals']
        need(k not in universe and es and len(es)==len(set(es)),'bad baseline shard')
        universe[k]=dict(s)
        for e in es:by_pair.setdefault((p,e),[]).append(k)
    proved=set()
    for row in result['new_actuals']:
        key=tuple(row)
        need(key in by_pair and key not in proved,'invalid or duplicate proof key')
        proved.add(key)
    residual={k:list(s['remaining_actuals']) for k,s in universe.items()}
    for p,e in proved:
        for k in by_pair[p,e]:residual[k].remove(e)
    oldleft=[dict(s,remaining_actuals=residual[k]) for k,s in universe.items() if residual[k]]
    closed=[s for k,s in universe.items() if not residual[k]]
    need(result['remaining_shards']==oldleft and result['closed_shards']==closed,'shard mismatch')
    need(result['open']==len(oldleft) and result['closed']==baseline['closed']+len(closed) and
         result['new_shards']==len(closed) and result['closed']+result['open']==3072,'shard count')
    need(result['baseline_closed']==baseline['closed'] and result['baseline_open']==baseline['open'] and
         result['baseline_actuals']==len(by_pair) and result['remaining_actuals']==len(by_pair)-len(proved),'pair count')
    sources=lambda ps:dict(Counter(str(p) for p,_ in ps))
    shard_roots=lambda ss:dict(Counter(str(s['root']) for s in ss))
    need(result['new_actuals_by_root']==sources(proved) and result['remaining_actuals_by_root']==sources(by_pair.keys()-proved)
         and result['new_shards_by_root']==shard_roots(closed) and result['remaining_shards_by_root']==shard_roots(oldleft),'root totals')
    print(f'{len(proved)} exact keys, {len(closed)} new closed shards, {len(oldleft)} open; '
          f'{sum(len(s["remaining_actuals"])==1 for s in oldleft)} singleton open shards')


if __name__=='__main__':main()
