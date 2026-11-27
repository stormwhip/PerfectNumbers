"""Cold local checks for prefix-aware supplier pricing; no whole-fiber claim."""
import gzip
import json
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(H), str(R/'Session20261126')]
from PivotCheck import C
from PrefixPrice import excludes

LEAF2 = [(13,372),(438552673580231875649,12),(756749110661077,4),(463891,28),(2239,2),(128599,60),(3,2)]


def certify(q, ecpp):
    u = q
    if u >= 2**64:
        chain = ecpp[str(q)]; assert chain
        for row in chain:
            assert row[0] == u and u >= 2**64
            u = C.pc.level(*row)
    assert type(q) is int and q > 2 and C.pc.prime64(u)


def main():
    assert __debug__
    path = H/'Leaf2.json'
    d = json.loads(path.read_bytes()); assert set(d)=={'parts','ecpp'}
    rows = list(map(tuple,d['parts'])); assert rows == LEAF2
    assert set(d['ecpp']) == {str(q) for q,_ in rows if q >= 2**64}
    for q,_ in rows: certify(q,d['ecpp'])
    s=C.State(rows); assert not s.conflict and s.base <= 10**2400
    result=excludes(rows,s.bad,[0,5]); assert result==(1,[4442,9335,8483])
    print('PASS conditional exact path',rows,result,flush=True)


def regression():
    assert __debug__
    d=json.loads(gzip.decompress((R/'FinalSprint/JointTree31x388.json.gz').read_bytes()))
    q=d['tree']['q']; assert (d['p'],d['e'],q)==(31,388,29941246365965400246754591)
    assert d['tree']['cases']['18']['type']=='price'
    rows=[(31,388),(q,18)]
    for p,_ in rows:certify(p,d['ecpp'])
    result=excludes(rows,C.State(rows).bad,[0,1]); assert result==(10,[5188,1814,0])
    print('PASS known price leaf',rows,result,flush=True)


if __name__=='__main__':
    if sys.argv[1:]==['--regression']:regression()
    else:
        assert not sys.argv[1:]
        main()
