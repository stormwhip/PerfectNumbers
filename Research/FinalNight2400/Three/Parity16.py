"""Tiny factor-free contradiction for the last R16 terminal. No price-kernel import."""
from math import gcd,prod,isqrt
F=((3,12),(797161,66),(5897,6),(42059143035592870990447,16),(1338473377,6),(4013,106));B=10**2400
def sig(q,h):return (q**(h+1)-1)//(q-1)
def run():
 assert __debug__;X=prod(q**h for q,h in F);S=prod(sig(q,h) for q,h in F);D=S//gcd(S,X);Z=[sig(q,h)//gcd(X,sig(q,h)) for q,h in F];Z=[b for b in Z if b>1];assert prod(Z)==D and gcd(X,D)==1 and len(Z)==4
 assert all(gcd(b,c)==1 for i,b in enumerate(Z) for c in Z[:i]);assert all(isqrt(b)**2!=b for b in Z)
 # Any odd prime dividing a block exceeds the certified trial floor. One possible Euler exception globally.
 lows=[]
 for b,L in zip(Z,(500000,500000,100,500000)):
  assert b%2==1 and all(b%v for v in range(3,L+1,2));lows.append(L+1)
 bound=X*D*prod(sorted(lows)[:-1]);assert bound>B;return True
if __name__=='__main__':assert run();print('PASS four disjoint nonsquare blocks, one Euler-free parity allowance')
