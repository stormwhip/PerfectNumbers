"""No import whatsoever from candidate 906 code. Replay sealed cube-root and polynomial conditions."""
from pathlib import Path
from fractions import Fraction
from math import gcd,isqrt,prod,comb
import sys,json,gzip,hashlib
P=Path(__file__).resolve().parent;DIR=P.parent/'AuditNext';sys.path.insert(0,str(P));from VerifyLattice import coprime
A=(7**907-1)//6;B=10**2400;X=7**906;W=X*7;D0=1814

def lattice(name,u,ex):
    z=json.loads(gzip.decompress((DIR/(name+'.json.gz')).read_bytes()));assert z['u']==u and ex in (1,2)
    m=7**u;RR=[pow(a,7**(u-1),m) for a in [2,4]];assert all(pow(a,3,m)==1 and a%7 in [2,4] for a in RR)
    M=D0*m;R=[1+D0*((a-1)*pow(D0,-1,m)%m) for a in RR]
    if ex==1:R+= [A*pow(a,-1,M)%M for a in R]
    bb=z['bands'];assert bb[0][1]==isqrt(A) and bb[-1][0]<=min(R) and all(v[0]==w[1]+1 for v,w in zip(bb,bb[1:]));assert all(1<r<M and A%r for r in R)
    seen=set()
    for i,j,*ww in z['w']:
        assert (i,j) not in seen;seen.add((i,j));r=R[i];a,b,k,n=bb[j];assert 0<a<=b and k>0 and n>k;cap=(b-r)//M;assert cap>0
        c=(r*pow(M,-1,A)+A//2)%A-A//2;pp=[]
        for w in ww:
            assert len(w)==n;v=[0]*n
            for l,coef in enumerate(w):
                d=min(l,ex*k);shift=l-d;f=coef*A**(k-d//ex)
                for h in range(d+1):v[shift+h]+=f*comb(d,h)*c**(d-h)
            if sum(abs(t)*cap**i for i,t in enumerate(v))<a**(ex*k):pp.append(v)
        assert any(coprime(f,g) for h,f in enumerate(pp) for g in pp[h+1:])
    assert seen=={(i,j) for i,r in enumerate(R) for j,(_,b,_,_) in enumerate(bb) if (b-r)//M>=1};print('PASS 906 independent',name,len(seen),flush=True)

def main():
    assert __debug__ and gcd(A,1814*7*6)==1 and isqrt(A)**2!=A and A**3%49==22
    assert all(907%k for k in range(2,isqrt(907)+1))
    for n,u,e in [('Divisor906',255,1),('Repeated906',160,2),('RepeatedMid906',150,2),('RepeatedDeep906',140,2)]:lattice(n,u,e)
    # Balanced bound in the common W>=Q branch; all endpoint cases inclusive.
    H=[];E=[];I=[]
    for s in range(1,907):
        Y=7**s;Q=2*Y-1
        if X*A*Q**5>B:H.append(s)
        if X*A*Q*((2*Q+2)//3)>B:E.append(s)
        if X*A*Q*max(1,Fraction(Y*Q,max(W,Q)*(W//Y+4)))>B:I.append(s)
    assert H==list(range(206,907)) and E==list(range(514,907)) and set(E)&set(I)==set(range(711,907))
    # Test reported high-Euler normalized cost explicitly for *all* unit representatives (no Fermat filter needed except actual small-prime eligibility).
    rr=list(range(2,7));m=7
    for v in range(1,907):
        for z in rr:
            if z>=3 and z%4==1 and z!=19 and z**5<m*m:assert pow(2,z-1,z)!=1
        rr=[pow(a,7,7*m) for a in rr];m*=7
    print('PASS complete alpha>=5 order/length price checks, high=206,external=514,tail=711')
if __name__=='__main__':sys.set_int_max_str_digits(0);main()
