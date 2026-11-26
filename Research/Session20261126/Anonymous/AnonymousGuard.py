"""For five anonymous A roots: rigorously exclude all high-t order-3 A-source primes whose square divides A.
python -I -S -B AnonymousGuard.py SNAPSHOT [gen|verify] [p:e ..]; gen needs python-flint; verification stdlib.
"""
import sys,json,gzip
from pathlib import Path
from math import gcd,isqrt,log
ROOT=Path(sys.argv[1]);here=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'Research/NightMerge'));import LatticeLeaf as L
sys.set_int_max_str_digits(60000)
CASES={(7,906):183,(7,738):150,(7,456):94,(13,612):124,(13,618):125}
def classes(p,e):
    A=(p**(e+1)-1)//(p-1); n=e+1;assert all(n%i for i in range(2,isqrt(n)+1));assert A%n;Y=p**CASES[p,e];T=2*n*Y;assert gcd(A,T)==1
    for a in range(2,p):
        if pow(a,3,p)!=1:continue
        b=pow(a,p**(CASES[p,e]-1),Y);assert pow(b,3,Y)==1
        z=b+Y*((1-b)*pow(Y,-1,2*n)%(2*n));yield A,a,z,T

def do(p,e,gen):
    if gen:
        sys.path.insert(0,str(here/'vendor'));from flint import fmpz_mat,fmpz_poly
    for A,a,z,T in classes(p,e):
        name=here/f'Anon{p}x{e}Mod{a}.json.gz';boxes=[] if gen else json.loads(gzip.decompress(name.read_bytes()));lo=z;hi=isqrt(A);ix=0
        while lo<=hi:
            end=min(lo*10**7,hi)
            if gen:
                beta=log(lo)/log(A);found=None
                for d in (4,5,6,7,8,9,10,12,14,16):
                    for m in sorted({max(1,min(d-1,round(2*beta*d)+j)) for j in (0,-1,1,2)},key=lambda j:abs(j-2*beta*d)):
                        first,rad,mid,cent,K,rows=L.build(A,2,z,T,lo,end,d,m)
                        if rad<0:found=[2,1,[0,0],[]];break
                        w=[K**j for j in range(d)];M=fmpz_mat([[v*h for h,v in zip(w,row)] for row in rows]);red,tr=M.lll(transform=True)
                        for i in range(d):
                            if sum(abs(int(red[i,j])) for j in range(d))>=first**m:continue
                            pol=fmpz_poly([int(red[i,j])//w[j] for j in range(d)]);linear=[]
                            for g,h in pol.factor()[1]:
                                if g.degree()==1:
                                    b,c=int(-g[0]),int(g[1]);linear.extend([[b if c>0 else -b,abs(c)]]*h)
                            wit=[d,m,[int(tr[i,j]) for j in range(d)],linear]
                            if L.verify(A,2,z,T,lo,end,wit):found=wit;break
                        if found:break
                    if found:break
                assert found,(p,e,a,ix);boxes.append([lo,end,found]);
            else:
                u,v,w=boxes[ix];assert (u,v)==(lo,end) and L.verify(A,2,z,T,u,v,w)
            ix+=1;lo=end+1
        assert ix==len(boxes)
        if gen:name.write_bytes(gzip.compress(json.dumps(boxes,separators=(',',':')).encode(),mtime=0))
        print(p,e,'modp',a,'depth',CASES[p,e],'boxes',ix,flush=True)
if __name__=='__main__':
    assert __debug__;pairs=[tuple(map(int,x.split(':'))) for x in sys.argv[3:]] or list(CASES)
    for p,e in pairs:do(p,e,sys.argv[2]=='gen')
