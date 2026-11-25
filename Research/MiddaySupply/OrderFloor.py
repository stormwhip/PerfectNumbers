"""Largest closed prefix of impossible Euler multipliers in an emitter-specific order class.
No PRP acceptance; only certified compositeness produces a skip."""
from math import isqrt
from functools import lru_cache
from pathlib import Path
import sys,argparse,json
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Joint as J

def small(n):
    flags=bytearray(b'\1')*(n+1);flags[0:2]=b'\0\0'
    for d in range(2,isqrt(n)+1):
        if flags[d]: flags[d*d::d]=bytes((n-d*d)//d+1)
    return [i for i in range(3,n,2) if flags[i]]
PS=small(2001)
@lru_cache(maxsize=1024)
def order_floor(p,s,n,span):
    Y=p**s;ban=J.U.O.tb.forbidden(p)
    # q|sigma_f(r), q>f+1 => ord_q(r)>1 divides f+1=n; hence gcd(q-1,n)>1.
    from math import gcd
    if 2*Y-1<=n:return 2*Y-1
    for k in range(1,2*span+1,2):
        q=2*Y*k-1
        if k%p==0 or gcd(q-1,n)==1 or any(k%b==0 or q%b==0 for b in ban) or any(q%t==0 for t in PS if q!=t):continue
        # No unproved restriction on the cofactor k is used.
        if pow(2,q-1,q)!=1:continue
        return q
    return 2*Y*(2*span+1)-1
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('n',type=int);ap.add_argument('s',nargs='+',type=int);ap.add_argument('--span',default=8000,type=int);a=ap.parse_args();out=[]
 for s in a.s:
    q=order_floor(a.p,s,a.n,a.span);k=(q+1)//(2*a.p**s);out.append([s,k]);print(s,k,flush=True)
 (D/f'Order{a.p}_{a.n}.json').write_text(json.dumps(out)+'\n')
