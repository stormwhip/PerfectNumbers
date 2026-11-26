"""One-shot verifier for root 3,1162. Uses stdlib, existing fixed JSON, pre-found duals; no writes."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Joint import *
from Base import check_range,envelope
from Flow import getdual

def cover():
    a=cert['cell10'];b=cert['cell11'];split=[17,23,29,37,41];allp=[r for r in small if 17<=r<=157 and r not in BAN]
    assert len(a)==12 and len(b)==30
    for mask in range(1<<5):
        pos={r for j,r in enumerate(split) if mask>>j&1};neg={5}|(set(split)-pos)
        assert any(set(l['present'])<=pos and set(l['absent_extra'])<=neg for l in a)
    assert any(set(l['present'])=={5} and set(l['absent_extra'])==set(allp) for l in b)
    for i,r in enumerate(allp):assert any(set(l['present'])=={5,r} and set(l['absent_extra'])==set(allp[:i]) for l in b)

def window():
    # R=10000; valid maximum discount at k=1, as suppliers >=43 imply 43^6>10^8.
    from fractions import Fraction
    R=10000;K=R**2;d=Fraction(1)
    assert 43**6>K
    for r in small:
        if r>=R:break
        if r%3!=1 or r in BAN or any(sig(r,2)%t==0 for t in BAN):continue
        assert r>=43;d*=Fraction(K,r*r)
    assert all(2*pe*(2*3**s-1)**2*K**(e-s)*d.denominator>3*B*d.numerator for s in range(1,1020))

def main():
    assert __debug__;euler2219='--conditional-2219' in sys.argv[2:];sys.argv[2:] = ['verify'];window();cover();check_range(e,10**11);base,_=envelope(e,10**11);assert base==[5052805597654,5000477672899]
    from Prefix import prefix
    from Hybrid import hybrid
    from LegacySingle import calc
    base[0],arg=prefix();assert base[0]>=5067135038412
    if euler2219:base[0]=2219*lo(10) # deliberately downward; certified by independent Range + Euler verifiers
    print('bases',base,'minimum external window',arg,'requires_parity_2219',euler2219,flush=True)
    approved=[[],[]]
    for i in range(42):
        clean,by=leaf(i,True);vals=[min([clean]+list(by.values())),clean]
        for k,tag in [(0,'DualExternal'),(1,'DualFlow')]:
            if (Path(__file__).parent/(tag+str(i)+'.json')).exists():vals[k]=max(vals[k],getdual(i,k==0)['net_nanonats'])
        if base[0]+vals[0]<=2400*hi(10):
            if i in (0,1,5,6,12):vals[0]=max(vals[0],calc(i))
            elif clean+base[0]>2400*hi(10):vals[0]=max(vals[0],hybrid(i,base[0],(clean,by))[0])
        tot=[(z+b)//hi(10) for z,b in zip(vals,base)]
        for k,z in enumerate(tot):
            if z>2400 or (z==2400 and vals[k]+base[k]>2400*hi(10)):approved[k].append(i)
        print(json.dumps(dict(leaf=i,scaled_aux=vals,decimal_floors=tot)),flush=True)
    both=len(approved[0])==len(approved[1])==42
    print(json.dumps(dict(excluded=approved,all_joint_subdomains=both,conditional_on_parity_2219=euler2219,also_requires='b=0 source theorem and E0/E1/E2'),separators=(',',':')),flush=True)
    if euler2219:assert both
if __name__=='__main__':main()
