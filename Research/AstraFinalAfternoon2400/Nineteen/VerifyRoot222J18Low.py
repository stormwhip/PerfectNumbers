"""Final low exact child below the (19,222) j18 packet: full fifth-pivot check."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyRoot222J18 import *

W=5642747947
S=P+((K,2),)

def main():
    need(__debug__,'assertions required')
    a=readz(HERE/'Root222J18.json.gz');need(tuple(map(tuple,a['prefix']))==P and a['pivot']==K and a['remaining']==[2],'exact preceding remainder')
    z=readz(HERE/'Root222J18Low.json.gz');need(z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and tuple(map(tuple,z['prefix']))==S and z['pivot']==W,'scope')
    E=z['ecpp'];seen=set()
    @cache
    def prime(q):
        p=q;need(type(q)==int and q>2 and q%2==1,'odd label')
        if q>=2**64:
            a=E[str(q)];need(bool(a),'empty prime witness');seen.add(str(q))
            for row in a:need(row[0]==p,'prime witness subject');p=C.pc.level(*row)
        return C.pc.prime64(p)
    need(all(prime(q)for q in (*dict(S),W)) and sig(K,2)%W==0 and exact(S) is not None,'compulsory pivot')
    d,tail=domain(S,W); need(d==list(range(2,49,2)) and tail==97 and z['raw_domain']==d,'entire fifth domain and strict tail')
    closed=set(map(int,z['children']));need(closed<=set(d) and sorted(set(d)-closed)==z['remaining'],'coverage receipt')
    def terminal(rows,v):
        X,D=exact(rows);is_ab='abundance_only' in v
        if is_ab:K=v['abundance_only']
        else:K,O,H=v['forest']
        need(len(K)==len(set(K)) and all(prime(q) and q not in dict(rows) and D%q==0 for q in K),'certified roots')
        f=sum(h%2 for _,h in rows);bad=[]
        for E,M in v['bans']:
            st=C.State(rows,absent=bad);need(not st.conflict,'mask predecessor');need(len(E)==len(set(E)) and not set(E)&set(bad),'new bans')
            I=Fraction(prod(sig(p,h)for p,h in rows),X);mins=[]
            for q in K:
                lo=val(D,q);h=lo
                while not st.possible(q,h,lo):h+=1
                mins.append([q,h]);I*=Fraction(sig(q,h),q**h)
            need(M==mins,'minimum exposure receipt')
            for q in E:
                need(prime(q) and q not in dict(rows) and D%q!=0,'uncharged absent prime');h=1 if not f and q%4==1 else 2
                need(I*Fraction(sig(q,h),q**h)>2,'strict abundance cut')
            bad+=E
        st=C.State(rows,absent=bad);need(not st.conflict,'no false mask')
        if is_ab:
            I=Fraction(prod(sig(p,h)for p,h in rows),X);mins=[]
            for q in K:
                lo=val(D,q);h=lo
                while not st.possible(q,h,lo):h+=1
                mins.append([q,h]);I*=Fraction(sig(q,h),q**h)
            need(mins==v['minima'] and I>2,'strict abundance terminal')
            return
        C.validate_forest(st,K,O,H,prime)
        a=C.Forest(st,K,O,H).lower()[0];b=exact_absence_bound(rows,K,O,H,bad,B) if bad else exact_leaf(rows,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==v['floor10'],'integer leaf')
    def visit(P,r,node):
        if 'forest' in node or 'abundance_only' in node:
            terminal(P,node);return
        q=node['pivot'];need(prime(q) and exact(P)[1]%q==0 and q not in dict(P),'nested compulsory prime')
        d0,t0=domain(P,q);need(d0==node['raw_domain'] and t0==node['raw_tail'] and set(map(int,node['children']))==set(d0),'full nested domain required')
        for h in d0:visit(P+((q,h),),r,node['children'][str(h)])
    for g in sorted(closed):
        v=z['children'][str(g)];visit(S+((W,g),),g,v);print('PASS final j18 low child',g,flush=True)
    need(seen==set(E),'unconsumed witnesses')
    print('COVER j18 low',len(closed),'of',len(d),'strict raw tail',tail,'remaining',z['remaining'],'ECPP',len(seen))

if __name__=='__main__':main()
