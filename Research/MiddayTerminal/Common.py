"""Certificate format inputs. Nominations are not divisibility assumptions."""
import sys,math,json,gzip
from functools import cache
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent
sys.path[:0]=[str(R/'MiddayFive'),str(R/'RootFiveNext'),str(R/'Session20261122/Python')]
from PrimeCheck import level,prime64
ORDER=(19,7,11,31,13,3,5,17)
@cache
def dataset():return json.loads(gzip.decompress((H/'Base.json.gz').read_bytes()))
@cache
def chain(n):
 if n<=2:return False
 v=n
 if v>=2**64:
  for row in dataset()['ecpp'].get(str(n),[]):
   if row[0]!=v:raise ValueError('unbound ECPP')
   v=level(*row)
 return v<2**64 and prime64(v)
@cache
def bank():
 from hashlib import sha256
 archive=json.loads((R/'NightUniform/ThreeAvoid.json').read_bytes());case=archive['cases'][0];caps=dict(case['promoted']);edges=list(case['new']);proof=dict(archive['proof'])
 for tag in ('Original','Replacement'):
  raw=(R/f'Session20261122/Certificates/Terminal{tag}.json.gz').read_bytes()
  if sha256(raw).hexdigest()!=archive['archive_sha256'][tag]:raise ValueError('archive binding')
  old=json.loads(gzip.decompress(raw));edges.extend(old['edges']);proof.update(old['proofs'])
 @cache
 def prove(q):
  if q<2**64:return prime64(q)
  F=1;used=set()
  for p,k,a in proof.get(str(q),[]):
   if not(1<p<q and type(k)==int and 1<=k<=q.bit_length() and p not in used and 1<a<q and prove(p)):return False
   F*=p**k;used.add(p)
   if (q-1)%F or pow(a,q-1,q)!=1 or math.gcd(q,pow(a,(q-1)//p,q)-1)!=1:return False
  return F*F>q
 # Reproduce optional archival nominations, never use their old mask on base options.
 return {q:(max(32,min(128,caps.get(q,0))) if q<5001 else min(82,caps.get(q,0))) for q in (set(caps)|{z for p,f,z,k in edges})-{3,5,7,11,13,19,31} if prove(q)}
def init(root,e,extra,wide):
 if root not in (*ORDER,0) or (root==0)!=(e==0):raise ValueError('unsupported root')
 bad=tuple(sorted((set(ORDER[:ORDER.index(root)]) if root else set())|set(extra)))
 if any(not chain(p) for p in bad):raise ValueError('bad mask')
 if root in bad:raise ValueError('root excluded')
 V=(set(dataset()['rows'].get(f'{root}:{e}',())) if root else set())-set(bad)
 if any(not chain(p) for p in V):raise ValueError('unproved base')
 P={q:k for q,k in bank().items() if q not in bad} if wide else {}
 return bad,V,P
