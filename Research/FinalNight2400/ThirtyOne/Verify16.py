"""Cold conditional proof: the exact first t^16 under 31^16; not t^22."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')];from AtomPrice import *
from PivotCheck import C,floor10
from functools import cache
assert __debug__;B=10**2400;T=751670559138758105956097;R=[(31,16),(T,16)];S=C.State(R);book=json.loads((H/'Cert16.json').read_bytes());a=json.loads((H/'Forest16.json').read_bytes());K,O,head=a['roots'],a['owners'],a['head'];seen=set()
@cache
def prime(z):
 q=z
 if z>=2**64:
  seen.add(str(z))
  for row in book[str(z)]:assert row[0]==q;q=level(*row)
 assert prime64(q);return True
assert prime(31) and prime(T) and not S.conflict and C.sigma(31,16)==T and C.sigma(T,16)%T==1
C.validate_forest(S,K,O,head,prime);assert set(book)==seen
# If q occurs among forest labels, its Euler linear factor provides no T units. All remaining supply costs >=T^(12*15) from even atoms, including the Euler-square atom.
V=set(K)|{z for z,_ in O};assert not any(z%4==1 and (z+1)%T==0 for z in V);u,n=bound(15,12);assert u==1 and n==0 and S.X*T**(15*12)>B
# Otherwise every forest label has ordinary even exponent. Set only the occupied-Euler-slot flag; prefix X,D and bans stay unchanged.
S.fixed_euler=True;v,m=C.Forest(S,K,O,head).lower();assert m is None and v>B
print('PASS 31^16 exact t^16. Euler-on-vertex restricted via t-price; absent via ordinary forest.',len(V),'vertices',len(book),'ECPP, floor',floor10(v),'price floor',floor10(S.X*T**180))
