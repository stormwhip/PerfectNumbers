"""An entire r-exponent progression excluded in the 19,282 t^10 fiber."""
from fractions import Fraction
from math import prod,isqrt
p,t,r=19,1735317810514627,8383027
def sig(z,h):return (z**(h+1)-1)//(z-1)
def main():
    assert __debug__;sm=[3,7,13,23,157];assert all(all(x%j for j in range(2,isqrt(x)+1)) for x in sm)
    assert sig(19,282)%r==0 and sig(19,282)%t==0 and sig(t,10)%23==0 and sig(r,2)%prod([3,7,13,157])==0
    assert len(set(sm+[p,t,r]))==8
    bound=Fraction(sig(19,282),19**282)*prod(Fraction(sig(z,2),z*z) if z%4==3 else Fraction(z+1,z) for z in sm)
    assert bound>2;domain=list(range(2,101,2));cut=[h for h in domain if (h+1)%3==0];assert cut==list(range(2,99,6))
    print('PASS no h == 2 mod 3 (all even live h==2 mod6); lower abundance x1e6 floor',bound.numerator*10**6//bound.denominator,'whole progression',cut)
if __name__=='__main__':main()
