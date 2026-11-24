"""No network, no writes. python -B Research/NightFive/Verify.py [packet ...]"""
import sys
from Rough import H,R,I,root,load_duals,prime,F,json
from Replay import replay

def verify(packet,ds):
 a=json.loads(packet.read_text());T=a.get('threshold',100000);a=a.get('exponents',a); es=set();ps=[r for r in I.sieve_primes(T) if r not in F];assert 2<=T<=10**7
 for key,items in a.items():
  e=int(key);A=(5**(e+1)-1)//4;rs=list(map(int,items));assert e>0 and e%2==0 and all(prime(r) and A%r==0 for r in rs) and len(rs)==len(set(rs));v=root(e,rs,ps,T,ds);assert v['closed'] and replay(e,rs,ds,T),('not closed',e);es.add(e)
 return es
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not run with -O')
 ds=load_duals(); es=set.union(*(verify(H/packet,ds) for packet in (sys.argv[1:] or ['Batch1.json'])));manifest=json.loads((R/'EveningMerge/Audit.json').read_text());shards={s['id']:set(s['remaining_actuals']) for s in manifest['remaining_shards'] if s['root']==5};base=set.union(*shards.values());assert len(shards)==77 and len(base)==102 and es<=base;print('root 5: proven',sorted(es),'closed shards',sorted(k for k,v in shards.items() if v and v<=es),'remaining actuals',len(base-es))
