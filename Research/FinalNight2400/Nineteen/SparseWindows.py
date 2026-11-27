"""Exact bounded two-factor profile after new u<=143 cap."""
from fractions import Fraction
from math import gcd
X=7**906;W=7*X;A=(W-1)//6;B=10**2400;U=579125
if __name__=='__main__':
    assert __debug__;ss=set();us=set();pairs=[]
    for s in range(1,711):
        Y=7**s;Q=2*Y-1;bal=max(Fraction(1),Fraction(Y*Q,max(W,Q)*(W//Y+4)))
        for u in range(144):
            rem=max(0,906-s-5-u)
            if X*A*Q*bal.numerator*7**(2*rem)<=B*U*bal.denominator:ss.add(s);us.add(u);pairs.append((s,u))
    assert ss==set(range(482,666)) and us==set(range(82,144)) and (604,82) in pairs
    print('PASS <=2 A factors necessary s=482..665 and one factor delivers 82..143 units; all q emitters internal. Pairs',len(pairs))
