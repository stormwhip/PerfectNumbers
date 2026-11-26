"""Verify the descriptive TSV against the current JSON ledger. Numerical discovery scores do not enter the certificate proof."""
from pathlib import Path
from math import isqrt
import csv,json
H=Path(__file__).resolve().parent;S=(19,7,11,31,13,3,5,17)

def run():
    d=json.loads((H/'Delta.json').read_bytes());keys={(s['root'],e) for s in d['remaining_shards'] for e in s['remaining_actuals']};seen=set()
    with (H/'OpenFrontier.tsv').open(encoding='utf8',newline='') as f:
        for r in csv.DictReader(f,delimiter='\t'):
            p,e=int(r['p']),int(r['e']);assert (p,e) in keys and (p,e) not in seen;seen.add((p,e));ids=[s['id'] for s in d['remaining_shards'] if s['root']==p and e in s['remaining_actuals']];assert sorted(ids)==sorted(r['shards'].split(','));nums=lambda key:[int(t) for t in r[key].split(',') if t]
            assert nums('forbidden')==list(S[:S.index(p)]) and nums('indices')==[i for i in range(2,e+2) if (e+1)%i==0]
            A=(p**(e+1)-1)//(p-1)
            for q in nums('known_small_prime_divisors'):
                assert 2<q<10**6 and q%2 and all(q%j for j in range(2,isqrt(q)+1)) and A%q==0
                while A%q==0:A//=q
            assert A.bit_length()==int(r['unchecked_remainder_bits'])
    assert keys==seen;print('PASS diagnostic frontier projection:',len(keys),'distinct unresolved pairs')
if __name__=='__main__':
    if not __debug__:raise SystemExit('do not run with -O')
    run()
