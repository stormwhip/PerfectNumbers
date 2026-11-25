"""Conditional primality sieve: a candidate Euler q has order-5 roots modulo q.
If q is prime and q|Phi5(r), these four residues exhaust r modulo q. No PRP accepted as a prime."""
import sys,math,time,json,argparse
from pathlib import Path
from functools import cache
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import OrderFloor as O
@cache
def bound(p,e,s,c,n,C,span):
    assert (p,e,n,c)==(11,718,5,2)
    y=p**s;lim=math.isqrt(C);ban=O.J.U.O.tb.forbidden(p);lo=2*y-1
    assert lo>max(5,lim,2*span+1)
    # Write k odd, k=inv(Y) mod 5 since q=1 mod5, then sieve the progression.
    start=pow(y,-1,5);start+=5*(not start%2);delta=10;nn=max(0,(span-start)//delta+1);flags=bytearray(b'\1')*nn
    for prime in O.small(20000):
        for coeff,offset in [(2*y*delta,2*y*start-1)]+([(delta,start)] if prime==p or prime in ban else []):
            if coeff%prime==0:
                if offset%prime==0:flags[:]=bytes(nn)
                continue
            j=-offset*pow(coeff,-1,prime)%prime;flags[j::prime]=bytes(len(flags[j::prime]))
    survivors=0
    for j,yes in enumerate(flags):
        if not yes:continue
        k=start+delta*j;q=2*y*k-1
        # Euler q must be prime. Hence x^5=1 for x=a^((q-1)/5). If this fails q cannot be Euler.
        for a in (2,3,5,7,13,17):
            x=pow(a,(q-1)//5,q)
            if pow(x,5,q)!=1:break
            if x==1:continue
            t=x;ok=False
            for _ in range(4):
                if 3<=t<=lim and C%(t*t)==0:ok=True;break
                t=t*x%q
            if ok:return q
            break
        else:return q
        survivors+=1
    return 2*y*(span+1)-1
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('s',nargs='+',type=int);ap.add_argument('--span',type=int,default=120000);a=ap.parse_args();p,e,rs=11,718,(8629,);C=O.J.context(p,e,rs)[3][719];out=[]
 for s in a.s:
    st=time.monotonic();q=bound(p,e,s,2,5,C,a.span);out.append([s,(q+1)//(2*p**s)]);print(s,out[-1],round(time.monotonic()-st,1),flush=True)
 (D/'EulerPrefix11.json').write_text(json.dumps(out)+'\n')
