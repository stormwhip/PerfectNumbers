"""Independent finite domain and parity-capacity replays for three first-18 scopes."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import B,split
from Check31Forest import PR,forest
T,R,Q=7579985624053,3705121363,108501737266216818637411
P=((19,222),(T,18)); source=H.parent/'Nineteen'

def load(p):return json.loads(gzip.decompress(p.read_bytes()))

def main():
    assert __debug__
    f=source/'Extra18x222.json.gz';raw=f.read_bytes();assert sha256(raw).hexdigest()=='6bbeb54c6a1ee3a538cf073f938565a97537ee8a0293a5a7950292fc72da850d'
    d=json.loads(gzip.decompress(raw));orig=source.parents[1]/'FinalNight2400/Root222'
    thirds=load(orig/'ThirdForests.json.gz')['cases'];seconds=load(orig/'TwoForests.json.gz')['cases']['18']
    groups=[load(source/name)['windows'] for name in ('Forest222.json.gz','Forest222Stage2.json.gz')]
    used=set();labelset=set();seen=set()
    for rec in d['cases']:
        row=tuple(map(tuple,rec['prefix']));assert row[:2]==P
        p,g=row[2];assert p==R and str(g) not in seconds and split(P,R,())[0][g]==row[:3]
        if len(row)==3:
            assert g==12 and f'18:{g}' not in thirds;j=None
        else:
            assert row[3]==(Q,4);j=4;k=f'18:{g}';hist=thirds[k]
            live,tail=split(row[:3],Q,());assert live[j]==row and hist['q']==Q and live.keys()==set(hist['left'])|{int(h) for h in hist['children']}
            assert j in set(hist['left'])-set().union(*(set(m.get(k,{}).get('closed',[])) for m in groups))
        assert (g,j) not in seen;seen.add((g,j));roots,edges,head=rec['forest'];labelset|=dict(row).keys()|set(roots)|{u for u,_ in edges}
        assert forest(row,dict(roots=roots,owners=edges,head=head),())>B
    for q in labelset:
        if q>=2**64:
            k=str(q);used.add(k); steps=d['ecpp'][k];assert steps
            for s in steps:assert s[0]==q;q=PR['level'](*s)
        assert PR['prime64'](q)
    assert seen=={(12,None),(2,4),(22,4)} and used==d['ecpp'].keys() and len(used)==140
    print('PASS independent exact split scope/strict forests, new g12 and g2/g22 j4 only, 140 ECPP')

if __name__=='__main__':main()
