"""Alternative independently directed integer ln bounds via atanh series. No Decimal, floating arithmetic, or external package."""
from functools import cache
from fractions import Fraction
S=2**80;P=2**176
# For 1<=m<=2: log m=2 sum t^(2j+1)/(2j+1), t=(m-1)/(m+1)<=1/3.
# Truncate after 60 terms; residual <= 2*(1/3)^121 / (121*(1-1/9)) < 2^-176.
assert 18*P < 8*121*3**121
@cache
def norm(a,b):
 assert b<=a<=2*b
 lo=(a-b)*P//(a+b);hi=-(-(a-b)*P//(a+b));l=lo;h=hi;l2=l*l//P;h2=-(-h*h//P);low=high=0
 for j in range(1,120,2):
  low+=2*l//j;high+=-(-2*h//j);l=l*l2//P;h=-(-h*h2//P)
 return low,high+1
@cache
def lg(n):
 assert n>0;k=n.bit_length()-1;u,v=norm(n,1<<k);a,b=norm(2,1);return k*a+u,k*b+v
@cache
def logs(n,d=1):
 if n==d:return 0,0
 l,u=lg(n);a,b=lg(d);return (l-b)*S//P,-(-(u-a)*S//P)
