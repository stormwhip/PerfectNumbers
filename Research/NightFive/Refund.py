"""Lower bound on the negative ordinary reduced-cost credit omitted when a known vertex is deleted. Mirrors the exact f=2/4 enumeration in upstream verifier, not its tail approximations."""
from functools import lru_cache
from DualTree import I
@lru_cache(None)
def refunds(p,mu,lam,entrytxt):
 import json
 a=json.loads(entrytxt);fbd=(19,7,11,31,13,3);Fm=I.get_f_min(p,fbd);entries=[(r,f,w,qty) for r,f,w,qty in a['flows'] if r==p or w==p]; theta=sum(qty*10**6 for r,f,w,qty in entries if w==p);fmax=max([0]+[f for r,f,w,qty in entries if r==p]);cut=max(Fm,fmax+2) if fmax else Fm
 if p<=80:cut=max(cut,64)
 elif p<=300:cut=max(cut,42)
 # Only take explicitly enumerated f in authoritative verifier; when cap equals fm the tail uses f=fm but different abundance, ignored here.
 best=0;lr=I.log_interval(p)[0];lp=I.log_interval(5)[1]
 if p>5000:return 0
 for f in range(Fm,cut,2):
  if I.sigma_has_forb(p,f,fbd):continue
  ab=I.log_interval((p**(f+1)-1)//(p-1),p**f)[1] if p<=500 and f<=60 else I.log_interval(p,p-1)[1]; flow=sum(qty*10**6 for r,n,w,qty in entries if r==p and n==f);rc=f*lr+flow-theta-lam*lp*I.vp_sigma(5,p,f)-mu*ab; best=max(best,-rc)
 return best

def attach(d,a):
 import json
 from functools import cache
 text=json.dumps(a,separators=(',',':'))
 @cache
 def premium(p):return refunds(p,d.mu,d.lam_p,text) if p<5000 else 0
 d.refund=premium;return d
