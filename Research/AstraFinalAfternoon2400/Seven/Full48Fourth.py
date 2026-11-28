"""Close the entire first fiber v_6106505825833677713=4 at canonical (7,48)."""
from functools import cache
import gzip,json
from hashlib import sha256
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyForest import B,C,S48,A48,abgt2,child_domain,sig,val,verify
P=[(7,48),(S48,4)]
RECEIPTS={'a':'65361a2a06a7aabecfbe2e6d54bea1468554b5a10c61bc3fd40f9c9a9ec4c44e','b':'92d1684d24a071b2f9e3636c55760ef1f63b6c91c024e5144846d72fbb897fdf'}

def elementary():
    # A^2 fixed: 3,11,29,41 are compelled; 11 cannot be Euler, and 11^2 emits forbidden 19.
    row=P+[(A48,2)]
    assert all(C.pc.prime64(q) for q in (3,7,11,13,19,29,41,S48))
    assert sig(7,48)%29==0 and sig(S48,4)%(11*41*A48)==0 and sig(A48,2)%3==0
    assert 3%4==11%4==3 and sig(11,2)%19==0
    base=[(7,48),(11,4),(29,1),(41,1)]
    assert abgt2(base+[(3,4)])       # 3 is even-valuation, so exactly two.
    assert sig(3,2)==13             # thus 13 is also compulsory.
    assert abgt2(base+[(3,2),(13,1)])
    print('A^2: forcing 3^2 via strict abundance then forcing 13 is contradictory',flush=True)

def main():
    assert __debug__; dom,tail=child_domain(P,(19,),A48)
    assert list(map(int,dom))==list(range(2,19,2)) and tail==37
    new={2}
    for tag,digest in RECEIPTS.items():
        f=H/f'Forest48{tag}.json.gz'; raw=f.read_bytes(); assert sha256(raw).hexdigest()==digest
        ds=json.loads(gzip.decompress(raw))['records']; seen=set()
        for r in ds:
            rows=list(map(tuple,r['P'])); assert rows[:-1]==P and rows[-1][0]==A48 and r['bad']==[19]
            assert rows[-1][1] not in seen; seen.add(rows[-1][1])
        assert new.isdisjoint(seen);new|=seen
        verify(f)  # also proves the large A48 label (root prefix) by ECPP.
    assert new==set(map(int,dom)); elementary()
    print('PASS complete exact first fiber (7,48), t=6106505825833677713, v_t=4; directly live A exponents:',list(map(int,dom)),'raw tail',tail,flush=True)

if __name__=='__main__':main()
