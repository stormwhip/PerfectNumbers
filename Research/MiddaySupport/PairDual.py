"""Cold stdlib-only replay of two conditional exponent sets. Under N<=10^2400, the independently proved four-root hitting set forces 11 when 3/5/7 absent, or 7 when 3/5/11 absent. Verify promoted local option cutoffs, factor edges, rough anonymous source rows, fixed-p residual dual, upper exponent tail and every integer exponent below it. No scipy, sympy, external generators or previous survivor lists trusted. Printed survivors compared after all branches. Older 13-only release has a different model: do not silently substitute its model ID.
"""
from pathlib import Path
from functools import cache
import sys,math,gzip,json,hashlib,argparse,time
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import DYADIC,verify;from RoadblockDual import SCALE,odd_primes,log_bounds
sys.path.insert(0,str(R/'TeichmullerValuation'));from VerifyGeminiExponents2400 import is_prime_det64

def req(a,s):
    if not a:raise ValueError(s)
@cache
def sigma(r,e):return (r**(e+1)-1)//(r-1)
@cache
def prod(L):return math.prod(odd_primes(L-1))
@cache
def hg(n,L):
    c=0
    while n>=L:n//=L;c+=1
    return sum(log_bounds(L+2*j,L+2*j-1)[1] for j in range(c))
@cache
def rough(n):
    for L in (300001,100001,30001,10001):
        if math.gcd(n,prod(L))==1:return L
    return 5001

def val(n,p):
    a=0
    while n%p==0:a+=1;n//=p
    return a

