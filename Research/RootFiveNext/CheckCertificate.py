"""Offline public verifier for the minimized root-5 certificate. Python stdlib, no network."""
import argparse,json
from functools import cache
from hashlib import sha256
from PrimeCheck import prime64,level,check
from LeafCheck import Replay,I,H,F,sigma
from DualTree import add_test,load_duals
from Tree import Tree
from GapIndependent import replay as independent_gap
from GapDual import root as gap_root
from Shards import delta

def verify(pack):
 check((pack['version'],pack['root'],pack['target_digits'])==(1,5,2400),'wrong scope'); used=set()
 @cache
 def certprime(n):
  if n<2**64:return prime64(n)
  h=sha256(str(n).encode()).hexdigest()[:24];rows=pack['ecpp'][h];q=n;used.add(h)
  for row in rows:
   check(row[0]==q,'invalid ECPP chain');q=level(*row)
  return prime64(q)
 ds=load_duals();check(max(d.mu for d in ds)<=7500,'unexpected dual bank');Tree.extra=add_test(ds);ps=[p for p in I.sieve_primes(20000) if p not in F|{2,5}];es=pack['exponents'];g=set(pack['gap']);check(es==sorted(set(es)) and g<=set(es),'mismatched exponent sets');chains={}; results={}
 for tag,cs in pack['chains'].items():
  p,f=map(int,tag.split(':'));vs=list(map(int,cs));check(p>2 and f>=1 and len(vs)==len(set(vs)),'bad chain key');check(all(certprime(r) and sigma(p,f)%r==0 for r in vs),'bad chain factors');chains[p,f]=vs
 for e in es:
  check(e>=2 and e%2==0,'incorrect exponent parity');rs=list(map(int,pack['root_factors'][str(e)]));check(all(certprime(r) and sigma(5,e)%r==0 for r in rs),'bad root factor');check(len(rs)==len(set(rs)),'duplicate root divisor');
  if e in g:
   check(gap_root(e,rs,ds)['closed'] and independent_gap(e,rs,ds),'gap failure '+str(e));results[e]={'method':'gap','valuation_values':e+1}
  else:
   tr=Tree(e,rs,20,15000);tr.chains=chains;check(tr.run(),'primary factor-tree failure '+str(e));rr=Replay(e,rs,ps,ds,20);rr.chains=chains;check(rr.visit({5:e}),'independent factor-tree failure '+str(e));results[e]={'method':'tree','primary_nodes':tr.st['nodes'],'independent_nodes':rr.nodes}
 d=delta(set(es));check(d['exponents']==es,'claimed exponent not on input frontier');check(used==set(pack['ecpp']),'unused ECPP certificate');return dict(base_open=1045,root=5,complete_actuals=len(es),complete_shards=len(d['shards']),**d,methods=results,ecpp=len(used))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',default='RootFiveCertificate.json');ap.add_argument('--emit',action='store_true');ap.add_argument('--result',default='RootFiveVerified.json');a=ap.parse_args();out=verify(json.loads((H/a.certificate).read_text()));s=json.dumps(out,indent=1)+'\n'
 if a.emit:(H/a.result).write_text(s)
 else:check(s==(H/a.result).read_text(),'archived result differs')
 print('root 5:',out['complete_actuals'],'complete actual exponents;',out['complete_shards'],'new official shards;',out['ecpp'],'ECPP chains')
if __name__=='__main__':main()
