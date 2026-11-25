"""Add a digit-slope check for exterior Euler emitters, exact p valuation.
Exploratory. No assumption of q dividing A; caller's baseline guard excludes this class.
"""
import sys,json,argparse
from pathlib import Path
from math import gcd
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Joint as J,Digits as DG
U=J.U;B=J.B

def run_ext(p,e,rs,s):
    A,pe,k,chunks,cost,M,V=J.context(p,e,tuple(rs));y=p**s;Q=J.euler_floor(p,s,U.O.tb.forbidden(p),128);budget=B*y**k
    Hmax=B//(M*Q);witness=[]
    for f in range(2,U.logi(Hmax,3)+1,2):
        # If root valuation order is nontrivial then odd order divides f+1. If r=1 mod p, only b<=v_p(f+1) possible.
        def search(i,j):
            v=V;lo=max(3,U.root((2*Q*p**i)//3,f)+1);hi=min(U.root(Hmax,f),U.root(B*(y*p**j)**k*v.denominator//(Q*v.numerator),f),U.root(B*p**j//(pe*A),2*f))
            if lo>hi:return False
            roots=U.lifts(p,1,i,f);classes=roots if roots is not None else [(1,2)]
            if not any(lo+(z-lo)%T<=hi for z,T in classes):return False
            if i<j:
                m=(i+j)//2;return search(i,m) or search(m+1,j)
            for z,T in classes:
                first=lo+(z-lo)%T
                if first>hi:continue
                if (hi-first)//T<128:
                    for r in range(first,hi+1,T):
                        if r==p or A%r==0 or r in U.O.tb.forbidden(p):continue
                        if r<2**64 and not U.O.G.is_prime_det64(r):continue
                        sg=U.sig(r,f)
                        if U.val(sg,p)!=i or any(sg%q==0 for q in U.O.tb.forbidden(p)):continue
                        fhi=min(B//(M*r**f),sg//p**i, B*(y*p**i)**k*V.denominator//(V.numerator*r**f))
                        if J.old.interval_factor(sg//p**i,y,p,Q,fhi,U.O.tb.forbidden(p),64):
                            witness.append([f,i,'shortbase',len(str(r))]);return True
                    continue
                # A necessary relation linear modulo p^min(i,s); count possible candidates without imposing internal divisor constraints.
                if i and s and (f+1)%p and (m0:=p**min(i,s))>(W:=U.sig(hi,f)//(Q*p**i)):
                    if not W:continue
                    mod=p**i*m0;inv=pow(first-1,-1,mod);t=(pow(first,f+1,mod)-1)*inv%mod
                    if t%p**i:raise ArithmeticError('bad lift')
                    deriv=((f+1)*pow(first,f,m0)-t)*inv%m0;alpha= -deriv*(T//p**i)%m0;beta=-(t//p**i)%m0;n=(hi-first)//T+1
                    if DG.floors(n,m0,alpha,beta-1)==DG.floors(n,m0,alpha,beta-1-W):continue
                witness.append([f,i,'widebase',len(str(lo)),len(str(hi))]);return True
            return False
        if search(0,e-s):break
    return witness[:1]
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('s',nargs='+',type=int);args=ap.parse_args();p,e,rs=next(x for x in J.CASES if x[0]==args.p);rows=[]
 for s in args.s:
    w=run_ext(p,e,rs,s);rows.append([s,w]);print(p,e,s,w,flush=True);(D/f'Exterior{p}.json').write_text(json.dumps(rows)+'\n')
