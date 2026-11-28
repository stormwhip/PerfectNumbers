"""Factor-free constraints on Euler q^a in a hypothetical OPN at 7^906. No first/shard closure."""
from fractions import Fraction
from math import gcd,isqrt
p=7;X=p**906;W=p*X;A=(W-1)//6;B=10**2400
assert gcd(A,6*7)==1 and pow(7,907,A)==1 and A%907!=0 and A%2 and isqrt(A)**2!=A
# For s>0, q does not divide A by quadratic reciprocity (see proof).
high=[];linear=[];external=[]
for s in range(1,907):
 Y=p**s;Q=2*Y-1
 if X*A*Q**5>B:high.append(s)
 # Balance lower for an internal emitter; no floating-point arithmetic.
 out=X*A*Q*((2*Q+2)//3)>B
 inside=X*A*Q*max(1,Fraction(Y*Q,max(W,Q)*(W//Y+4)))>B
 if out:external.append(s)
 if out and inside:linear.append(s)
assert high==list(range(206,907)) and external==list(range(514,907)) and linear==list(range(711,907))
print('PASS (7,906): s>=711 excluded for all Euler exponents; 514<=s<=710 requires q^1 AND all q-emitters internal to A; 206<=s<=513 requires q^1.')
