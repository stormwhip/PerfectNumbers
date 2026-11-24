"""Independent standard-library replay of additional prime witnesses and both batch-1 leaf routines."""
from Verify import H,R,root,replay,load_duals,I,F,json,prime
from PrimeCheck import level,prime64
from PaidCheck import root
from PaidReplay import replay
from hashlib import sha256

def run(ds,packet):
 T=packet['threshold']; assert 2<=T<=10**7;ps=[r for r in I.sieve_primes(T) if r not in F];results=set();used=set()
 for s,rs in packet['exponents'].items():
  e=int(s);A=(5**(e+1)-1)//4;rs=list(map(int,rs));assert 2<=e<=2400 and not e%2
  for r in rs:
   assert r>2 and r not in F and A%r==0
   if prime(r):continue
   key=sha256(str(r).encode()).hexdigest()[:24];used.add(key);n=r
   for row in packet['ecpp'][key]:
    assert row[0]==n;n=level(*row)
   assert prime64(n)
  assert root(e,rs,ps,T,ds)['closed'] and replay(e,rs,ds,T),e;results.add(e)
 assert used==set(packet['ecpp']);return results
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not use -O')
 result=run(load_duals(),json.loads((H/'Batch5.json').read_text()));baseline=json.loads((R/'EveningMerge/Audit.json').read_text());S={s['id']:set(s['remaining_actuals']) for s in baseline['remaining_shards'] if s['root']==5};old=set(map(int,json.loads((H/'Batch1.json').read_text())));old.update(map(int,json.loads((H/'Batch2.json').read_text())['exponents']));old.update(map(int,json.loads((H/'Batch3.json').read_text())['exponents']));old.add(660);assert not old&result and result<=set.union(*S.values());print('Batch5',sorted(result),'new shards',[k for k,v in S.items() if v and v<=result|old and not v<=old]);print('cumulative',len(result|old),'remaining',len(set.union(*S.values())-(result|old)),sum(not v<=result|old for v in S.values()))
