"""Verify final exact local additions under root222 first 1 and 18 without first-fiber claims."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

Q={1:3789992812027,18:108501737266216818637411}
RANGES={(1,16):{2,4,8,12,16,18,36},(1,22):{2,4,16},(18,2):{6,10},(18,16):{2,4,6,10,12,16},(18,22):{2,6,10,12}}

def main():
    need(__debug__,'assertions needed')
    z=readz(HERE/'Last18And1222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984','canonical frozen input');p=z['ecpp'];seen=set();m={}
    @cache
    def prime(q):
        n=q;need(type(q)==int and q>2 and q%2==1,'valid odd prime')
        if q>=2**64:
            a=p[str(q)];need(bool(a),'empty chain');seen.add(str(q))
            for w in a:need(w[0]==n,'wrong prime subject');n=C.pc.level(*w)
        return C.pc.prime64(n)
    need(all(prime(x)for x in (19,T,R,*Q.values())) and sig(19,222)%(T*R)==0,'compelled primes')
    first=RESEARCH/'FinalNight2400/Root222';old=readz(first/'ThirdForests.json.gz')['cases']
    got=set()
    for row in z['cases']:
        P=tuple(map(tuple,row['prefix']));f,g,j=[h for q,h in P[1:]];need(P==((19,222),(T,f),(R,g),(Q[f],j)) and j in RANGES[f,g] and (f,g,j) not in got and exact(P) is not None,'new exact residual');got.add((f,g,j))
        x=old[f'{f}:{g}'];d,k=domain(P[:3],Q[f]);l=set(x['left']);y=set(map(int,x['children']));need(set(d)==l|y and not l&y and j in l and x['q']==Q[f],'frozen third partition')
        K,O,H=row['forest'];s=C.State(P);need(not s.bad and not s.conflict and s.fixed_euler==(f==1),'actual Euler compatibility')
        C.validate_forest(s,K,O,H,prime);a=C.Forest(s,K,O,H).lower()[0];b=exact_leaf(P,K,O,H);need(min(a,b)>B and [floor10(a),floor10(b)]==row['floor10'],'dual integer terminal')
        m.setdefault(f'{f}:{g}',set()).add(j);print('PASS',f,g,j,row['floor10'],flush=True)
    need(got and seen==set(p),'bound prime inventory')
    actual={k:sorted(RANGES[tuple(map(int,k.split(':')))]-v)for k,v in m.items()}
    need(actual==z['remaining_by_touched_secondary'],'exact difference')
    print('COMPLETE additional disjoint exact cuts',len(got),'ECPP',len(seen),'new residual',actual)

if __name__=='__main__':main()
