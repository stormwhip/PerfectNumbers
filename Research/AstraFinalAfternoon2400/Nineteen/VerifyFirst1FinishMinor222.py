"""Two full second branches and one third branch under canonical (19,222), first exponent 1."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,sig,need,T,R,exact_leaf
from functools import cache

P=((19,222),(T,1));Q=3789992812027;A=12223575034313786292211
EXPECTED={4:(A,list(range(2,41,2)),81),46:(Q,list(range(2,39,2)),77)}

def main():
    need(__debug__,'assertions required')
    z=readz(HERE/'First1Minor222.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984','scope')
    src=RESEARCH/'FinalNight2400/Root222';second=readz(src/'TwoForests.json.gz')['cases']['1'];third=readz(src/'ThirdForests.json.gz')['cases'];ec=z['ecpp'];used=set();seen=set();n=0
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd eligible label')
        if q>=2**64:
            c=ec[str(q)];need(bool(c),'missing ECPP chain');used.add(str(q))
            for a in c:need(a[0]==q,'incorrect prime subject');q=C.pc.level(*a)
        return C.pc.prime64(q)
    need(all(prime(q)for q in (19,T,R,Q,A)) and sig(19,222)%(T*R)==0 and T%4==1 and sig(T,1)%(2*Q)==0,'forced prefix and Euler')
    gd,tt=domain(P,R)
    def terminal(S,h):
        nonlocal n
        n+=1;K,O,H=h['forest'];s=C.State(S);need(not s.conflict and s.fixed_euler and not s.bad and exact(S) is not None,'fixed Euler mode')
        C.validate_forest(s,K,O,H,prime);a=C.Forest(s,K,O,H).lower()[0];b=exact_leaf(S,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==h['floor10'],'dual strict forest terminal')
        print('PASS f1 minor',tuple(j for _,j in S[2:]),h['floor10'],flush=True)
    for node in z['cases']:
        S=tuple(map(tuple,node['prefix']));g=S[2][1];tag=f'1:{g}';need(S[:2]==P and S[2][0]==R and exact(S) is not None and g in gd and str(g) not in second and g not in seen,'frozen live scope');seen.add(g)
        if g in EXPECTED:
            need(len(S)==3 and tag not in third,'unrefined second');q,vs,tail=EXPECTED[g];d,k=domain(S,q);need(node['pivot']==q and d==vs and k==tail and set(map(int,node['children']))==set(d),'complete original strict window')
            for j in d:terminal(S+((q,j),),node['children'][str(j)])
        else:
            need(g==22 and S==P+((R,22),(Q,18)),'one targeted third residual')
            row=third[tag];d,k=domain(S[:3],Q);x=set(row['left']);y=set(map(int,row['children']));need(row['q']==Q and 18 in x and set(d)==x|y and not x&y,'live original third scope');terminal(S,node)
    need(seen=={4,22,46} and n==40 and used==set(ec),'exact whole and prime inventory')
    print('COMPLETE two second windows [4,46]; one exact third at g22,j18; strict terminal count',n,'ECPP',len(used))

if __name__=='__main__':main()
