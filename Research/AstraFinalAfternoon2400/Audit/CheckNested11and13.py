"""Independent branching and parity-capacity recurrences for five sealed complete first fibers."""
from functools import cache
from hashlib import sha256
import gzip,json,runpy,sys
from math import gcd,prod
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path[:0]=[str(H),str(H.parent/'ElevenThirteen')]
from Check31Forest import PR, forest
from Check31Domains import B, split
from Check11and13Forest import ORDER, POCK
P=H.parent/'ElevenThirteen'
BOOK=(('Second-11-16-13.json.gz',(11,16,13),(4,1),'a7b772587e78e66d57060cb99f25b52ab052e84ded7a64987f31eb677b0a0b10'),
      ('Second-11-16-26.json.gz',(11,16,26),(57,2),'49d9f7a2ed23a932c6306e5cfb1fd2321c6906b19bfe70d9e0c91846ff2cdef1'),
      ('Second-11-18-9.json.gz', (11,18,9), (11,1),'176c08f4cfa07b1b8a584befff0aa9896a6704db93599c9f28891a5e4c1238ea'),
      ('Second-11-48-14.json.gz',(11,48,14),(60,4),'908928cf20efd980dde706fc84a530aa6cbb75e9d39a59c079fe255718e31e54'),
      ('Second-11-48-24.json.gz',(11,48,24),(2,1),'3ee3625ce0d17793a7863683a12086f21eb8d00351df28a8815ac6d0539a4dc3'),
      ('Second-11-48-26.json.gz',(11,48,26),(6,1),'b04ae4c4efc4f4c16cb31a9793cdd3376fc8e71f19e8962a6df019e26cb4dcd0'),
      ('Second-11-48-32.json.gz',(11,48,32),(66,3),'6563528ad1a8c10fb443d733c465c978e6309fafbe68ed0a950f41c56e4b4bd5'),
      ('Second-13-6-124.json.gz',(13,6,124),(37,3),'43ae206135da77f89f9266a40699ab6ca523a17ad510cfa1aaa1a8929c39ed68'),
      ('Second-13-6-150.json.gz',(13,6,150),(19,2),'b0bd453d6bca069b3921c5670e4926851cb9f1affa8ba760b179124082d8ebcb'))


def verify():
    assert __debug__
    current=json.loads((P/'ForestCoverage.json').read_bytes())
    additions=runpy.run_path(str(P/'SupplementalPrimes.py'))
    base=runpy.run_path(str(P/'Coverage.py'))
    for name,key,expected,digest in BOOK:
        raw=(P/name).read_bytes(); assert sha256(raw).hexdigest()==digest
        d=json.loads(gzip.decompress(raw)); r=d['row']; p,e,f=key; assert key==(r['p'],r['e'],r['f'])
        before=current[f'{p}:{e}']; q=before['pivot']; assert f in before['remaining']
        bans=ORDER[:ORDER.index(p)];domain,tail=split(((p,e),),q,bans)
        assert f in domain
        certs=d['ecpp']; seen=set()
        @cache
        def authenticate(z):
            if z<2**64:assert PR['prime64'](z);return
            if str(z) in certs:
                seen.add(str(z)); entries=certs[str(z)];assert entries
                for step in entries:
                    assert step[0]==z; z=PR['level'](*step)
                assert PR['prime64'](z);return
            if z in POCK:
                F=prod(POCK[z]);assert F*F>z and (z-1)%F==0 and pow(2,z-1,z)==1
                for p0 in POCK[z]:
                    authenticate(p0);assert gcd(pow(2,(z-1)//p0,z)-1,z)==1
                return
            assert (z in additions['CERT'] and additions['prime_extra'](z)) or (z in base['POCK'] and base['prime'](z))
        authenticate(p);authenticate(q)
        leaves=branches=0;min_cost=None
        def walk(rows,t):
            nonlocal leaves,branches,min_cost
            if 'split' in t:
                z=t['split'];authenticate(z);c,_=split(rows,z,bans)
                assert set(c)==set(map(int,t['cases']));branches+=1
                for h1 in c:walk(c[h1],t['cases'][str(h1)])
            else:
                for z in [*t['roots'],*(z for z,_ in t['owners'])]:authenticate(z)
                v=forest(rows,t,bans);assert v>B;leaves+=1
                min_cost=v if min_cost is None else min(min_cost,v)
        walk(domain[f],r['tree'])
        assert (leaves,branches)==expected and seen==certs.keys()
        print('PASS independent complete first fiber',key,'initial strict tail',tail,'nested',branches,'strict forests',leaves,'ECPP',len(seen),'floor',len(str(min_cost))-1,flush=True)

if __name__=='__main__':verify()
