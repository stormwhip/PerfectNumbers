"""Independent standard-library certificate reader for the root-three multiplicative trees.
    python -I -S Research/ThreeChainNext/Replay.py
A missing/tampered prime witness, an unresolved branch, or a wrong coverage set is fatal.
"""
import argparse, csv, gzip, json, sys
from math import gcd, isqrt, prod
from functools import cache
from hashlib import sha256
from pathlib import Path
from bisect import bisect_right
H=Path(__file__).resolve().parent;R=H.parent;B=10**2400;BANNED=(7,11,13,19,31)
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def require(test,why):
    if not test:raise ValueError(why)
def load(p):return json.loads(p.read_text(encoding='utf8'))
def mr(n):
    if not 2<=n<2**64:return False
    if n%2==0:return n==2
    d=n-1;t=0
    while d%2==0:d//=2;t+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a%n==0:continue
        x=pow(a,d,n)
        if x==1:continue
        for _ in range(t):
            if x==n-1:break
            x=x*x%n
        else:return False
    return True

def elliptic(n,t,s,a,point):
    # Mixed Jacobian, two independent fixed-affine multiplications; every conditional
    # division and every projective nonzero Z stays a unit mod every divisor of n.
    m=n+1-t;require(n>3 and gcd(n,6)==1 and t*t<4*n and s>=1 and m%s==0,'invalid ECPP order');q=m//s
    require((isqrt(isqrt(n))+2)**2<q<n,'Hasse bound failure'); x,y=[v%n for v in point];b=(y*y-x*x*x-a*x)%n
    require(gcd(4*a**3+27*b*b,n)==1,'singular curve');units=1
    def dbl(P):
        nonlocal units
        if P is None or P[1]==0:return None
        X,Y,Z=P;units=units*Y%n;u=Y*Y%n;h=(3*X*X+a*pow(Z,4,n))%n;d=4*X*u%n;v=(h*h-2*d)%n
        return v,(h*(d-v)-8*u*u)%n,2*Y*Z%n
    def add(P):
        nonlocal units
        if P is None:return (x,y,1)
        X,Y,Z=P;z2=Z*Z%n;d=(x*z2-X)%n;v=(y*z2*Z-Y)%n
        if d==0:
            if v==0:return dbl(P)
            require((y*z2*Z+Y)%n==0,'inconsistent inverse');units=units*v%n;return None
        units=units*d%n;u=d*d%n;w=u*d%n;g=X*u%n;xx=(v*v-w-2*g)%n
        return xx,(v*(g-xx)-Y*w)%n,Z*d%n
    def mul(k):
        Q=None
        for bit in bin(k)[2:]:
            Q=dbl(Q)
            if bit=='1':Q=add(Q)
        return Q
    part=mul(s);require(part is not None and gcd(part[2],n)==1,'trivial cofactor point');require(mul(m) is None and gcd(units,n)==1,'invalid ECPP order witness');return q
@cache
def bundle():
    with gzip.open(H/'Primality.json.gz','rt',encoding='utf8') as f:return json.load(f)
@cache
def proven(n):
    if n<2**64:return mr(n)
    a=bundle()[sha256(str(n).encode()).hexdigest()[:24]];k=n
    for node in a:
        require(node[0]==k,'wrong certificate chain');k=elliptic(*node)
    require(mr(k),'wrong certificate terminus');return True

def ilog(n,b):
    j=0
    while n>=b:n//=b;j+=1
    return j

def val(n,r):
    k=0
    while n%r==0:n//=r;k+=1
    return k

def sigma(r,f):return (r**(f+1)-1)//(r-1)
@cache
def legal(r,f):
    return all(pow(r,f+1,z*(r-1))!=1 for z in BANNED)
@cache
def lower(r,c,odd):
    if odd and (r%4!=1 or any((r+1)%b==0 for b in BANNED)):return None
    g=c+(1-c)%4 if odd else c+c%2
    while not legal(r,g):g+=4 if odd else 2
    return g
PR=[r for r in range(5,16000,2) if r not in BANNED and all(r%d for d in range(3,isqrt(r)+1,2))];SM=[r for r in PR if r<=2000]
@cache
def tails(ex,eu):
    t=1;n=d=1;out=[1];ab=[(1,1)]
    for r in PR:
        if r in ex:continue
        t*=r;cap=t*t//(1 if eu else r)
        if cap>B:break
        n*=r;d*=r-1;out.append(cap);ab.append((n,d))
    else:raise ArithmeticError('short tail table')
    return out,ab
@cache
def discount(r,f,C):
    # Required even component already charged through f. A unit is possible only
    # at a legal 3^j-1 threshold. Allow ALL earlier free units through floor f.
    if r%3!=1:return 0
    j=ilog(f+1,3); out=C*j; h=3**(j+1)-1
    while legal(r,h):
        cost=(r**(h-f)).bit_length()-1
        if cost>=C:break
        out+=C-cost;f=h;h=3*(h+1)-1
    return out
@cache
def small_discount(C):
    require(16000**2>=1<<C,'short discount table');return sum(discount(r,0,C) for r in PR if r*r<1<<C)

