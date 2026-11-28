"""Prove canonical (13,618) also excludes s=536; no factorization assumptions."""
from pathlib import Path
from math import gcd
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from HighLinear import B,P,ROUGH,inputs,cell,minimum_q,floor_root,ceil_root,require


def prove():
    e,s=618,536; X,W,A,M,_=dat=inputs(e)
    require(cell(e,s,dat)=={(10,5)},'boundary shape')
    h,c=10,5; d=h+1-c;Y=P**s;Q=minimum_q(s,h);u=(Q+1)//(2*Y)
    step=2*(h+1);require(u==27 and step==22 and (u*Y)%11==1,'first admissible Euler progression')
    # Every possible Euler prime is q=2*m*Y−1 for m in {27,49,71,...}.
    # Even if all larger progression members are prime, the monotone signed
    # source bound already forbids them at the first larger member.
    R=2*(u+step)*Y-1;T=B//(X*A*R); L=ceil_root((2*R+2)//3,h)
    U=min(floor_root(A//ROUGH,c),floor_root(T,h-c));Dmax=(P-1)*(A//L**c)
    pos=(W-1)*U**d//(R*Y);neg=(R*U**d+(R+1)*Dmax)//(R*Y)
    # For larger q, (q+1)/q decreases; check negative upper monotonically.
    J=(-1-(P-1)*A)*pow(Y,-1,M)%M
    require((pos,neg,J)==(187,0,223) and pos<(J or M) and neg<((-J)%M or M),'monotone signed obstruction')
    require(pow(2,Q-1,Q)!=1,'first candidate must be definitely composite')
    print('PASS canonical (13,618): s=536 excluded',flush=True)
    s=535;Y=P**s
    require(cell(e,s,dat)=={(8,3),(10,5)},'535 shape roster')
    tested=0
    for h,c in ((8,3),(10,5)):
        d=h+1-c;Q=minimum_q(s,h);u=(Q+1)//(2*Y);step=2*(h+1)
        require((h,u) in ((8,25),(10,43)),'exact starting multiplier')
        R=2*1411*Y-1;T=B//(X*A*R);L=ceil_root((2*R+2)//3,h)
        U=min(floor_root(A//ROUGH,c),floor_root(T,h-c));Dmax=(P-1)*(A//L**c)
        pos=(W-1)*U**d//(R*Y);neg=(R*U**d+(R+1)*Dmax)//(R*Y)
        J=(-1-(P-1)*A)*pow(Y,-1,M)%M
        require(pos<(J or M) and neg<((-J)%M or M),'535 monotone signed tail')
        for j in range(u,1411,step):
            if gcd(j,P*19*7*11*31)!=1:continue
            Q=2*j*Y-1
            require(pow(2,Q-1,Q)!=1,('535 noncomposite survivor',h,j))
            tested+=1
    require(tested==97,'535 finite candidate count')
    print('PASS canonical (13,618): s=535 excluded; all s>=535 excluded after HighLinear',tested,'Fermat witnesses',flush=True)

if __name__=='__main__':prove()
