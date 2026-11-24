"""Independent mandatory-pivot certificates; every alternative exponent covered. No discovery modules."""
import sys,math,json,gzip,hashlib
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'EveningTree'));import IndependentTree as I

class Checked(I.Proof):
    def visit(self,parts,X,S,ban):
        self.stats['nodes']+=1
        if self.stats['nodes']>16000:return False
        # If Y=N/X, gcd(X,Y)=1, S|2XY. Reconstruct D by lcm rather than separately charging sigma factors.
        U=math.lcm(X,S//math.gcd(2,S))//X;eu=any(f%2 for r,f in parts)
        if math.gcd(U,2*X*math.prod(ban))>1 or X*U>I.B or S>2*X:return True
        ds={};base=X;savings={}
        for z in self.pr:
            if U==1:break
            if U%z:continue
            c=I.vp(U,z);U//=z**c;bad=I.forbidden_indices(z,ban);m=I.least(z,c,bad,False);a=None if eu else I.least(z,c,bad,True);ds[z]=c,m,a,bad;base*=z**m
            if a is not None:savings[z]=z**max(0,m-a)
        base*=U
        if base>I.B*max([1]+list(savings.values())):return True
        if self.valuation_close(X,S,U,base,ds,eu):return True
        if not ds or len(parts)>self.depth_limit:return False
        # Known choice of compulsory pivot. Its priority influences runtime only.
        z=max(ds,key=lambda z:(z**ds[z][1],z));c,m,a,bad=ds[z];without=base//z**m
        for f0,step,save in [(m,2,max([1]+[v for r,v in savings.items() if r!=z]))]+([] if a is None else [(a,4,1)]):
            f=f0;power=z**f
            while without*power<=I.B*save:
                if I.permissible(f,bad) and not self.visit(parts+((z,f),),X*power,S*I.sigma(z,f),ban):return False
                power*=z**step;f+=step
        return True

def run(p,e,fs,depth):
    t=Checked(p,e,fs,False,True);t.depth_limit=depth
    return t.prove(),int(t.stats['nodes'])

def main():
    if not __debug__:raise SystemExit('assertions required')
    name=sys.argv[1];raw=json.loads((H/name).read_text());cert=json.loads(gzip.decompress((H/(name+'.gz')).read_bytes()));live={(s['root'],e) for s in json.load(open(R/'EveningMerge/Audit.json'))['remaining_shards']for e in s['remaining_actuals']};seen=set();used=set()
    for row in raw:
        p,e=row['p'],row['e'];assert (p,e)in live-seen and p not in (3,5,17);seen.add((p,e));fs=row['fs'];assert len(fs)==len(set(fs)) and {w for z,f,w in row['edges']}==set(fs)
        for z,f,w in row['edges']:
            assert f>=1 and z>2 and w>2 and pow(z,f+1,(z-1)*w)==1;n=w
            if w>=2**64:
                k=str(w);used.add(k)
                for level in cert[k]:assert level[0]==n;n=I.ec.level(*level)
            assert I.ec.prime64(n)
        ok,nodes=run(p,e,fs,row['depth']);assert ok,(p,e,nodes);print(p,e,nodes,'closed',flush=True)
    assert used==set(cert)
if __name__=='__main__':main()
