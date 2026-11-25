"""Integer-cost lemma to separately charge a positive supply by the emitter to external Euler q (a=1)."""
from DualTree import I,J,lnlo

def lnhi(v):
 t=max(0,v.bit_length()-36);return I.log_interval((v>>t)+1)[1]+t*I.LN2_HI

def paid(s,e,terms,dc,u):
 if not s:return False
 y=5**s;Q=2*y-1
 # q > max(f+1) removes q|(f+1) exception when r=1 mod q. In fact order-one also works since 5!=q.
 if Q<=I.MAX_EXPONENT+1:return False
 lq=lnlo(Q);lt=lq+I.log_interval(2,3)[0];Lmax=I.LN_B_HI
 for j in range(1,min(J,e-s)+1):
  v=5**j*lt+lq
  for typ in ['ext','u']+list(dc):
   if typ=='u' and u==1:continue
   valid=False
   for base,L,d,pm in terms:
    dq=d.delta_q if Q<=10**18 else min(d.delta_q,d.mu*((I.SCALE+Q-2)//(Q-1)));loss=d.delta_src if typ=='ext' else lnhi(u) if typ=='u' else pm[typ]+lnhi(typ**dc[typ]);
    if base+L*(e-s-j)+v-dq-loss>Lmax:valid=True;break
   if not valid:return False
 return True
