"""Finite stress test of factoring a true component list into explicit/removed/tail groups.
Compare proxy abundance against its own sigma(N)/N, no need to assume perfectness.
Uses products and Fraction only. Records forced anonymous Euler and generic high-k edge.
"""
from itertools import product
from fractions import Fraction as Q
from collections import Counter
from math import prod, gcd

def sigma(p,f):return (p**(f+1)-1)//(p-1)
# Explicit 3,5,7; promote 11 past the cutoff and leave target 13 generic.
cuts={3:6,5:2,7:2,11:2,13:0}; primes=[*cuts,19,31,37,41];L=9
relations=[(3,4,11,2),(3,2,13,1)];blocks={(7,2):19,(5,2):31}
for p,f,q,v in relations:assert sigma(p,f)%q**v==0
for (p,f),n in blocks.items():assert sigma(p,f)%n==0 and min(n,L)==L and gcd(prod(cuts),n)==1
# For 3^8->13^2 check 13^2|sigma? instead 3^26 gives valuation 1+v13(9)=1; use 3^38 => v13=2.
assert sigma(3,38)%13**2==0
# Find generic edge multiplicity greater than represented minimum 2, using 3^(3*13^2-1), ord_13(3)=3.
assert sigma(3,3*13**2-1)%13**3==0 # generic 13^4 must satisfy, even if representative is 2
cnt=Counter()
for es in product(*[([0,1,2,4] if p%4==1 else [0,2,4]) for p in primes]):
 d=dict(zip(primes,es));sp=sum(e%2 for e in es)
 if sp>1 or any(d[p]==f and d[q]<v for p,f,q,v in relations):continue
 if any(d[p]==f and not d[n] for (p,f),n in blocks.items()):continue
 N=prod(p**e for p,e in d.items());act=prod(Q(sigma(p,e),p**e) for p,e in d.items());C=1;ab=Q(1);costeu=0;removed=set();cnt['states']+=1
 for p,cut in cuts.items():
  f=d[p]
  if not f:continue
  is_euler=f%2;costeu+=is_euler;ex=f<=cut;n0=f if ex else next(k for k in range(cut+1,f+1) if (k%4==1 if is_euler else k%2==0));C*=p**n0;ab*=Q(sigma(p,f),p**f) if ex else Q(p,p-1)
  if (p,f) in blocks:
   n=blocks[p,f];assert n not in removed and n not in cuts;removed.add(n);C*=n;ab*=Q(L,L-1);cnt['removed_euler']+=d[n]%2
 for p in primes:
  if p in cuts or p in removed or not d[p]:continue
  C*=L if d[p]%2 else L**2;ab*=Q(L,L-1);costeu+=d[p]%2
 assert C<=N and ab>=act and costeu<=sp
 if d[11]>2:cnt['promoted_tail']+=1
 if d[3]==4:cnt['active_targetk2']+=1
# Exercise an anonymous Euler explicitly: 13 divides sigma(3^2). If promoted as an explicit target it MUST NOT be charged again.
assert sigma(3,2)==13; NN=3**2*13; assert NN*13>NN; assert 13%4==1
# Can validly erase the sole Euler component; requiring one remaining slot would reject the mapping.
assert all(cnt[k]>0 for k in ('states','promoted_tail','active_targetk2'))
assert any(sigma(p,2)%37==0 for p in (47,)); assert sigma(47,2)==37*61
N=47**2*37*61**2 # 37^1 is hidden in C=37*61. Do not impose equality 1 on remaining Euler slots.
assert 37%4==1 and (47**2*37*61)<=N and Q(37,36)*Q(39,38)>=Q(38,37)*Q(sigma(61,2),61**2);cnt['removed_euler_separate_fixture']=1
print(dict(cnt));print('anti-patterns witnessed: overlap 3^2 -> 13; removed Euler 37; generic representative at exponent 2 versus k=3')
