"""Independent per-root rational-coupon additive bound for weighted forest. Input validation delegates only label/ECPP and schema checks."""
from WeightedReplay import H,B,I,R,proof,verify,sys,json,gzip,math,cache
from LeafCheck import block,lower_pow,ln_low,max_ab,sigma

def second(row):
 mu=row['mu'];T=row['T'];e=row['e'];U0=sigma(5,e);P=tuple(row['roots']);F={3,7,11,13,19,31};small=[p for p in I.sieve_primes(T) if p>2 and p not in F|{5}];debt={p:max(0,mu*max_ab(p)-lower_pow(p,1,False)*ln_low(p)) for p in small};odddebt=max([0]+[max(0,mu*max_ab(p)-debt[p]-ln_low(p)) for p in small if lower_pow(p,1,True) is not None]);debit=sum(debt.values())+odddebt;comp=math.prod(small)*5*U0*math.prod(q for q,z in row['owners']);children={}
 for q,z in row['owners']:children.setdefault(z,[]).append(q)
 def vp(n,p):
  u=0
  while n%p==0:n//=p;u+=1
  return u
 def strip(n):
  while (g:=math.gcd(n,comp))>1:n//=g
  return n
 # Compute a rational multiplier directly, without the first implementation's fixed-point beta ceiling.
 num=T*ln_low(T)-mu*I.SCALE;den=T*ln_low(T);assert num>=0
 @cache
 def calc(z,c,sp):
  f=lower_pow(z,c,sp)
  if f is None:return None
  def bare(f):return max(0,f*ln_low(z)-mu*max_ab(z)+debt.get(z,0))
  a=b=10**26
  for _ in range(row['head']):
   if bare(f)>=max(a,b):break
   y=sigma(z,f)//(2 if sp else 1);cost=bare(f)+ln_low(strip(y))*num//den;rebate=0
   for q in children.get(z,[]):
    d=vp(y,q)
    if d:
     nor,flex=calc(q,d,False);o=calc(q,d,True);cost+=nor;rebate=max(rebate,nor-min(flex,o[0]) if o else nor-flex)
   a=min(a,cost);b=min(b,cost-rebate);f+=(4 if sp else 2)
   while not block(z,f):f+=(4 if sp else 2)
  return min(a,bare(f)),min(b,bare(f))
 cs={z:vp(U0,z) for z in P};modes=[0]+[z for z in P if calc(z,cs[z],True) is not None];base=e*ln_low(5)+mu*(I.LN2_LO-max_ab(5))-debit;vals=[]
 for special in modes:
  qv=[calc(z,cs[z],special==z) for z in P];bound=base+sum(n for n,m in qv);vals.append(bound-max([0]+[n-m for n,m in qv]) if not special else bound)
 return min(vals)
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 d=json.loads(gzip.decompress((H/sys.argv[1]).read_bytes()));
 for r in d['rows']:
  proof(r,d['ecpp']);a=verify(r);b=second(r);assert min(a,b)>I.LN_B_HI;print('weighted root five',r['e'],a//I.LN10_HI,b//I.LN10_HI)
