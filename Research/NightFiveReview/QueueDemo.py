"""Stateless chunk replay and fail-closed merger demo, real e=196 Any root.
Coordinator directly reruns local verifications in this demo: JSON True or digest is NOT evidence.
This is a coverage primitive, not a scheduler or a new trusted primality implementation.
"""
from LocalModel import *
import hashlib
class Reject(ValueError):pass
def need(x,why):
 if not x:raise Reject(why)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def domain(x,p):
 X=math.prod(r**f for r,f in x);S=math.prod(sig(r,f) for r,f in x);D=S//math.gcd(S,2*X);d=D;c=0
 while d%p==0:d//=p;c+=1
 need(c and math.gcd(D,X*2*bad)==1,'pivot not forced or state contradictory');vals=[];lim=B//(X*d);pw=p**c;f=c;eu=any(k%2 for r,k in x)
 while pw<=lim:
  if (f%2==0 or (not eu and f%4==p%4==1)) and not math.gcd(sig(p,f),bad)>1:vals.append(f)
  pw*=p;f+=1
 return vals
class Budget(Model):
 def state(self,x):
  if self.stats['nodes']>=self.limit:raise Reject('OPEN/budget exhausted')
  return super().state(x)
def seal(packet,x,p,ds,scope,chunks,limit):
 vals=domain(x,p);seen=set();work=0
 for task in chunks:
  need(task['id']==digest([scope,task['indices']]),'scope or indices changed');s=task['indices'];need(s and all(type(i) is int and 0<=i<len(vals) for i in s),'out of range');need(not seen.intersection(s) and len(s)==len(set(s)),'overlap');seen.update(s)
 need(seen==set(range(len(vals))),'gap');
 for task in chunks:
  for i in task['indices']:
   tr=Budget(x[0][1],packet,ds);tr.limit=limit;need(tr.any([*x,(p,vals[i])]),'OPEN/no proof');work+=tr.stats['nodes']
 return work
if __name__=='__main__':
 c=json.loads((R/'IndicatorCapacity/Certificates/DualP5.json').read_text());a=json.loads((NF/'Batch13.json').read_text());ds=[Bank(v,c['R_act'],primes(c['R_act'])) for v in c['duals']+a['duals']];x=[(5,196)];p=max(map(int,a['roots']['196']));ctx=digest(['any/v1',str(B),F,x,str(p),a,c,hashlib.sha256(Path(__file__).with_name('LocalModel.py').read_bytes()).hexdigest(),hashlib.sha256(Path(__file__).read_bytes()).hexdigest()]);vals=domain(x,p);job=lambda s:{'indices':s,'id':digest([ctx,s])};jobs=[job(list(range(i,len(vals),3))) for i in range(3)];print('exponents',vals,'split root into',len(jobs),'chunks;',seal(a,x,p,ds,ctx,jobs,1000),'subtree nodes');
 for tag,ch,cap in [('gap',jobs[1:],1000),('overlap',jobs+jobs[:1],1000),('omit odd 1',[job(list(range(1,len(vals))))],1000),('stale hash',[dict(jobs[0],id='stale')]+jobs[1:],1000),('cap',jobs,0)]:
  try:seal(a,x,p,ds,ctx,ch,cap)
  except Reject as ex:print('rejected',tag,str(ex))
  else:raise AssertionError(tag)
