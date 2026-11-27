"""Independent exact CRT + repeated-divisor certificate for the sparse 906 high-source branch."""
from pathlib import Path
from math import prod,gcd,comb,isqrt
from fractions import Fraction
import json,gzip,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from VerifyLattice import coprime
A=(7**907-1)//6;X=7**906;B=10**2400;U=579125;m7=7**140;M=1814*m7

def rootfloor(v,j):
    lo=1;hi=1<<(1+(v.bit_length()+j-1)//j)
    while hi-lo>1:
        m=(hi+lo)//2
        if m**j<=v:lo=m
        else:hi=m
    return lo

def reps(j):
    if j%7==0:
        assert A**3%49 not in [1,48] and all(pow(i,21,49) in (1,48) for i in range(1,49) if i%7);return []
    deg=3*j;roots=[i for i in range(1,7) if pow(i,deg,7)==pow(A,3,7) and A*pow(i,-j,7)%7 in (2,4)];m=7
    for _ in range(1,140):
        K=m*7;roots=[x+m*((-((pow(x,deg,K)-pow(A,3,K))//m)*pow(deg*pow(x,deg-1,7),-1,7))%7) for x in roots];m=K
    return [1+1814*((x-1)*pow(1814,-1,m)%m) for x in roots]

def columns(R,lo,hi,j,k,n):
    width=(hi-R)//M;c=R*pow(M,-1,A)%A
    if 2*c>A:c-=A
    basis=[]
    for l in range(n):
        d=min(l,j*k);shift=l-d;F=A**(k-d//j);c0=[0]*n
        for h in range(d+1):c0[shift+h]=F*comb(d,h)*c**(d-h)
        basis.append(c0)
    return basis,width

def check():
    assert __debug__;D=json.loads(gzip.decompress((P/'Sparse906.json.gz').read_bytes()));W={(j,i,b):vv for j,i,b,*vv in D['w']};seen=set();needed=[]
    for j in range(2,110):
        if 10**(7*j)>A:break
        rr=reps(j);H=rootfloor(A,j);d=[r for r in rr if r<=H]
        if not d:continue
        needed.append(j);bands=D['bands'][str(j)];assert bands[0][1]==H and min(d)>=bands[-1][0] and all(x[0]==y[1]+1 for x,y in zip(bands,bands[1:]))
        for i,R in enumerate(rr):
            if R>H:continue
            assert R>1 and A%R
            for b,(lo,hi,k,n) in enumerate(bands):
                assert 0<lo<=hi and k>0 and n>k
                if (hi-R)//M<=0:continue
                seen.add((j,i,b));cols,dx=columns(R,lo,hi,j,k,n);polys=[]
                for v in W[j,i,b]:
                    assert len(v)==n;f=[sum(x*y for x,y in zip(v,col)) for col in zip(*cols)];assert sum(abs(y)*dx**a for a,y in enumerate(f))<lo**(j*k);polys.append(f)
                assert len(polys)==2 and coprime(*polys)
    assert j==110-1 and (10**7)**110>A and set(W)==seen and needed==[2,4,5]
    print('PASS no A=r*b^j for a simple high-order-3 r at depth 140:',needed,len(seen),'CRT/band pairs',flush=True)
if __name__=='__main__':sys.set_int_max_str_digits(0);check()
