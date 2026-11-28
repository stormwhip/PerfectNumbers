"""Independently verify price leaf at one exact fixed-Euler root-31 prefix."""
from math import gcd,lcm,isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check31Domains import B,state,vp
from Check31Forest import PR
T=917087137
A=((31,6),(T,72),(20668766888345125939752429067,2),
   (142399308228250619911869629856705143726156604422206306519,4),
   (1360496847191,6),(1382896061,16),(3,2),(13,2),(61,1))


def feasible(b):
    return b>=3 and b%2 and b not in (19,7,11,*dict(A)) and all(
        pow(p,b-1,b)==1 for p in (2,3,5,7,11,13,17,19,23) if p<b)


def check(row):
    assert row==A
    X,S,ok=state(row)
    assert ok and [p for p,h in row if h%2]==[61] and 72-vp(S,T)==71
    assert PR['prime64'](T) and 3**5030<=B<3**5031<T**5031 and T>5031
    D=lcm(X,S)//X
    os=[o for o in range(3,5032,2) if (T-1)%o==0 and 3**(o-1)<T**142]
    tested=0
    for o in os:
        fac=[p for p in range(2,o+1) if o%p==0 and all(p%d for d in range(2,isqrt(p)+1))]
        for g in range(2,T):
            r=pow(g,(T-1)//o,T)
            if all(pow(r,o//p,T)!=1 for p in fac):
                break
        selected={i for i in range(1,o) if gcd(o,i)==1}
        m=T
        for z in range(1,72):
            assert pow(r,o,m)==1
            rr=set(); b=1
            for i in range(1,o):
                b=b*r%m
                if i in selected:
                    rr.add(b)
                    if (b.bit_length()-1)*(o-1)<2*m.bit_length() and b**(o-1)<m*m and feasible(b):
                        assert X*lcm(D,b**(o-1))>B,(b,o,z)
                        tested+=1
            assert len(rr)==len(selected)
            n=m*T
            r+=m*((-(pow(r,o,n)-1)//m)*pow(o*pow(r,o-1,T),-1,T)%T)
            m=n
    n=X*T**142
    assert n>B
    print('PASS root 31 pinned odd Euler leaf: no deficits; relevant orders',os,'size-filter events',tested,'floor10',len(str(n))-1)
    return True


if __name__=='__main__':
    assert __debug__;check(A)
