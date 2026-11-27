"""Reference root exponent cover and frozen-to-current exact incidence check; no forest claim."""
from pathlib import Path
import json,runpy
H=Path(__file__).resolve().parent;R=H.parent;order=(19,7,11,31,13,3,5,17)
if __name__=='__main__':
    assert __debug__
    v=runpy.run_path(str(R/'Session20261122/Python/VerifyRootExponentCoverage.py'))
    rows=list(v['canonical_tasks'](order));m={a['id']:a for a in rows};assert len(rows)==len(m)==3072
    old=json.loads((R/'GeminiFrontier/ShardToKeys.json').read_bytes());new=json.loads((H/'OpenFrontier.json').read_bytes())['ShardRemainders']
    for S in (old,new):
        for name,K in S.items():
            t=m[name];d=t['exponent'];p=t['root'];cap=v['exponent_ceiling'](p,10**2400)
            for q,e in K:
                assert p==q and 1<=e<=cap and (e%2==0 or e%4==p%4==1)
                assert e==d if t['exact'] else (e+1)%(d+1)==0
    print('PASS',len(m),'canonical root-exponent representatives; old/new exact incidences',sum(map(len,old.values())),sum(map(len,new.values())))
