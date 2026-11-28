"""Verify strict unmasked exact j=2 terminal in the (19,222) f=2/g=22 window."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

Q=2032322226061
P=((19,222),(T,2),(R,22),(Q,2))

def main():
    need(__debug__,'assertions enabled')
    z=readz(HERE/'Plain222J2.json.gz'); need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P,'exact scope')
    a=RESEARCH/'FinalNight2400/Root222'; w=readz(a/'ThirdForests.json.gz')['cases']['2:22']
    d,tail=domain(P[:3],Q);live=set(w['left']);old=set(map(int,w['children']))
    need(w['q']==Q and live=={1,2,4,18,28} and set(d)==live|old and not live&old and tail==114 and 2 in live,'frozen exact third window')
    e=z['ecpp'];seen=set()
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd prime label')
        if p>=2**64:
            a=e[str(p)];need(bool(a),'empty prime chain');seen.add(str(p))
            for row in a:need(row[0]==q,'prime subject mismatch');q=C.pc.level(*row)
        return C.pc.prime64(q)
    need(all(prime(q)for q in dict(P)) and sig(19,222)%(T*R)==0 and sig(T,2)%Q==0 and exact(P) is not None,'mandatory primality and emission')
    K,O,H=z['forest'];st=C.State(P); need(not st.conflict and st.bad==(),'unrestricted Euler and no local assumptions')
    C.validate_forest(st,K,O,H,prime);a=C.Forest(st,K,O,H).lower()[0];b=exact_leaf(P,K,O,H)
    need(min(a,b)>B and [floor10(a),floor10(b)]==z['floor10'] and seen==set(e),'strict dual forest terminal/ledger')
    print('PASS (19,222) f=2 g=22 j=2, strict floors',z['floor10'],'roots',len(K),'edges',len(O),'ECPP',len(e))

if __name__=='__main__':main()
