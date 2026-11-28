"""Cold Euler-location partition targeted to five old openings, no discovery-time imports."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ForceQ import tests
from EulerGroup import measure
from Score import *
Z=2719475404574062750177556064626770984612172161050693998086064689414615488121825606606912057
from Masked import adapt

def certify(j):
 assert __debug__ and j in (2,6);data=json.loads((H/f'Q2J{j}.json').read_bytes());book=json.loads((H/f'CertJ{j}.json').read_bytes());base=data['base'];assert set(map(int,data['cases']))==({50,58,178} if j==2 else {50,58});row=[(7,430),(Q,2),(Z,j)];stats=[]
 @cache
 def prime(z):
  assert int(z)==z and z>2;q=z
  if z>=2**64:
   for r in book[str(z)]:assert q==r[0];q=C.pc.level(*r)
  assert C.pc.prime64(q);return True
 assert prime(Q) and prime(Z) and sig(7,430)%Q==0 and sig(Q,2)%Z==0
 for key,t in data['extras'].items():
  z,h=map(int,key.split(':'));g=sig(z,h);assert all(prime(y) and g%y==0 for y in t)
 for mask0,entry in data['cases'].items():
  m=int(mask0);yes=frozenset(z for i,z in enumerate(C.ORDER) if m>>i&1);no=set(C.ORDER)-yes;s=C.State(row,yes,no);assert not s.conflict and m%4==2;k,o=adapt(s,base);head=base['head'];C.validate_forest(s,k,o,head,prime);E,lb=measure(s,k,o,head);S=set(entry['possible']);assert S<=E and lb([])>B and lb(E-S)>B # every Euler outside all vertices or in complement rejected
  used=set();count=0
  for q in sorted(S):
   def flags(z,h):return data['extras'][f'{z}:{h}']
   un=tests(row,s,k,o,head,q,flags)
   for a,v in un:
    key=f'{q}:{a}';t=entry['fix'][key];used.add(key);r=row+[(q,a)];u=C.State(r,s.present,s.bad);assert not u.conflict and u.fixed_euler;C.validate_forest(u,t['roots'],t['owners'],t['head'],prime);assert C.Forest(u,t['roots'],t['owners'],t['head']).lower()[0]>B;count+=1
  assert used==set(entry['fix']);stats.append((m,j,len(S),count));print('PASS',stats[-1],flush=True)
 return stats
if __name__=='__main__':
 for j in map(int,sys.argv[1:]):certify(j)
