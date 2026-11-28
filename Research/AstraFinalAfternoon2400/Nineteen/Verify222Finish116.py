"""Three final exact scopes under canonical root222 f1 g16."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache
from hashlib import sha256

Q=3789992812027
P=((19,222),(T,1),(R,16))

def main():
    need(__debug__,'assertions needed');prior=HERE/'Last18And1222.json.gz';need(sha256(prior.read_bytes()).hexdigest()=='15bcab2082e9d1ffd0dfb74477465629e32ba9f33e357f37601770419810b970','prior scope hash');old=readz(prior)['remaining_by_touched_secondary'];need(old['1:16']==[16,18,36],'precisely last three')
    z=readz(HERE/'Finish116x222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==P,'exact scope');e=z['ecpp'];s=set()
    @cache
    def prime(q):
        p=q;need(type(q)==int and q>2 and q%2==1,'odd prime')
        if q>=2**64:
            a=e[str(q)];need(bool(a),'empty ECPP');s.add(str(q))
            for b in a:need(b[0]==p,'incorrect ECPP subject');p=C.pc.level(*b)
        return C.pc.prime64(p)
    need(all(prime(q)for q in (19,T,R,Q)) and sig(19,222)%(T*R)==0 and sig(T,1)%(2*Q)==0 and T%4==1 and exact(P) is not None,'compelled fixed-Euler scope')
    old=readz(RESEARCH/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']['1:16'];d,tail=domain(P,Q);right=set(old['left']);left=set(map(int,old['children']));need(tail==z['raw_tail'] and old['q']==Q and set(d)==right|left and not right&left and right=={2,4,8,12,16,18,36,40,42},'frozen exact partition')
    need(set(z['cells'])=={'16','18','36'},'complete final cells')
    for j in (16,18,36):
        r=z['cells'][str(j)];pp=P+((Q,j),);K,O,H=r['forest'];st=C.State(pp);need(st.fixed_euler and not st.bad and not st.conflict,'fixed Euler only')
        C.validate_forest(st,K,O,H,prime);a=C.Forest(st,K,O,H).lower()[0];b=exact_leaf(pp,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==r['floor10'],'strict integer comparisons');print('PASS',j,r['floor10'])
    need(s==set(e),'unused prime record');print('COMPLETE second 16 under first 1 at (19,222); raw tail',tail,'ECPP',len(s),'no first/key closure')

if __name__=='__main__':main()
