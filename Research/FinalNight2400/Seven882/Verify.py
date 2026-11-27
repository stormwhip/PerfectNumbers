from Domain import *
def run(f,partial=False):
 assert __debug__ and f in piv;g=json.loads(gzip.decompress((H/f'Packet{f}.json.gz').read_bytes()));book=g['ecpp'];seen=set();stats=[0,0,0];opens=[]
 @cache
 def prime(q):
  assert type(q)==int and q>2;y=q
  if q>=2**64:
   seen.add(str(q))
   for row in book[str(q)]:assert row[0]==y;y=C.pc.level(*row)
  assert C.pc.prime64(y);return True
 assert prime(7) and prime(Q) and C.valuation(C.sigma(*ROOT),Q)==1 and g['first']==f
 def walk(row,t):
  u=state(row);assert not u.conflict and u.base<=B
  if t['type']=='open':assert partial;opens.append(tuple(row));stats[2]+=1;return
  if t['type']=='split':
   q=t['q'];assert prime(q);cs=domain(row,q);assert set(cs)==set(t['cases']),(row,q,set(cs)^set(t['cases']));stats[0]+=1
   for h,r in cs.items():walk(r,t['cases'][h])
  else:
   assert t['type']=='forest';k=t['roots'];o=t['owners'];h=t['head'];C.validate_forest(u,k,o,h,prime);assert C.Forest(u,k,o,h).lower()[0]>B;stats[1]+=1
 walk([ROOT,(Q,f)],g['tree']);assert set(book)==seen;print('certified (7,882) first',f,'splits/strict forests/open',stats,'ECPP',len(book),flush=True);return opens
if __name__=='__main__':
 for f in map(int,sys.argv[1:]):assert not run(f)
