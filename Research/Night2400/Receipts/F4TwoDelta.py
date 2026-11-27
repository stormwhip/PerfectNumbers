"""Extract new exact first f2 after checking prior F4 subtree and proof identity."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path('Research/Night2400/F4')
def load(name,h):
    raw=(H/name).read_bytes();assert sha256(raw).hexdigest()==h
    return json.loads(gzip.decompress(raw))
a=load('ReviewOldPacket.json.gz','4cde99ecee143874fa6609c5858bb9c5f83673ee213c619c452ddd433beeefde')
b=load('Fibers19x282.json.gz','0a1561392e8142d0d178322e5422d61646bffb7494904d153e90bd8269d91d8b')
assert set(a)==set(b)=={'p','e','pivot','cases','ecpp'}
assert all(a[k]==b[k] for k in ('p','e','pivot'))
assert set(a['cases'])=={'4','8','16','28','30','36'}
assert set(b['cases'])-set(a['cases'])=={'2'} and all(b['cases'].get(k)==v for k,v in a['cases'].items())
assert all(b['ecpp'].get(k)==v for k,v in a['ecpp'].items())
n=b['cases']['2'];used={str(b['pivot'])} if b['pivot']>=2**64 else set()
def collect(t):
    if t['type']=='split':
        if t['q']>=2**64:used.add(str(t['q']))
        for w in t['cases'].values():collect(w)
    else:
        assert t['type']=='forest'
        used.update(str(q) for q in set(t['roots'])|set(dict(t['owners'])) if q>=2**64)
collect(n)
assert set(b['ecpp'])-set(a['ecpp'])<=used
out=dict(p=b['p'],e=b['e'],pivot=b['pivot'],cases={'2':n},ecpp={k:b['ecpp'][k] for k in sorted(used)})
p=Path(sys.argv[1]);assert not p.exists();p.write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0))
print('new chains',len(set(b['ecpp'])-set(a['ecpp'])),'chains in extracted proof',len(used),'extracted SHA256',sha256(p.read_bytes()).hexdigest())
