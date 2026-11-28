"""Independent exact inverse cofactor caps for broad high-valuation overlap."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Verify618Square import A
p=19

def cap():
    # For u>=206: exact argument in Verify618Square proves ord in {3,9}, v19(h+1)<=1.
    # For u>=308 we get r^9=1 mod 19^307; exclude even a single factor of A.
    m=19;roots=[r for r in range(1,19) if pow(r,9,19)==1 and r!=1]
    for _ in range(1,307):
        k=m*p;roots=[r+m*((-((pow(r,9,k)-1)//m)*pow(9*pow(r,8,p),-1,p))%p) for r in roots];m=k
    assert m==19**307
    for r in roots:
        K=1238*m;R=r+m*((1-r)*pow(m,-1,1238)%1238);J=A*pow(R,-1,K)%K
        assert R%1238==1 and J and R*J>A
    return 308
