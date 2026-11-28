"""Verify nine root-11/13 forest subdomains against a separate parity-capacity DP."""
from functools import cache
import gzip
import hashlib
import json
from math import gcd,prod
from pathlib import Path
import subprocess
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B, BASE, split
from Check31Forest import PR, forest
P=H.parent/'ElevenThirteen'
ORDER=(19,7,11,31,13,3,5,17)

# Source-specific factor labels for the Pocklington chain; repeat all primality arithmetic.
POCK={100641220283951395639601683:(342317075795753046393203,),
      342317075795753046393203:(34781251350919838081,),
      34781251350919838081:(35291471,1539910457)}


def main():
    assert __debug__
    raw=(P/'Forests.json.gz').read_bytes()
    d=json.loads(gzip.decompress(raw))
    expect=json.loads((P/'ForestCoverage.json').read_bytes())
    assert d['rows'].keys()==expect.keys() and len(expect)==9
    historic=json.loads(subprocess.check_output(['git','show',f'{BASE}:Research/FinalNight2400/OpenFrontier.json']))
    old=json.loads(subprocess.check_output(['git','show',f'{BASE}:Research/FinalNight2400/Results.json']))
    old2=json.loads(subprocess.check_output(['git','show',f'{BASE}:Research/GeminiFrontier/November28/Results.json']))
    actual_keys={tuple(k) for v in historic['ShardRemainders'].values() for k in v}
    rowscope={tuple(map(int,k.split(':'))) for k in expect}
    assert rowscope<=actual_keys
    print('Prior FinalNight rows for audited keys:',[(r['Key'],r['Status'],r.get('ProofReference')) for r in old if tuple(r['Key']) in rowscope],flush=True)
    assert not any(tuple(r['Key']) in rowscope for r in old2['Entries'])
    used=set()
    @cache
    def cert(n):
        if n<2**64:
            assert PR['prime64'](n)
        elif n in POCK:
            factors=POCK[n]
            f=prod(factors)
            assert len(set(factors))==len(factors) and f*f>n and (n-1)%f==0 and pow(2,n-1,n)==1
            for q in factors:
                cert(q)
                assert gcd(pow(2,(n-1)//q,n)-1,n)==1
        else:
            key=str(n)
            used.add(key)
            steps=d['ecpp'][key]
            assert steps
            for step in steps:
                assert step[0]==n
                n=PR['level'](*step)
            assert PR['prime64'](n)
    total=0
    for k,rr in expect.items():
        p,e=map(int,k.split(':'))
        q=rr['pivot']
        cert(p);cert(q)
        bans=ORDER[:ORDER.index(p)]
        domain,tail=split(((p,e),),q,bans)
        out=d['rows'][k]
        accepted=sorted(map(int,out))
        assert list(map(str,accepted))==list(map(str,rr['accepted']))
        assert sorted(domain.keys()-set(accepted))==rr['remaining']
        assert set(accepted)<=domain.keys()
        floors=[]
        for f in accepted:
            leaf=out[str(f)]
            for b in (*leaf['roots'],*(b for b,_ in leaf['owners'])):
                cert(b)
            bound=forest(domain[f],leaf,bans)
            assert bound>B,(k,f)
            floors.append(len(str(bound))-1)
        print(k,'pivot',q,'tail',tail,'full local',len(accepted),'/',len(domain),'minimum integer floor',min(floors),flush=True)
        total+=len(accepted)
    assert used==d['ecpp'].keys()
    print('PASS independent domain + arithmetic; distinct ECPP',len(used),'conditional fibers',total,'SHA256',hashlib.sha256(raw).hexdigest(),flush=True)


if __name__=='__main__':
    main()
