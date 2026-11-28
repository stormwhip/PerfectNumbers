"""Independent top and second domain verification for canonical (7,438)."""
import gzip,json,sys,subprocess
from pathlib import Path
from hashlib import sha256
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckSevenForestDomains import sig,split
T=572749682520506652634407616247
BASE='495c59f55456a70994ce7848487e0c4e262c1984'
REPO=H.parents[2]


def historical(name):
    return subprocess.check_output(['git','show',f'{BASE}:Research/{name}'],cwd=REPO)


def frozen_pack(path, digest):
    b=historical(path); assert sha256(b).hexdigest()==digest
    return json.loads(gzip.decompress(b))


def main():
    assert __debug__
    p=[(7,438)]; d,tail=split(p,{19},T)
    assert tail==57 and set(d)=={2,4,6,10,12,14,16,18,20,22,24,28}
    f1=frozen_pack('Night2400/Fibers7x438.json.gz','112faa9f5618a97bdae40cad1eb6ada8df6b90a18ad68447ceb84383ca3d24a9')
    f2=frozen_pack('Night2400/G3/Seven438.json.gz','86801a494e509019196ec3a69a4c297bf64f3c33b4405dfe1c44dea27a3e506b')
    def first(w):return set(map(int,w['cases']))
    a,b=first(f1),first(f2)
    assert not a&b and set(d)-a-b=={10,12,18,22}
    g=json.loads(historical('GeminiFrontier/FollowupResults.json'))
    cuts=[row for row in g['conditional_proofs'] if (row['p'],row['e'])==(7,438)]
    assert any(row['prefix']==f'7^438 * {T}^f' and row['covered']=='v_t(N) in {18, 22} (all canonical supports)' for row in cuts)
    assert set(d)-a-b-{18,22}=={10,12}
    s,tail=split(d[12],{19},27431)
    assert set(s)==set(range(2,111,2)) and tail==221
    n=frozen_pack('FinalNight2400/SevenNext/New438Credits.json.gz',sha256(historical('FinalNight2400/SevenNext/New438Credits.json.gz')).hexdigest())
    old2=set(map(int,n['nodes']['27431'])); assert old2==set(range(30,73,2))
    old=(set(range(74,111,2))|old2|{28})
    assert len(old)==42
    new=set()
    for name in ['Seven/Forest438t12a.json.gz','Seven/Forest438t12b.json.gz','Seven/Forest438t12c.json.gz','Propagation/Reserved438x12-12-14-16-18-20-24.json.gz','Propagation/Reserved438x12-10.json.gz','Propagation/Reserved438x12-26.json.gz']:
        pack=json.loads(gzip.decompress((H.parent/name).read_bytes()))
        for row in pack['records']:
            prefix=[tuple(z) for z in row['P']]; h=prefix[-1][1]
            assert prefix==s[h] and h not in new and h not in old
            new.add(h)
    assert new==set(range(2,27,2))-{22}
    assert old|new|{22}==s.keys()
    final=json.loads(historical('FinalNight2400/OpenFrontier.json'))['ShardRemainders']
    fwd=json.loads(historical('GeminiFrontier/ShardToKeys.json'))
    inv=json.loads(historical('GeminiFrontier/KeyToShards.json'))
    expected='P7_I00084'
    assert final[expected]==fwd[expected]==[[7,438]] and inv['7,438']==[expected]
    assert [n for n,ls in final.items() if [7,438] in ls]==[expected]
    print('PASS independent first 12 exact/57 raw tail; t^12: 55 exact / 221 tail / 42 frozen + 13 new; singleton',expected)

if __name__=='__main__':main()
