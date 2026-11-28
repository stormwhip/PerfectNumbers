"""Exact arithmetic coverage for the nine factored-prefix canonical keys."""
from functools import cache
from hashlib import sha1
from math import gcd, isqrt, prod
from pathlib import Path
import gzip, json, sys

H=Path(__file__).resolve().parent
R=H.parents[1]
ORDER=(19,7,11,31,13,3,5,17)
COMMIT='495c59f55456a70994ce7848487e0c4e262c1984'
B=10**2400
FACTORS={
 (11,4):((5,1),(3221,1)), (11,6):((43,1),(45319,1)),
 (11,16):((50544702849929377,1),), (11,18):((6115909044841454629,1),),
 (11,48):((43,1),(45319,1),(510810301,1),(1065264019,1),(100641220283951395639601683,1)),
 (13,2):((3,1),(61,1)), (13,4):((30941,1),), (13,6):((5229043,1),),
 (13,8):((3,2),(61,1),(1609669,1)),
}
PIVOTS={k:max(q for q,_ in v) for k,v in FACTORS.items()}
# Use the larger source for (13,8) but cover all exponent branches of the same source.
POCK={100641220283951395639601683:(342317075795753046393203,),
      342317075795753046393203:(34781251350919838081,),
      34781251350919838081:(35291471,1539910457),
      32607907713428723311:(731363,16787009),
      2718112670273680688549131:(3939293725034319838477,),
      3939293725034319838477:(4952021799131003,)}


def require(test,why):
    if not test:raise ValueError(why)


@cache
def prime64(n):
    if not 2<=n<2**64:return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0:return n==p
    d=n-1;s=0
    while d%2==0:d//=2;s+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a%n==0:continue
        v=pow(a,d,n)
        if v in (1,n-1):continue
        for _ in range(s-1):
            v=v*v%n
            if v==n-1:break
        else:return False
    return True


def prime(n):
    if n<2**64:return prime64(n)
    fs=POCK[n]; F=prod(fs)
    return F*F>n and (n-1)%F==0 and pow(2,n-1,n)==1 and all(prime(f) and gcd(pow(2,(n-1)//f,n)-1,n)==1 for f in fs)


@cache
def sigma(b,h):return (b**(h+1)-1)//(b-1)


def trim(n,p):
    while n%p==0:n//=p
    return n


def val(n,q):
    h=0
    while n%q==0:n//=q;h+=1
    return h


def initial(p,e):
    a=sigma(p,e);fac=FACTORS[p,e];q=PIVOTS[p,e]
    require(all(prime(r) for r,h in fac) and prod(r**h for r,h in fac)==a, ('A factorization',p,e))
    require(all(a%r for r in ORDER[:ORDER.index(p)]), ('forbidden initial',p,e))
    return a,q


def legal_prefix(rows,ban):
    names=dict(rows)
    if len(names)!=len(rows) or any(q in ban for q in names):return False
    if sum(f%2 for f in names.values())>1:return False
    if any(f%2 and f%4!=1 or f%2 and q%4!=1 for q,f in names.items()):return False
    x=prod(q**f for q,f in names.items());s=prod(sigma(q,f) for q,f in names.items())
    if gcd(s,prod(ban))!=1 or s>2*x:return False
    sd=s//(s&-s);d=sd
    for q,f in names.items():
        if sd%(q**(f+1))==0:return False
        d=trim(d,q)
    return x*d<=B


def domain(p,e,q=None,mask=None):
    a,t=initial(p,e)
    if q is None:q=t
    require(a%q==0 and prime(q),('first pivot',p,e,q))
    c=val(a,q);x=p**e*(a//q**c); raw=c;r=x*q**c;live=[];rejected=[]
    bans=ORDER[:ORDER.index(p)] if mask is None else tuple(v for i,v in enumerate(ORDER) if not (mask>>i)&1)
    require(p not in bans and all(z in bans for z in ORDER[:ORDER.index(p)]),('mask',mask))
    while r<=B:
        (live if legal_prefix(((p,e),(q,raw)),bans) else rejected).append(raw)
        raw+=1;r*=q
    require(r>B and r//q<=B,('tail',p,e,q))
    return live,raw,rejected


def blob(path,hexdigest):
    raw=(R/path).read_bytes().replace(b'\r\n',b'\n')
    require(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==hexdigest,('frozen blob',path))
    return json.loads(raw)


EXPECTED_COUNTS={
 (11,4):(211,683), (11,6):(98,514), (11,16):(47,143), (11,18):(37,127), (11,48):(19,90),
 (13,2):(297,1343), (13,4):(122,534), (13,6):(50,357), (13,8):(89,385),
}
EXPECTED_SHARDS={
 'P11_I00001':((11,4),), 'P11_I00002':((11,6),(11,48)), 'P11_I00005':((11,16),), 'P11_I00006':((11,18),),
 'P13_I00001':((13,2),(13,8)), 'P13_I00002':((13,4),), 'P13_I00003':((13,6),),
 'P13_I00111':((13,612),), 'P13_I00113':((13,618),),
}


def main():
    top=blob('FinalNight2400/OpenFrontier.json','6dd4c8d3ca351811807c5ec078f7e4bcb1538575')
    prior=blob('Session20261126/OpenSupport.json','3942774712efa94ec6251dd22426590fa775e473')
    shards={s:tuple(map(tuple,rows)) for s,rows in top['ShardRemainders'].items() if any(p in (11,13) for p,e in rows)}
    require(shards==EXPECTED_SHARDS,'target shard disagreement')
    require(len({row for rows in shards.values() for row in rows})==11 and sum(len(x)==1 for x in shards.values())==7,'target projection counts')
    require(tuple(prior['order'])==ORDER,'historical support order')
    print(COMMIT, '9 targeted shards; 11 keys; 7 singleton shards', flush=True)
    for p,e in FACTORS:
        fs,t,rej=domain(p,e)
        require((len(fs),t)==EXPECTED_COUNTS[p,e],('raw exact prefix counts',p,e))
        print(p,e,PIVOTS[p,e],len(fs),t,fs[:15],fs[-8:],'historical masks',prior['rows'][f'{p}:{e}'],flush=True)
    for e in (612,618):
        a=sigma(13,e);require(all(a%q for q in ORDER[:4]),('anonymous initial',e))
        print(13,e,'anonymous',a.bit_length(),'bits','historical masks',prior['rows'][f'13:{e}'],flush=True)

if __name__=='__main__':main()
