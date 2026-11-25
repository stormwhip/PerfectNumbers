"""Independent factor-tree replay, with every discovered factor and prime witness reverified."""
from Rough import H,R,prime,prime64,level,hashlib,I,F,load_duals,json
from Tree import Tree
from DualTree import add_test
from LeafCheck import Replay,sigma

def run(packet):
 e=packet['e'];es=list(map(int,packet['root']));chains={};used=set()
 def cert(r):
  if prime(r):return True
  k=hashlib.sha256(str(r).encode()).hexdigest()[:24];used.add(k)
  for row in packet['ecpp'][k]:
   assert row[0]==r;r=level(*row)
  return prime64(r)
 for key,v in packet['chains'].items():
  p,f=map(int,key.split(':'));rr=list(map(int,v));assert p>2 and f>=1 and len(set(rr))==len(rr) and all(cert(r) and sigma(p,f)%r==0 for r in rr);chains[p,f]=rr
 assert e>=2 and e%2==0 and len(set(es))==len(es) and all(cert(r) and sigma(5,e)%r==0 for r in es) and used==set(packet['ecpp']);ds=load_duals();Tree.extra=add_test(ds);t=Tree(e,es,35,12000);t.chains=chains;assert t.run();ps=[r for r in I.sieve_primes(20000) if r not in F];v=Replay(e,es,ps,ds,35);v.chains=chains;assert v.visit({5:e});return (e,t.st['nodes'],v.nodes)
if __name__=='__main__':
 if not __debug__:raise SystemExit('Run without -O')
 print('verified (exponent, primary nodes, independent nodes)',run(json.loads((H/'ChainPacket376.json').read_text())))
