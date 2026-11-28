"""Independent exact current-fiber and strict terminal replay for twelve final conditional scopes."""
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
R=H.parent/'Nineteen'; T=7579985624053; U=3705121363
QS={1:3789992812027,18:108501737266216818637411}
EXPECTED={(1,16):{2,4,8,12},(1,22):{4},(18,2):{6},(18,16):{2,4,6,10},(18,22):{2,12}}

def read(p):return json.loads(gzip.decompress(p.read_bytes()))

def main():
    assert __debug__
    raw=(R/'Last18And1222.json.gz').read_bytes();assert sha256(raw).hexdigest()=='15bcab2082e9d1ffd0dfb74477465629e32ba9f33e357f37601770419810b970'
    d=json.loads(gzip.decompress(raw));hist=read(R.parents[1]/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']
    first=read(R/'Forest222.json.gz')['windows'];second=read(R/'Forest222Stage2.json.gz')['windows'];extra=read(R/'Extra18x222.json.gz')['cases'];minor=read(R/'First1Minor222.json.gz')['cases']
    already={tuple(map(tuple,o['prefix'])) for o in extra+minor};used=set();ps=set(); seen={}
    for x in d['cases']:
        r=tuple(map(tuple,x['prefix'])); f,g,j=[e for _,e in r[1:]]; q=QS[f]; k=f'{f}:{g}'
        assert r==((19,222),(T,f),(U,g),(q,j)) and r not in already and j in EXPECTED[f,g]
        hs,tail=split(r[:-1],q,()); w=hist[k];lc=set(w['left']);other={int(h) for h in w['children']}
        assert hs[j]==r and w['q']==q and hs.keys()==lc|other and not lc&other
        assert j in lc-set(first.get(k,{}).get('closed',[]))-set(second.get(k,{}).get('closed',[]))
        seen.setdefault((f,g),set()); assert j not in seen[f,g];seen[f,g].add(j)
        roots,owners,head=x['forest'];ps|=dict(r).keys()|set(roots)|{z for z,_ in owners}
        assert forest(r,dict(roots=roots,owners=owners,head=head),())>B
    for p in ps:
        if p>=2**64:
            k=str(p);used.add(k); c=d['ecpp'][k];assert c
            for rr in c:assert rr[0]==p;p=PR['level'](*rr)
        assert PR['prime64'](p)
    assert seen==EXPECTED and used==d['ecpp'].keys() and len(used)==440
    print('PASS independent 12 exact live and disjoint root19 third restrictions; 440 ECPP, strict forest DP on every row')

if __name__=='__main__':main()
