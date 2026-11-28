"""Ordinary forest with the unknown external Euler prime reserved, with exact cofactor-class rebate."""
from Window import *
@cache
def block(Z,m):
 """A lower bound on the prime-to-q part of Z, for q ≡ 2m−1 mod 4m."""
 q=2*m-1
 if q<=1:return 1
 n=Z;size=q
 # If q^a divides Z with a maximal, its remaining cofactor is in a residue class mod 4m. Take smallest possible cofactor over admissible a, including a=0.
 best=Z;res=Z%(4*m);inv=pow(q,-1,4*m)
 while size<=Z:
  res=res*inv%(4*m);lo=res or 4*m
  if lo<=Z//size:
   if lo+4*m>Z//size and Z%lo:pass
   else:best=min(best,lo)
  size*=q
 return best

def ef(row,t,j):
 s=C.State(row);k=t['roots'];o=t['owners'];head=t['head'];Q=2*T**j-1;m=T**j;assert Q>1
 V=set(k)|{q for q,p in o};assert all(z%4!=1 or val(z+1,T)!=j for z in V)
 fs={z:val(s.D,z) for z in k};base=s.X*Q*block(s.D//prod(z**v for z,v in fs.items()),m);pool=s.X*s.D*prod(q for q,p in o);kids={z:[] for z in V}
 for z,parent in o:kids[parent].append(z)
 kk={z:prod(v) for z,v in kids.items()}
 @cache
 def node(z,c):
  best=B+1;e=c+c%2;done=0
  while z**e<best and done<head:
   if C.permitted(z,e,s.bad):
    done+=1;A=sig(z,e);n=block(C.nonsupport(A,pool),m);v=z**e*n
    if gcd(A,kk[z])>1:
     for a in kids[z]:
      if A%a==0:v*=node(a,val(A,a))
    best=min(best,v)
   e+=2
  return min(best,z**e)
 return base*prod(node(z,h) for z,h in fs.items())
if __name__=='__main__':
 root=json.loads((O/'ShortWitness22.json').read_bytes());row=[(31,16),(T,22)];
 for j in range(16,22):print(j,floor10(ef(row,root,j)),flush=True)
 for band in (0,1):
  data=json.loads((H/f'Sub22_{band}.json').read_bytes());M=json.loads((H/f'Window22_{band}.json').read_bytes());counts={};
  for h,m in M.items():
   t=data[h];r=row+[(47,int(h))];bad=[]
   for j,*_ in m:
    v=ef(r,t,j);
    if v<=B:bad.append([j,floor10(v)])
   counts[h]=bad
  (H/f'Reserved{band}.json').write_text(json.dumps(counts));print('reserved',band,counts,flush=True)
