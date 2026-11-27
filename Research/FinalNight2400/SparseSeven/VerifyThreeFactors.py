"""Eliminate every residual <=2 A-prime profile by exact emitter-remainder congruences."""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from VerifyPatterns import make,lowbounds,rootfloor,A,X,W,B,U

def derive(rows):
    stats=[0,0];patterns=set();hard=[]
    for s,u,a,j,h,g,who in rows:
        assert 633<=s<=665 and h==2;R,L=lowbounds(u,a,j);Y=7**s;Q=2*Y-1;v=max(0,906-s-5-u);bud=B*U//(X*Q*7**(2*v))
        if who=='b':
            ZL=max(L,rootfloor((2*Q+2)//3-1,g)+1);ZH=min(rootfloor(A//R**a,j),rootfloor(bud//R**h,g));H,m=g,j
        else:
            ZL=max(R,rootfloor((2*Q*7**u+2)//3-1,h)+1);ZH=min(rootfloor(A//L**j,a),rootfloor(bud//L**g,h));H,m=h,a
        d=H+1-m;assert d>=1;Dh=6*(A//ZL**m)
        # Z0=Dk(z-1)-z^d-D nonzero: mod the prime w|A distinct from z gives -z^d.
        nonpositive=Q*ZH**d+(Q+1)*Dh<Q*Y;nonnegative=(W-1)*ZH**d<Q*Y
        if nonpositive and nonnegative:stats[0]+=1;continue
        assert nonpositive and (a,j,h,g,who) in [(1,2,2,2,'b'),(2,1,2,2,'r')];patterns.add((a,j,h,g,who));hard.append((s,u))
        # Here A=w z^2 and q*k=z^2+z+1, both distinct ordinary bases.
        # Since z^2 >2q/3 and z>=3, w < (3/2)A/q and wk <= (13/9)A/q.
        # Hence 6w(k+1)-1 < 18A/q and 6w <9A/q; Z=(...)^2+6w is a positive multiple of Y.
        assert (18*A)**2+9*A*Q<Y*Q**2
        stats[1]+=1
    assert stats==[1404,86] and len(patterns)==2
    print('PASS all <=2-A-prime configurations impossible, labeled exclusions',stats,'hard s range',min(s for s,u in hard),max(s for s,u in hard),flush=True)
if __name__=='__main__':
    assert __debug__;sys.set_int_max_str_digits(0);out,ss,n,rows=make();assert n==1490 and min(ss)==633 and max(ss)==665;derive(rows)
