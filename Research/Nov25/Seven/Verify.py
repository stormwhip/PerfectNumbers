"""Verify self-contained root-7/11 forest packets and return pinned baseline obligations."""
import gzip
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path[:0]=[str(H.parents[1]/'NightSevenForest/Release'),str(H.parent)]
from importlib.util import module_from_spec,spec_from_file_location
from Ledger import load_baseline,obligations

# Other proof paths may import a different file also called Replay.py.
_spec=spec_from_file_location('Nov25PinnedSevenForest',H.parents[1]/'NightSevenForest/Release/Replay.py')
_pinned=module_from_spec(_spec)
_spec.loader.exec_module(_pinned)
B,proof=_pinned.B,_pinned.proof


def verify(path):
    if not __debug__:raise RuntimeError('do not use -O')
    data=json.loads(gzip.decompress(Path(path).read_bytes()))
    if set(data)!={'rows','ecpp'} or not data['rows']:
        raise ValueError('invalid packet')
    due=obligations(load_baseline()['remaining_shards']); out=set(); seen=set(); used=set()
    for r in data['rows']:
        if not set(r)<={'p','e','roots','owners','head','den','rho'}:
            raise ValueError('unrecognized row fields')
        p,d=r['p'],r['e']
        if (p,d) not in due or (p,d) in seen:raise ValueError('not a distinct live baseline seed')
        seen.add((p,d)); used.update(str(q) for q in {*r['roots'],*dict(r['owners'])} if q>=2**64)
        vals=proof(r,data['ecpp']); den=r.get('den',1); v=min(vals.values())
        if v<=B**den:raise ValueError(f'unclosed seed {p},{d}')
        effects={(q,f) for q,f in due if q==p and (f+1)%(d+1)==0}
        out.update(effects)
        print('PASS pinned forest',p,d,'Euler modes',len(vals),'floor',(len(str(v))-1)//den,'live exponents',sorted(effects),flush=True)
    if used!=set(data['ecpp']):raise ValueError('unexpected or missing ECPP chain')
    return out

if __name__=='__main__':
    for p in sys.argv[1:]:print('verified pairs',sorted(verify(p)))
