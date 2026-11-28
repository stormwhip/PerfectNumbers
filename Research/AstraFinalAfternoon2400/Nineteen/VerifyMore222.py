"""Three additional complete second prefixes under surviving (19,222) first fibers."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

TARGET={(1,40),(18,42),(18,46)}
Q=3789992812027

def main():
    need(__debug__,'assertions required')
    z=readz(HERE/'More222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984','frozen scope');ec=z['ecpp'];used=set()
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd-prime label')
        if q>=2**64:
            c=ec[str(p)];need(bool(c),'empty chain');used.add(str(p))
            for a in c:need(a[0]==q,'incorrect chain subject');q=C.pc.level(*a)
        return C.pc.prime64(q)
    need(all(prime(p)for p in (19,T,R,Q)) and sig(19,222)%(T*R)==0 and sig(T,1)%(2*Q)==0,'fixed geometry')
    old=RESEARCH/'FinalNight2400/Root222';x=readz(old/'TwoForests.json.gz')['cases'];w=readz(old/'ThirdForests.json.gz')['cases']
    a,_=domain(((19,222),),T);need(len(a)==53,'first domain')
    seen=set();n=0
    def terminal(P,o):
        nonlocal n
        n+=1
        K,O,H=o['forest'];s=C.State(P);need(not s.conflict and s.bad==(),'no unproved absence');C.validate_forest(s,K,O,H,prime)
        u=C.Forest(s,K,O,H).lower()[0];v=exact_leaf(P,K,O,H);need(min(u,v)>B and [floor10(u),floor10(v)]==o['floor10'],'strict dual terminal')
        print('PASS',tuple(h for _,h in P[1:]),o['floor10'],flush=True)
    for row in z['cases']:
        P=tuple(map(tuple,row['prefix']));f,g=P[1][1],P[2][1];need(P==((19,222),(T,f),(R,g)) and (f,g) in TARGET and (f,g) not in seen and exact(P) is not None,'exact second scope');seen.add((f,g))
        first,tail=domain(P[:1],T);d,t2=domain(P[:2],R);need(len(first)==53 and tail==144 and f in first and g in d and str(g) not in x[str(f)] and f'{f}:{g}' not in w,'historically unrefined second prefix')
        if f==1:
            need(row['pivot']==Q and exact(P)[1]%Q==0,'compelled certified third pivot');ds,k=domain(P,Q);need(ds==list(range(2,43,2)) and k==86 and set(map(int,row['children']))==set(ds),'entire 21-child window with tail')
            for j in ds:terminal(P+((Q,j),),row['children'][str(j)])
        else:terminal(P,row)
    need(seen==TARGET and set(ec)==used and n==23,'exact accepted count/prime inventory')
    print('COMPLETE second windows',sorted(seen),'23 strict leaves; ECPP',len(used),'no first or shard closure')

if __name__=='__main__':main()
