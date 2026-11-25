"""Read-only packet integrity manifest generator; exact proof still uses Verify.py."""
import gzip
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent
for f in sorted(H.glob('*.pack.json.gz')):
    b=f.read_bytes(); packet=json.loads(gzip.decompress(b))
    rs=[dict(p=r['p'],e=r['e'],roots=len(r['roots']),owners=len(r['owners']),head=r['head'],den=r.get('den',1)) for r in packet['rows']]
    print(json.dumps(dict(file=f.name,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),rows=rs,chains=len(packet['ecpp']))))
