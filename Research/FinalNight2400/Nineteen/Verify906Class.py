"""Independent full (s,u) enumeration of two-A-prime classes, no clamp/monotonicity reliance."""
from fractions import Fraction as F
from math import isqrt,gcd
p=7;e=906;X=p**e;W=p*X;A=(W-1)//6;B=10**2400;U=579125;C=10**7

def test(low):
    surv=set();ext=set();he=set();other=set()
    for s in range(1,711):
        Y=p**s;Q=2*Y-1;b=X*A*Q;bal=F(Y*Q,max(W,Q)*(W//Y+4));den=bal.denominator;num=max(den,bal.numerator)
        for u in range(259):
            v=max(0,906-s-5-u);hh=u>=low;K=(C*p**(u-4) if hh else 1);z=b*K
            if z*p**(2*v)>B*U:continue
            if 2*z*Q*p**v<=3*B*U:ext.add(s)
            if not hh:surv.add(s);continue
            if z*p**(2*v)*num<=B*U*den:other.add(s);surv.add(s)
            K=max(K,isqrt((2*Q*p**u+2)//3));
            if b*K*p**(2*v)<=B*U:he.add(s);surv.add(s)
    assert not ext and not he and other==set(range(514,648))
    print('all (s,u) high threshold',low,'total s',min(surv),max(surv),len(surv),'high other emitter',min(other),max(other))
    return surv
if __name__=='__main__':
    assert __debug__ and A**3%49==22
    assert test(154)==set(range(462,711));assert test(144)==set(range(482,711))
