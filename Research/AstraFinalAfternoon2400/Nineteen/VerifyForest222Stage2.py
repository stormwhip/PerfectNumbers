"""Verify a disjoint second-stage forest overlay on the sealed root 222 packet."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from VerifyForest222 import *
from Pock import verify


def main():
    need(__debug__,'assertions required')
    hp=RESEARCH/'FinalNight2400'/'Root222'; old=hp/'ThirdForests.json.gz'; prior=HERE/'Forest222.json.gz'
    C0=readz(old)['cases'];C1=readz(prior)['windows'];C2=readz(hp/'TwoForests.json.gz')['cases']
    packet=readz(HERE/'Forest222Stage2.json.gz')
    need(packet['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984' and packet['status']=='CONDITIONAL_FOREST222_STAGE2','baseline or packet status')
    need(hashlib.sha256(old.read_bytes()).hexdigest()==packet['thirds_sha256'],'frozen data hash')
    need(hashlib.sha256(prior.read_bytes()).hexdigest()==packet['prior_sha256']=='4f5d3a750a8f1d6bc120e6e2217157172f146ffd3c0d7df6a9924997e0941440','prior data hash')
    ecc=packet['ecpp'];pok=packet['pock'];eu=set();pu=set()
    @cache
    def prime(q):
        need(type(q)==int and q>2 and q%2==1,'odd prime input')
        p=q;k=str(q)
        if p>=2**64:
            if k in pok:return verify(p,pok,C.pc.prime64,pu)
            seq=ecc[k];need(bool(seq),'missing chain');eu.add(k)
            for t in seq:need(t[0]==p,'wrong ECPP subject');p=C.pc.level(*t)
        return C.pc.prime64(p)
    need(all(prime(q) for q in (19,T,R)),'fixed primes')
    win={};seen=set()
    for s in packet['cases']:
        p=tuple(tuple(x)for x in s['prefix']);need(len(p)in (3,4) and p not in seen and exact(p) is not None,'not a new live exact prefix');seen.add(p)
        f,g=p[1][1],p[2][1];k=f'{f}:{g}'
        need(p[0]==(19,222) and p[1][0]==T and p[2][0]==R and f in (1,2,18) and (f,g)!=(1,58),'scope')
        first,tail=domain(p[:1],T);need(len(first)==53 and tail==144 and f in first,'complete first raw window')
        second,_=domain(p[:2],R);need(g in second and str(g) not in C2[str(f)],'live second before frozen third')
        h=C0.get(k);q,j=p[3] if len(p)==4 else (None,None)
        if q is None:
            need(h is None and k not in C1,'second window must be unresolved and unrefined')
            before=None;tail=None
        else:
            need(prime(q) and isinstance(h,dict) and h['q']==q,'certified frozen third pivot')
            d,tail=domain(p[:3],q);frozen=set(h['left']);closed=set(map(int,h['children']))
            need(set(d)==frozen|closed and not frozen&closed,'complete raw third window')
            earlier=set(C1.get(k,{}).get('closed',[]));need(earlier<=frozen,'prior scope')
            before=sorted(frozen-earlier-({40,42} if (f,g)==(1,16) else {1} if (f,g) in ((2,16),(2,22)) else set()))
            need(j in before,'overlaps a frozen or stage1 cut')
        w=win.setdefault(k,dict(pivot=q,before=before,raw_tail=tail,closed=[]))
        need((w['pivot'],w['before'],w['raw_tail'])==(q,before,tail),'duplicate or change of pivot')
        w['closed'].append(j)
        K,O,N=s['forest'];st=C.State(p);need(not st.conflict and st.bad==(),'canonical state')
        C.validate_forest(st,K,O,N,prime)
        v=C.Forest(st,K,O,N).lower()[0];z=exact_leaf(p,K,O,N)
        need(min(v,z)>B and [floor10(v),floor10(z)]==s['floor10'],'strict forest terminal')
        print('PASS root222 stage2',p,'floor10',s['floor10'],flush=True)
    for w in win.values():w['closed'].sort();w['after']=[] if w['before'] is None else sorted(set(w['before'])-set(w['closed']))
    need(eu==set(ecc) and pu==set(pok),'unused prime certificate')
    need(win==packet['windows'],'coverage receipt mismatch')
    print('COVER',len(seen),'new leaves;',sum(not w['after'] for w in win.values()),'closed second windows; ECPP',len(eu),'Pocklington',len(pu))
    print(json.dumps(win,sort_keys=True),flush=True)

if __name__=='__main__':main()
