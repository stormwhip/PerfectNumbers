"""Replay and assemble the complete first (7,48) t² proof. No other first claimed."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import Verify48Price as P
import Verify48Overlap as O
import Verify48Forest as F
import Verify48Masks as M
import Verify48StrongMasks as S
import Verify48FinalSquare as E


def main(cold=True):
    assert __debug__
    parent=[(P.P,48),(P.T,2)]
    r=P.PIVOT[2]; U,tail=P.domain(parent,r)
    assert U==list(range(2,97,2)) and tail==195
    domains=set(U); done=set(); masks=set()
    def add(h):
        assert h in domains and h not in done
        done.add(h)
    if cold:
        P.main()
        M.replay(F.forest_file('orbit48no3'),[(0,0)])
    for h in P.PUBLISH[2]:add(h)
    for h,lab in O.EXTRA[2].items():
        if cold:O.check(2,h,lab)
        add(h)
    for tag in ('orbit48sq','orbit48sqmid'):
        if cold:F.replay(F.forest_file(tag),F.PACKS[tag])
        for f,h in F.PACKS[tag]:assert f==2;add(h)
    for tag,expected in S.PACKS.items():
        if cold:S.verify(F.forest_file(tag),expected)
        for h,m in expected:
            assert h in domains-done and (h,m) not in masks
            masks.add((h,m))
    covered={h for h,m in masks if (h,2) in masks and (h,6) in masks}
    assert len(done)==39 and covered=={2,4,6,8,10,16,18,22}
    for h in covered:add(h)
    assert domains-done=={12} and masks-{(h,m) for h in covered for m in (2,6)}=={(12,6)}
    if cold:
        assert E.verify()==tuple(parent+[(r,12),(3,2)])
    else:
        assert E.PARENT==parent+[(r,12),(3,2)]
    add(12)
    assert done==domains
    print(('PASS complete' if cold else 'Roster only for complete proof'),
          'canonical (7,48) first t^2; 48 of 48 direct assignments, tail 195. Not the entire key.',flush=True)

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--sets-only'])
    main(not sys.argv[1:])
