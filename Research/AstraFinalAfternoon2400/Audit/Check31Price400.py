"""Independent complete analytic first 400 for canonical (31,2)."""
from fractions import Fraction
from math import gcd,isqrt,lcm,prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check31Domains import B,BANS,geometric,state,split,vp
from Check31Masks import block,internal,prime,R

P,T=31,331
ROW=((P,2),(T,400))


def main():
    assert __debug__ and prime(P) and prime(T)
    assert geometric(P,2)==3*T
    d,tail=split(((P,2),),T)
    assert len(d)==143 and tail==952 and d[400]==ROW
    X,S,ok=state(ROW)
    A=block(T,400,1)
    assert ok and gcd(A,3*P*T)==1 and lcm(X,S)==X*3*A and vp(S,T)==1 and vp(S,P)==0
    assert 3**5030<=B<3**5031 and 3**(T-1)>=T*T
    tab={}
    for o in range(3,5032,2):
        if (T-1)%o or 3**(o-1)>=T**798:continue
        divisors=[n for n in range(1,o) if o%n==0]
        g=next(z for z in range(2,T) if pow(z,o,T)==1 and all(pow(z,n,T)!=1 for n in divisors))
        idx=[i for i in range(1,o) if gcd(i,o)==1]
        m=T
        for z in range(1,400):
            assert pow(g,o,m)==1
            rs={pow(g,k,m) for k in idx}; assert len(rs)==len(idx)
            for b in rs:
                if b<3 or b%2==0 or b in (P,T,*BANS) or (b.bit_length()-1)*(o-1)>=2*m.bit_length():continue
                v=b**(o-1)
                if v>=m*m or X*lcm(3*A,v)>B:continue
                # Keep all odd squares; only exact witnesses may reject a nonsquare.
                if isqrt(b)**2!=b and any(pow(a,b-1,b)!=1 for a in [2,3,5,7,11,13,17,19,23] if a<b):continue
                tab[b]=max(tab.get(b,1),Fraction(m*m,v))
            m*=T;g=pow(g,T,m)
    u=prod(tab.values()); U=(u.numerator+u.denominator-1)//u.denominator
    assert len(tab)==1
    split_counts=[0,0,0,0]
    for i in range(3):
        for j in range(400):
            m=P**i*T**j;q0=2*m-1;q=max(5,q0);rest=T**(2*(399-j))
            for a in (1,5):
                if X*q*rest>B*U:
                    split_counts[0]+=1;continue
                c=internal(A,401,q0,4*m) if j==0 else 0
                assert not c or 9*X*max(A,c**a)>B
                if 9*X*A*R*q**a>B:
                    split_counts[1]+=1;continue
                if 2*X*q**(a+1)>3*B:
                    split_counts[2]+=1;continue
                assert 4*X*X*3*A*q**(a+3)*rest>9*B*B*U*A
                split_counts[3]+=1
    assert sum(split_counts)==2400
    print('PASS (31,2),331^400 exact; complete Euler windows',split_counts,'U ceil',U,'one excess label',flush=True)


if __name__=='__main__':main()
