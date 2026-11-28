"""Final two exact child cuts under (19,222) first 18 second 16."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache
from hashlib import sha256

Q=108501737266216818637411
P=((19,222),(T,18),(R,16))

def main():
    need(__debug__,'assertions needed');prior=HERE/'Last18And1222.json.gz';need(sha256(prior.read_bytes()).hexdigest()=='15bcab2082e9d1ffd0dfb74477465629e32ba9f33e357f37601770419810b970','prior scope hash');old=readz(prior)['remaining_by_touched_secondary'];need(old['18:16']==[12,16],'precisely last two')
    z=readz(HERE/'Finish1816x222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P,'exact scope');e=z['ecpp'];s=set()
    @cache
    def prime(q):
        p=q;need(type(q)==int and q>2 and q%2==1,'odd prime')
        if q>=2**64:
            a=e[str(q)];need(bool(a),'empty ECPP');s.add(str(q))
            for b in a:need(b[0]==p,'incorrect ECPP subject');p=C.pc.level(*b)
        return C.pc.prime64(p)
    need(all(prime(q)for q in (19,T,R,Q)) and sig(19,222)%(T*R)==0 and sig(T,18)%Q==0 and exact(P) is not None,'compelled scope')
    old=readz(RESEARCH/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']['18:16'];d,tail=domain(P,Q);right=set(old['left']);left=set(map(int,old['children']));need(tail==49 and old['q']==Q and set(d)==right|left and not right&left and right=={2,4,6,8,10,12,16},'frozen exact partition')
    need(set(z['cells'])=={'12','16'},'complete final cells')
    for j in (12,16):
        r=z['cells'][str(j)];pp=P+((Q,j),);K,O,H=r['forest'];st=C.State(pp);need(not st.fixed_euler and not st.bad and not st.conflict,'unrestricted Euler')
        C.validate_forest(st,K,O,H,prime);a=C.Forest(st,K,O,H).lower()[0];b=exact_leaf(pp,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==r['floor10'],'strict integer comparisons');print('PASS',j,r['floor10'])
    need(s==set(e),'unused prime record');print('COMPLETE second 16 under first 18 at (19,222); ECPP',len(s),'no first/key closure')

if __name__=='__main__':main()
