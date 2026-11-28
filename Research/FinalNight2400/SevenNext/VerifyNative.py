"""Exact admissible-forest arithmetic. Check named package leaves plus all prime labels."""
import sys,json,gzip
from pathlib import Path
from functools import cache
from math import prod,gcd
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B,exact_leaf
Q=16148168401;T=C.sigma(Q,12)//13;S=62936242392988051361
def run(file,expected):
 assert __debug__;z=json.load(gzip.open(H/file));seen=set();lc=set()
 @cache
 def prime(n):
  if n<2**64:return C.pc.prime64(n)
  if str(n) in z['luc']:
   lc.add(str(n));g,fs=z['luc'][str(n)]; assert prod(int(u)**h for u,h in fs.items())==n-1 and pow(g,n-1,n)==1 and all(0<h and prime(int(u)) and gcd(pow(g,(n-1)//int(u),n)-1,n)==1 for u,h in fs.items());return True
  y=n;seen.add(str(y))
  for row in z['ecpp'][str(n)]:assert y==row[0];y=C.pc.level(*row)
  return C.pc.prime64(y)
 assert all(prime(q) for q in [Q,T,S]) and C.sigma(7,12)==Q and C.sigma(Q,12)==13*T and C.sigma(T,6)%S==0
 assert sorted(map(int,z['nodes']))==expected
 for k in expected:
  rows=[(7,12),(Q,12),(T,6),(S,k)];s=C.State(rows);assert not s.conflict and s.base<=B;rt,es,head=z['nodes'][str(k)];C.validate_forest(s,rt,es,head,prime)
  lb=min(C.Forest(s,rt,es,head).lower()[0],exact_leaf(rows,rt,es,head));assert lb>B;print(k,'floor',len(str(lb))-1,'strict',lb>B,flush=True)
 assert set(z['luc'])==lc and set(z['ecpp'])==seen
if __name__=='__main__':run('Native.json.gz',[8,12])
