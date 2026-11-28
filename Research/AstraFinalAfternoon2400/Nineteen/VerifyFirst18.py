"""Unrestricted-Euler proof for the entire (19,276) first exponent 18."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import B,C,HERE,RESEARCH,exact,domain,floor10,need,readz,exact_leaf,sig
from functools import cache
import hashlib

T=1176672733
P=((19,276),(T,18))

def main():
    need(__debug__,'assertions enabled')
    base=RESEARCH/'FinalNight2400'/'Ten276'/'Cases64.json.gz'
    z=readz(base);d,tail=domain(P[:1],T)
    need(len(d)==70 and tail==188 and len(z)==64 and set(d)-set(map(int,z))=={1,2,8,16,18,28},'historical raw coverage')
    need(hashlib.sha256(base.read_bytes()).hexdigest()=='d6c3e97838d42244f97ee4bc074719dde5bf53bba5b5718ef05ee6dd2bcf73db','frozen forest packet hash')
    book=readz(HERE/'First18.json.gz'); used=set()
    need(book['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and book['status']=='CONDITIONAL_FULL_FIRST_FIBER' and tuple(map(tuple,book['prefix']))==P,'sealed exact scope')
    ecc=book['ecpp']
    @cache
    def prime(q):
        need(type(q)==int and q>2 and q%2==1,'odd-prime label');p=q
        if q>=2**64:
            u=ecc[str(q)];need(bool(u),'empty ECPP certificate');used.add(str(q))
            for a in u:need(a[0]==p,'incorrect chain subject');p=C.pc.level(*a)
        return C.pc.prime64(p)
    need(all(prime(q)for q in (19,T)) and sig(19,276)%T==0 and exact(P) is not None,'actual forced first pivot')
    K,O,H=book['forest'];state=C.State(P)
    need(not state.fixed_euler and not state.conflict and state.bad==(),'unrestricted Euler canonical mode')
    C.validate_forest(state,K,O,H,prime)
    a=C.Forest(state,K,O,H).lower()[0];b=exact_leaf(P,K,O,H)
    need(min(a,b)>B and [floor10(a),floor10(b)]==book['floor10'],'not a strict dual recurrence bound')
    need(used==set(ecc),'unused ECPP label')
    print('PASS: entire first exponent 18 at (19,276), exact pivot',T)
    print('Strict floor10:',book['floor10'],'forest roots',len(K),'edges',len(O),'ECPP',len(used))
    print('First raw live',len(d),'tail',tail,'remaining (this packet alone)',sorted(set(d)-set(map(int,z))-{18}))

if __name__=='__main__':main()
