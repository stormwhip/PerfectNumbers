"""Project already verified actuals and support certificates. This is ledger arithmetic, not a replacement for proof replay."""
from pathlib import Path
from collections import Counter
import json,sys
H=Path(__file__).resolve().parent;R=H.parent
sys.path.insert(0,str(R/'SupportSplit'));import Verify as S

def projection():
    base=json.loads((R/'Midday/Delta.json').read_bytes());pairs={(s['root'],e) for s in base['remaining_shards'] for e in s['remaining_actuals']}
    prior={(p,e,tuple(sorted(h))) for p,e,h,q in S.WITNESSES}|{(31,8,(3,5,13,31))}
    universe={(p,e,tuple(sorted(h))) for p,e in pairs for h in S.masks(p) if not S.leaf(p,e,h)}-prior;assert len(universe)==6556
    rows=json.loads((H/'Support/Ledger.json').read_bytes());conditional={(p,e,tuple(h)) for p,e,h in rows};assert conditional<=universe
    hit={s for s in universe if not set(s[2])&{3,5,17,19}};scope=conditional|hit
    now=json.loads((H/'Delta.json').read_bytes());full=set(map(tuple,now['new_actuals']));dead={s for s in universe if s[:2] in full};left=universe-scope-dead
    # A proof forcing 23 or 29 does not by itself exclude an S8 support.
    survivors={s[:2] for s in left};assert survivors==pairs-full
    masks={f'{p}:{e}':sorted(sum(1<<S.ROOTS.index(t) for t in h) for pp,ee,h in left if pp==p and ee==e) for p,e in sorted(survivors)}
    if '--check-masks' in sys.argv:
        companion=json.loads((H/'OpenSupport.json').read_bytes());assert companion['order']==list(S.ROOTS) and companion['rows']==masks and companion['keys']==len(survivors) and companion['triples']==len(left)
    print(json.dumps(dict(frozen_support=len(universe),support_packets=len(conditional),global_hit=len(hit),new_global_beyond_packets=len(hit-conditional),support_union=len(scope),fully_proved_keys_cover=len(dead),overlap=len(dead&scope),remaining_supported_triples=len(left),remaining_actuals=len(survivors),remaining_triples_by_root=Counter(p for p,e,h in left)),sort_keys=True))
if __name__=='__main__':
    if not __debug__:raise SystemExit('no -O')
    projection()
