"""Disjoint root-34 proof union, with full cold verification by default."""
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import Verify34Forest as F
import Verify34Masks as M


def main(cold=True):
    assert __debug__
    D,tail=F.child_domain(F.P,(19,),F.q);D=set(map(int,D)); assert len(D)==78 and tail==217
    found=set()
    for tag,record in F.PACKS.items():
        record=set(record)
        assert record<=D and not found&record
        if cold:assert F.replay(H/f'Reserved438x12-{tag}.json.gz',tuple(sorted(record)))==record
        found|=record
    r=set(M.EXPECTED);assert not r&found and r<=D and len(found)==52
    if cold:assert M.replay()==r
    found|=r
    left=sorted(D-found)
    assert len(found)==57 and left==[1,4,6,10,16,18,22,24,28,30,34,36,40,42,46,52,58,60,66,72,78]
    print('Canonical (7,34):',len(found),'excluded of',len(D),'direct first values; raw tail',tail,'remaining',left,flush=True)
    print('Mode:', 'cold replay' if cold else 'set arithmetic only','-- no whole key or shard closure.',flush=True)

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--sets-only']);main(not sys.argv[1:])
