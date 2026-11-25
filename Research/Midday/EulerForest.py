"""A fixed Euler prime can be paid even when its assigned forest parent is inactive.
Discovery: always promote the given q to a root, restrict it to f == 1 mod 4,
and enforce even exponents at all remaining nodes. Other labels cannot use its coupon.
"""
from SeedScan import *
from BoostScore import load,admissible,ORDER,valuation

def score(row,q):
    p,e=row['p'],row['e'];A=sigma(p,e);K=set(row['roots'])|{q};P=dict(row['owners']);P.pop(q,None);V=K|P.keys();U=p*A*q*math.prod(P);kids={z:[] for z in V};ban=ORDER[:ORDER.index(p)];cap=row['head'];c0={z:valuation(A,z) for z in K};base=e*math.log10(p)+math.log10(A)-sum(h*math.log10(z) for z,h in c0.items());trace={}
    for z,w in P.items():kids[w].append(z)
    @cache
    def node(z,h):
        sp=z==q;f=h+((1-h)%4 if sp else h%2);step=4 if sp else 2;cnt=0;best=math.inf
        while True:
            if not admissible(z,f,ban):f+=step;continue
            v=f*math.log10(z)
            if cnt==cap or v>=best:
                if v<best:best=v;trace[z,h]=(f,False,[])
                break
            S=arithmetic(z,f);active=[(t,c) for t in kids[z] if (c:=valuation(S,t))];v+=math.log10(nonsupport(S,U))+sum(node(t,c) for t,c in active)
            if v<best:best=v;trace[z,h]=(f,True,active)
            cnt+=1;f+=step
        return best
    hs=[(z,max(1,c)) for z,c in c0.items()];ans=base+sum(node(z,h) for z,h in hs);cells=[]
    while hs:
        z,h=hs.pop();f,on,sub=trace[z,h];hs.extend(sub)
        if on:cells.append((z,f))
    node.cache_clear();return ans,cells

def main():
    ap=argparse.ArgumentParser();ap.add_argument('row',type=Path);ap.add_argument('q',type=int);ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();b=Builder(a.bank);d=load(a.row);p,e=d['p'],d['e'];q=a.q;P=dict(d['owners']);A=p*sigma(p,e)*q;seen=set();d['head']=max(96,d['head']);best=0
    for j in range(100):
        v,cs=score(d,q);
        if v>best:best=v;a.out.write_text(json.dumps(dict(d,conditionalEuler=q,scout=v),separators=(',',':')));print('best',p,e,q,round(v,2),len(P),flush=True)
        if v>2400.02:break
        adds={};sw=[]
        for z,f in cs:
            if (z,f) not in seen:
                seen.add((z,f));hs=b.hints(z,f) if z.bit_length()*(f+1)<14000 else ()
                for t in hs:
                    if A%t and t not in P:adds[t]=z
            S=arithmetic(z,f);g=math.gcd(S,math.prod(P));
            if g>1:
                for t,w in P.items():
                    if t!=q and z!=w and g%t==0:
                        x=z
                        while x in P and x!=t:x=P[x]
                        if x!=t:sw.append((t,z))
        if adds:P.update(adds)
        else:
            alts=[(score(dict(d,owners=sorted((P|{t:z}).items())),q)[0],t,z) for t,z in sw[:35]]
            if not alts or max(alts)[0]<v+0.00001:break
            _,t,z=max(alts);P[t]=z
        d['owners']=sorted(P.items())
if __name__=='__main__':main()
