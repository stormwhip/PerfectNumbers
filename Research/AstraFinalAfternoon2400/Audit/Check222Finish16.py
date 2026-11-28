"""Independent frozen/supplementary exact joins and five strict final forests at g16."""
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
N=H.parent/'Nineteen'; T=7579985624053; R=3705121363

def z(p):return json.loads(gzip.decompress(p.read_bytes()))

def main():
    assert __debug__
    hist=z(N.parents[1]/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']; overlays=[z(N/i)['windows'] for i in ('Forest222.json.gz','Forest222Stage2.json.gz','Forest222Stage3.json.gz')]
    later=z(N/'Last18And1222.json.gz'); checked=0
    for f,q,name,jj,count,hash0 in ((1,3789992812027,'Finish116x222',{16,18,36},52,'030b00a6d8c6f270e7dc6090e298330d842bcefc3a8df60a00c060da2ee6f487'),(18,108501737266216818637411,'Finish1816x222',{12,16},8,'d2ac154068b225c2ca6374cd2adaac32c85a2563f73f2f5c51f03b55104be466')):
        raw=(N/(name+'.json.gz')).read_bytes();assert sha256(raw).hexdigest()==hash0
        d=json.loads(gzip.decompress(raw)); p=((19,222),(T,f),(R,16));assert p==tuple(map(tuple,d['prefix']))
        k=f'{f}:16'; all_e,t=split(p,q,()); prior=set(hist[k]['left']);assert set(all_e)==prior|{int(j) for j in hist[k]['children']} and hist[k]['q']==q
        earlier=set().union(*(set(o.get(k,{}).get('closed',[])) for o in overlays))
        if f==1: # Frozen Gemini B certificate.
            earlier|={40,42}
        earlier|={r['prefix'][-1][1] for r in later['cases'] if tuple(map(tuple,r['prefix'][:-1]))==p}
        assert prior-earlier==jj and set(map(int,d['cells']))==jj
        pp=set();used=set()
        for e in jj:
            roots,edges,cap=d['cells'][str(e)]['forest'];row=all_e[e]; pp|=dict(row).keys()|set(roots)|{q for q,_ in edges}
            assert forest(row,dict(roots=roots,owners=edges,head=cap),())>B;checked+=1
        for q in pp:
            if q>=2**64:
                name=str(q);used.add(name);steps=d['ecpp'][name];assert steps
                for r in steps:assert r[0]==q;q=PR['level'](*r)
            assert PR['prime64'](q)
        assert used==d['ecpp'].keys() and len(used)==count
        print('PASS exact residual join and independently strict terminal DP',f,16,sorted(jj),'tail',t,'ECPP',count,flush=True)
    assert checked==5

if __name__=='__main__':main()
