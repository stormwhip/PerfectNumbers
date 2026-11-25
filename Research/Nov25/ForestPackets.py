"""Offline verification of explicitly registered Nov25 ordinary forest packets."""
import gzip
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Ledger import load_baseline, obligations


def verify(packet):
    if not __debug__:raise RuntimeError('do not use -O')
    sys.path.insert(0,str(H.parent/'NightLowRoute/Release'))
    from ForestReplay import proof, B
    data=json.loads(gzip.decompress(Path(packet).read_bytes()))
    if set(data)!= {'rows','ecpp'} or not data['rows']:
        raise ValueError('bad packet fields')
    cs=data['ecpp']; used=set(); active=obligations(load_baseline()['remaining_shards']); out=set(); seen=set()
    for row in data['rows']:
        if not set(row)<={'p','e','roots','owners','head','den','rho'}:
            raise ValueError('only ordinary unconditional rows can be lifted')
        p,e=row['p'],row['e']
        if (p,e) in seen:raise ValueError('duplicate row')
        seen.add((p,e))
        due={(q,f) for q,f in active if q==p and (f+1)%(e+1)==0 and f>=e}
        if not due:raise ValueError('no baseline obligations for forest seed')
        used.update(str(q) for q in {*row['roots'],*dict(row['owners'])} if q>=2**64)
        vals=proof(row,cs);m=min(vals.values());den=row.get('den',1)
        if m<=B**den:raise ValueError(f'{p},{e} remains open')
        out.update(due)
        print('PASS forest anchor',p,e,'Euler modes',len(vals),'live targets',len(due),flush=True)
    if used!=set(cs):raise ValueError('unexpected or missing primality chain')
    return out

if __name__=='__main__':
    for name in sys.argv[1:]:
        print('verified pairs',sorted(verify(name)))
