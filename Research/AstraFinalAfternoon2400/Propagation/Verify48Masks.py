"""Standard-library verification of explicit 3-support bins for the t² case."""
from functools import cache
from pathlib import Path
from math import gcd,prod
from hashlib import sha256
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path[:0]=[str(H),str(H.parent/'Seven')]
from Verify48Forest import C,B,P,T,PIVOT,PUBLISH,EXTRA,prime64,level
from Verify48Price import domain
from VerifyForest import abgt2,exact_state
from Full48Eight import independently
from Propagation import sigma

BASE=[(P,48),(T,2)]

def lemma():
    assert P==7 and 3%4==11%4==3 and all(prime64(q) for q in (3,5,7,11,13,19,29,61,T))
    assert sigma(7,48)%29==sigma(T,2)%61==0 and sigma(11,2)%19==0
    a=[(7,48),(29,1),(61,1)]
    assert abgt2(a+[(3,2),(5,1)])
    assert abgt2(a+[(3,4),(11,4)])
    assert sigma(3,2)==13 and abgt2(a+[(3,2),(11,4),(13,1)])
    assert sigma(3,4)==11**2


def replay(path, expected):
    assert __debug__;lemma()
    blob=path.read_bytes();obj=json.loads(gzip.decompress(blob));assert set(obj)=={'records','ecpp'}
    seen=set(); reached=[];cert=obj['ecpp']
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        k=str(p); seen.add(k);u=p
        for s in cert[k]:assert s[0]==u;u=level(*s)
        return prime64(u)
    for row in obj['records']:
        rows=list(map(tuple,row['P'])); assert rows[:2]==BASE and all(prime(q) for q,k in rows)
        assert not row['unresolved']
        bad=tuple(row['bad']); t=row['tree']
        have=tuple(row.get('present',()));lo=dict(row.get('lo',())); outer=[x for x in rows if x[0]!=3]
        h=0
        if len(outer)==3:
            q,h=outer[-1]; assert q==PIVOT[2] and prime(q) and h in domain(BASE,q)[0]
        else:
            assert outer==BASE
        if bad==(19,3):
            assert rows==outer and not have and not lo; mode=0
        elif rows==outer+[(3,2)]:
            assert bad==(19,5,11) and not have and not lo; mode=2
        else:
            assert rows==outer and bad==(19,5,11) and have==(3,) and lo=={3:6}; mode=6
        assert exact_state(rows,bad)[0]
        reached.append((h,mode));
        assert set(t)=={'type','roots','owners','head'} and t['type']=='forest'
        r,e,Hd=(t[k] for k in ('roots','owners','head'))
        s=C.State(rows,present=have,absent=bad[1:],lo=lo); assert not s.conflict
        C.validate_forest(s,r,e,Hd,prime); assert set(have)<=set(r)
        a=C.Forest(s,r,e,Hd).lower()[0]; b=independently(rows,bad,r,e,Hd,have,lo)
        assert min(a,b)>B
        print('48 square support bin',h,mode,'digits',len(str(min(a,b)))-1,'vertices',len(r)+len(e),flush=True)
    assert reached==list(expected) and len(reached)==len(set(reached)) and seen==set(cert)
    print('PASS (7,48) support bins',reached,'ECPP',len(seen),'sha256',sha256(blob).hexdigest(),flush=True)

if __name__=='__main__':
    replay(H/'Reserved438x12-orbit48no3.json.gz',[(0,0)])
