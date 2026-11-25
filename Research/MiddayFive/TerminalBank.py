"""Extended terminal background. Incorporate promoted authenticated archival
prime labels; all used output multiplicities are derived anew by division."""
from Joint import *
from hashlib import sha256

def banklabels():
 path=R/'NightUniform/ThreeAvoid.json';auth=json.loads(path.read_bytes());promoted=dict(auth['cases'][0]['promoted']);edges=auth['cases'][0]['new'][:];proofs={str(k):v for k,v in auth['proof'].items()}
 for label in ['Original','Replacement']:
  raw=(R/f'Session20261122/Certificates/Terminal{label}.json.gz').read_bytes();assert sha256(raw).hexdigest()==auth['archive_sha256'][label];arc=json.loads(gzip.decompress(raw));proofs.update(arc['proofs']);edges.extend(arc['edges'])
 base=set(promoted)|set(z for q,f,z,h in edges);caps={p:max(32,min(128,promoted.get(p,0))) if p<5001 else min(82,promoted.get(p,0)) for p in base if p not in set(BAD)|{5}};return caps,proofs
@cache
def labels():return banklabels()
@cache
def pock(n):
 if type(n) is not int or n<2:return False
 if n<2**64:return prime64(n)
 rows=labels()[1].get(str(n));prod0=1;seen=set()
 if not rows:return False
 for q,k,a in rows:
  if not (type(q)==type(k)==type(a)==int and 1<q<n and q not in seen and 0<k<=n.bit_length() and 1<a<n and pock(q)):return False
  seen.add(q);prod0*=q**k
  if (n-1)%prod0 or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//q,n)-1,n)!=1:return False
 return prod0**2>n

def specs():return {q:c for q,c in labels()[0].items() if pock(q)}
if __name__=='__main__':print(len(labels()[0]),len(specs()),sum(specs().values()))
