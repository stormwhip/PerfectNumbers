"""Independent caller of GMP modular arithmetic for large anonymous windows."""
from pathlib import Path
from argparse import ArgumentParser
from math import gcd
from subprocess import run
import sys,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from ThinGeneral import inputs,cell,minimum_q,bounds,signed_end,primes,P,require
from EmitterCRT import possible_q_prime


def verify(e,s,NATIVE,cap=6_000_000):
    dat=inputs(e);X,W,A,M,_=dat;Y=P**s
    require(500<=s<=536 and 2*Y-1>20000,'scope and sieve range')
    O=sorted(cell(e,s,dat));prime=primes(20000)
    for h,c in O:
        d=h+1;step=2*d;first=(minimum_q(s,h)+1)//(2*Y);lim=signed_end(dat,s,h,c,first)
        r=len(range(first,lim,step));require(r<=cap,('OPEN cap',e,s,h,c,r))
        sieve=bytearray(b'\1')*r
        for p in prime:
            if (2*Y)%p==0:continue
            target=pow((2*Y)%p,-1,p);g=gcd(step,p)
            if g>1:
                if (first-target)%p==0:sieve[:]=bytes(r)
            else:
                ix=(target-first)*pow(step,-1,p)%p
                if ix<r:sieve[ix::p]=bytes(len(range(ix,r,p)))
        us=[first+step*j for j,v in enumerate(sieve) if v and gcd(first+step*j,13*19*7*11*31)==1]
        n_ok=0;unresolved=[]
        for k in range(0,len(us),2000):
            uu=us[k:k+2000];qs=[2*i*Y-1 for i in uu]
            lines=''.join(f'{n:x}\n' for n in qs)
            z=run([NATIVE],input=lines,encoding='ascii',capture_output=True,check=True,timeout=240)
            flags=list(map(int,z.stdout.split()));require(len(flags)==len(qs) and set(flags)<={0,2,3},'native result framing')
            for u,q,f in zip(uu,qs,flags):
                if f:continue
                require(pow(2,q-1,q)==1 and pow(3,q-1,q)==1,'native/pure survivor discrepancy')
                n_ok+=1
                q,l,m,_,_=bounds(dat,s,h,c,u)
                if possible_q_prime(q,d,l,m,M,1):unresolved.append(u)
        require(not unresolved,('OPEN subgroup',e,s,h,c,unresolved))
        print(e,s,h,c,first,lim,r,len(us),n_ok,'PASS',flush=True)

if __name__=='__main__':
    ap=ArgumentParser();ap.add_argument('e',type=int);ap.add_argument('s',type=int);ap.add_argument('--native',default=str(H/'.discovery-deps/modbatch'));ap.add_argument('--cap',type=int,default=6_000_000);a=ap.parse_args();t=time.monotonic();verify(a.e,a.s,a.native,a.cap);print('seconds',round(time.monotonic()-t,2),flush=True)
