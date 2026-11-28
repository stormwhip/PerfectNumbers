"""Independent finite-sum and exact abundance audit for the whole (7,48) first-four fiber."""
import gzip,json,sys
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
from math import prod
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckSevenForestDomains import sig,split
T=6106505825833677713
Z=5913168485260377611579965807967983090512568398832018674784831
P=[(7,48),(T,4)]


def main():
    assert __debug__
    assert sig(7,48)%T==0 and sig(T,4)%Z==0
    branch,tail=split(P,{19},Z); assert set(branch)==set(range(2,19,2)) and tail==37
    found={2}
    for file,hash0 in [('Forest48a.json.gz','65361a2a06a7aabecfbe2e6d54bea1468554b5a10c61bc3fd40f9c9a9ec4c44e'),('Forest48b.json.gz','92d1684d24a071b2f9e3636c55760ef1f63b6c91c024e5144846d72fbb897fdf')]:
        b=(H.parent/'Seven'/file).read_bytes(); assert sha256(b).hexdigest()==hash0
        for rec in json.loads(gzip.decompress(b))['records']:
            p=[tuple(x) for x in rec['P']]; f=p[-1][1]
            assert branch[f]==p and f not in found and rec['bad']==[19] and not rec['unresolved']
            found.add(f)
    assert found==branch.keys()
    assert sig(7,48)%29==sig(T,4)%(11*41)==sig(Z,2)%3==0
    assert 11%4==3%4==3 and sig(11,2)%19==0 and sig(3,2)==13
    common=prod(Fraction(sig(q,h),q**h) for q,h in [(7,48),(11,4),(29,1),(41,1)])
    assert common*Fraction(sig(3,4),3**4)>2 and common*Fraction(sig(3,2),3**2)*Fraction(14,13)>2
    print('PASS independent active nine exponents, exact two-packet cover, and A^2 abundance/factor contradiction, strict raw tail 37')

if __name__=='__main__':main()