def main():
    if not __debug__:raise SystemExit('run without -O')
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);args=ap.parse_args();D=json.loads(args.packet.read_text());now=time.perf_counter();A=[];proof=D['proof'];sup=set()
    for lab in ('Original','Replacement'):
        file=T/f'Certificates/Terminal{lab}.json.gz';req(hashlib.sha256(file.read_bytes()).hexdigest()==D['archive_sha256'][lab],'archive');ar=json.load(gzip.open(file,'rt'));verify(ar);A.append(ar);sup.update(q for r,f,q,v in ar['edges'])
    @cache
    def prime(n):
        if n in sup:return True
        if n<2**64:return is_prime_det64(n)
        F=1;seen=set()
        for q,k,a in proof.get(str(n),[]):
            if not(type(q)==type(k)==type(a)==int and 2<=q<n and q not in seen and 1<=k<=n.bit_length() and 1<a<n and prime(q)):return False
            F*=q**k;seen.add(q)
            if (n-1)%F or pow(a,n-1,n)!=1 or math.gcd(pow(a,(n-1)//q,n)-1,n)!=1:return False
        return F*F>n
    out=[];prior=set()
    for x in D['cases']:
        p=x['p'];bad=x['forbidden'];cap=x['cut'];req(type(p)==int and p in (3,5,7) and type(bad)==list and set(bad)=={3,5,7}-{p} and len(set(bad))==len(bad) and p not in prior and type(cap)==int and 22<=cap<=100,'invalid case');prior.add(p);base=set(odd_primes(5000))-set(bad);M={r:cap for r in base};E={}
        def legal(r,f):return all((f+1)%q if r%q==1 else pow(r,f+1,q)!=1 for q in bad)
        rawprom=x['promoted'];rawprom={int(r):f for r,f in rawprom.items()} if isinstance(rawprom,dict) else dict(rawprom);promoted=set()
        for r,f in rawprom.items():
            req(type(r)==type(f)==int and r>2 and r not in bad and r!=p and r not in promoted and 1<=f<=400 and prime(r),'secondary');promoted.add(r);M[r]=max(M.get(r,0),f)
        for ar in A:
            for r,f,q,c in ar['edges']:
                if r in base and r!=p and q not in bad and q!=p and f<=cap and legal(r,f):E[r,f,q]=max(c,E.get((r,f,q),0))
        for r,f,q,c in x['new']:
            req(all(type(z)==int for z in (r,f,q,c)) and r!=p and r in M and 1<=f<=M[r] and (not f%2 or r%4==f%4==1) and legal(r,f) and q>2 and q!=r and q!=p and q not in bad and 1<=c<=255 and sigma(r,f)%q**c==0 and prime(q),'factor');E[r,f,q]=max(c,E.get((r,f,q),0))
        es=sorted((*ks,c) for ks,c in E.items());ps=sorted(set(M)|{q for r,f,q,c in es});C=[];ab=[];eu=[];G={};exact={}
        for r in ps:
            ls=[];l=log_bounds(r)[0];stop=M.get(r,0)
            for start,step,sp in ((2,2,False),(1,4,True)):
                if sp and (r%4!=1 or not legal(r,1)):continue
                f=start
                while f<=stop:
                    if legal(r,f):
                        j=len(C);C.append(f*l);ab.append(log_bounds(sigma(r,f),r**f)[1]);ls.append((j,f,sp,True));exact[r,f]=(j,sp)
                        if sp:eu.append(j)
                    f+=step
                while not legal(r,f):f+=step
                j=len(C);C.append(f*l);ab.append(log_bounds(r,r-1)[1]);ls.append((j,f,sp,False));
                if sp:eu.append(j)
            G[r]=ls
        tail=len(C);lo=log_bounds(5001)[0];hi=log_bounds(5001,5000)[1];C.extend((2*lo*SCALE//hi,lo));ab.extend((SCALE,hi));eu.append(tail+1);original=C.copy();used=math.prod(set(ps)|set(bad));seen=set();bl=[];by_origin={}
        for r,f,n,L in x['blocks']:
            req(all(type(a)==int for a in (r,f,n,L)) and r!=p and (r,f) in exact and (r,f) not in seen and n>1 and n%2 and sigma(r,f)%n==0 and math.gcd(n,used)==1 and 5001<=L<=300001 and L%2 and math.gcd(n,prod(L))==1,'anonymous');seen.add((r,f));req(all(math.gcd(n,v)==1 for b,v in by_origin.items() if b!=r),'coactive overlap');by_origin[r]=math.lcm(n,by_origin.get(r,1));j,sp=exact[r,f];C[j]+=log_bounds(n)[0];ab[j]+=hg(n,L);bl.append((r,j,n,L))
        rows=[(list(enumerate(-v for v in ab)),-log_bounds(2)[0]+log_bounds(p,p-1)[1]), ([(j,SCALE) for j in eu],SCALE)];rows.extend(([(j,SCALE) for j,f,sp,ex in G[r]],0 if r==p else SCALE) for r in ps)
        for r,f,q,c in es:
            j,s=exact[r,f];rows.append(([(j,SCALE)]+[(i,-SCALE) for i,g,sp,ex in G[q] if (not s or not sp) and (not ex or g>=c)],0))
        red=[c*DYADIC for c in C];v=0;last=-1;w0=0
        for i,w in x['weights']:
            req(type(i)==type(w)==int and last<i<len(rows) and w>=0,'weight');last=i;ts,dr=rows[i];v-=w*dr
            if i==0:w0=w
            for j,a in ts:red[j]+=w*a
        req(red[tail]>=0,'tail');v+=sum(min(0,c) for j,c in enumerate(red) if j!=tail);gm={}
        for r,ls in G.items():
            rr=[red[j] for j,f,sp,ex in ls];gm[r]=min(0,min(rr));v+=gm[r]-sum(min(0,b) for b in rr)
        req(v==x['constant'],'fixed dual');lim=2400*DYADIC*log_bounds(10)[1];unit=DYADIC*log_bounds(p)[0];top=max(0,1+(lim-v)//unit);B=10**2400;surv=[];counts={}
        H=Path(__file__).resolve().parent
        sys.path.insert(0,str(R/'RootFiveNext'));from PrimeCheck import prime64,level
        HN=json.loads((H/'PairHints.json').read_text()); hints=HN['factors']; chains=HN['cert']; results={}; original_surv=[]; digits={}; oldblocks=math.prod({b for r,j,b,L in bl}); explicit=math.prod(ps)*math.prod(bad)
        Noms=json.loads((H/'HintNominations.json').read_text()); Pock=json.loads((H/'Pock.json').read_text());
        if (H/'MorePock.json').is_file():
            Pock.update(json.loads((H/'MorePock.json').read_text()))
            for e,ls in json.loads((H/'MoreHints.json').read_text()).items():Noms[e]=sorted(set(Noms.get(e,[]))|set(ls))
        for e,fs0 in Noms.items():hints[e]=sorted(set(hints.get(e,[]))|{q for q in fs0 if q<2**64 or str(q) in Pock})
        if p!=7:
            hints={};pk=H/f'Pock{p}.json'
            if pk.exists():
                Pock.update(json.loads(pk.read_text()));hints={e:[q for q in ls if q<2**64 or str(q) in Pock] for e,ls in json.loads((H/f'Hints{p}.json').read_text()).items()}
        @cache
        def pock(q):
            if q<2**64:return 2<=q and is_prime_det64(q)
            F=1;seenq=set()
            for r,k,a in Pock[str(q)]:
                req(2<=r<q and r not in seenq and 0<k<=q.bit_length() and 1<a<q and pock(r),'pock chain');seenq.add(r);F*=r**k
                req((q-1)%F==0 and pow(a,q-1,q)==1 and math.gcd(q,pow(a,(q-1)//r,q)-1)==1,'pock witness')
            return F*F>q
        @cache
        def hinted(q):
            if q<2**64:return q>2 and prime64(q)
            if str(q) in Pock:return pock(q)
            t=q
            for row in chains[str(q)]:
                req(t==row[0],'ECPP link');t=level(*row)
            return t<2**64 and prime64(t)
        for e in range(2,top,2):
            a=sigma(p,e);pe=p**e
            if math.gcd(a,math.prod(bad))>1:counts['forbidden']=counts.get('forbidden',0)+1;continue
            if a*pe>B:counts['size']=counts.get('size',0)+1;continue
            n=a;fs={}
            for r in ps:
                if n%r==0:c=val(n,r);fs[r]=c;n//=r**c
            z=v+unit*e+DYADIC*log_bounds(n)[0]-w0*hg(n,rough(n));ch={};affected=set(fs)
            for r,j,b,L in bl:
                b0=b;g=math.gcd(b0,n)
                while g!=1:b0//=g;g=math.gcd(b0,n)
                if b0!=b:ch[j]=DYADIC*(log_bounds(b0)[0]-log_bounds(b)[0])+w0*(hg(b,L)-hg(b0,L));affected.add(r)
            explicit_gain=0
            for r in affected:
                c=fs.get(r,0);best=min(red[j]+ch.get(j,0)+DYADIC*max(0,c*log_bounds(r)[0]-original[j]) for j,f,sp,ex in G[r]);z+=(best if c else min(0,best))-gm[r]
                if not c:continue
                alt=[];lr=log_bounds(r)[0]
                for j,f,sp,ex in G[r]:
                    if ex and f<c:continue
                    g=max(c,f);g+=((1-g)%4 if sp else g%2);step=4 if sp else 2
                    while not legal(r,g):g+=step
                    # Exact model options cannot be silently reinterpreted as larger.
                    if ex and g!=f:continue
                    vals=[]
                    while ex or g<=f+8:
                        c1=sigma(r,g)//(2 if sp else 1)
                        for uu in (explicit,a,oldblocks):
                            while (dd:=math.gcd(c1,uu))>1:c1//=dd
                        vals.append(DYADIC*((g-f)*lr)+max(0,DYADIC*log_bounds(c1)[0]-w0*hg(c1,rough(c1))))
                        if ex:break
                        g+=step
                        while not legal(r,g):g+=step
                    if not ex:vals.append(DYADIC*(g-f)*lr)
                    alt.append(red[j]+ch.get(j,0)+min(vals))
                explicit_gain+=max(0,min(alt)-best)
            if z>lim:counts['dual']=counts.get('dual',0)+1;continue
            original_surv.append(e)
            # Refund bound already accounted for ALL anonymous blocks sharing n.
            # Refine n into authenticated prime powers and unclassified rem.
            # Each new ordinary prime needs the next even exponent. Euler may
            # consume at most one of these discounts, and may be elsewhere.
            rem=n;extra=0;save=0;benef=0;known=[]
            for q in hints.get(str(e),[]):
                req(hinted(q) and a%q==0,'hint');k=val(rem,q)
                if not k:continue
                rem//=q**k;known.append((q,k));benef+=log_bounds(q,q-1)[1]
                if k%2:
                    extra+=log_bounds(q)[0]
                    if q%4==1 and legal(q,1):save=max(save,log_bounds(q)[0])
            # Factor geometrical sum into cyclotomic layers. Distinct layer
            # pieces need not be coprime: move their common prime support to
            # a last piece before using the ordinary odd-valuation bonus.
            parts={};left=rem;raw=[]
            for h in range(3,e+2,2):
                if (e+1)%h:continue
                ph=(p**h-1)//(p-1)
                for k,bq in parts.items():
                    if not h%k:ph//=bq
                parts[h]=ph;sv=math.gcd(left,ph);left//=sv
                if sv>1:raw.append((h,sv))
            req(left==1,'cyclotomic cover');prior=1;col=1;revised=[]
            for j,(h,u) in enumerate(raw):
                w=math.prod(v for i,(_,v) in enumerate(raw) if i!=j);u0=u
                while (g:=math.gcd(u,w))>1:u//=g
                col*=u0//u
                if u>1:revised.append((h,u))
            if col>1:revised.append((1,col))
            for h,u in revised:
                L=rough(u);order=1
                # For r|Phi_h(p), r not dividing h implies ord_r(p)=h;
                # r is odd, hence r=1 mod 2h. Ignore this if gcd(h,u)>1.
                if math.gcd(h,u)==1:order=2*h
                lower=L+((1-L)%order);j=0;v0=u
                while v0>=lower:v0//=lower;j+=1
                benef+=sum(log_bounds(lower+k*order,lower+k*order-1)[1] for k in range(j))
                if math.isqrt(u)**2!=u:
                    add=log_bounds(lower)[0];extra+=add
                    if u%4==1:save=max(save,add)
            # Priced second-generation factors from exact exponents of each
            # certified new q. Discard support of all old explicit bases,
            # coactive baseline blocks and the entire root sigma. Remaining
            # products across q divide N with full multiplicity; partial
            # overlaps may overcredit abundance but never cost.
            U=explicit*a; sk=[]
            for q,k in known:
                opts=[]
                for sp in (False,True):
                    if sp and not (q%4==1 and legal(q,1)):continue
                    step=4 if sp else 2;f=k+((1-k)%4 if sp else k%2)
                    fx=f;best=None
                    while f<=k+12:
                        if legal(q,f):
                            c=sigma(q,f)//(2 if sp else 1)
                            for unt in (U,oldblocks):
                                while (g:=math.gcd(c,unt))>1:c//=g
                            w=DYADIC*((f-k)*log_bounds(q)[0]+log_bounds(c)[0])-w0*hg(c,rough(c));best=w if best is None else min(best,w)
                        f+=step
                    w=DYADIC*(f-k)*log_bounds(q)[0];opts.append(max(DYADIC*(fx-k)*log_bounds(q)[0], min(w,best) if best is not None else w))
                sk.append(opts)
            # The bare term may only replace the priced child when omitting
            # that child's cost AND abundance; that corresponds to purchasing
            # its new support via generic tail, valid separately per source.
            plain=extra-sum(log_bounds(q)[0] for q,k in known if k%2); groups=[D0[0] for D0 in sk];disc=max([0]+[a0[0]-a0[1] for a0 in sk if len(a0)>1]+[log_bounds(lo_)[0]*DYADIC for h_,u_ in revised if math.isqrt(u_)**2!=u_ and u_%4==1 for lo_ in [rough(u_)+((1-rough(u_))%(2*h_ if math.gcd(u_,h_)==1 else 1))]])
            upgrade=max(DYADIC*(extra-save),DYADIC*plain+sum(groups)-disc)+w0*(hg(n,rough(n))-benef)
            # Fixed root abundance (the old model allows its limiting value).
            upgrade+=w0*max(0,log_bounds(p,p-1)[1]-log_bounds(a,pe)[1]);z+=explicit_gain+max(0,upgrade)
            digits[e]=z//(DYADIC*log_bounds(10)[1]);
            if z>lim:results[e]=digits[e]
            else:surv.append(e)
        req(top==x['tail'] and original_surv==x['survivors'],'baseline partition mismatch');out.append(dict(forbidden=bad,p=p,tail=top,remaining=len(surv),max_remaining=max(surv,default=0),new=results,survivors=surv,scores=digits,cuts=counts))
    req(out,'empty');(H/('PairResults.json' if p==7 else f'PairResults{p}.json')).write_text(json.dumps(dict(cases=out),separators=(',',':'))+'\n');print('new',results,'surviving',len(surv),'elapsed',round(time.perf_counter()-now,3))
if __name__=='__main__':main()
