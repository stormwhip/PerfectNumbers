"""Proof-grade exact pivot domains and unrestricted-Euler forest terminal overlay."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import B,C,HERE,RESEARCH,exact,domain,floor10,val,need,readz,exact_leaf,sig
from functools import cache
import hashlib,json

T=1176672733


def main():
    need(__debug__,'assertions must be enabled')
    base=RESEARCH/'FinalNight2400'/'Ten276'/'Cases64.json.gz'
    z=readz(base);P0=((19,276),);live,tail=domain(P0,T)
    need(len(live)==70 and tail==188 and set(live)-set(map(int,z))=={1,2,8,16,18,28},'historical first partition')
    need(hashlib.sha256(base.read_bytes()).hexdigest()=='d6c3e97838d42244f97ee4bc074719dde5bf53bba5b5718ef05ee6dd2bcf73db','historical scope hash')
    pack=readz(HERE/'Even276.json.gz')
    need(pack['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and pack['status']=='CONDITIONAL_EVEN_FIRST_SLICES','scope')
    book=pack['ecpp'];used=set()
    @cache
    def prime(q):
        need(type(q)==int and q>2 and q%2==1,'odd prime only');p=q
        if q>=2**64:
            ch=book[str(q)];need(bool(ch),'missing large-prime witness');used.add(str(q))
            for row in ch:need(row[0]==p,'prime subject mismatch');p=C.pc.level(*row)
        return C.pc.prime64(p)
    need(all(prime(q)for q in (19,T)) and sig(19,276)%T==0,'root/pivot arithmetic')
    for sf,s in sorted(pack['cases'].items()):
        f=int(sf);need(f in {2,8,16,18,28},'new first condition')
        rows=(*P0,(T,f));need(exact(rows) is not None,'first row not raw live')
        q=s['pivot'];need(prime(q) and exact(rows)[1]%q==0,'certified second pivot')
        d,tail=domain(rows,q)
        need(d==s['raw_domain'] and tail==s['raw_tail'],'second domain mismatch')
        covered=set(map(int,s['forests']));need(covered<=set(d) and sorted(set(d)-covered)==s['remaining'],'live domain subtraction')
        for sh,w in sorted(s['forests'].items(),key=lambda j:int(j[0])):
            h=int(sh);p=(*rows,(q,h));state=C.State(p)
            K,O,H=w['forest'];C.validate_forest(state,K,O,H,prime)
            a=C.Forest(state,K,O,H).lower()[0];b=exact_leaf(p,K,O,H)
            need(min(a,b)>B and [floor10(a),floor10(b)]==w['floor10'],'strict dual forest terminal')
            print('PASS (19,276)',f,'exact second',q,h,'floor10',w['floor10'],flush=True)
        print('COVER (19,276)',f,'pivot',q,'strict raw tail',tail,'remaining',s['remaining'],'COMPLETE FIRST FIBER' if not s['remaining'] else 'OPEN',flush=True)
    need(used==set(book),'unconsumed primality records')
    print('Exact used ECPP chains:',len(used),flush=True)

if __name__=='__main__':main()
