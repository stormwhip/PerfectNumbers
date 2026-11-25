"""Strict root-node dual: sieve rough cofactor to T, pay its even sources at L<=4 log T; track the maximum theta deletion exactly."""
import sys,json,argparse,math,time,hashlib
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'RootFiveNext'))
from DualTree import I,S,LP,B,abhi,lnlo,point,load_duals,J
from PrimeCheck import prime64,level
from Tree import ok
F={2,3,5,7,11,13,19,31};cachepath=R.parents[1]/'upstream/Research/RootFiveNext';pack=json.loads((R/'RootFiveNext/RootFiveCertificate.json').read_text()); logB=I.LN_B_HI
@cache
def prime(r):
 if r<2**64:return prime64(r)
 key=hashlib.sha256(str(r).encode()).hexdigest()[:24]; rows=pack['ecpp'].get(key)
 if rows is None:return False
 for row in rows:
  if row[0]!=r:raise ValueError('ECPP mismatch')
  r=level(*row)
 return prime64(r)

def parts(A,rs,ps):
 u=A;dc={}
 for r in set(rs).union(ps):
  if u%r:continue
  c=0
  while u%r==0:u//=r;c+=1
  dc[r]=c
 return dc,u

def root(e,rs,ps,T,duals):
 P=5**(e+1);pe=P//5;A=(P-1)//4;dc,u=parts(A,rs,ps);num=I.ilog(u,T);target=I.LN2_LO-abhi(5)-sum(abhi(r) for r in dc)-num*abhi(T);terms=[];known=rough=False; Tlo=lnlo(T);xs={r:lnlo(r) for r in dc}
 for d in duals:
  L=min(d.lam_p*LP,4*Tlo) if u>1 else d.lam_p*LP
  line=lnlo(pe*A)+d.mu*target+d.const_no_target-sum(th for r,th in d.theta_map.items() if A%r==0)-(num*L+3)//4
  payments={r:point(r,c,False,L) for r,c in dc.items()};base=line+sum(payments.values());deltas=[point(r,c,True,L)-payments[r] for r,c in dc.items() if point(r,c,True,L) is not None];known|=not deltas or base+min(deltas)+L*e>logB
  rough|=u==1 or base+L*(e-min(e,I.ilog(u+1,5)+J,e//2+J))>logB
  terms.append((base,L,d,payments))
 open1=[];openh=[];fails={}; margins=[]
 for s in range(e+1):
  y=5**s;Q=max(5,2*y-1);lq=lnlo(Q);k=e-s
  def cost(row):
   base,L,d,pm=row;aq=(S+Q-2)//(Q-1); lost=min(d.delta_q,d.mu*aq) if Q>10**18 else d.delta_q
   return base+L*k-lost
  rows=[(cost(row),row[2],row[3]) for row in terms];high=max(lnlo(3125),max(0,5*s-5)*LP)
  if max(base+L*k+high-d.delta_q for base,L,d,pm in terms)<=logB:openh.append(s)
  if max(b+lq for b,d,pm in rows)>logB:continue
  if not s or 32*pe*Q**6<243*B:open1.append(s);fails[s]='source supply';continue
  den=max(P,Q)*(P//y+4);t=max(0,den.bit_length()-28);denhi=I.log_interval((den>>t)+1)[1]+t*I.LN2_HI;joint=lnlo(Q*Q*y)-denhi
  ext=max(b+2*lq+I.log_interval(2,3)[0]-d.delta_src for b,d,pm in rows);ur=max(b+joint for b,d,pm in rows) if u>1 else 10*logB
  kn=10*logB
  for r,c in dc.items():
   f=2*((c+1)//2)
   while 3*r**f<=2*Q or not ok(r,f):f+=2
   kn=min(kn,max(b+max(joint,lq+(f-c)*xs[r])-pm[r] for b,d,pm in rows))
  m=min(ext,ur,kn);margins.append(m-logB)
  if m<=logB:open1.append(s);fails[s]=['external','rough','known'][(ext,ur,kn).index(m)]
 from collections import Counter
 from GapDual import intervals
 return dict(e=e,closed=known and rough and not open1 and not openh,known=known,rough=rough,one=intervals(open1),higher=intervals(openh),first=None if not open1 else [open1[0],fails[open1[0]]],counts=dict(Counter(fails.values())),rough_digits=len(str(u)),forced=[str(r) for r in sorted(dc)],minmargin=min(margins,default=0)/S)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--threshold',type=int,default=10**5);ap.add_argument('--min',type=int,default=500);ap.add_argument('--output',default='RoughAudit.json');args=ap.parse_args();ds=load_duals();assert max(d.mu for d in ds)<=7500; T=args.threshold;ps=[r for r in I.sieve_primes(T) if r not in F]; es=sorted({e for s in json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'] if s['root']==5 for e in s['remaining_actuals']},reverse=True);cs=json.loads((cachepath/'Candidates.json').read_text());rows=[]
 for e in es:
  if e<args.min:continue
  rs=[int(r) for r in cs[str(e)] if prime(int(r))];row=root(e,rs,ps,T,ds);rows.append(row);print(e,row['closed'],row['one'],row['first'],flush=True)
 (H/args.output).write_text(json.dumps(rows,indent=1)+'\n')
if __name__=='__main__':main()
