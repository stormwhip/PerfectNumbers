"""Forest with Euler restricted to a named subset, using shared ordinary costs and ancestry."""
from Masked import *
class Group(C.Forest):
 def node(self,z,h,m):
  if m==0:return self.ordinary.node(z,h,0)
  if not self.allowed or z not in self.anc:return self.ordinary.node(z,h,0)
  if m==1 and z not in self.allowed:return self.node(z,h,3)
  return super().node(z,h,m)
def measure(s,k,o,head):
 base=C.Forest(s,k,o,head);parent=dict(o);F=Group(s,k,o,head);F.ordinary=base;A=set(k)|set(parent);euler={z for z in A if C.euler(z,s.bad)}
 def lb(allowed):
  F.allowed=set(allowed);F.anc=set();F.memo={}
  for v in allowed:
   while v not in F.anc:
    F.anc.add(v)
    if v not in parent:break
    v=parent[v]
  return F.lower()[0]
 return euler,lb

def scan(s,k,o,head):
 zz,lb=measure(s,k,o,head);plain=lb([]);cuts=[];miss=[]
 if plain<=B:return -1,[],[]
 def test(v):
  if not v:return
  w=lb(v)
  if w>B:cuts.append((len(v),floor10(w)));return
  if len(v)==1:miss.append(v[0]);return
  n=len(v)//2;test(v[:n]);test(v[n:])
 test(sorted(zz));return floor10(plain),cuts,miss
if __name__=='__main__':
 f,j=map(int,sys.argv[1:]);a=json.loads((D/f'Even430F{f}J{j}.json').read_bytes());res={}
 for m,s,r in states(f,j):
  if f==2 and (m,j) not in ((50,2),(58,2),(178,2),(50,6),(58,6)):continue
  k,o=adapt(s,a);v,c,l=scan(s,k,o,a['head']);res[m]=l;print(m,j,'plain',v,'miss',len(l),l[:12],flush=True)
 (H/f'Group{f}J{j}.json').write_text(json.dumps(res))
