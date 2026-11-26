"""Replay and unite all disjoint exact fibers of canonical (13,372)."""
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path[:0]=[str(H),str(H/'C5')]
from Verify import KEY, Q, MASKS, verify_all
from Masked13x372 import replay as masks
from VerifyFibers import verify
from FrontierTree import replay as deep


def replay():
    assert __debug__
    ordinary=verify(H/'Fibers13x372.json.gz')
    domain,additional,partial=verify_all()
    remaining_masks=masks(H/'Masked13x372V2.json.gz')
    last=deep(H/'Frontier13x372V12Complete.json.gz')
    assert all(tuple(g['key'])==KEY for g in (ordinary,remaining_masks,last))
    assert all(int(g['pivot'])==Q for g in (ordinary,last))
    assert set(ordinary['domain'])==domain==set(last['domain'])
    assert set(ordinary['open'])|set(ordinary['covered'])==domain
    extra=set(remaining_masks['confirmed_masks'])
    assert not partial & extra and partial|extra==set(MASKS)
    assert remaining_masks['primary']==2 and 2 in domain
    assert last['covered']==[12] and not last['open_paths']
    parts=[set(ordinary['covered']),additional,{2},{12}]
    assert set().union(*parts)==domain and sum(map(len,parts))==len(domain)
    return {'key':list(KEY),'scope':'EXACT_COMPLETE','domain':sorted(domain),'parts':[sorted(x) for x in parts],
            'open':[],'deep_sha256':last['sha256']}


if __name__=='__main__':
    print(json.dumps(replay()),flush=True)
