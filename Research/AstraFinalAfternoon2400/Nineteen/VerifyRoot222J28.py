"""Complete exact j=28 terminal tree below the last root222 f=2 second prefix."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

Q=2032322226061
K=631981559132591077
P=((19,222),(T,2),(R,22),(Q,28))
TARGET=[1,2,4,5,6,8,9,10,12,13,14,16,17,18,20]

def main():
    need(__debug__,'assertions enabled')
    z=readz(HERE/'Root222J28.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P and z['pivot']==K,'sealed scope')
    s=RESEARCH/'FinalNight2400/Root222';w=readz(s/'ThirdForests.json.gz')['cases']['2:22'];d,tail=domain(P[:3],Q)
    old=set(map(int,w['children']));left=set(w['left']);need(w['q']==Q and set(d)==old|left and not left&old and left=={1,2,4,18,28} and tail==114,'frozen third window')
    e=z['ecpp'];seen=set()
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd prime label')
        if p>=2**64:
            a=e[str(p)];need(bool(a),'empty prime chain');seen.add(str(p))
            for row in a:need(row[0]==q,'prime subject mismatch');q=C.pc.level(*row)
        return C.pc.prime64(q)
    need(all(prime(q)for q in (*dict(P),K)) and sig(19,222)%(T*R)==0 and sig(T,2)%Q==0 and sig(Q,28)%K==0 and exact(P) is not None,'mandatory primality and emission')
    dd,tail=domain(P,K);need(dd==TARGET and tail==41 and set(map(int,z['children']))==set(dd),'entire fourth window')
    for h in dd:
        p=P+((K,h),);m=z['children'][str(h)];s=C.State(p);a,o,n=m['forest'];need(not s.conflict and s.bad==(),'no local assumption')
        C.validate_forest(s,a,o,n,prime);x=C.Forest(s,a,o,n).lower()[0];y=exact_leaf(p,a,o,n)
        need(min(x,y)>B and [floor10(x),floor10(y)]==m['floor10'],'strict dual terminal')
        print('PASS j28 child',h,m['floor10'],flush=True)
    need(seen==set(e),'unedited prime records')
    print('CLOSED entire f=2,g=22,j=28; raw tail',tail,'children',len(dd),'ECPP',len(seen),'remaining j=18 in union')

if __name__=='__main__':main()
