"""Independently rebuild and verify exact Stage3 root222 coverage."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import *
from Pock import verify


def main():
    need(__debug__,'assertions enabled')
    hp=RESEARCH/'FinalNight2400'/'Root222'; old=hp/'ThirdForests.json.gz'
    initial=readz(old)['cases']; C2=readz(hp/'TwoForests.json.gz')['cases']; one=HERE/'Forest222.json.gz'; two=HERE/'Forest222Stage2.json.gz'
    packet=readz(HERE/'Forest222Stage3.json.gz');e=packet['ecpp'];p=packet['pock'];eu=set();pu=set()
    need(packet['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and packet['status']=='CONDITIONAL_FOREST222_STAGE3','root scope')
    need(hashlib.sha256(one.read_bytes()).hexdigest()=='4f5d3a750a8f1d6bc120e6e2217157172f146ffd3c0d7df6a9924997e0941440','stage1 digest')
    need(hashlib.sha256(two.read_bytes()).hexdigest()=='10688cbd5ecab9ca8fbd88ffc3c61a454f86febcdac43289359685a037f6dae0','stage2 digest')
    C1=readz(one)['windows'];C3=readz(two)['windows']
    @cache
    def prime(q):
        need(type(q)==int and q>2 and q%2==1,'odd prime label')
        k=str(q);n=q
        if q>=2**64:
            if k in p:return verify(q,p,C.pc.prime64,pu)
            eu.add(k);seq=e[k];need(bool(seq),'empty ECPP chain')
            for row in seq:need(row[0]==n,'bad chain subject');n=C.pc.level(*row)
        return C.pc.prime64(n)
    need(all(prime(q) for q in (19,T,R)),'fixed primes')
    seen=set();windows={}
    for s in packet['cases']:
        P=tuple(tuple(x)for x in s['prefix']);need(len(P)==4 and P not in seen and exact(P) is not None,'live leaf');seen.add(P)
        f,g=P[1][1],P[2][1];q,j=P[3];tag=f'{f}:{g}';need(P[:3]==((19,222),(T,f),(R,g)) and (f,g) in {(1,2),(2,16)},'scoped path')
        fdom,ft=domain(P[:1],T);gdom,gt=domain(P[:2],R);tdom,tt=domain(P[:3],q)
        need(ft==144 and len(fdom)==53 and f in fdom and g in gdom and str(g) not in C2[str(f)],'root/second coverage')
        h=initial[tag];base=set(h['left']);removed=set(map(int,h['children']));need(prime(q) and h['q']==q and set(tdom)==base|removed and not base&removed,'frozen third coverage')
        before=sorted(base-set(C1.get(tag,{}).get('closed',[]))-set(C3.get(tag,{}).get('closed',[]))-({1} if (f,g)==(2,16) else set()))
        need(j in before,'nonoverlapping leaf'); w=windows.setdefault(tag,dict(pivot=q,before=before,strict_raw_tail=tt,closed=[]));w['closed'].append(j)
        K,O,H=s['forest'];st=C.State(P);need(st.bad==() and not st.conflict,'silent scope change')
        C.validate_forest(st,K,O,H,prime); a=C.Forest(st,K,O,H).lower()[0];b=exact_leaf(P,K,O,H)
        need(min(a,b)>B and [floor10(a),floor10(b)]==s['floor10'],'strict leaf proof');print('PASS stage3',P,s['floor10'],flush=True)
    need((eu,pu)==(set(e),set(p)),'unbound prime record')
    for w in windows.values():w['closed'].sort();w['remaining']=sorted(set(w['before'])-set(w['closed']))
    need(windows==packet['windows'],'windows receipt mismatch')
    print('COVER',len(seen),'new terminals;',sum(not w['remaining'] for w in windows.values()),'completed second window; ECPP',len(eu),'Pocklington',len(pu));print(json.dumps(windows,sort_keys=True),flush=True)

if __name__=='__main__':main()
