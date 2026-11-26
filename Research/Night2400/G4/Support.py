"""Replay extra complete masks against the verified (19,372) tree's explicit gaps."""
from pathlib import Path
from fractions import Fraction
from math import prod,gcd
from functools import cache
import argparse,gzip,json,sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
import Verify as V

ORDER=(19,7,11,31,13,3,5,17)


def projected_tree(d):
    """Find all open exact paths, never accepting a leaf not checked by Verify."""
    result={}
    def walk(rows,node):
        if node['type']=='open':result.setdefault(rows[1][1],[]).append(rows)
        elif node['type']=='split':
            for f,v in node['cases'].items():walk(rows+[(node['q'],int(f))],v)
    for f,t in d['cases'].items():walk([(V.P,V.E),(V.Q,int(f))],t)
    return result


def check_masks(tree_file,support_file):
    if not __debug__:raise RuntimeError('assertions required')
    tree=V.verify(tree_file)
    assert tree['root_domain']==sorted(map(int,tree['data']['cases']))
    data=json.loads(gzip.decompress(support_file.read_bytes()));assert set(data)=={'masks','ecpp'}
    tab=data['ecpp'];used=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2
        n=z
        if z>=2**64:
            rr=tab[str(z)];assert rr
            for a in rr:
                assert a[0]==n;n=V.C.pc.level(*a)
            used.add(str(z))
        assert V.C.pc.prime64(n);return True
    allg=projected_tree(tree['data']); paths=[r for f in sorted(allg) for r in allg[f]]
    for sm,row in sorted(data['masks'].items(),key=lambda x:int(x[0])):
        m=int(sm);assert str(m)==sm and m in range(1,256,2)
        needed=tuple(q for i,q in enumerate(ORDER) if i and m>>i&1); banned=tuple(q for i,q in enumerate(ORDER) if not m>>i&1)
        assert len(row)==len(paths)
        stats=[0,0]
        for assignment,part in zip(paths,row):
            fixed=dict(assignment);x=prod(q**h for q,h in assignment)
            s=prod(V.sig(q,h)//(1+h%2) for q,h in assignment)
            direct=gcd(s*prod(fixed),prod(banned))>1
            if direct:
                assert part is None;stats[0]+=1;continue
            r=part;assert isinstance(r,list) and r==sorted(set(r))
            D=V.trim(s,prod(fixed));assert all(prime(q) and q not in fixed and q not in banned and (q in needed or D%q==0) for q in r)
            def low(q,odd):
                f=max(1,V.val(D,q));f+=((1-f)%4 if odd else f%2)
                while any(pow(q,f+1,z*(q-1))==1 for z in banned):f+=2+2*odd
                return Fraction(V.sig(q,f),q**f)
            even={q:low(q,0) for q in r};v=Fraction(prod(V.sig(q,h) for q,h in assignment),x)*prod(even.values());vals=[v]
            if not any(h%2 for h in fixed.values()):vals.extend(v/even[q]*low(q,1) for q in r if q%4==1 and gcd(q+1,prod(banned))==1)
            assert min(vals)>2,(m,assignment)
            stats[1]+=1
        print('FULL MASK',m,'direct, abundance',stats,flush=True)
    assert used==set(tab)


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--tree',type=Path,default=H/'Nineteen372.json.gz');a.add_argument('--support',type=Path,default=H/'Support372.json.gz');ns=a.parse_args();check_masks(ns.tree,ns.support)
