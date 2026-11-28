"""Independent two-target source-factor price in the 1093^156 Q^46 fiber."""
from Joint157 import *
from Emitters import first_not_rejected,inside_euler,min_additional_abundance_lower
from CleanPrice import lower_mass
from hashlib import sha256

def q_envelope():
    ro,R,X,S,D,spec,cp,cq,hmax,os=orders()
    c,M,L=heavy(ro,q,6,even_only=True,square_atoms=True)
    return c,M,L

def one_target():
    rows,R,X,S,D,spec,cp,cq,hmax,os=orders();c,M,L=q_envelope()
    V=F(X*q**(6*c))/M[c]
    print('all Euler via linear atom',len([z for row in L for z in row]),floor10(V),flush=True)
    rem=[];count=[0,0,0]
    for i in range(cp+1):
        for j in range(cq+1):
            m=p**i*q**j;a=2*m-1;e=first_not_rejected(a,4*m,spec)
            Fq=F(q**(6*(cq-j)),M[cq-j]);V0=X*e*Fq
            if V0>B:count[0]+=1;continue
            if X*D*e>B:count[1]+=1;continue
            if any(inside_euler(a,m,b) for _,_,b in spec):rem.append((i,j,True));continue
            add=min_additional_abundance_lower(X,S,D,R,e)
            if X*D*e*R**len(spec)*add>B:count[2]+=1;continue
            rem.append((i,j,False))
    assert count==[1510,0,0] and len(rem)==5666 and sum(t[2] for t in rem)==1086
    assert min(j for i,j,x in rem)==2 and max(j for i,j,x in rem)==45
    print(count,len(rem),sum(t[2] for t in rem),'range j',min(j for i,j,x in rem),max(j for i,j,x in rem),'sha256',sha256(repr(rem).encode()).hexdigest(),flush=True)
if __name__=='__main__':one_target()
