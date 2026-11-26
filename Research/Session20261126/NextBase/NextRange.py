"""Square-kernel / factor bounds for the next four root exponents. Requires python-flint."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
from flint import fmpz_mod_poly_ctx,ctx
ctx.threads=2

def search(e,b=32768,m=140000):
    A=(3**(e+1)-1)//2;d=2*(e+1);C=fmpz_mod_poly_ctx(A);g=1
    def poly(a,n):
        if n==1:return C([1+d*a,1])
        h=n//2;return poly(a,h)*poly(a+h,n-h)
    p=poly(1,b);R=1+d*b*m
    for j in range(0,m,8192):
        z=p.multipoint_evaluate([d*b*k for k in range(j,min(j+8192,m))])
        for t in z:g=g*int(t)%A
    assert __debug__ and math.gcd(g,A)==1,(e,R,math.gcd(g,A))
    print(e,R,math.gcd(g,A),flush=True)
if __name__=='__main__':
    for e in (1108,970,990,856):search(e)
