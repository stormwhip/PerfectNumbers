"""Recheck ordinary forest packets using two existing integer implementations.
The fresh delta is a projection of the pinned 204-shard ledger, not a count of files.
Run: python -I -S -B Research/Session20261126/Replay.py [--write]
"""
from pathlib import Path
from hashlib import sha256
import sys,json,gzip
H=Path(__file__).resolve().parent
R=H.parent
sys.path[:0]=[str(R/'MiddayForest'),str(R/'Midday')]
from Verify import verify
from ModeCheck import replay

def projection():
    raw=(R/'Midday/Delta.json').read_bytes().replace(b'\r\n',b'\n')
    import hashlib
    if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!='3a7b6812aafed3dddd228c34ed9575324d242887':
        raise ValueError('unexpected baseline ledger')
    sh=json.loads(raw)['remaining_shards']; original={(s['root'],e) for s in sh for e in s['remaining_actuals']}
    assert len(sh)==204 and len(original)==244
    proofs=[];excluded=set()
    for path in sorted(H.glob('Forest*.json.gz')):
        p,e,floor,digest=verify(path);data=json.loads(gzip.decompress(path.read_bytes()));row,=data['rows']
        assert path.name==f'Forest{p}x{e}.json.gz' and (p,e) in original
        assert set(row)=={'p','e','head','owners','roots'}
        pp,ee,values=replay({'general':row,'special':{},'ecpp':data['ecpp']})
        assert (pp,ee)==(p,e) and values==[floor]
        hits=sorted(f for q,f in original if q==p and (f+1)%(e+1)==0)
        excluded.update((p,f) for f in hits)
        proofs.append(dict(packet=path.name,sha256=digest,seed=[p,e],floor=floor,actuals=hits))
        print('PASS',p,e,floor,hits,flush=True)
    remaining=[];closed=[]
    for s in sh:
        left=[e for e in s['remaining_actuals'] if (s['root'],e) not in excluded]
        if left:remaining.append(dict(s,remaining_actuals=left))
        else:closed.append(s['id'])
    assert {(s['root'],e) for s in remaining for e in s['remaining_actuals']}==original-excluded
    return dict(baseline='2889e47f6db49c8a9bc8dda2c9153829c18a70ca',status='INCOMPLETE_FRONTIER',proofs=proofs,new_actuals=sorted(map(list,excluded)),new_shards=closed,closed=2868+len(closed),open=len(remaining),open_actuals=len(original-excluded),remaining_shards=remaining)

if __name__=='__main__':
    if not __debug__ or sys.argv[1:] not in ([],['--write']):raise SystemExit('assertions required; optional argument --write')
    result=projection();dest=H/'Delta.json'
    if sys.argv[1:]:dest.write_text(json.dumps(result,indent=1)+'\n',encoding='utf8',newline='\n')
    elif result!=json.loads(dest.read_bytes()):raise ValueError('ledger mismatch')
    print('closed / open / open actuals:',result['closed'],result['open'],result['open_actuals'])
