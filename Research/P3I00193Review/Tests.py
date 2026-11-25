"""Adversarial certificate checks, total-multiplicity regression, frozen-ledger isolation."""
import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ReplayCandidate import HERE, INPUT, load_model, pools
from VerifyDualRational import logs, verify
from VerifyPartial import power,B
import check


def rejected(fn):
    try:
        fn()
    except (AssertionError,ValueError):
        return
    raise AssertionError('mutated certificate accepted')


def run():
    c=json.loads((INPUT/'P3E1162Complete.json').read_text())
    row=json.loads((HERE/'RebuiltDual.json').read_text())
    leaf=c['cell10'][row['leaf_index']]
    u,_=pools(leaf)
    absent={7,11,13,19,31}|set(leaf['absent_extra'])
    req=F(row['required_abundance_candidate'])
    verify(row['lp'],absent,u,req)
    bad=copy.deepcopy(row['lp']);bad['u_dual']=[1,1]
    rejected(lambda:verify(bad,absent,u,req))
    bad=copy.deepcopy(row['lp']);bad['sel_dual'][str(bad['P'][0])]=[-1,1]
    rejected(lambda:verify(bad,absent,u,req))
    bad=copy.deepcopy(row['lp']);bad['inf_dual'][0][3]=100000
    rejected(lambda:verify(bad,absent,u,req))
    m=load_model()
    rejected(lambda:m.verify_partition([],[],[5],[17,23,29,37,41]))
    # Exact shared-factor regression from the previous audit.
    from math import gcd
    a,b=12754929700003,15469435877248501
    assert gcd(a,b)==13567 and check.prime64(13567)
    for h in range(2,5000,2):
        assert check.valuation(h+1,3)<=h//2
    assert logs(2)[0]>F(2,3) and logs(2)[1]<F(7,10)
    for a in [2,5,37,43,3**1162]:
        for n in [0,1,2,5,12,100]:
            assert power(a,n)==min(B+1,a**n)
    assert power(2,B.bit_length()+1)==B+1
    replay=json.loads((HERE/'ReplayResults.json').read_text())
    for name,digest in replay['frozen'].items():
        assert hashlib.sha256((HERE.parent/'Midday'/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==digest
    for name in ['ReplayResults.json','PartialResults.json','RebuiltDual.json','RationalDualResults.json']:
        assert json.loads((HERE/name).read_text())['accepted_actuals']==[]
    assert len(replay['leaves'])==42
    assert replay['source_enumeration_verified'] and replay['source_primes_expanded']==5829
    manifest=json.loads((HERE/'InputManifest.json').read_text())
    for entry in manifest['files']:
        raw=(HERE/entry['stored']).read_bytes().replace(b'\r\n',b'\n')
        assert hashlib.sha256(raw).hexdigest()==entry['sha256_lf']
    assert hashlib.sha256((INPUT/'OriginalBundle.zip').read_bytes()).hexdigest()==manifest['original_zip_sha256']
    delta=json.loads((HERE.parent/'Midday'/'Delta.json').read_text())
    open_actuals={(s['root'],e) for s in delta['remaining_shards'] for e in s['remaining_actuals']}
    assert {(3,e) for e in [856,970,990,1108,1162]}<=open_actuals
    print('PASS: rational dual; 3 hostile mutations; incomplete partition; shared-factor regression; frozen ledger; empty acceptance')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Assertions must be enabled')
    run()
