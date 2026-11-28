"""Price a subprefix of canonical 11^396,2383^f using its exact fixed outgoing blocks."""
from math import gcd,prod
from functools import cache
from pathlib import Path
import runpy,sys
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B
p,t=11,2383
@cache
def loss():return runpy.run_path(str(H/'Verify.py'))['losses']()

def proves(P):
    # The caller must prove that these are exact components at this path and all labels are prime.
    assert P[0]==(11,396) and P[1][0]==t and P[1][1] in range(2,233,2)
    st=C.State(P);assert not st.conflict and st.base<=B
    cp=396-C.valuation(st.S,p);ct=P[1][1]-C.valuation(st.S,t);assert cp>=0 and ct>=0
    U=loss();X=st.X;D=st.D
    # No loss multiplication with mandatory mass: separate budget comparisons.
    Pp=p**cp;Tt=t**ct;A=X*Pp**4*Tt**2*U.denominator;BB=B*U.numerator
    if st.fixed_euler:return A>BB
    pieces=[C.sigma(r,h) for r,h in P];pieces=[z//gcd(z,X) for z in pieces];assert prod(pieces)==D
    # Rough upper cap on a linear allocation m=p^i*t^j for an interior q.
    cap=(B//(X*D)+1)//2
    for (r,h),z in zip(P,pieces):
        bound=Tt if r==p else Pp if r==t else Pp*Tt
        cap=max(cap,min((z+1)//2,bound))
    pp=[p**i for i in range(cp+1)];tt=[t**j for j in range(ct+1)]
    import bisect
    w=0
    for v in tt:
        k=bisect.bisect_right(pp,cap//v)-1
        if k<0:break
        w=max(w,pp[k]**3*v)
    if A>BB*w:return True
    # H bounds the largest primary part of D with a single base, even for overlapping blocks.
    Hm=max(z*prod(gcd(z,v) for j,v in enumerate(pieces) if j!=k) for k,z in enumerate(pieces))
    def outside(z,m,Q):
        if Q>z:return True
        if z//Q>=4*m:return False
        k=z*pow(Q,-1,4*m)%(4*m);return not(0<k<=z//Q and z%k==0)
    for j,v in enumerate(tt):
        for i,u in enumerate(pp):
            m=u*v;Q=2*m-1;den=u**4*v*v
            if A*Q>BB*den:continue
            if any(not ((r==p and i) or (r==t and j) or outside(z,m,Q)) for (r,h),z in zip(P,pieces)):return False
            if X*D*Q>B:continue
            cap=3*B*Hm//(2*X*D*Q**2);w=0
            # Maximum P³T under P*T<=cap, P<=p^(cp-i), T<=t^(ct-j).
            for a in tt[:ct-j+1]:
                k=min(cp-i,bisect.bisect_right(pp,cap//a)-1)
                if k<0:break
                w=max(w,pp[k]**3*a)
            if 2*A*Q**2<=3*BB*den*w:return False
    return True
