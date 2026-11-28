"""Independent exact-domain and historical-coverage check of the third root-222 overlay."""
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckForest222Domains import parts,live,T,U,R


def read(path):return json.loads(gzip.decompress(path.read_bytes()))


def main():
    assert __debug__
    f=R/'Nineteen/Forest222Stage3.json.gz'
    raw=f.read_bytes(); assert sha256(raw).hexdigest()=='a0082daac618fe518eb7365058024616168788abd9fd46a41d89000893a8acae'
    data=json.loads(gzip.decompress(raw)); old=read(R.parent/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']
    prior1=read(R/'Nineteen/Forest222.json.gz')['windows']; prior2=read(R/'Nineteen/Forest222Stage2.json.gz')['windows']
    inert={tuple(tuple(z) for z in row['prefix']) for row in json.loads((R/'Nineteen/Inert222.json').read_bytes())['cases']}
    scopes={}
    for item in data['cases']:
        pf=[tuple(z) for z in item['prefix']]; a,b=pf[1][1],pf[2][1]; k=f'{a}:{b}'
        assert pf[:3]==[(19,222),(T,a),(U,b)] and parts(pf) and tuple(pf) not in inert
        q,j=pf[-1]; domain,tail=live(pf[:-1],q)
        hist=old[k];assert q==hist['q'] and tail==data['windows'][k]['strict_raw_tail']
        rem=set(hist['left']); closed={int(x) for x in hist['children']}
        assert rem|closed==domain and not rem&closed
        for w in (prior1,prior2):rem-=set(w.get(k,{}).get('closed',[]))
        rem-={p[-1][1] for p in inert if list(p[:-1])==pf[:-1]}
        assert j in rem and list(sorted(rem))==data['windows'][k]['before']
        seen=scopes.setdefault(k,set());assert j not in seen;seen.add(j)
    assert scopes=={'1:2':{18},'2:16':{2,4,18,28}}
    assert data['windows']['2:16']['remaining']==[] and data['windows']['1:2']['remaining']==[16]
    print('PASS third-stage independent exact domains, first/second overlay and inert subtraction; g=16 closed at f=2')

if __name__=='__main__':main()
