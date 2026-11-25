"""Additional certified *all-index* implications. No bound on N needed."""
from fractions import Fraction
from itertools import chain
from math import prod,isqrt

def prime(q):return q>2 and all(q%j for j in range(2,isqrt(q)+1))
def I(q,f):return Fraction(q**(f+1)-1,(q-1)*q**f)
def least(seed,bad,K,fixed):
    X=dict(fixed);sp=any(f%2 for f in X.values());r=set(K)-X.keys();choices=[0,*[q for q in r if not sp and q%4==1 and all((q+1)%b for b in bad)]];known=prod(I(q,f) for q,f in X.items());p,f0=seed;known*=I(p,f0)
    def exp(q,sp,h):
        f=h+( (1-h)%4 if sp else h%2)
        while any((q**(f+1)-1)//(q-1)%b==0 for b in bad):f+=4 if sp else 2
        return f
    return min(known*prod(I(q,exp(q,q==t,K[q])) for q in r) for t in choices)

def check(p,bad0,br,seq):
    assert prod(br)==(p**11-1)//(p-1) and all(map(prime,br));K={q:1 for q in {*br,3,5}};bad=list(bad0);fixed=[];out=[]
    for k,ls in seq:
        a=[]
        for q in ls:
            if k=='absent':v=least((p,10),bad,{**K,q:1},fixed)
            elif k=='exact1':v=least((p,10),bad,{**K,q:2},fixed)
            else:v=least((p,10),bad,{**K,q:3},fixed)
            if v<=2:raise ValueError((k,q,v))
            a.append([q,v.numerator*10**6//v.denominator]);
        out.append([k,a]);
        if k=='absent':bad+=ls
        else:fixed.extend((q,1 if k=='exact1' else 2) for q in ls)
    return out
if __name__=='__main__':
 print('31',check(31,[19,7,11],(23,397,617,150332843),[('absent',[13]),('absent',[17,29,37]),('exact1',[5])]))
 print('13',check(13,[19,7,11,31],(23,419,859,18041),[('absent',[17,29,37,41,43,47,53,59,61]),('exact2',[3]),('exact1',[5])]))
