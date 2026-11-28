"""Independent root-19 first-18 forest replay and direct live-domain reconstruction."""
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B, split
from Check31Forest import PR, forest

T=1176672733; P=((19,276),(T,18))


def main():
    assert __debug__
    f=H.parent/'Nineteen/First18.json.gz'; raw=f.read_bytes()
    assert sha256(raw).hexdigest()=='d38b7f915e9f3110683b2a6117670c6a7a2c5c708d01e1a7b8aa27ddad537547'
    doc=json.loads(gzip.decompress(raw)); assert tuple(map(tuple,doc['prefix']))==P
    live,tail=split(P[:1],T,())
    assert (len(live),tail)==(70,188) and live[18]==P
    f=H.parents[1]/'FinalNight2400/Ten276/Cases64.json.gz'; old=f.read_bytes()
    assert sha256(old).hexdigest()=='d6c3e97838d42244f97ee4bc074719dde5bf53bba5b5718ef05ee6dd2bcf73db'
    frozen=set(map(int,json.loads(gzip.decompress(old))))
    assert len(frozen)==64 and frozen <= live.keys() and live.keys()-frozen=={1,2,8,16,18,28}
    k,o,h=doc['forest']; S=set(k)|{p for p,_ in o}|{19,T}; reached=set()
    for p in S:
        n=p
        if n>=2**64:
            key=str(n); reached.add(key); chain=doc['ecpp'][key]; assert chain
            for row in chain:
                assert row[0]==n;n=PR['level'](*row)
        assert PR['prime64'](n)
    assert reached==doc['ecpp'].keys()
    L=forest(P,dict(roots=k,owners=o,head=h),())
    assert L>B
    print('PASS independent root-19 first-18 exact domain and Euler-capacity forest: 70 live, tail188, 6 roots, 551 edges, 39 ECPP; strict lower bound')

if __name__=='__main__':main()