def replay(row,cap=20000):
    e=row['e'];require(type(e)==int and 2<=e<=3000 and e%2==0,'invalid e');A=sigma(3,e);rr=set(map(int,row['root'])); require(all(z>3 and A%z==0 and proven(z) for z in rr),'invalid root prime'); edges={}
    for raw,j,child in row['edges']:
        r,z=int(raw),int(child);require(type(j)==int and r>3 and 0<j<=8000 and z>3 and pow(r,j+1,(r-1)*z)==1 and proven(z),'bad sigma factor');edges.setdefault((r,j),set()).add(z)
    stats={};nodes=0;maxdepth=0
    def end(s):stats[s]=stats.get(s,0)+1;return True
    def walk(ex,depth):
        nonlocal nodes,maxdepth
        nodes+=1;maxdepth=max(maxdepth,depth);require(nodes<=cap and depth<60,'branch budget exhausted');X=prod(r**j for r,j in ex);S=prod(sigma(r,j) for r,j in ex);eu=any(j%2 for r,j in ex);D=S//gcd(S,2*X)
        if gcd(D,X*prod(BANNED))!=1 or S>2*X or D*X>B:return end('sigma')
        keys=rr|set(SM)
        for k in ex:keys|=edges.get(k,set())
        sizes={};M=X;U=D
        for r in keys:
            if U%r:continue
            c=val(U,r);U//=r**c;fe=lower(r,c,False);fo=None if eu else lower(r,c,True);M*=r**fe;sizes[r]=(fe,fo)
        M*=U
        def best(skip):return max([1]+[r**max(0,f-o) for r,(f,o) in sizes.items() if o is not None and r!=skip]);
        room=B*best(None)//M
        if not room:return end('floor')
        K=ilog(U,2001);n=S*2001**K*prod(sizes);d=X*2000**K*prod(r-1 for r in sizes);xs,ab=tails(tuple(i for i in PR[:18] if i in sizes or any(i==z for z,j in ex)),eu);an,ad=ab[bisect_right(xs,room)-1]
        if n*an<2*d*ad:return end('abundance')
        k=e-val(S,3)
        require(k>=0,'root surplus should already have closed')
        for C in (12,17,22,27):
            loss=small_discount(C)+sum(discount(r,f,C) for r,(f,o) in sizes.items())+(U.bit_length() if U>1 else 0);rhs=B<<loss
            if eu:
                if M<<(C*k)>rhs:return end('valuation')
            else:
                # Euler among known primes, or external to them (subtract its overlap with U).
                if M*3**k<=rhs*U:continue
                if all(o is None or ((M//(r**f)*r**o)<<(C*max(0,k-7-(val(r+1,3) if r%3==2 else 0))))>rhs for r,(f,o) in sizes.items()):return end('valuation')
        if not sizes:return False
        r=max(sizes);f,o=sizes[r];fixed=M//r**f
        # Two complete arithmetic progressions. An unknown/missing edge can only weaken this proof.
        for start,step,cap_ in [(f,2,B*best(r))]+([] if o is None else [(o,4,B)]):
            j=start;power=r**start
            while fixed*power<=cap_:
                if legal(r,j) and not walk(ex+[(r,j)],depth+1):return False
                j+=step;power*=r**step
        return end('split')
    require(walk([(3,e)],0),'unexcluded branch at e='+str(e));return {'e':e,'nodes':nodes,'depth':maxdepth,'rules':stats}

def coverage(proved):
    te=load(R/'TeichmullerValuation/Audit2400.json');ge=load(R/'TeichmullerValuation/GeminiBatchAudit2400.json');old={tuple(x) for x in ge['verified_exponents']}|{(r['root'],step['exponent']) for r in te['additions'] for step in r['proof']}
    for p in ('SupplierBatch/BatchAudit2400.json','IndicatorCapacity/Audit2400.json'):old.update((r['root'],r['exponent']) for r in load(R/p)['exact_exponents'])
    with (R/'FermatRootValuation/Exponents.csv').open(encoding='utf8') as src:universe={int(v['actual_e']) for v in csv.DictReader(src) if v['p']=='3' and v['result']=='OPEN' and (3,int(v['actual_e'])) not in old}
    baseline={1296,1300,1302,1308,1312,1330};require(len(universe)==350 and baseline<=universe,'baseline exponent mismatch');pending=universe-baseline;require(proved<=pending,'exponent not in pending baseline');removed={r['id'] for r in ge['additions']};shards=[r for r in te['open_manifest'] if r['id'] not in removed];require(len(shards)==1045,'shard baseline mismatch');out={};prior=[];partial=0;orig=0
    for r in shards:
        if r['root']!=3:continue
        es={e for e in universe if (e==r['exponent'] if r['exact'] else (e+1)%(r['exponent']+1)==0)}
        if not es:continue
        rem=es-baseline
        if not rem:prior.append(r['id']);continue
        orig+=1
        if rem<=proved:out[r['id']]=sorted(rem)
        elif rem&proved:partial+=1
    require(len(prior)==3,'expected three baseline closed shards');return {'baseline':'4aad42d','baseline_global_open':1042,'root3_pending_actual':len(pending),'root3_pending_actual_after':len(pending-proved),'root3_open_with_live_actual':orig,'complete':out,'partial_shards':partial,'global_open_with_this_batch_alone':1042-len(out)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--file',type=Path,default=H/'Certificates.json');p.add_argument('--only',type=int,nargs='+');p.add_argument('--write-summary',type=Path);a=p.parse_args();rows=load(a.file);result=[];tests=set()
    for row in rows:
        if a.only and row['e'] not in a.only:continue
        require(row['e'] not in tests,'duplicate exponent');tests.add(row['e']);r=replay(row);result.append(r);print('ACCEPT',row['e'],r['nodes'],flush=True)
    require(not a.only or tests==set(a.only),'missing selected exponent');cv=coverage(tests);summary={'actual_exponents':sorted(tests),'rows':result,'coverage':cv};print('ACCEPT',len(tests),'actual exponents;',len(cv['complete']),'complete shards;',cv['global_open_with_this_batch_alone'],'global open.');
    if a.write_summary:a.write_summary.write_text(json.dumps(summary,indent=1)+'\n',encoding='utf8')
