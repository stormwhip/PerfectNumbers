"""Exact directed fixed-point forest/abundancy certificate. No binary floating-point numbers in any acceptance test."""
from FiveForestReplay import proof,B,H,valuation,nonsupport,sigma,check,R
from functools import cache
import gzip,json,sys,math
sys.path.insert(0,str(H.parent/'IndicatorCapacity'));import VerifyIndicatorCapacity2400 as I

def verify(row):
 p=row['p'];e=row['e'];T=row['T'];mu=row['mu'];P=set(row['roots']);parents=dict(row['owners']);assert p==5 and type(T)==int and 1000<=T<=100000 and type(mu)==int and 0<=mu<=10000;A=sigma(5,e);zv={z:valuation(A,z) for z in P};assert math.prod(z**k for z,k in zv.items())==A;forb=R[:R.index(p)];S=I.SCALE;cap=I.LN_B_HI
 @cache
 def low(x):
  shift=max(0,x.bit_length()-36);return I.log_interval(x>>shift)[0]+shift*I.LN2_LO
 @cache
 def abundance(z):return (S+z-2)//(z-1) if z>20000 else I.log_interval(z,z-1)[1]
 small=[q for q in I.sieve_primes(T) if q not in {2,5,*forb}];neg={q:max(0,mu*abundance(q)-I.get_f_min(q,forb)*low(q)) for q in small};euler=max([0]+[max(0,mu*abundance(q)-neg[q]-low(q)) for q in small if q%4==1 and all((q+1)%b for b in forb)]);constant=-sum(neg.values())-euler
 # Choose rational beta=ceil(mu S^2/(T*lnlo(T)))/S. For any z>T the loss mu ln(z/(z-1)) <= beta ln z and also <= beta*h ln z for h>=1.
 beta=(mu*S*S+T*low(T)-1)//(T*low(T));assert beta<=S;U=5*A*math.prod(parents)*math.prod(small);children={z:[] for z in set(parents)|P}
 for q,z in parents.items():children[z].append(q)
 def odd(z):return z%4==1 and all((z+1)%b for b in forb)
 @cache
 def node(z,c,mode):
  if mode==1:return min(node(z,c,3),node(z,c,2)) if odd(z) else node(z,c,3)
  sp=mode==2;f=c+((1-c)%4 if sp else c%2);step=4 if sp else 2;delta=neg.get(z,0)-mu*abundance(z);best=10**26;i=0
  while i<row['head']:
   start=max(0,f*low(z)+delta)
   if start>=best:break
   if not I.sigma_has_forb(z,f,forb):
    y=sigma(z,f)//(2 if sp else 1);rough=nonsupport(y,U);value=start+(S-beta)*low(rough)//S;credit=0
    for q in children[z]:
     h=valuation(y,q)
     if h:
      full=node(q,h,0);value+=full
      if mode==3:credit=max(credit,full-node(q,h,1))
    best=min(best,value-credit);i+=1
   f+=step
  while I.sigma_has_forb(z,f,forb):f+=step
  return min(best,max(0,f*low(z)+delta))
 vals=[node(z,zv[z],0) for z in P];full=e*low(5)+constant+mu*(I.LN2_LO-abundance(5))+sum(vals);return full-max([0]+[v-node(z,zv[z],1) for z,v in zip(P,vals)])
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 d=json.loads(gzip.decompress((H/sys.argv[1]).read_bytes()));
 for r in d['rows']:
  proof(r,d['ecpp']);b=verify(r);assert b>I.LN_B_HI;print(r['e'],b//I.LN10_HI,'certified floor')
