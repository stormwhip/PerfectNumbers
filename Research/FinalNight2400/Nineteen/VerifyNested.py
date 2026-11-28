"""Apply exact 618 pricing kernel recursively to a finite compulsory-prime tree."""
from pathlib import Path
from math import prod
import sys,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));from AnchorKernel import Kernel,M,C,p,t,e,B,val,sig

def main(pack):
    K=Kernel();visits=0
    for table in [pack['root'],pack['forced']]:
        for r,hh in table.items():
            for h,zz in hh.items():
                Y=sig(int(r),int(h))
                for label,chain in zz.items():
                    z=n=int(label);assert z>2 and Y%z==0
                    for row in chain:assert n==row[0];n=C.pc.level(*row)
                    assert C.pc.prime64(n)
    def test(f,rows,zk,node):
        nonlocal visits;visits+=1
        if K.run(f,rows,zk):return
        assert node is not None,(f,rows)
        r=node['r'];assert r in zk and r not in rows and r not in (p,t) and (r%(4*t**(f-1))!=2*t**(f-1)-1 or r%4==3)
        full={p:e,t:f,**rows};X=prod(x**h for x,h in full.items());S=prod(sig(x,h) for x,h in full.items());D=S
        for x in full:D=C.strip(D,x)
        c=val(D,r);assert c>0;k=c+c%2;scale=X*D//r**c
        while scale*r**k<=B:
            zz=zk|set(map(int,pack['forced'].get(str(r),{}).get(str(k),{})));
            test(f,rows|{r:k},zz,node['kids'].get(str(k)));k+=2
    for f0,row in pack['cases'].items():
        f=int(f0);zk=set(map(int,pack['root'][str(t)][f0]))-{p};test(f,{},zk,row);print('PASS complete 618 f=',f,'cumulative visited',visits,flush=True)
if __name__=='__main__':
    assert __debug__;D=json.loads((P/'Nested618.json').read_bytes());assert set(D['cases'])=={'14'};main(D)
