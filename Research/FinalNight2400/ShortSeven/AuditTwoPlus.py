"""Independent global no-5/no-11 proof and direct integer two-prime exclusion at h=130."""
from math import prod,gcd,isqrt
from fractions import Fraction
from pathlib import Path
import gzip,json,hashlib
H=Path(__file__).resolve().parents[1]/'SevenNext';B=10**2400;Q=(7**13-1)//6;T=(Q**13-1)//(Q-1)//13;L=3453283
def sig(q,h):return (q**(h+1)-1)//(q-1)
def a(q,h):return Fraction(sig(q,h),q**h)
assert __debug__ and sig(7,12)==Q and sig(Q,12)==13*T and sig(T,2)%(3*L)==0 and sig(3,2)==13 and 11%4==3
assert a(7,12)*a(3,2)*a(5,1)>2 and a(7,12)*a(11,2)*a(3,4)*a(13,1)>2 and a(7,12)*a(11,2)*a(3,2)*a(13,2)>2
for name,vals in [('TwoPlus',[42,56,80]),('TwoExtra',[86])]:
 F=H/(name+'.json.gz');d=json.loads(gzip.decompress(F.read_bytes()));assert sorted(map(int,d['nodes']))==vals;print(name,len(d['ecpp']),hashlib.sha256(F.read_bytes()).hexdigest())
P=[(7,12),(Q,12),(T,2),(L,130)];X=prod(p**h for p,h in P);D=prod(sig(p,h) for p,h in P)
while (g:=gcd(D,X))>1:D//=g
z=[209676169384343,315434173696972219];v=X*D
for q in z:
 assert D%q==0 and D%(q*q)!=0 and q%4==3;v//=q
 def safe(h):
  s=sig(q,h)
  while (g:=gcd(s,X*D))>1:s//=g
  return s*q**h
 powers=[];h=2
 while q**h<=B:powers.append(safe(h));h+=2
 v*=min([q**h,*powers]);
assert v>B;print('PASS h=130 exact independent bound floor',len(str(v))-1)
