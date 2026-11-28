"""Verify a deep exact (19,222) j18 cover, permitting explicit and locally proved masks."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import RESEARCH,HERE,C,B,exact,domain,readz,floor10,val,sig,need,T,R,exact_leaf
sys.path.insert(0,str(RESEARCH/'Night2400/A'))
from MaskedForest import exact_absence_bound
from functools import cache
from fractions import Fraction
from math import prod,gcd

Q=2032322226061
K=45031669
P=((19,222),(T,2),(R,22),(Q,18))

def raw(P,q,bad=()):
    D,tail=domain(P,q)
    return [a for a in D if gcd(sig(q,a),prod(bad))==1],tail

def main():
    need(__debug__,'assertions required')
    n=readz(HERE/'Root222J18.json.gz');need(n['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,n['prefix']))==P and n['pivot']==K,'exact scope')
    A=RESEARCH/'FinalNight2400/Root222';old=readz(A/'ThirdForests.json.gz')['cases']['2:22']
    D,tail=domain(P[:3],Q);left=set(old['left']);cov=set(map(int,old['children']));need(old['q']==Q and tail==114 and set(D)==left|cov and not left&cov and left=={1,2,4,18,28},'frozen third window')
    e=n['ecpp'];seen=set()
    @cache
    def prime(p):
        q=p;need(type(p)==int and p>2 and p%2==1,'odd prime')
        if p>=2**64:
            a=e[str(p)];need(bool(a),'empty certificate');seen.add(str(p))
            for row in a:need(row[0]==q,'changed certificate subject');q=C.pc.level(*row)
        return C.pc.prime64(q)
    need(all(prime(q)for q in (*dict(P),K)) and sig(19,222)%(T*R)==0 and sig(T,2)%Q==0 and sig(T,2)%K==0 and exact(P) is not None,'mandatory prime proof')
    def leaf(p,v):
        K,O,H=v['forest'];X,D=exact(p);need(all(prime(z) and z not in dict(p) and D%z==0 for z in K),'true compulsory roots')
        f=sum(a%2 for _,a in p);bad=[]
        for entries,hh in v.get('derive_bans',[]):
            need(bool(entries) and len(entries)==len(set(entries)) and not set(entries)&set(bad),'unique new mask batch')
            I=Fraction(prod(sig(z,a)for z,a in p),X);m=[]
            for q in K:
                h0=val(D,q);u=h0;s=C.State(p,absent=bad);need(not s.conflict,'valid earlier state')
                while not s.possible(q,u,h0):u+=1
                m.append([q,u]);I*=Fraction(sig(q,u),q**u)
            need(m==hh,'minimum exposure')
            for q in entries:
                need(prime(q) and q not in dict(p) and D%q!=0 and q not in K,'uncharged proposed absent prime')
                u=1 if q%4==1 and not f else 2
                need(I*Fraction(sig(q,u),q**u)>2,'strict abundance exclusion')
            bad.extend(entries)
        st=C.State(p,absent=bad);need(not st.conflict and set(st.bad)==set(bad),'mask not justified');C.validate_forest(st,K,O,H,prime)
        a=C.Forest(st,K,O,H).lower()[0];b=exact_absence_bound(p,K,O,H,bad,B) if bad else exact_leaf(p,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==v['floor10'],'strict terminal')
        return a,b
    DD,tt=domain(P,K);need(len(DD)==47 and tt==126 and DD==n['domain'],'complete fourth-pivot domain')
    covered=set(map(int,n['children']));need(covered<=set(DD) and sorted(set(DD)-covered)==n['remaining'],'explicit remainders')
    for h in sorted(covered):
        v=n['children'][str(h)];p=P+((K,h),);a,b=leaf(p,v);print('PASS j18 child',h,'floor10',v['floor10'],flush=True)
    need(seen==set(e),'unconsumed prime records')
    print('COVER j18',len(covered),'of',len(DD),'strict tail',tt,'remaining',n['remaining'],'ECPP',len(seen))

if __name__=='__main__':main()
