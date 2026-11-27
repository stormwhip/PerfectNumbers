from Masked import *
from math import prod,gcd

def tests(row,s,k,o,head,q,fac):
 # Given Euler q, its odd linear output E=(q+1)/2 is compulsory, and its base q|N. Already paid part of E in initial odd fixed sigmas is NOT optional: distinct rows supply multiplicity additively.
 # Add E to the fixed emissions before the forest and remove it exactly once from Euler sigma. Need a modified Euler row. Simpler: split Euler component, enumerate a=1,5... until base bound X·D*q^a or conflicts. Include ordinary forest only, preserving q's former descendants as possible roots when sigma(q^a) activates them.
 E=(q+1)//2
 if gcd(E,prod(s.bad))>1 or any(val(s.S*E,z)>h for z,h in row):return []
 owed=prod(x for x in s.present if x not in s.rows and s.D%x and x!=q);floor=s.base//q**val(s.D,q)*owed;bad=[]
 children={z for z,v in o if v==q};remaining=[(z,v) for z,v in o if z!=q and v!=q];a=1
 while floor*q**a<=B:
  rows=row+[(q,a)];u=C.State(rows,s.present,s.bad);a0=a;a+=4
  if u.conflict or u.base>B:continue
  N=prod(sig(z,h) for z,h in rows);den=u.X;K=set(k)|children|set(fac(q,a0));K={z for z in K if z not in u.rows and z not in u.bad and (u.D%z==0 or z in s.present)}
  # direct compulsory abundancy
  for z in K:
   h=max(1,val(u.D,z));h+=h%2
   while not C.permitted(z,h,u.bad):h+=2
   N*=sig(z,h);den*=z**h
  if N>2*den:continue
  vis=set(K);O=[]
  for z,v in remaining:
   if v in vis and z not in vis and z not in u.rows and z not in u.bad and u.D%z:O.append((z,v));vis.add(z)
  # Only known roots selected and their descendants. Removing one subtree always safe.
  plain=C.Forest(u,sorted(K),O,head);lb,mark=plain.lower()
  if lb<=B:bad.append((a0,floor10(lb)))
 return bad
if __name__=='__main__':
 sys.path.insert(0,str(H.parent/'Three'));import NativeForest as N
 f,j=map(int,sys.argv[1:]);a=json.loads((D/f'Even430F{f}J{j}.json').read_bytes());g=json.loads((H/f'Group{f}J{j}.json').read_bytes());ans=[]
 for m,s,r in states(f,j):
  if str(m) not in g:continue
  k,o=adapt(s,a)
  for q in g[str(m)]:
   b=tests(r,s,k,o,a['head'],q,N.fac);ans.append([m,q,b]);print(m,str(q)[:30],len(b),b[:4],flush=True)
  (H/f'Forced{f}J{j}.json').write_text(json.dumps(ans))
