"""56 first fibers below 150; authenticated labels plus two forest recurrences."""
from pathlib import Path
from functools import cache
from math import gcd,prod
import gzip,hashlib,json,runpy,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B,exact_leaf
UNPROVED={2,4,6,8,12,22,24,26,36,70,78,82,96,106,112,126,136,138}

def even_bound(st,K,edges,head):
    pool=st.X*st.D*prod(y for y,_ in edges); kids={p:[] for p in [*K,*(y for y,_ in edges)]}
    for y,z in edges:kids[z].append(y)
    def vp(n,p):
        a=0
        while n%p==0:a+=1;n//=p
        return a
    @cache
    def node(z,c):
        v=B+1;h=c+c%2;n=0
        while n<head and z**h<v:
            s=(z**(h+1)-1)//(z-1)
            if gcd(s,19*7)==1:
                n+=1;rem=s
                while (g:=gcd(rem,pool))>1:rem//=g
                v=min(v,z**h*rem*prod(node(y,vp(s,y)) for y in kids[z] if s%y==0))
            h+=2
        return min(v,z**h)
    return st.X*(st.D//prod(z**vp(st.D,z) for z in K))*prod(node(z,vp(st.D,z)) for z in K)

def verify():
    assert __debug__
    raw=(H/'LowForests.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='e9f6606040e499f86159dcd81201bdccf0953a863802aac66c9ceffe14158edc';D=json.loads(gzip.decompress(raw));cases=D['cases'];assert set(map(int,cases))==set(range(2,150,2))-UNPROVED
    U=runpy.run_path(str(H/'Verify.py'))['losses']();seen=set();modes=[]
    @cache
    def prime(z):
        n=z
        if n>=2**64:
            for row in D['ecpp'][str(z)]:assert n==row[0];n=C.pc.level(*row)
            seen.add(str(z))
        assert C.pc.prime64(n);return True
    assert prime(2383) and C.valuation(C.sigma(11,396),2383)==1
    for f0,o in cases.items():
        f=int(f0);P=[(11,396),(2383,f)];st=C.State(P);assert set(st.bad)=={19,7} and not st.conflict
        K,O,n=o['roots'],o['owners'],o['head'];C.validate_forest(st,K,O,n,prime)
        if o['even']:
            modes.append(f);c=396-C.valuation(st.S,11);v=f-C.valuation(st.S,2383)
            for q in {*K,*(r for r,z in O)}:
                if q%4==1:
                    i,j=C.valuation(q+1,11),C.valuation(q+1,2383)
                    if i<=c and j<=v:assert st.X*q*11**(4*(c-i))*2383**(2*(v-j))>B*U
            other=even_bound(st,K,O,n);st.fixed_euler=True
        else:other=exact_leaf(P,K,O,n)
        assert min(other,C.Forest(st,K,O,n).lower()[0])>B
    assert sorted(modes)==[42,48,72,80,102,124] and seen==set(D['ecpp']);print('PASS 50 unrestricted + 6 Euler-partition fibers; 1188 certificates; remaining',sorted(UNPROVED));return UNPROVED
if __name__=='__main__':verify()
