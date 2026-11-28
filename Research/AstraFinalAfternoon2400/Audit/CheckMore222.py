"""Independent exact-domain and forest replay for three finished (19,222) second fibers."""
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
R=H.parent/'Nineteen'; T=7579985624053; U=3705121363; Q=3789992812027
TARGET={(1,40),(18,42),(18,46)}

def z(path):return json.loads(gzip.decompress(path.read_bytes()))

def main():
    assert __debug__
    pack=(R/'More222.json.gz').read_bytes()
    assert sha256(pack).hexdigest()=='75e22e331489a04cf1ddd17f52c471bfddad3b684bb64f3d7493a071eaf224dd'
    obj=json.loads(gzip.decompress(pack)); frozen=R.parents[1]/'FinalNight2400/Root222'
    x=z(frozen/'TwoForests.json.gz')['cases']; y=z(frozen/'ThirdForests.json.gz')['cases']; primes=set(); seen=set(); terms=0
    root=((19,222),); initial,tail=split(root,T,()); assert len(initial)==53 and tail==144
    for o in obj['cases']:
        row=tuple(map(tuple,o['prefix']));f,g=row[1][1],row[2][1]
        assert row==root+((T,f),(U,g)) and (f,g) in TARGET and (f,g) not in seen
        assert split(initial[f],U,())[0][g]==row and str(g) not in x[str(f)] and f'{f}:{g}' not in y
        seen.add((f,g))
        if f==1:
            leaves,tail=split(row,Q,()); assert leaves.keys()==set(range(2,43,2)) and tail==86
            assert set(map(int,o['children']))==leaves.keys()
            cases=[(v,o['children'][str(e)]) for e,v in leaves.items()]
        else:cases=[(row,o)]
        for p,data in cases:
            k,edge,h=data['forest']; primes|=set(k)|{v for v,_ in edge}|dict(p).keys()
            assert forest(p,dict(roots=k,owners=edge,head=h),())>B;terms+=1
    used=set()
    for p in primes:
        if p>=2**64:
            key=str(p); used.add(key); e=obj['ecpp'][key]; assert e
            for row in e:assert row[0]==p;p=PR['level'](*row)
        assert PR['prime64'](p)
    assert seen==TARGET and terms==23 and len(used)==203 and used==obj['ecpp'].keys()
    print('PASS three independent scopes, entire 21-child / raw86 subdomain, 23 strict forests and 203 ECPP')

if __name__=='__main__':main()
