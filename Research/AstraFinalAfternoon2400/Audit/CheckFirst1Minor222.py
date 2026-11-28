"""Independent exact forests for two final second scopes and one third scope at (19,222)."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
R=H.parent/'Nineteen'; T=7579985624053; U=3705121363
Q=3789992812027; A=12223575034313786292211
P=((19,222),(T,1));expected={4:(A,set(range(2,41,2)),81),46:(Q,set(range(2,39,2)),77)}

def load(p):return json.loads(gzip.decompress(p.read_bytes()))

def main():
    assert __debug__ and T%4==1
    raw=(R/'First1Minor222.json.gz').read_bytes();assert sha256(raw).hexdigest()=='27f7e65fd61c50012452b48e8c04a99cf52175359aef61d2f2131e9f41324586'
    a=json.loads(gzip.decompress(raw)); based=R.parents[1]/'FinalNight2400/Root222'
    old=load(based/'ThirdForests.json.gz')['cases'];sec=load(based/'TwoForests.json.gz')['cases']['1'];N=0
    reached=set();scopes=set();labels=set()
    for rec in a['cases']:
        row=tuple(map(tuple,rec['prefix']));p,g=row[2];assert p==U and row[:2]==P and g not in scopes
        assert str(g) not in sec and split(P,U,())[0][g]==row[:3];scopes.add(g)
        if g in expected:
            q,hs,t=expected[g];assert len(row)==3 and f'1:{g}' not in old and rec['pivot']==q
            c,tail=split(row,q,());assert c.keys()==hs and tail==t and set(map(int,rec['children']))==hs
            tests=[(v,rec['children'][str(h)]) for h,v in c.items()]
        else:
            assert g==22 and row[3]==(Q,18)
            c,tail=split(row[:3],Q,());hist=old['1:22'];assert c[18]==row and hist['q']==Q and 18 in hist['left']
            assert c.keys()==set(hist['left'])|{int(h) for h in hist['children']}
            tests=[(row,rec)]
        for p,k in tests:
            a0,b0,c0=k['forest'];labels|=dict(p).keys()|set(a0)|{q for q,_ in b0}
            assert forest(p,dict(roots=a0,owners=b0,head=c0),())>B;N+=1
    for p in labels:
        if p>=2**64:
            k=str(p);reached.add(k); book=a['ecpp'][k];assert book
            for s in book:assert s[0]==p;p=PR['level'](*s)
        assert PR['prime64'](p)
    assert scopes=={4,22,46} and reached==a['ecpp'].keys() and len(reached)==159 and N==40
    print('PASS independent exact even children tails 81/77, one g22,j18 scope, 40 strict forests, 159 ECPP')

if __name__=='__main__':main()
