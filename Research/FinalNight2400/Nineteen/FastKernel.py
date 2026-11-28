"""Discovery acceleration; same decisions as BestKernel on integer arithmetic."""
from pathlib import Path
import sys
from functools import cache
from fractions import Fraction
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import BestKernel as S;import AnchorKernel as A;from FastBounds import scaled
@cache
def net(z):
    # Upper bound h+1 <= 5100 so v_19(h+1)<=2. Only h near the minimum can lower the minimum ratio!
    o=next((i for i in (1,3,9) if pow(z,i,19)==1),0);b=A.val(z**o-1,19) if o>1 else 0
    mg=0;g=None;m=z*z;h=2
    while m<=A.B:
        u=b+A.val(h+1,19) if o and (h+1)%o==0 else 0;mg=max(mg,u)
        if g is None or m*g.denominator<g.numerator*19**(2*u):g=Fraction(m,19**(2*u))
        m*=z*z;h+=2
    return g,mg
class Kernel(S.Kernel):
    def __init__(self):
        super().__init__();A.M.loglo=scaled;A.M.net=net
