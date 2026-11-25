"""Per-source intersection of forest and flow. Only a failing forest atom is tested; LP atom need not equal it.
Search uses scipy optionally. Validation reconstructs rows and adjusts the exact integer flow dual.
"""
import sys,json,inspect
from pathlib import Path
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here));import Flow as ff
from Joint import *
from Prefix import prefix
# Capture external factors using same coefficient builder; explicit assertions guard intended substitution.
s=inspect.getsource(ff.model);p='if left>1 and (not external or (prime(left) and nosource(left))):vv+=lo(left)*(lo(50000)-2*hi(3))//lo(50000)';assert s.count(p)==1
s=s.replace(p,'if left>1:\n                        lefts[len(data)]=left;vv+=lo(left)*(lo(50000)-2*hi(3))//lo(50000)').replace('opts={};rows=[]','lefts={};opts={};rows=[]').replace('return data,rows,rhs,names','return data,rows,rhs,names,lefts');env=dict(vars(ff));exec(s,env);model=env['model'];DEN=ff.DEN

def hybrid(i,base,forest=None,search=False):
    clean,by=leaf(i,True) if forest is None else forest
    target=2400*hi(10)-base+1
    bad=[(val,t) for t,val in by.items() if val<target]
    # If source is not in any failing forest atom, the forest's lower bound applies.
    valid=[v for v in by.values() if v>=target];minimum=min(valid+[clean]);assert clean>=target
    if not bad:return minimum,[]
    data,rows,rhs,names,lefts=model(i);size=len(data);iv=names.index('vol');dn=lo(50000)-2*hi(3);dd=lo(50000)
    def solver(rowlist):
        import numpy as np
        from scipy.optimize import linprog
        from scipy.sparse import coo_matrix
        I=[];J=[];V=[]
        for k,row in enumerate(rowlist):I.extend([k]*len(row));J.extend(row);V.extend(v/T for v in row.values())
        result=linprog(np.array(data)/T,A_ub=coo_matrix((V,(I,J)),shape=(len(rowlist),size)).tocsr(),b_ub=np.array(rhs)/T,bounds=[(0,1)]*(size-1)+[(0,None)],method='highs');assert result.success
        return {k:int(round(max(0.,-a)*DEN)) for k,a in zip(names,result.ineqlin.marginals) if a<0}
    def dual(rr,weights):
        assert set(weights)<=set(names) and all(type(x)==int and x>=0 for x in weights.values());rc=[c*DEN for c in data];v=0
        for row,name,b in zip(rr,names,rhs):
            h=weights.get(name,0)
            if h:
                v-=h*b
                for j,z in row.items():rc[j]+=h*z
        den=DEN
        if rc[-1]<0:
            k=T*DEN;d=k-rc[-1];rc=[k*z+(d-k)*c*DEN for z,c in zip(rc,data)];v*=k;den*=d
        assert rc[-1]>=0
        for name,row in zip(names,rr):
            if name.startswith('sel'):v+=min(0,min(rc[j] for j in row))
        return v//den
    ans=[];wits=here/f'hybrid-{i}.json';w=json.loads(wits.read_bytes()) if wits.exists() else {};commons=[]
    for p in [here/f'flow{i}.json',here/f'external{i}.json']:
        if p.is_file():commons.append(json.loads(p.read_bytes()))
    for z,t in sorted(bad):
        rr=rows.copy();rr[iv]=rr[iv].copy()
        for j,x in lefts.items():
            y=x
            while (g:=gcd(y,t))>1:y//=g
            if x!=y:rr[iv][j]-=lo(x)*dn//dd-lo(y)*dn//dd if y>1 else lo(x)*dn//dd
        v=max([z]+[dual(rr,d) for d in commons]);k=str(t)
        if k in w:v=max(v,dual(rr,w[k]))
        if v<target and search:
            d=solver(rr);v=max(v,dual(rr,d));w[k]=d;wits.write_text(json.dumps(w,separators=(',',':')))
        minimum=min(minimum,v);ans.append((t,v));
    return minimum,ans
if __name__=='__main__':
    base=prefix()[0]
    for i in (int(x) for x in sys.argv[2:] if x.isdigit()):
        z,r=hybrid(i,base,search='search' in sys.argv[2:]);print(json.dumps(dict(i=i,base=base,net=z,floor=(z+base)//hi(10),bad=[(t,v) for t,v in r if v+base<=2400*hi(10)])),flush=True)
