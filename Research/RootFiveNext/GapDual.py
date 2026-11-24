"""Internal/external Euler emitter gap + verified removed-node dual on forced root factors."""
import argparse,math,json
from DualTree import H,I,S,LP,J,B,lnlo,abhi,point,load_duals
from Tree import proved,check,PR,F

def intervals(seq):
 z=[]
 for x in seq:
  if z and z[-1][-1]+1==x:z[-1][-1]=x
  else:z.append([x,x])
 return z

def root(e,rs,duals):
 P=5**(e+1);pe=P//5;A=(P-1)//4;u=A;dc={}
 for r in list(rs)+[x for x in PR if x<=2000]:
  if u%r==0:
   c=0
   while u%r==0:u//=r;c+=1
   dc[r]=c
 gift=I.ilog(u,2001**4); target=I.LN2_LO-abhi(5)-sum(abhi(r) for r in dc)-I.ilog(u,2001)*abhi(2001); logB=I.LN_B_HI; known=False;rough=u==1;terms=[]
 for d in duals:
  L=min(d.lam_p*LP,lnlo(2001)) if u>1 else d.lam_p*LP
  line=lnlo(pe*A)+d.mu*target+d.const_no_target-sum(th for r,th in d.theta_map.items() if A%r==0)-L*gift
  payments={r:point(r,c,False,L) for r,c in dc.items()};pay=sum(payments.values()); base=line+pay
  dis=[]
  for r,c in dc.items():
   alt=point(r,c,True,L)
   if alt is not None:dis.append(base-payments[r]+alt)
  known|=not dis or min(dis)+L*e>logB
  # If q|A, writing A=qC and q=-1 mod 5^t forces 4C=1 mod 5^t; hence 2t<=e. For a>1 the LTE bonus is at most J.
  rough|=base+L*(e-min(e,I.ilog(u+1,5)+J,e//2+J))>logB
  terms.append((base,L,d.delta_q,d.delta_src,max([0]+list(payments.values()))))
 open_high=[];open_one=[]
 for s in range(e+1):
  Y=5**s;Q=max(5,2*Y-1);k=e-s
  high=max(lnlo(3125),max(0,5*s-5)*LP)
  if all(base+L*k+high-dq<=logB for base,L,dq,ds,w in terms):open_high.append(s)
  lq=lnlo(Q)
  if any(base+L*k+lq-dq>logB for base,L,dq,ds,w in terms):continue
  if not s or pe*2**5*Q**6<3**5*B:open_one.append(s);continue
  # Euler now deliberately constrained to outside A by case split, not by 2s>e.
  # Verified GapSupply inequality is independent of that criterion once q\nmid A is assumed.
  aq=S//(Q-1)+1 if Q>10**18 else None
  def lost(dq):return dq if aq is None else min(dq,7500*aq) # all mu<=7500; q>10^18 has no flow
  left=lnlo(Q*Q*Y); den=max(P,Q)*(P//Y+4);t=den.bit_length()-1;shift=max(0,t-28);den_hi=I.log_interval((den>>shift)+1)[1]+shift*I.LN2_HI
  joint=left-den_hi # q*r^(f-c) > Q^2Y/(max(P,Q)*(delta+4))
  # Universal stronger internal bound for KNOWN source r: sigma(r^f)>q implies r^f > (2/3)q.
  # Take minimum over source choices *after* dual maximization.
  branch_ext=any(base+L*k+2*lq+I.log_interval(2,3)[0]-lost(dq)-ds>logB for base,L,dq,ds,w in terms)
  branch_rough=u==1 or any(base+L*k+joint-lost(dq)>logB for base,L,dq,ds,w in terms)
  def internal(r,c):
   v=lnlo(r);f=2*((c+1)//2)
   while 3*r**f<=2*Q:f+=2
   # no source valuation under the non-supply size test. Build exact cost in excess of c.
   from Tree import ok
   while not ok(r,f):f+=2
   log_extra=max(0,f-c)*v
   return any(base+L*k+max(joint,lq+log_extra)-lost(dq)-point(r,c,False,L)>logB for base,L,dq,ds,w in terms)
  if not (branch_ext and branch_rough and all(internal(r,c) for r,c in dc.items())):open_one.append(s)
 return dict(e=e,known=known,rough=rough,one=intervals(open_one),higher=intervals(open_high),closed=known and rough and not open_one and not open_high)

def main():
 args=argparse.ArgumentParser();args.add_argument('es',type=int,nargs='*');args.add_argument('--output',default='GapAudit.json');a=args.parse_args();ds=load_duals();check(all(d.mu<=7500 for d in ds),'mu outside bound');cs=json.loads((H/'Candidates.json').read_text());rows=[]
 for e in a.es or [r['e'] for r in json.loads((H/'DualAudit.json').read_text()) if not r['closed']]:
  rs=sorted({int(x) for x in cs[str(e)] if proved(int(x))});A=(5**(e+1)-1)//4;check(all(A%r==0 for r in rs),'invalid input');row=root(e,rs,ds);rows.append(row)
  if row['closed']:print('CLOSED',e,flush=True)
 (H/a.output).write_text(json.dumps(rows,indent=1)+'\n');print(len(rows),sum(r['closed'] for r in rows))
if __name__=='__main__':main()
