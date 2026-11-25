"""Exhaustive binary positive/negative support at an arbitrary CERTIFIED prime.
Primary: rebuild the existing exact-prefix Compose.Forest. Independent: direct integer
ordered-state recursion and different elliptic arithmetic. Both halves must pass.
"""
import argparse,sys,json,gzip,math
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent; R=H.parent;sys.path.insert(0,str(R/'Nov25/Compose'));import Compose as C
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('IndependentElliptic',R/'ThreeChainNext/Replay.py');E=module_from_spec(spec);spec.loader.exec_module(E)
B=10**2400;ORDER=(19,7,11,31,13,3,5,17)
def req(x,m):
    if not x:raise ValueError(m)

def run(d,independent):
    req(set(d)=={'p','e','tree','ecpp'},'schema');p,e=d['p'],d['e'];req(type(p)==type(e)==int and p in ORDER and 2<=e<=7000 and not e%2,'exact even');T=d['tree'];req(set(T)=={'kind','q','yes','no'} and T['kind']=='support','partition');q=T['q'];ban=ORDER[:ORDER.index(p)];req(q not in (*ban,p),'extra support scope');seen=set();pv=d['ecpp']
    @cache
    def prime(z):
        req(type(z)==int and z>2,'prime type');t=z
        if z>=2**64:
            w=pv[str(z)];req(w,'empty certificate');seen.add(str(z))
            for r in w:req(r[0]==t,'chain');t=E.elliptic(*r) if independent else C.pc.level(*r)
        req(t<2**64 and (E.mr(t) if independent else C.pc.prime64(t)),'primality');return True
    prime(q);bounds=[];A=(p**(e+1)-1)//(p-1)
    for yes in (False,True):
        l=T['yes' if yes else 'no'];req(set(l)=={'kind','roots','owners','head'} and l['kind']=='forest','leaf');K=l['roots'];o=l['owners'];h=l['head'];s=C.State([(p,e)],present=[q] if yes else [],absent=[] if yes else [q]);req(not s.conflict,'not a forest leaf');C.validate_forest(s,K,o,h,prime)
        if not independent:m=C.Forest(s,K,o,h).lower()[0]
        else:
            parents=dict(o);ks=set(K);allowed=math.prod(ban if yes else (*ban,q));extra=q if yes else 1;U=p*A*math.prod(parents)*extra;child={z:[] for z in ks|parents.keys()}
            for z,a in parents.items():child[a].append(z)
            def val(x,t):
                c=0
                while x%t==0:c+=1;x//=t
                return c
            @cache
            def low(z,v):
                ordinary=flex=B+1
                for odd in (False,True):
                    if odd and (z%4!=1 or math.gcd(z+1,allowed)>1):continue
                    step=4 if odd else 2;j=v+((1 if odd else 0)-v)%step;n=0
                    while n<h and z**j<(flex if odd else max(ordinary,flex)):
                        S=(z**(j+1)-1)//(z-1)
                        if math.gcd(S,allowed)==1:
                            n+=1;S//=2 if odd else 1;C0=S
                            while (a:=math.gcd(C0,U))>1:C0//=a
                            arr=[low(y,val(S,y)) for y in child[z] if S%y==0];a=z**j*C0*math.prod(c for c,f in arr)
                            if not odd:ordinary=min(a,ordinary);a=min([a]+[a//c*f for c,f in arr])
                            flex=min(flex,a)
                        j+=step
                    flex=min(flex,z**j)
                    if not odd:ordinary=min(ordinary,z**j)
                return ordinary,flex
            start=p**e*A;arr=[]
            for z in ks:c=val(A,z);start//=z**c;arr.append(low(z,max(1,c)))
            full=start*math.prod(n for n,f in arr);m=min([full]+[full//n*f for n,f in arr]);low.cache_clear()
        req(m>B,'one support branch open');bounds.append(len(str(m))-1)
    req(seen==set(pv),'unused certificate');return p,e,q,bounds
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--audit',action='store_true');ap.add_argument('files',nargs='+',type=Path);args=ap.parse_args()
    for f in args.files:print('PASS SUPPORT',run(json.loads(gzip.decompress(f.read_bytes())),args.audit),flush=True)
