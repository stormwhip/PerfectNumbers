"""Independent exact price on the two special leaves of canonical (31,2) 331^316."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,lcm,prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check31Domains import B,BANS,state,vp
from Check31Masks import prime
P,T=331,1510189


def row_for(f):return ((31,2),(P,316),(T,f),(3,2),(13,2),(61,1))


@cache
def roots(p,o,c):
    factors=[a for a in range(2,o+1) if o%a==0 and prime(a)]
    g=next(t for a in range(2,p) if (t:=pow(a,(p-1)//o,p))!=0 and all(pow(t,o//q,p)!=1 for q in factors))
    ids={j for j in range(1,o) if gcd(j,o)==1}
    out=[(1,(0,))];m=p
    for _ in range(c):
        assert pow(g,o,m)==1
        y=1;rs=[]
        for j in range(1,o):
            y=y*g%m
            if j in ids:rs.append(y)
        assert len(set(rs))==len(ids)
        out.append((m,tuple(rs)))
        m*=p;g=pow(g,p,m)
    return tuple(out)


@cache
def check(row):
    f=dict(row)[T]
    assert f in (52,58) and row==row_for(f)
    assert prime(P) and prime(T) and 3**5030<=B<3**5031<T**5031 and T>5031
    x,s,ok=state(row); assert ok and [p for p,h in row if h%2]==[61]
    D=lcm(x,s)//x
    C=(316-vp(s,P),f-vp(s,T)); assert C==(315,f-1)
    os=[[o for o in range(3,5032,2) if (q-1)%o==0] for q in (P,T)]
    for o,r in product([1,*os[0]],[1,*os[1]]):
        assert gcd(o*r,P)==1
        assert 2*(3 in (o,r))+sum(k-3 for k in (o,r) if k>3)<=lcm(o,r)-1
    assert 3**(P-1)>=P*P
    notes=[];w=[]
    def tab(rr):
        gain={}
        for m,y,h in rr:
            if y<3 or y%2==0 or y in (*dict(row),*BANS) or (y.bit_length()-1)*h>=2*m.bit_length():continue
            if any(y%k==0 and y!=k for k in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)) or pow(2,y-1,y)!=1:continue
            b=y**h
            if b<m*m and x*lcm(D,b)<=B:
                gain[y]=max(gain.get(y,1),Fraction(m*m,b))
        notes.append(len(gain));w.extend(gain.values())
    left,right=roots(P,3,C[0]),roots(T,3,C[1])
    def joint():
        for (m,rr),(n,ss) in product(left,right):
            u=n*pow(n,-1,m)
            for a,b in product(rr,ss):yield m*n,(b+u*(a-b))%(m*n),2
    tab(joint())
    for p,oo,c in zip((P,T),os,C):
        tab((m,y,o-3) for o in oo if o>3 and 3**(o-3)<p**(2*c) for m,bb in roots(p,o,c)[1:] for y in bb)
    U=prod(w)
    assert x*(P**C[0]*T**C[1])**2>B*U
    print('PASS independent (31,2),331^316 special price on exponent',f,'losses',notes,flush=True)
    return True

if __name__=='__main__':
    assert __debug__
    for f in (52,58):check(row_for(f))
