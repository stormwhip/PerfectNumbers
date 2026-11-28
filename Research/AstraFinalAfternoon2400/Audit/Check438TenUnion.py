"""Independent frozen/new set reconciliation for the full first v_t=10 fiber."""
import gzip
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from CheckSevenForestDomains import sig, split
from Check438ReserveDomains import main as reserve_rule

R=Path(__file__).resolve().parents[1]
OLD=R.parent/'FinalNight2400/SevenNext'
T=572749682520506652634407616247
P=[(7,438),(T,10)]


def unpack(path):return json.loads(gzip.decompress(path.read_bytes()))


def main():
    assert __debug__
    reserve_rule()
    ds,tail=split(P,{19},67)
    candidates=set(ds)
    assert candidates==set(range(2,301,2))
    frozen_a=set(range(228,293,2))
    # Membership of the three later frozen proofs is read from their exact
    # data, not from the applicant's current union table.
    old=unpack(OLD/'New438Credits.json.gz')
    # SevenNext/Verify438New.py binds these exact stored codes to v_t=10.
    frozen_b=set(map(int,old['nodes']['67']))
    frozen_c=set(map(int,unpack(OLD/'Mixed67Primes.json.gz')['nodes']['67']))
    frozen_d=set(map(int,unpack(OLD/'Mixed67More.json.gz')['nodes']['67']))
    hist=set()
    for part in (frozen_a,frozen_b,frozen_c,frozen_d):
        assert part <= candidates and not hist&part
        hist.update(part)
    assert len(hist)==72 and candidates-hist==set(range(2,159,2))-{148}
    union=set()
    for tag in 'abcdefgh':
        path=R/f'Seven/Forest438{tag}.json.gz'; data=unpack(path); vals=set()
        for row in data['records']:
            prefix=[tuple(x) for x in row['P']]; h=prefix[-1][1]
            assert not row['unresolved'] and row['bad']==[19] and h not in vals and prefix==ds.get(h)
            vals.add(h)
            if tag >= 'd':
                n=row['tree']; assert n['type']=='reserve'
                V=set(n['roots'])|{z for z,_ in n['owners']}
                assert all(q%(4*T**9)!=2*T**9-1 for q in V)
        assert vals and not (vals&(hist|union))
        union |= vals
        print(tag, len(vals),sha256(path.read_bytes()).hexdigest(),flush=True)
    assert len(union)==78 and hist|union==candidates
    print('PASS independent first-10 union:',tail,'raw tail;',len(candidates),'live, 72 frozen + 78 new, no open exact children')

if __name__=='__main__':main()
