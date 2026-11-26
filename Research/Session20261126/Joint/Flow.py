"""Joint finite-prime/unknown-tail LP strengthened by all incoming edges, aggregate and threshold cuts.
Usage python -B Flow.py SNAPSHOT search|verify index [certificate]; verify needs only stdlib.
Witness coefficients are nonnegative multiples of 1/10^7. Output bounds are recomputed by integer weak duality.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Joint import *
DEN=10**7

def model(i,external=False):
    leaf=(cert['cell10']+cert['cell11'])[i];F=leaf['forest'] or {};Lp=leaf['lp'] or {};absent=BAN|set(leaf['absent_extra']);req=set(leaf['present']);ps=set(map(int,F.get('cut_even',{})))|set(Lp.get('P',[]));pool=sorted(ps)
    # Dynamically admit small primes beyond original forest to use all their inflows, including for forest-only leaves.
    ps.update(r for r in small if r<3000 and r not in absent);pool=sorted(ps);L=next(r for r in small if r not in ps|absent)
    assert all(prime(t) and A%t and t<Q and nosource(t) for t in pool)
    opts={};rows=[];rhs=[];names=[];data=[];flows={};absrow={};volrow={};vmin={};vcap={}
    def add(name,row,b):names.append(name);rows.append(row);rhs.append(b)
    for r in pool:
        stop=F.get('cut_even',{}).get(str(r),42 if r<100 else 22 if r<400 else 12);opts[r]=[];fe=stop
        while any(sig(r,fe)%t==0 for t in absent):fe+=2
        for f in list(range(2,stop,2))+[None]:
            if f is None:
                c=fe*lo(r)-(4*hi(fe+1) if r%3==1 else 0);ab=hi(r)-lo(r-1);vv=0
            else:
                n=sig(r,f)
                if any(n%t==0 for t in absent):continue
                c=f*lo(r)-4*hi(3)*val(n,3);ab=hi(n)-f*lo(r);n//=3**val(n,3)
                for t in pool:
                    if n%t==0:
                        h=val(n,t);n//=t**h;flows.setdefault(t,{})[len(data)]=h
                # Newly enlarged pool has unchanged or smaller cleaned residues on original options;
                # also check each new row rather than relying on old audit.
                if gcd(n,A)!=1 or n>=Q:vv=0
                else:
                    b,left=small_parts(n);vv=sum(h*(lo(t)-(2*hi(3) if t%3==1 else 0)) for t,h in b)
                    assert all(nosource(t) for t,h in b)
                    if left>1 and (not external or (prime(left) and nosource(left))):vv+=lo(left)*(lo(50000)-2*hi(3))//lo(50000)
            j=len(data);data.append(c);opts[r].append((f,j));absrow[j]=-ab;volrow[j]=vv
        add('sel'+str(r),{j:T for _,j in opts[r]},T)
        if r in req:add('req'+str(r),{j:-T for _,j in opts[r]},-T)
    # Partition into finite primes, unknown auxiliary primes, and the exceptional A,q,r.
    # A's prime factors >1e8 (verified via modular trial below); at most 70, hence log abundance <1e-6.
    # External source and q each >~5e4 in base (global small-base test); both together cost <0.00005.
    for r in range(2*(e+1)+1,10**8+1,2*(e+1)):
        assert pow(3,e+1,r)!=1 or not prime64(r)
    assert all(nosource(t) for t in small if t not in BAN)
    ext=len(data);data.append(T)
    # scale A_ij,T for external log-net variable in *nats*, c_ab upward.
    absrow[ext]=-((hi(L)-lo(L-1))*T//(2*(lo(L)-2*hi(3)))+1);volrow[ext]=-T
    add('ab',absrow,-(lo(4)-hi(3)-50000));add('vol',volrow,0)
    for t,fl in flows.items():
        upper= B.bit_length()//max(1,t.bit_length()-1) # exact finite global exponent ceiling
        row={j:v*T for j,v in fl.items()}
        for f,k in opts[t]:row[k]=row.get(k,0)-(upper if f is None else f)*T
        add('sum'+str(t),row,0)
        # Individual supports and multiplicity covers; add every finite edge.
        for j,v in fl.items():
            row={j:T}
            for f,k in opts[t]:
                if f is None or f>=v:row[k]=row.get(k,0)-T
            add('edge'+str((t,j)),row,0)
    return data,rows,rhs,names

def getdual(i,external=False):
    data,rows,rhs,names=model(i,external);key=Path(__file__).parent/(('DualExternal' if external else 'DualFlow')+str(i)+'.json');optmode=sys.argv[2]
    if optmode=='search':
        import scipy.optimize as so,numpy as np
        from scipy.sparse import coo_matrix
        def solve(active):
            I=[];J=[];V=[]
            for k in active:
                rr=rows[k];I.extend([len(b)]*len(rr));J.extend(rr);V.extend(val/T for val in rr.values());b.append(rhs[k]/T)
            a=coo_matrix((V,(I,J)),shape=(len(b),len(data))).tocsr();res=so.linprog([c/T for c in data],A_ub=a,b_ub=b,bounds=[(0,1)]*(len(data)-1)+[(0,None)],method='highs');assert res.success,res.message
            return {names[k]:int(round(max(0.,-float(m))*DEN)) for k,m in zip(active,res.ineqlin.marginals) if m<0}
        b=[];dual=solve(range(len(rows)));key.write_text(json.dumps(dual,separators=(',',':')),encoding='utf-8')
    else:assert optmode=='verify';dual=json.loads(key.read_bytes())
    assert set(dual)<=set(names) and all(type(v)==int and v>=0 for v in dual.values());rc=[v*DEN for v in data];bound=0
    for row,b,n in zip(rows,rhs,names):
        a=dual.get(n,0)
        if not a:continue
        for j,v in row.items():rc[j]+=a*v
        bound-=a*b
    # An unbounded external variable: always fix any roundoff by reducing all multipliers proportionately.
    if rc[-1]<0:
        k=T*DEN;d=k-rc[-1];rc=[k*v+(d-k)*c*DEN for v,c in zip(rc,data)];bound*=k;den=DEN*d
    else:den=DEN
    assert rc[-1]>=0;bound=(bound+sum(min(0,v) for v in rc[:-1]))//den
    return dict(i=i,rows=len(rows),cols=len(data),net_nanonats=bound,dual_nonzero=len(dual),branch='E3a' if external else 'E3b',floor=((5052805597654 if external else 5000477672899)+bound)//hi(10))
if __name__=='__main__':
    assert __debug__;print(getdual(int(sys.argv[3]),'external' in sys.argv[4:]),flush=True)
