"""Replicate exact final j=16 cut, finishing f=1,g=2 at canonical (19,222)."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

Q=3789992812027
P=((19,222),(T,1),(R,2),(Q,16))

def main():
    need(__debug__,'assertions enabled')
    z=readz(HERE/'Root222F1G2.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P,'scoped exact prefix')
    a=RESEARCH/'FinalNight2400/Root222';w=readz(a/'ThirdForests.json.gz')['cases']['1:2'];d,k=domain(P[:3],Q);earlier=set(map(int,w['children']));old=set(w['left']);need(w['q']==Q and k==144 and set(d)==earlier|old and not earlier&old and old=={2,4,12,16,18,42},'frozen remainder')
    for name in ('Forest222.json.gz','Forest222Stage2.json.gz','Forest222Stage3.json.gz'):
        x=readz(HERE/name)['windows']['1:2'];need(x['pivot']==Q and set(x['closed'])<=old,'disjoint inherited scope');old-=set(x['closed'])
    need(old=={16},'last exact tertiary value')
    ec=z['ecpp'];seen=set()
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd-prime label')
        if q>=2**64:
            r=ec[str(p)];need(bool(r),'missing ECPP');seen.add(str(p))
            for x in r:need(x[0]==q,'broken ECPP subject');q=C.pc.level(*x)
        return C.pc.prime64(q)
    need(all(prime(q)for q in dict(P)) and sig(19,222)%(T*R)==0 and sig(T,1)%(2*Q)==0 and exact(P) is not None,'certified compulsory divisors')
    K,O,H=z['forest'];s=C.State(P);need(s.fixed_euler and not s.conflict and s.bad==(),'Euler at fixed t only');C.validate_forest(s,K,O,H,prime)
    a=C.Forest(s,K,O,H).lower()[0];b=exact_leaf(P,K,O,H);need(min(a,b)>B and [floor10(a),floor10(b)]==z['floor10'] and seen==set(ec),'strict dual terminal')
    print('PASS canonical root 222 f=1,g=2,j=16 dual floors',z['floor10'],'ECPP',len(seen),'COMPLETE second prefix f=1,g=2 in union')

if __name__=='__main__':main()
