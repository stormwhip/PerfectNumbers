"""Cold union for complete exact first t^10 at canonical (7,48)."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import Verify48Price as P
import Verify48Overlap as O
import Verify48Forest as F


def main(cold=True):
    assert __debug__
    parent=[(P.P,48),(P.T,10)]; pivot=P.PIVOT[10]
    A,tail=P.domain(parent,pivot)
    assert A==list(range(2,171,2)) and tail==344
    A=set(A); closed=set()
    def add(values):
        take=set(values);assert take<=A and not take&closed;closed.update(take)
    if cold:P.main()
    add(P.PUBLISH[10]);assert len(closed)==34
    for h,z in O.EXTRA[10].items():
        if cold:O.check(10,h,z)
        add([h])
    assert len(closed)==38
    M=0
    for tag,records in F.PACKS.items():
        fs={f for f,h in records}
        if fs=={2}:continue
        assert fs=={10}
        if cold:F.replay(F.forest_file(tag),records)
        add(h for f,h in records);M+=len(records)
    assert M==47 and closed==A
    print(('PASS complete' if cold else 'Roster only for complete proof'),
          'canonical (7,48) first t^10; 34 price + 4 CRT + 47 forests = 85 direct assignments, raw tail 344.',flush=True)
    return 10

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--sets-only'])
    main(not sys.argv[1:])
