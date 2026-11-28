"""Exploratory integer comparisons; surviving windows are not exclusions."""
if __package__ in ('',None):
    from pathlib import Path
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parent))
from Prices import *
from sys import argv
P=((3,6),(1093,2))
CASES={f'6-2-{h}':P+((398581,h),) for h in (102,108,150)}
CASES.update({f'12-1-{h}':((3,12),(797161,1),(398581,h)) for h in (102,108)})
CASES.update({'12-96':((3,12),(797161,96)), '6-156':((3,6),(1093,156),(2035349,46)), '6-256':((3,6),(1093,256))})

def test(k,weights):
    rows=CASES[k];targets=tuple((p,w) for (p,h),w in zip(rows[1:],weights));print(k,targets,flush=True)
    V,E=price(rows,targets);F0,odd,X,S,D,blocks=get_context(rows)
    print('Vfloor',floor10(V),'discounts',len(E),'XD floor',floor10(X*D),'blocks',[(floor10(b),'sq' if isqrt(b)**2==b else 'non') for b in blocks],flush=True)
    cs=[F0[p]-vp(S,p) for p,w in targets];tot=0;gaps=[0,0,0];unres=[];R=20_000_001
    for ls in product(*(range(c+1) for c in cs)):
        m=prod(p**i for (p,w),i in zip(targets,ls));a=max(5,2*m-1);W=prod(p**(w*i) for (p,w),i in zip(targets,ls));tot+=1
        if V*a>B*W:gaps[0]+=1;continue
        if X*D*a>B:gaps[1]+=1;continue
        internal=any((l:=((b*pow(2*m-1,-1,4*m))%(4*m) or 4*m))<=(u:=b//a) and ((u-l)//(4*m)>32 or any(b%v==0 for v in range(l,u+1,4*m))) for b in blocks)
        if (not internal) and floor10(4*V*X*D*a**4/(9*W*max(blocks)))>4800 and max(weights)==2:
            gaps[2]+=1;continue
        unres.append((ls,internal,floor10(V*a/W),floor10(X*D*a)))
    print('windows',tot,'cut',gaps,'left',len(unres),unres[:8],unres[-8:],flush=True)
if __name__=='__main__':test(argv[1],list(map(int,argv[2].split(','))))
