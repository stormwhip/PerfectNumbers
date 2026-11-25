"""Discovery: put exact-prefix divisor states into graph space. Each child fixes the
selected donor, recomputes the product of exact odd sigmas, then globally re-roots the forest.
One explicit high-exponent tail per split is required. Float values are never acceptance inputs.
"""
from AdaptiveSeeds import *
sys.path.insert(0,str(R/'Nov25/Compose'));import Compose as C

def project(s,row,engine):
    P=dict(row['owners']);V=set(row['roots'])|P.keys();qs=set()
    for z,f in s.rows.items():
        if z==s.p:continue
        qs.update(engine.candidates(z,f))
    V.update(qs);K={z for z in V if z not in s.rows and z not in s.bad and not s.D%z}|set(s.lo);live=set(K);ow={};kid=defaultdict(list)
    for q,z in P.items():kid[z].append(q)
    queue=list(K)
    while queue:
        z=queue.pop()
        for q in kid[z]:
            if q not in live and q not in s.rows and q not in s.bad and s.D%q:ow[q]=z;queue.append(q);live.add(q)
    return K,ow

def grow(s,row,b,steps):
    K,ow=project(s,row,b);have=set();A=s.D*s.X*C.prod(s.present);best=0;bestrow=None;cs=[];cap=max(64,row['head']);
    for i in range(steps+1):
        F=C.Forest(s,sorted(K),sorted(ow.items()),cap,record=True);v,m=F.lower();
        if v>best:best=v;bestrow=dict(roots=sorted(K),owners=sorted(ow.items()),head=cap);cs=list(F.witness(m)) if v<=C.B else []
        if best>C.B:break
        st=list(F.witness(m));adds={}
        for z,f,rem in st:
            if not rem or (z,f) in have:continue
            have.add((z,f));
            for q in b.candidates(z,f):
                if q not in s.bad and q not in K and A%q and q not in ow:adds.setdefault(q,z)
        if not adds:break
        ow.update(adds)
    return best,bestrow,cs

def campaign(p,e,row,b,depth,seconds):
    end=time.monotonic()+seconds;stats=defaultdict(int);failure=[];minfloor=30000
    def solve(rows,lo,l,graph):
        nonlocal minfloor
        s=C.State(rows,lo=lo);stats['states']+=1
        if s.conflict or s.base>C.B:return {'kind':'direct'}
        g,bc,w=grow(s,graph,b,20 if l else 3);floor=int(math.log10(g))
        if g>C.B:minfloor=min(floor,minfloor);return {'kind':'forest',**bc}
        zlist=[(q,f) for q,f,rem in w if q in bc['roots'] and q not in lo and rem];
        if not l or not zlist or time.monotonic()>end:
            failure.append((floor,[(str(q)[:25],f) for q,f in rows],[(str(q)[:25],f) for q,f in lo.items()]));return None
        q=max(zlist,key=lambda qf:math.log(qf[0])*(qf[1] if qf[1]<12 else 1))[0];c=C.valuation(s.D,q);cut=max(8,min(100,2*((2400-floor)//max(1,int(math.log10(q)))+5)));higher=dict(lo);higher[q]=cut+1
        tail=solve(rows,higher,l-1,bc);cells={};ok=tail is not None
        for f in range(1,cut+1):
            if not s.possible(q,f,c):continue
            v=solve([*rows,(q,f)],lo,l-1,bc);cells[str(f)]=v;ok &= v is not None
            if time.monotonic()>end and not ok:break
        if ok:return dict(kind='exp',q=q,cut=cut,cells=cells,tail=tail)
    tree=solve([(p,e)],{},depth,row);return tree,dict(stats),sorted(failure,key=lambda x:x[0]),minfloor

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=int,default=30);ap.add_argument('--depth',type=int,default=2);ap.add_argument('files',type=Path,nargs='+');a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True);b=Engine(a.bank)
    for f in a.files:
        row=load(f);p,e=row['p'],row['e'];tree,st,fail,m=campaign(p,e,row,b,a.depth,a.seconds);print(p,e,st,len(fail),fail[:2],bool(tree),flush=True)
        if tree:(a.out/f'Tree{p}x{e}.json').write_text(json.dumps(dict(p=p,e=e,tree=tree),separators=(',',':')))
        C.sigma.cache_clear()
if __name__=='__main__':main()
