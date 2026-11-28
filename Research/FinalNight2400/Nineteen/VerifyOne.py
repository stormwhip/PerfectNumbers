"""Certified source/credit decision tree for exact v_2477=1 under 19^618."""
from pathlib import Path
from functools import cache
from math import prod
import sys,json
P=Path(__file__).resolve().parent;sys.path[:0]=[str(P),str(P.parents[1]/'RootFiveNext')];import PrimeCheck as pc
from Verify618 import p,e,t,B,n,d,deficit,val,sig
K=10000
@cache
def loglo(z):return (z**K).bit_length()-1
@cache
def opts(z):
    O=[];m=z*z;h=2;o=next((j for j in (1,3,9) if pow(z,j,p)==1),0);b=val(z**o-1,p) if o>1 else 0
    while m<=B:
        u=(b+val(h+1,p)) if o and (h+1)%o==0 else 0
        score=d*h*loglo(z)-n*u*(loglo(p)+1);O.append((h,score));m*=z*z;h+=2
    return O

def main():
    assert __debug__ and pc.prime64(19) and pc.prime64(t);pack=json.loads((P/'OneTree.json').read_bytes());A=sig(p,e);S0=A*((t+1)//2);X0=p**e*t
    seen=set();primes={3,7,59};assert (t+1)//2==prod(primes)
    for k,zz in pack['emissions'].items():
        s=int(k);assert s>0 and all(type(z)==int and z>2 and s%z==0 and pc.prime64(z) for z in zz)
    U,V=deficit(); raw=(B**d*U)//(X0**d*p**(n*e)*V)+1
    # Upper bound on K log2(price budget). Use 100th power only, losing <0.01 bit.
    threshold=(raw**100).bit_length()*(K//100);counts=[0,0,0]
    def walk(rows,S,roots,score,node):
        counts[0]+=1
        if any(val(S,z)>h for z,h in rows.items()):return
        avail={z:[(h,v) for h,v in opts(z) if h>=val(S,z)] for z in roots if z not in rows}
        if any(not O for O in avail.values()):return
        mins={z:min(v for h,v in O) for z,O in avail.items()};cur=score+sum(mins.values())
        if cur>threshold:counts[1]+=1;return
        ratN=prod(sig(z,h) for z,h in rows.items());ratD=prod(z**h for z,h in rows.items())
        for z,O in avail.items():
            h=O[0][0];ratN*=sig(z,h);ratD*=z**h
        if ratN>2*ratD:counts[2]+=1;return
        assert isinstance(node,dict);z=node['q'];O=avail[z];kids=node['cases']
        live=[(h,v) for h,v in O if cur-mins[z]+v<=threshold]
        assert set(str(h) for h,v in live)<=set(kids)
        for h,v in live:
            emit=sig(z,h);zz=pack['emissions'][str(emit)];walk(rows|{z:h},S*emit,roots|set(zz),score+v,kids[str(h)])
    walk({p:e,t:1},S0,primes,0,pack['tree']);print('PASS 19^618 Euler 2477^1; visited / priced / abundant',counts,flush=True)
if __name__=='__main__':main()
