"""More secure exact (19,222) first-18 dependents with dual integer recurrence."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

P=((19,222),(T,18));Q=108501737266216818637411

def main():
    need(__debug__,'assertions required')
    z=readz(HERE/'Extra18x222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984','scope')
    src=RESEARCH/'FinalNight2400/Root222';old=readz(src/'ThirdForests.json.gz')['cases'];prev=readz(HERE/'Forest222.json.gz')['windows'];st2=readz(HERE/'Forest222Stage2.json.gz')['windows'];t2=readz(src/'TwoForests.json.gz')['cases']['18']
    e=z['ecpp'];used=set();covered=set()
    @cache
    def prime(p):
        q=p
        if q>=2**64:
            w=e[str(q)];need(bool(w),'empty chain');used.add(str(q))
            for a in w:need(a[0]==q,'bad subject chain');q=C.pc.level(*a)
        return C.pc.prime64(q)
    need(all(prime(q)for q in (19,T,R,Q)) and sig(19,222)%(T*R)==0,'fixed required primes')
    gd,tab=domain(P,R)
    for row in z['cases']:
        S=tuple(map(tuple,row['prefix']));need(S[:2]==P and S[2][0]==R and len(S) in (3,4) and exact(S) is not None,'exact branch scope');g=S[2][1];need(g in gd and str(g) not in t2,'frozen second live')
        k=f'18:{g}'
        if len(S)==4:
            q,j=S[3]; cert=old[k];need(q==Q==cert['q'],'frozen tertiary pivot')
            d,tail=domain(S[:3],q);l=set(cert['left']);h=set(map(int,cert['children']));need(set(d)==h|l and not h&l,'raw third coverage')
            need(j in l-set(prev.get(k,{}).get('closed',[]))-set(st2.get(k,{}).get('closed',[])),'new exact leaf')
        else:
            j=None;need(g==12 and k not in old,'whole formerly unrefined second')
        need((g,j) not in covered,'duplicate');covered.add((g,j))
        K,O,H=row['forest'];s=C.State(S);need(not s.conflict and not s.fixed_euler and not s.bad,'all Euler positions remain');C.validate_forest(s,K,O,H,prime)
        a=C.Forest(s,K,O,H).lower()[0];b=exact_leaf(S,K,O,H);need(min(a,b)>B and [floor10(a),floor10(b)]==row['floor10'],'strict terminal');print('PASS',g,j,row['floor10'],flush=True)
    need(covered=={(12,None),(2,4),(22,4)} and set(e)==used,'seal and label inventory')
    print('COMPLETE first18 g12 second window; one leaf each in g2/g22; ECPP',len(e))

if __name__=='__main__':main()
