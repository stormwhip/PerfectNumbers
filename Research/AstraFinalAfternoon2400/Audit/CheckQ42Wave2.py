"""Independent exact domains, frozen residual intersection and reserved CRT ranges."""
import gzip,json,sys,runpy
from math import gcd,lcm,prod
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from CheckSevenForestDomains import replay_basics, sig,split
from Check31Domains import vp
Q=16148168401; R=173;B=10**2400
P=[(7,12),(Q,42)]; HERE=H.parent/'Seven'
EXPECTED={1,4,8,12,16,18,24,30,36,40,42,48,58,78,106,150,166,190}
NORMAL=(('f',(18,24),'8bd27215bd8c81fa7e17ff430ad1b7454b2a6217403045e11270c78ca610b4b4'),
        ('g',(190,),'20ff9d8cb7d75bbdb1c94ca4ecb338e6575b70a61069cf74595d97911c651279'),
        ('h',(166,),'48cf93f36f80e9ac5586f20e9afd1af4c983273d3723b0df11c3f856a881856f'),
        ('i',(150,),'2a5da6d84436cd44cfa75cbb5530c2640d56eab066f160544d9c256aab04665f'),
        ('j',(42,48),'44875997480438adc773b8c8da17bbb1710b8d15ee4ae3fa141f4344d95a00bc'),
        ('k',(40,),'0f9415a3c18b34a61e4caafcf8bc3c6d47f5591a6260e10f97924e66117650ab'),
        ('l',(58,),'06da885eb12d7591e449d644453a6ba16cf3a901c98bdb93d1b63aa069812b09'),
        ('m',(16,),'c6093e39a3c7805a0c2a3afb50bef69e04353b5f267573b13f8358ea06f3e3ce'),
        ('n',(36,),'1900dbd3cc1293ad307122c3437fb98b2e929d23976384caf3ce64d948487c3d'))


def data(name,digest=None):
    raw=(HERE/name).read_bytes()
    if digest:assert sha256(raw).hexdigest()==digest
    return json.loads(gzip.decompress(raw))


def main():
    assert __debug__
    raw,tail=split(P,{19},R)
    assert {1,2,4,6,10}<=raw.keys() and 210 in raw
    active={1}|(set(range(2,211,2))-{126,130,136,138,156,158,172,176,180,182,184,192,196,198,200,202,204,206,208,210})
    done=set()
    for t in 'abcde':
        s={rec['P'][-1][1] for rec in data(f'Forest12{t}.json.gz')['records'] if rec['P'][-1][0]==R}
        assert s<=active and not done&s;done |=s
    assert len(done)==65
    newer=set()
    for t,hs,digest in NORMAL:
        s=set(hs);assert s<=active and not (done|newer)&s
        replay_basics(f'Forest12{t}.json.gz',digest,{('12R',h) for h in hs});newer|=s
    qodd=P+[(R,1)]; assert sig(R,1)==2*3*29 and sig(Q,42)%43==0 and sig(3,2)==13
    z=prod(Fraction(sig(p,h),p**h) for p,h in qodd+[(29,2),(43,2)])
    I=lambda p,h:Fraction(sig(p,h),p**h)
    assert all(z*I(3,4)*I(p,2)>2 for p in (5,11,13))
    assert all(z*I(3,2)*I(13,2)*I(p,2)>2 for p in (5,11,17,23,31,37))
    assert I(7,12)*I(3,2)*I(5,1)>2
    for name,digest,reported in [
        ('Forest12Odd.json.gz','db65692d6a615db06052ea906f2a286bb53a59dfec9d190dbd0f377bb8c48650',{(1,(19,5,11,13)),(1,(19,5,11,17,23,31,37))}),
        ('Forest12MaskFour.json.gz','d3a59d90b9503e02dd8544a20e8f0cb4e140f898c2887fa0ab0a95788e5118ed',{(4,b) for b in ((19,3),(19,5))}),
        ('Forest12Mask.json.gz','de406c34f3cb5acb244dc2c71a242cdc50d2c1b18721f734a31f592db5cac3f4',{(h,b) for h in (8,12,30) for b in ((19,3),(19,5))})]:
        table=data(name,digest);tag=set()
        for v in table['records']:
            p=[tuple(x) for x in v['P']];k=p[2][1];bad=tuple(v['bad']);tag.add((k,bad));assert p[:3]==raw[k]
            if bad in ((19,5),(19,5,11,13)):
                assert v['present']==[3] and dict(v['lo'])=={3:4 if k==1 else 2}
            else:
                assert not v['present'] and not v['lo'] and len(p)==(4 if k==1 else 3)
        assert tag==reported and len(tag)==len(table['records'])
        claimed={h for h,_ in tag};assert claimed<=active and not claimed&(done|newer);newer |=claimed
    q42=HERE.parents[1]/'FinalNight2400/SevenNext/Odd42.py'
    U=runpy.run_path(str(q42))['cost'];U=U(Q,41,2,True,True)*U(R,231,38,True,True)
    eligible=[o for o in range(1,5032,2) if (Q-1)%o==0]
    for a in range(1,5032,2):
        qorders=[o for o in eligible if a%o==0]
        rk=vp(a,R)
        for o in qorders:
            for r in (1,43):
                if a%r:continue
                if r==43 and o%43==0: min_exp=(o-1-40)+40
                else:min_exp=(o-1)+(40 if r==43 else 0)
                assert min_exp+(R**rk-1)<=a-1 or (r==1 and lcm(o,R**rk)>a)
    d=data('Forest12Q42Reserve.json.gz','e272183658f5b408172f63f1c7a2f8a1060cc2fac8d73c6f7d194bcaf7c9e8ed')
    for w in d['records']:
        p=[tuple(x) for x in w['P']];h=p[-1][1];assert p==raw[h] and h in(78,106) and h not in done|newer;newer.add(h)
        X=prod(q**g for q,g in p);S=prod(sig(q,g) for q,g in p)
        c,j=42-vp(S,Q),h-vp(S,R); mods={(t['i'],t['k']) for t in w['params']}
        active0=0
        for i in range(c+1):
            for k in range(j+1):
                f=Q**i*R**k; m=X*(2*f-1)*Q**(2*(c-i))*R**(38*(j-k))
                if m<=B*U:
                    # An odd multiplier implies 2m-1 retains the weaker
                    # exact 1 mod4 Euler congruence even for high exponent.
                    assert any(f%(l:=Q**u*R**v)==0 and (2*f-1)%(4*l)==2*l-1 for u,v in mods)
                    active0+=1
        assert active0=={78:604,106:540}[h] and len(mods)==6
    assert newer==EXPECTED and active-(newer|done)=={2,6,10}
    print('PASS 18 disjoint new h at Q42 and exact output residual {2,6,10}; ordinary, masked, all shifted and congruence tails checked',flush=True)

if __name__=='__main__':main()
