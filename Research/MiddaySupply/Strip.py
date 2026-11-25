"""Exact two-dimensional lattice enumeration on an affine rectangle.
No LLL library: Gauss reduction with integer metric, determinant row bounds."""
from math import gcd

def cd(a,b):return -((-a)//b)

def roots(C,c,base,T,N,m,a,d,W,budget,expected=None):
    # points (x,y)=(x,d+a*x+m*j) in [0,N-1]x[1,W].
    if N<1 or W<1:return False
    X=max(1,N-1);Y=W;u=(1,a%m);v=(0,m)
    def dot(o,p):return o[0]*p[0]*Y*Y+o[1]*p[1]*X*X
    while True:
        if dot(v,v)<dot(u,u):u,v=v,u
        n=dot(u,u);q=(2*dot(u,v)+n)//(2*n)
        if not q:break
        v=(v[0]-q*u[0],v[1]-q*u[1])
    det=u[0]*v[1]-u[1]*v[0];
    if det<0:v=(-v[0],-v[1]);det=-det
    assert det==m
    amax=N-1;bmin=1-d;bmax=W-d
    cross=[u[0]*y-u[1]*x for x in (0,amax) for y in (bmin,bmax)];jmin=cd(min(cross),m);jmax=max(cross)//m
    if jmax-jmin>budget:return True
    n=0
    for j in range(jmin,jmax+1):
        low=high=None
        for u0,v0,l,h in ((u[0],v[0],0,amax),(u[1],v[1],bmin,bmax)):
            l-=j*v0;h-=j*v0
            if u0==0:
                if not l<=0<=h:low,high=1,0;break
                continue
            if u0<0:u0=-u0;l,h=-h,-l
            l0,h0=cd(l,u0),h//u0;low=l0 if low is None else max(l0,low);high=h0 if high is None else min(h0,high)
        n+=max(0,high-low+1)
        if n>budget:return True
        for k in range(low,high+1):
            x=u[0]*k+v[0]*j;r=base+T*x
            if expected is not None and not (0<=x<N and 1<=(a*x+d)%m<=W):raise ValueError('spurious lattice point')
            if C%r==0 and C%r**c==0:return True
    if expected is not None and n!=expected:raise ValueError('lattice enumeration disagrees with floor-count')
    return False
