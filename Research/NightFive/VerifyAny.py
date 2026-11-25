"""Batch 6 executable; all dependencies inside this checkout, no writing or network."""
from AnyProof import AnyTree,load_duals,I,H,json,hashlib
from AnyIndependent import check
from Refund import attach
from RefundCheck import bind
from copy import copy
from Rough import prime,prime64,level,R

ES=(250,276,268,246,240,238,232,228,210,202,198,196,190,186,178)
def verify():
 a=json.loads((H/'Batch13.json').read_text());roots=a['roots'];sec=a['secondary'];ds=load_duals();old=json.loads((I.CERT_DIR/'DualP5.json').read_text());ps=I.sieve_primes(old['R_act']);used=set()
 def primecheck(r):
  if prime(r):return True
  k=hashlib.sha256(str(r).encode()).hexdigest()[:24];rows=a['ecpp'][k];used.add(k)
  for row in rows:
   assert row[0]==r;r=level(*row)
  return prime64(r)
 for d in a['duals']:ds.append(I.verify_dual_entry(5,tuple(old['forbidden']),old['R_act'],old['W_max'],d,ps))
 entries=old['duals']+a['duals'];ds2=[bind(copy(d),v) for d,v in zip(ds,entries)];ds=[attach(d,v) for d,v in zip(ds,entries)]
 for k,rr in roots.items():
  e=int(k);assert e==int(k) and e in ES and len(set(rr))==len(rr) and all(primecheck(int(r)) and (5**(e+1)-1)//4%int(r)==0 for r in rr)
 for k,rr in sec.items():
  p,f=map(int,k.split(':'));assert p>2 and 1<=f<=I.MAX_EXPONENT and all(primecheck(int(r)) and (p**(f+1)-1)//(p-1)%int(r)==0 for r in rr)
 assert used==set(a['ecpp']);assert set(map(int,roots))==set(ES)
 for e in ES:
  t=AnyTree(e,list(map(int,roots[str(e)])),ds,sec);assert t.visit([(5,e)],12,5000),e;passed,n=check(e,roots,sec,ds2,12,5000);assert passed,e;print(e,t.nodes,n,flush=True)
 before=set(map(int,json.loads((H/'Batch1.json').read_text())));
 for j in range(2,6):before.update(map(int,json.loads((H/f'Batch{j}.json').read_text())['exponents']))
 before.update((576,616,376,592,568,460,396,388,340,528,540,286,310,318,346,360,378,408,532,562));now=before|set(map(int,roots));sh={s['id']:set(s['remaining_actuals']) for s in json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'] if s['root']==5};print('Batch13',sorted(now-before),'new shards',[k for k,v in sh.items() if v and v<=now and not v<=before]);print('remaining',len(set.union(*sh.values())-now),sum(not v<=now for v in sh.values()))
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 verify()
