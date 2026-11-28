"""Independent exact domain and finite source-length check for the root-seven 48 prices."""
import sys
from fractions import Fraction
from math import gcd, lcm, prod
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from CheckSevenForestDomains import sig,split
T=6106505825833677713
B=10**2400


def divs(n):return [i for i in range(1,5032,2) if n%i==0]


def main():
    assert __debug__
    d,_=split([(7,48)],{19},T)
    for f,r,count,tail,lo,hi,w in [(2,518019223567,48,195,76,96,2),(10,531983,85,344,104,170,10)]:
        vals,t=split(d[f],{19},r)
        assert set(vals)==set(range(2,2*count+1,2)) and t==tail and r%4==3
        assert all(vals[h]==[(7,48),(T,f),(r,h)] for h in range(lo,hi+1,2))
        dt,dr=divs(T-1),divs(r-1)
        assert min(x for x in dt if x>1)-1>=6 and min(x for x in dr if x>1)-1>=w
        assert gcd(T*prod(dt),r*prod(dr))==1
        # Weight six is meaningful only on actual nontrivial order, or on
        # separately paid order-one or LTE increments with effective lengths.
        assert all(lcm(u,v)-1 >= (u-1)+(v-1) for u in dt for v in dr)
        assert 3**5030<=B<3**5031 and T>5031 and r>5031
        print('PASS independent live domain and disjoint odd lengths at first',f,'raw tail',t,'accepted even intervals',lo,hi,'orders',dt,dr)

if __name__=='__main__':main()
