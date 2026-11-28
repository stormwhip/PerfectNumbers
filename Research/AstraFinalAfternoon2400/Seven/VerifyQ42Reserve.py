"""Exact even 173 fibers via weighted thresholds and complete reserved Euler congruences."""
from functools import cache
from hashlib import sha256
from pathlib import Path
from math import gcd,prod
import gzip,json,sys
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H))
from VerifyForest import Q,sig,val,known_scope,exact_state,C,B
from ReservedForest import reserve
sys.path.insert(0,str(H.parents[1]/'FinalNight2400/SevenNext'))
from Odd42 import cost
R=173

def lower_independent(P,roots,edges,head,m):
    _,X,D,n=exact_state(P,(19,)); assert n==0
    low=2*m-1; M=4*m; iv=pow(low,-1,M)
    xs=set(roots)|{y for y,_ in edges}; kids={p:[] for p in xs}
    for q,p in edges:kids[p].append(q)
    pool=X*D*prod(xs)
    def deplete(a,z):
        while (d:=gcd(a,z))>1:a//=d
        return a
    @cache
    def remaining(z):
        cap=z//low;k=iv; best=z
        while cap:
            f=z*k%M or M
            if f<=cap and (f+M<=cap or not z%f):best=min(best,f)
            cap//=low;k=k*iv%M
        return best
    @cache
    def vertex(p,v):
        k=v+v%2; pw=p**k; n=0; z=B+1
        while n<head and pw<z:
            S=(p*pw-1)//(p-1)
            if S%19:
                n+=1
                x=remaining(deplete(S,pool))*pw
                x*=prod(vertex(y,val(S,y)) for y in kids[p] if S%y==0)
                z=min(z,x)
            k+=2;pw*=p*p
        return min(z,pw)
    return X*low*remaining(deplete(D,prod(roots)))*prod(vertex(p,val(D,p)) for p in roots)


def verify(path):
    assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and (R-1)==4*43 and C.pc.prime64(43)
    assert Q>5100 and 3**5100>B and (Q-1)%R and sig(7,12)==Q
    z=json.loads(gzip.decompress(path.read_bytes()));assert set(z)=={'records','ecpp'}; used=set(); done=set()
    @cache
    def prime(p):
        q=p
        if p>=2**64:
            k=str(p);used.add(k)
            for row in z['ecpp'][k]:assert row[0]==q;q=C.pc.level(*row)
        return C.pc.prime64(q)
    U=cost(Q,41,2,True,True)*cost(R,231,38,True,True)
    for d in z['records']:
        assert set(d)=={'P','params'}; P=list(map(tuple,d['P'])); assert P[:2]==[(7,12),(Q,42)] and len(P)==3 and P[-1][0]==R
        h=P[-1][1]; assert h not in done and h%2==0 and known_scope(P,(19,))=='12R';done.add(h)
        assert all(prime(q) for q,_ in P)
        S=prod(sig(q,t) for q,t in P);c=42-val(S,Q); j=h-val(S,R); assert 0<=c<=41 and 0<=j<=231
        s=C.State(P); seen=set(); mins=[]; mods=[]
        for t in d['params']:
            assert set(t)=={'i','k','roots','owners','head'}
            i,k=t['i'],t['k']; assert i in range(c+1) and k in range(j+1) and (i,k) not in seen;seen.add((i,k))
            m=Q**i*R**k; assert m>1; rt,es,head=t['roots'],t['owners'],t['head']; C.validate_forest(s,rt,es,head,prime)
            assert all(p%(4*m)!=2*m-1 for p in set(rt)|{q for q,_ in es})
            a=reserve(P,rt,es,head,(19,),m); b=lower_independent(P,rt,es,head,m)
            assert min(a,b)>B; mins.append(min(a,b)*10**6//B);mods.append((i,k))
        priced=reserved=0
        for i in range(c+1):
            for k in range(j+1):
                m=Q**i*R**k; num=s.X*(2*m-1)*Q**(2*(c-i))*R**(38*(j-k))*U.denominator
                if num>B*U.numerator:priced+=1
                else:
                    assert any(i>=a and k>=b for a,b in mods),(h,i,k)
                    reserved+=1
        assert priced+reserved==(c+1)*(j+1)
        print('173',h,'priced, reserved',priced,reserved,'forest windows',len(mods),'min millionths',min(mins,default=None),flush=True)
    assert used==set(z['ecpp']) and done
    print('PASS Q42 exact 173 powers',sorted(done),'ECPP',len(used),'SHA256',sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':verify(Path(sys.argv[1]) if len(sys.argv)>1 else H/'Forest12Q42Reserve.json.gz')
