"""Small regression for exact-pair deduplication and shard completion semantics."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Ledger import aggregate,load_baseline


def check():
    baseline=load_baseline()
    controlled=dict(baseline,closed=3070,open=2,remaining_shards=[
        dict(id='x',root=19,remaining_actuals=[8,14]),
        dict(id='y',root=19,remaining_actuals=[14]),
    ])
    r=aggregate(controlled,(('first',[(19,14)]),('repeat',[(19,14)])))
    assert r['new_actuals']==[(19,14)] and r['new_shards']==1 and r['open']==1
    assert r['remaining_shards']==[dict(id='x',root=19,remaining_actuals=[8])]
    v=aggregate(controlled,(('finish',[(19,8),(19,14)]),))
    assert v['open']==0 and v['closed']==3072 and v['status']=='REQUIRES_GLOBAL_REPLAY'
    for keys in ([],[(7,14)],[(19,99)]):
        try:aggregate(controlled,(('out of domain',keys),))
        except ValueError:pass
        else:raise AssertionError(keys)
    print('PASS deduplication, overlap, incomplete/complete shard, out-of-domain regression')


if __name__=='__main__':
    if not __debug__:raise RuntimeError('do not use -O')
    check()
