from pathlib import Path
import json,hashlib,collections
H=Path(__file__).resolve().parent;names='Score.py Masked.py EulerGroup.py ForceQ.py VerifyQ.py Q2J2.json Q2J6.json CertJ2.json CertJ6.json Price12.py Win12.py Verify12.py Packet12.json Cert12.json Multi4.py SquareLast.py Verify4.py Pack4.json Cert4.json CompleteLow.py Full430.py Proof2.md Proof4.md Proof12.md'.split()
for name in names:
 b=(H/name).read_bytes();print(name,len(b),hashlib.sha256(b).hexdigest())
a=json.loads((H/'Pack4.json').read_bytes());c=collections.Counter()
def walk(n):
 c[n['type']]+=1
 for t in n.get('cases',{}).values():walk(t)
walk(dict(type='split',cases=a['cases']));print(dict(c))
