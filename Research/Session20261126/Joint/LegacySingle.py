"""E3a flow with overlap of one single pairwise-coprime support atom.
python -I -S -B theory-lab/SingleLoss.py unpack/PerfectNumbers-HEAD 12 [0]
"""
from pathlib import Path
import sys,inspect,json,math,time
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here));import Flow as f
from Joint import *
source=inspect.getsource(f.model)
source=source.replace('opts={};rows=[]','lefts={};opts={};rows=[]')
source=source.replace('if left>1 and (not external or (prime(left) and nosource(left))):vv+=lo(left)*(lo(50000)-2*hi(3))//lo(50000)','if left>1:\n                        lefts[len(data)]=left;vv+=lo(left)*(lo(50000)-2*hi(3))//lo(50000)')
source=source.replace('return data,rows,rhs,names','return data,rows,rhs,names,lefts')
ctx=dict(vars(f));exec(source,ctx); model=ctx['model'];DEN=f.DEN

def calc(i):
    data,rows,rhs,names,lefts=model(i);n=len(data);print('model',i,n,len(rows),len(lefts),flush=True)
    atoms=basis(lefts.values());unsafe=set(a for a in atoms if not(prime(a) and nosource(a)));bad={a:[] for a in unsafe};dv=rows[names.index('vol')]
    for j,x in lefts.items():
        for a in unsafe:
            y=x
            while (g:=gcd(y,a))>1:y//=g
            if y!=x:bad[a].append((j,lo(x)*(lo(50000)-2*hi(3))//lo(50000) - (lo(y)*(lo(50000)-2*hi(3))//lo(50000) if y>1 else 0)))
    print('atoms',len(atoms),len(unsafe),flush=True)
    def evaldual(dual,excluded=None):
        rc=[x*DEN for x in data]; total=0
        for name,row,b in zip(names,rows,rhs):
            a=dual.get(name,0)
            if a:
                for j,v in row.items():rc[j]+=a*v
                total-=a*b
        if excluded is not None:
            for j,x in bad[excluded]:rc[j]-=dual.get('vol',0)*x
        assert rc[-1]>=0
        # Each sel group permits at most one column: correct a *group* minimum,
        # not the sum of negative reduced costs over all options.
        for name,row in zip(names,rows):
            if name.startswith('sel'):
                total+=min(0,min(rc[j] for j in row))
        return total//DEN
    key=f.Path(f.__file__).parent; pool=[]
    for tag in ('flow','external'):
        local=here/('Dual'+tag.title()+str(i)+'.json'); path=local if local.exists() else key/('Dual'+tag.title()+str(i)+'.json')
        if not path.exists():path=local
        if not path.exists() and 'search' in sys.argv:
            from scipy.optimize import linprog
            from scipy.sparse import coo_matrix
            import numpy as np
            I=[];J=[];W=[]
            for h,rr in enumerate(rows):
                for j,x in rr.items():I.append(h);J.append(j);W.append((x-(lo(lefts[j])*(lo(50000)-2*hi(3))//lo(50000) if tag=='external' and names[h]=='vol' and j in lefts else 0))/T)
            mat=coo_matrix((W,(I,J)),shape=(len(rows),n)).tocsr();res=linprog(np.array(data)/T,A_ub=mat,b_ub=np.array(rhs)/T,bounds=[(0,1)]*(n-1)+[(0,None)],method='highs');assert res.success
            path.write_text(json.dumps({k:int(round(max(0.,-v)*DEN)) for k,v in zip(names,res.ineqlin.marginals) if v<0},separators=(',',':')),encoding='utf-8')
        pool.append(json.loads(path.read_bytes()))
    defaultbase=5067135038412 if i in (1,5,6) or i>=13 else 5052805597654
    denout=[]
    for d in pool:
        assert set(d)<=set(names) and all(type(x)==int and x>=0 for x in d.values())
        # Existing rounded witness needs a tiny global reduction for external ray.
        delta=max(0,d.get('ab',0)*(-rows[names.index('ab')][n-1])+d.get('vol',0)*T-T*DEN)
        if delta:
            d.update({k:(x*T*DEN)//(T*DEN+delta) for k,x in d.items()})
    bases=[evaldual(d) for d in pool];remain=[]
    # Accelerate per-group update using gross sum, reduced costs and minima.
    def table(d):
        rc=[x*DEN for x in data];obj=0;grps=[];idx={}
        for name,row,b in zip(names,rows,rhs):
            if name.startswith('sel'):
                for j in row:idx[j]=len(grps)
                grps.append(list(row))
            a=d.get(name,0)
            if a:
                obj-=a*b
                for j,x in row.items():rc[j]+=a*x
        assert rc[-1]>=0;old=[min(0,min(rc[j] for j in g)) for g in grps];obj+=sum(old);weight=d.get('vol',0)
        def test(a):
            gg={}
            for j,x in bad[a]:
                g=idx[j];gg[g]=min(gg.get(g,old[g]),rc[j]-weight*x)
            return (obj+sum(v-old[g] for g,v in gg.items()))//DEN
        return test
    tests=[table(d) for d in pool];cases=sorted(((max(h(a) for h in tests),a) for a in unsafe));print('initial',[(round((5052805597654+s)/hi(10),5),str(a)[:30]) for s,a in cases[:12]],flush=True)
    if 'search' in sys.argv:
        from scipy.optimize import linprog
        from scipy.sparse import coo_matrix
        import numpy as np
        iv=names.index('vol');I=[];J=[];V0=[]
        for hh,row in enumerate(rows):
            for jj,x in row.items():I.append(hh);J.append(jj);V0.append(x/T)
        base=coo_matrix((V0,(I,J)),shape=(len(rows),len(data))).tocsr()
        for z,a in cases:
            if z+defaultbase>2400*hi(10):break
            aa=base.copy().tolil();
            for jj,x in bad[a]:aa[iv,jj]=aa[iv,jj]-x/T
            res=linprog(np.array(data)/T,A_ub=aa.tocsr(),b_ub=np.array(rhs)/T,bounds=[(0,1)]*(n-1)+[(0,None)],method='highs');assert res.success
            d={k:int(round(max(0.,-v)*DEN)) for k,v in zip(names,res.ineqlin.marginals) if v<0};delta=max(0,d.get('ab',0)*(-rows[names.index('ab')][n-1])+d.get('vol',0)*T-T*DEN)
            if delta:d.update({k:(x*T*DEN)//(T*DEN+delta) for k,x in d.items()})
            zz=evaldual(d,a);print('separate',a,round((5052805597654+zz)/hi(10),5),[(j,next(name for name,row in zip(names,rows) if name.startswith('sel') and j in row),x) for j,x in bad[a]],flush=True)
            (here/f'Atom{i}x{str(a)[:20]}.json').write_text(json.dumps({'a':a,'d':d,'bound':zz},separators=(',',':')),encoding='utf-8')
    if 'verify' in sys.argv:
        minimum=min(bases) if not unsafe else max(bases)
        if i==12:
            # Conservative universal new base (all s other than 1137, or q>Q at 1137).
            pe=3**1162;A=(3*pe-1)//2
            base0=min(lo(pe*A*(q:=(2*3**s-1 if s!=1137 else 6*3**s-1)))+lo(2*q)-hi(3)+min(4*(1162-s-u)*lo(3)+max(0,2*u*lo(10**11)-hi(A)) for u in range(1162-s+1)) for s in range(1020,1163))
            assert (2*3**1137-1)%5==0
        else:base0=defaultbase
        for z,a in cases:
            if z+base0<=2400*hi(10):
                rec=json.loads((here/f'Atom{i}x{str(a)[:20]}.json').read_bytes());assert rec['a']==a and set(rec['d'])<=set(names) and all(type(x)==int and x>=0 for x in rec['d'].values());z=max(z,evaldual(rec['d'],a))
            minimum=min(z,minimum)
        assert base0+minimum>2400*hi(10),(i,base0,minimum)
        print('VERIFIED_PARTIAL_LEAF',i,base0,minimum,(base0+minimum)/hi(10),flush=True)
        return minimum
    path=here/f'SingleLoss{i}.json';path.write_text(json.dumps(dict(i=i,base=5052805597654,full=bases,atoms=len(atoms),unsafe=len(unsafe),worst=cases[:35],open_count=sum(s+5052805597654<=2400*hi(10) for s,_ in cases)))+'\n',encoding='utf-8')
if __name__=='__main__':
    assert __debug__
    for i in (int(x) for x in sys.argv[2:] if x.isdigit()):calc(i)
