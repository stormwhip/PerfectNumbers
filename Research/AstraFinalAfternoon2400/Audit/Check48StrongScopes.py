"""Independently derive the only uncovered positive-3 scope in canonical (7,48), t²."""
from fractions import Fraction
from math import prod
from pathlib import Path
import gzip,hashlib,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B,geometric,split
from Check31Forest import PR
P=7
T=6106505825833677713
R=518019223567
# Historical positive-3 scopes; digest binds the precise archive accepted in audit.
BOOK={
 'orbit48strong':('ad0d796471da29e6258e06b8f097ccb7ce88a0c48c29579fd5cc45ab7b7ab206',[(6,2),(8,2),(10,2)]),
 'orbit48strongmore':('7c56b29487df8df4da011208bb330e8250b227b2818a96f5441a011a9d66968f',[(2,2),(2,6),(4,2),(16,2)]),
 'orbit48strongextra':('4fa5f660fe33dee0adac10163c3c4f78a7a721e1115ce817493633f91024a6bc',[(4,6),(6,6),(8,6),(12,6),(18,2)]),
 'orbit48strongtail':('722d375c60d553494ca3afaa53c532bcf04c5965961de26063830e80186db9dc',[(10,6),(16,6),(22,2)]),
 'orbit48strong18':('6bc632babfc127445116dea0c84a1fe2b50ce1ee9cecf77286f6830a108069de',[(18,6)]),
 'orbit48strong22':('d4af154238142ce86ffae3605b91dce1374f563d74cff066dd140b5f1d4c618b',[(22,6)]),
}


def main():
    assert __debug__
    base=((P,48),(T,2))
    assert all(PR['prime64'](z) for z in (3,5,7,11,13,19,29,61,T,R))
    assert geometric(7,48)%29==geometric(T,2)%61==geometric(T,2)%R==0
    def abund(rows):return prod(Fraction(geometric(q,h),q**h) for q,h in rows)
    row=[(7,48),(29,1),(61,1)]
    # 3 present => exponent even. 5 is forbidden by minimum abundancy.
    assert abund(row+[(3,2),(5,1)])>2
    # If 11 present, exponent 2 alone emits banned 19 so its even exponent is ≥4.
    assert geometric(11,2)%19==0
    assert abund(row+[(3,4),(11,4)])>2
    assert geometric(3,2)==13 and abund(row+[(3,2),(11,4),(13,1)])>2
    assert geometric(3,4)==11*11
    live,tail=split(base,R,(19,))
    assert tail==195 and set(live)==set(range(2,97,2))
    result=set()
    for label,(digest,ex) in BOOK.items():
        path=H.parent/'Propagation'/f'Reserved438x12-{label}.json.gz'
        raw=path.read_bytes(); assert hashlib.sha256(raw).hexdigest()==digest
        data=json.loads(gzip.decompress(raw)); got=[]
        for rec in data['records']:
            rows=tuple(map(tuple,rec['P'])); h=rows[2][1]
            assert rows[:3]==live[h] and rec['bad'][:3]==[19,5,11] and not rec.get('unresolved')
            if len(rows)==4:
                assert rows[-1]==(3,2) and not rec.get('present') and not rec.get('lo')
                m=2
            else:
                assert len(rows)==3 and rec['present']==[3] and rec['lo']==[[3,6]]
                m=6
            got.append((h,m))
        assert got==ex
        assert not result&set(got)
        result.update(got)
    full={h for h,m in result if (h,2) in result and (h,6) in result}
    assert full=={2,4,6,8,10,16,18,22} and result-{(h,m) for h in full for m in (2,6)}=={(12,6)}
    print('PASS independent 3-support partition: exact 2 or >=6; 17 scoped leaves; pending h=12/v3=2',flush=True)


if __name__=='__main__':main()
