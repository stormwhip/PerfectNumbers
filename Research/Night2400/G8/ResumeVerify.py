"""Exact follow-up for the one remaining f=6 prefix; pins and replays the old packet."""
from pathlib import Path
from functools import cache
from hashlib import sha256
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
import MaskedVerify as V

PREFIX=[(13,508),(4073,6),(3032394642737237,4)]
BASE_HASH='d798580b1e3e4760bcb67da93e5f9c37611ef1997d543e4a6d904a0d722c9680'

def main():
    if not __debug__:raise RuntimeError('assertions required')
    base=H/'Thirteen508.json.gz'
    assert sha256(base.read_bytes()).hexdigest()==BASE_HASH
    pending=V.verify(base)
    raw=(H/'Resume6.json.gz').read_bytes();d=json.loads(gzip.decompress(raw))
    assert set(d)=={'roots','owners','head','ecpp'}
    seen=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        n=q
        if q>=2**64:
            rows=d['ecpp'][str(q)];assert rows
            for row in rows:assert row[0]==n;n=V.C.pc.level(*row)
            seen.add(str(q))
        assert V.C.pc.prime64(n);return True
    assert all(prime(q) for q,_ in PREFIX) and V.live(PREFIX,V.BASE_BAN)
    s=V.C.State(PREFIX);k,o,h=map(d.get,('roots','owners','head'))
    V.C.validate_forest(s,k,o,h,prime)
    a=V.C.Forest(s,k,o,h).lower()[0];b=V.second(PREFIX,(),V.BASE_BAN,k,o,h)
    v=min(a,b);assert v>V.B and seen==set(d['ecpp'])
    affected=[]
    for mask,values in pending.items():
        if 6 not in values:continue
        assert values.pop(6)==(tuple(PREFIX),)
        affected.append(mask)
    assert affected==[16,48,112,176]
    assert all(set(values)=={108} for values in pending.values())
    print('FOLLOW-UP', 'full new fiber',6,'affected masks',affected,'forest floor',V.floor10(v),'remaining',108,'masks',sorted(pending),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':main()
