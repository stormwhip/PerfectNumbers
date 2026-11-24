"""Certify two fresh, nonnegative flow-price vectors with the baseline exact verifier; replay the simple fractional-gift bounds twice."""
from Verify import H,R,root,replay,load_duals,I,F,json

def verify():
 a=json.loads((H/'Batch4.json').read_text());assert a['threshold']==10**6 and a['exponents']=={'660':[]};ds=load_duals();base=json.loads((I.CERT_DIR/'DualP5.json').read_text());ps=I.sieve_primes(base['R_act'])
 for d in a['duals']:ds.append(I.verify_dual_entry(5,tuple(base['forbidden']),base['R_act'],base['W_max'],d,ps))
 T=a['threshold'];e=660;pr=[r for r in I.sieve_primes(T) if r not in F];assert root(e,[],pr,T,ds)['closed'] and replay(e,[],ds,T);old=set(map(int,json.loads((H/'Batch1.json').read_text())))
 for pack in ('Batch2.json','Batch3.json'):old.update(map(int,json.loads((H/pack).read_text())['exponents']))
 S={s['id']:set(s['remaining_actuals']) for s in json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'] if s['root']==5};assert e not in old and e in set.union(*S.values());print('Batch4',e,'new shards',[k for k,v in S.items() if v and v<=old|{e} and not v<=old]);print('cumulative remaining',len(set.union(*S.values())-old-{e}),sum(not v<=(old|{e}) for v in S.values()))
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not run with -O')
 verify()
