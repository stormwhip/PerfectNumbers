"""Factor-free Euler-position/supply tail at the two canonical anonymous 13 keys."""
from pathlib import Path
from math import gcd, isqrt
from fractions import Fraction
import sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Propagation import sigma, outside_progression

p=13
B=10**2400

def prime(n):
    return n>=2 and all(n%d for d in range(2,1+isqrt(n)))


def euler_in_A(A, n, Y, X):
    """Sufficient elimination of internal q satisfying q≡-1 mod Y."""
    M=4*Y
    C=2*n
    # q≡2Y−1 modulo 4Y, and q≡1 modulo 2n by the exact odd order n at q.
    k=(((2*Y-2)//2)*pow(C//2,-1,M//2))%(M//2)
    residue=1+C*k
    modulus=n*M
    assert 0<residue<modulus and residue%M==2*Y-1 and residue%C==1
    return outside_progression(A,residue,modulus,max(5,residue),B//X)


def rows(e):
    n=e+1; X=p**e; W=X*p; A=sigma(p,e)
    assert e%2==0 and prime(n) and n!=p and gcd(A,p*(p-1)*n)==1
    assert all(A%z for z in (19,7,11,31))
    for s in range(1,e+1):
        Y=p**s; Q=2*Y-1
        exterior=euler_in_A(A,n,Y,X)
        # If q is not known exterior, X*q^5 is safe but charging A too
        # could double-count q. Pay all of A only after proving exteriority.
        high = (X*A*Q**5>B if exterior else X*Q**5>B)
        # q linear and exterior. Ordinary emitter z is external to A or internal.
        # Exterior z^g>2q/3 pays its full mass. Interior uses balanced bound.
        external_emitter = 2*X*A*Q*Q>=3*B
        inside_lb=Fraction(Y*Q,max(W,Q)*(W//Y+4))
        internal_emitter = X*A*Q*max(Fraction(1),inside_lb)>B
        yield s,exterior,high,external_emitter,internal_emitter


def contiguous(vals):
    if not vals:return None
    return (vals[0],vals[-1]) if vals==list(range(vals[0],vals[-1]+1)) else vals


def main():
    assert __debug__
    expected={612:[303,303,466,539],618:[306,306,460,539]}
    for e in (612,618):
        tab=list(rows(e))
        for i,label in [(1,'q-in-A'),(2,'higher q'),(3,'linear exterior q/exterior emitter'),(4,'linear exterior q/interior emitter')]:
            cut=[s for s,*bits in tab if bits[i-1]]
            assert cut==list(range(expected[e][i-1],e+1))
            print(e,label,contiguous(cut),flush=True)
        all_cut=[s for s,*bits in tab if all(bits)]
        assert all_cut==list(range(539,e+1))
        print(e,'all Euler locations/exponents',contiguous(all_cut),flush=True)

if __name__=='__main__':main()
