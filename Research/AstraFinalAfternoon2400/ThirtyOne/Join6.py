"""Reconstruct a formal complete mixed (31,6) packet from disjoint local parts.

This merely constructs the candidate. --require-complete replay is mandatory.
The previously certified/aged forest structure and prime witness sets are unchanged.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json,sys

H=Path(__file__).resolve().parent
BASE=('Certificate6Extended.json.gz','e423c40be321fc55b3033669bce8944f782ee6574cf1fdb776ba48a82baa7f79')
FIRST=('Certificate6First72.json.gz','187675038b42ee59cce728fb8d5871e0d46af2eb898304c40ec684bb1da8d352')
T=917087137
P=20668766888345125939752429067

def read(spec):
 name,h=spec
 raw=(H/name).read_bytes()
 assert sha256(raw).hexdigest()==h
 z=json.loads(gzip.decompress(raw));assert (z['e'],z['pivot'])==(6,T)
 return z

def combine():
 a,b=read(BASE),read(FIRST)
 assert a['cases']['72'] is None and b['cases']['72']['q']==P
 assert sum(n is None for n in a['cases'].values())==1 and sum(n is not None for n in b['cases'].values())==1
 a['cases']['72']=b['cases']['72']
 open_rows=[];types=Counter()
 def walk(row,n):
  if n is None:open_rows.append(row);return
  types[n['type']]+=1
  if n['type']=='split':
   for h,t in n['cases'].items():walk(row+[(n['q'],int(h))],t)
 walk([(31,6),(T,72)],a['cases']['72'])
 assert open_rows==[[(31,6),(T,72),(P,16)]] and types['price6']==1
 a['cases']['72']['cases']['16']={'type':'joint6'}
 labels=set(a['ecpp']) & set(b['ecpp'])
 assert len(labels)==286 and all(a['ecpp'][z]==b['ecpp'][z] for z in labels)
 book={**a['ecpp'],**b['ecpp']};a['ecpp']={str(k):book[str(k)] for k in sorted(map(int,book))}
 return gzip.compress(json.dumps(a,separators=(',',':')).encode(),mtime=0)

if __name__=='__main__':
 assert __debug__
 raw=combine()
 path=Path(sys.argv[1]) if len(sys.argv)>1 else H/'Certificate6CompleteJoined.json.gz'
 path.write_bytes(raw)
 print(path.name,len(raw),sha256(raw).hexdigest(),flush=True)
