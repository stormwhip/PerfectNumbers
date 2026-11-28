"""Independent monotone whole-source check at s=535 and 536 of canonical (13,618)."""
from math import gcd
from pathlib import Path
import sys
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H))
from Check7x808 import floorroot
from Check13HighLinear import qmin
import Check13HighLinear as audit
from Check7x808 import isprime

P=13; E=618; B=10**2400
X=P**E; W=X*P; A=sum(P**i for i in range(E+1)); L=2*(E+1)
R=10**7; BAN=(19,7,11,31)


def main():
    assert __debug__
    audit.SMALL=tuple(p for p in range(3,98,2) if isprime(p))
    assert A*12+1==W and all(pow(13,619,a)!=1 for a in range(L+1,R+1,L))
    tested=0
    for s,hs,ceiling,known in [(536,[(10,5)],49,[27]),(535,[(8,3),(10,5)],1411,[25,43])]:
        # Using the previously proved complete shape rosters of the safeguarded
        # HighLinear ordinary-source cases (the 535 roster replay is separate).
        y=P**s; pmod=(-1-12*A)%L
        mpos,=[k for k in range(1,L+1) if (k*y)%L==pmod]
        mneg,=[k for k in range(1,L+1) if (-k*y)%L==pmod]
        for (h,c),start in zip(hs,known):
            assert qmin(y,h)==2*y*start-1
            q=2*y*ceiling-1
            lo=max(R+1,floorroot(2*q//3,h)+1)
            t=B//(X*A*q)
            high=min(floorroot(A//R,c),floorroot(t,h-c))
            exponent=h+1-c; u=high**exponent; K=12*(A//lo**c)
            assert (W-1)*u <= q*y*mpos and q*u+(q+1)*K < q*y*mneg
            # Bounds stay true for all later q: upper z^d decreases and
            # lower z increases, so upper V decreases; (1+1/q) decreases.
            for k in range(start,ceiling,2*(h+1)):
                if gcd(k,P*prod_BAN)!=1:continue
                v=2*y*k-1
                assert pow(2,v-1,v)!=1
                if s==535:tested+=1
    assert tested==97
    print('PASS two independent signed bounds, progression and Fermat witnesses; (13,618) windows 535,536 closed (97 candidates at 535)')

prod_BAN=19*7*11*31
if __name__=='__main__':main()
