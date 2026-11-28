"""Complete exact conditional exclusion of the rare emitter 13^276."""
from pathlib import Path
from functools import cache
from math import gcd,prod
from fractions import Fraction
import sys,json

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/'Pricing'),str(HERE.parents[1]/'RootFiveNext')]
from PrimeCheck import prime64,level
from Pock import verify as pock
from Net13 import PREFIX, B, sig, vp, loss, X as X0, M as M0, C as DEM19, D13 as DEM13
from RareTarget13 import R,uniform_rare
import E4Price

E=24104457298489411978880226626239089834405670981
W=193674953884899827032111908407518984632293817664100530035167667243179946003138491029077057781
R4=2578012157088772906227552121660556427718057794243245064037125765899184360233830141
ROOTS=(67,967,8311,11621,50627,392233)
D2=(31,15413977)


def need(ok,msg):
    if not ok:raise ValueError(msg)

def state(rows):
    X=prod(p**h for p,h in rows);A=prod(sig(p,h)for p,h in rows);F=A//2;D=F//gcd(X,F)
    return X,F,D,A

def live(rows,B=B):
    X,F,D,A=state(rows)
    return X*D<=B and A<=2*X and all(F%p**(h+1) for p,h in rows)

def candidates(rows,q):
    X,F,D,A=state(rows);a=vp(D,q);need(q not in dict(rows) and a>0,'new forced prime')
    lo=a;scale=X*D//q**a;vals=[]
    while scale*q**a<=B:
        if a%2==0 and live(rows+((q,a),)):vals.append(a)
        a+=1
    return vals,a,lo

@cache
def minimum(p,a,C_R):
    """Gain for one compulsory base in common (19,13,ℓ) 20th-power price."""
    need(p not in dict(PREFIX) and p!=R,'compulsory outside prefix')
    best=None;where=None
    for f in range(a+a%2,5031,2):
        power=p**f
        if X0*R**2*power>B:break
        if best is not None and power**20>=best*(M0*M0)*R**77:break
        g=sig(p,f);u,v,w=vp(g,19),vp(g,13),vp(g,R)
        if u>DEM19 or v>DEM13 or w>C_R:continue
        d=loss().get(p,1)**2
        net=Fraction(power**20,(19**u*13**v)**38*R**(77*w))*d
        if best is None or net<best:best,where=net,f
    return best,where


def gain(rows,forced):
    assert len(forced)==len(set(forced))
    X,S,D,A=state(rows)
    c1=276-vp(S,19);c2=276-vp(S,13);c3=dict(rows)[R]-vp(S,R)
    need(min(c1,c2,c3)>=0,'incoming overfilled')
    exc=loss();Y=Fraction(X**20*(19**c1*13**c2)**38*R**(77*c3),prod(exc.values())**2)
    # With a later exact row fixed, its external debit is removed once.
    Y*=prod(exc.get(p,1)**2 for p,_ in rows)
    for q in forced:
        need(q not in dict(rows) and D%q==0,'not disjoint compelled row')
        z,f=minimum(q,vp(D,q),c3);need(z is not None,'raw forced empty')
        Y*=z
    return Y

def floor10(F):
    n,d=F.numerator,F.denominator
    k=max(0,((n.bit_length()-d.bit_length())*30103)//2000000)
    while 10**(20*k)*d>n:k-=1
    while 10**(20*(k+1))*d<=n:k+=1
    return k


def main():
    need(__debug__,'assertions needed')
    book=json.loads((HERE/'Hard13Certificate.json').read_text(encoding='utf8'))
    ecpp=book['ecpp'];pratt=book['pocklington'];used_e=set();used_p=set()
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        if str(p) in pratt:return pock(p,pratt,prime64,used_p)
        cur=p;chain=ecpp[str(p)];used_e.add(str(p));need(bool(chain),'missing chain')
        for row in chain:
            need(row[0]==cur,'bad ECPP subject');cur=level(*row)
        return prime64(cur)
    need(all(prime(p)for p in (*dict(PREFIX),R,E,W,R4,*ROOTS,*D2,3,5,11)),'all prime witnesses')
    need(uniform_rare() and gcd(R*(R-1),19*13*9)==1,'disjoint uniform rare supply')
    X,S,D,A=state(PREFIX)
    need(A%4==2 and PREFIX[1][0]%4==1 and live(PREFIX),'unique Euler slot')
    need(sig(19,276)%(1176672733*1109)==0 and vp(sig(13,276),1109)==1,'mandatory pivots and rare emitter')
    need(vp(D,R)==1 and vp(S,R)==1 and vp(sig(13,276),R)==1,'first compulsory pivot ℓ')
    need(3**5030<=B<3**5031,'odd index cap')
    hs,tail,first=candidates(PREFIX,R)
    need((hs,tail,first)==(book['R_domain'],book['R_tail'],1),'complete ℓ raw window')
    received={}
    for h in hs:
        P=PREFIX+((R,h),)
        if h!=2:
            if h==4:need(sig(R,4)%R4==0,'ℓ^4 output witness')
            V=gain(P,(R4,) if h==4 else ());need(V>B**20,('ℓ terminal',h));received[str(h)]=floor10(V)
    need(received==book['R_terminal_floors'],'ℓ floors')
    p=PREFIX+((R,2),)
    need(vp(state(p)[2],E)==1 and vp(sig(R,2),E)==1,'second compulsory pivot E')
    ins,tail2,first2=candidates(p,E)
    need((ins,tail2,first2)==(book['E_domain'],book['E_tail'],1),'complete E raw window')
    dig={}
    for h in ins:
        P=p+((E,h),)
        if h==4:
            V,credits=E4Price.compute((*ROOTS,*D2,5,11))
            need(V>B**10,'E^4 terminal');dig[str(h)]=floor10(V**2)
        else:
            forced=(*ROOTS,*D2,*((3,W) if h==2 else ()))
            if h==2:need(sig(E,2)==3*W,'E^2 output witnesses')
            V=gain(P,forced);need(V>B**20,('E terminal',h));dig[str(h)]=floor10(V)
    need(dig==book['E_terminal_floors'],'E floors')
    need(used_e==set(ecpp) and used_p==set(pratt),'unbound prime certificate')
    print('PASS entire exact (19^276,1176672733^1,1109^2,13^276) emitter state')
    print('L raw domain/tail:',hs,tail,'strict floor10:',received)
    print('E raw domain/tail:',ins,tail2,'strict floor10:',dig)

if __name__=='__main__':main()
