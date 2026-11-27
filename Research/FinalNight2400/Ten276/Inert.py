"""An assigned Euler and a forced odd valuation with no remaining ordinary sources."""
from math import gcd,prod,isqrt
B=10**2400

def excluded(P,l):
 # Caller certifies all row bases and l. No assumption that incoming fixed sums are coprime.
 if l in dict(P):return False
 if not any(h%2 for p,h in P):return False
 S=prod(((p**(h+1)-1)//(p-1))//(1+h%2) for p,h in P);c=0
 while S%l==0:S//=l;c+=1
 if c%2==0:return False
 if 3**(l-1)<=B:return False
 # If ordinary k>0 supplies l nontrivially then ord_l(base)>1 is odd and
 # divides k+1, so some odd prime dividing l-1 is <= k+1.
 a=l-1
 while a%2==0:a//=2
 # This elementary sufficient test avoids ever factoring a large odd part.
 # 3^5100 > 10^2400, so enough to check every odd possible order <=5100.
 assert 3**5100>B
 return all(a%d for d in range(3,5101,2))
