"""Cold complete fibers of (31,310) from the delegated unresolved set."""
from functools import cache
from fractions import Fraction
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126'),str(R/'Nov25/Compose')]
from PivotCheck import C,B,exact_leaf,floor10
from IndependentForest import replay
from PrefixPrice import excludes

KEY=(31,310);Q=5691933643219
DOMAIN=[2,4,6,10,12,14,16,18,20,22,24,28,30,32,34,36,38,40,42,46,48,50,52,54,56,58]


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X

def split(p,q):
    s=C.State(p);assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    n=h=C.valuation(s.D,q); a=s.base//q**h; out={};d=[];u=[]
    while a*q**n<=B:
        if not s.possible(q,n,h):u.append(n)
        elif dead(C.State(p+[(q,n)])):d.append(n)
        else:out[str(n)]=p+[(q,n)]
        n+=1
    return out,d,u,n


def packet(name,expected):
    raw=(H/name).read_bytes(); d=json.loads(gzip.decompress(raw));book=d['ecpp'];used=set()
    assert (d['p'],d['e'],d['pivot'])==(*KEY,Q)
    if expected:
        assert set(d)=={'p','e','pivot','cases','ecpp'} and set(d['cases'])==set(map(str,expected))
    elif name=='Paths4.json.gz':
        assert set(d)=={'p','e','pivot','paths','ecpp'}
    else:
        assert set(d)=={'p','e','pivot','complete','partial','ecpp'}
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q)); chain=book[str(q)];assert chain
            for row in chain:
                assert row[0]==n and n>=2**64
                n=C.pc.level(*row)
        assert C.pc.prime64(n);return True
    assert prime(KEY[0]) and prime(Q) and Q.bit_length()==43 and C.State([KEY]).bad==(19,7,11)
    dom,d0,i0,end=split([KEY],Q); assert (list(map(int,dom)),len(d0),len(i0),end)==(DOMAIN,25,65,117)
    stat=[0,0,0,0]; floors=[]
    def supported(p,rows,gaps=()):
        masks=set(range(8,256,16))-set(gaps)
        assert set(rows)==set(map(str,masks))
        count=[0,0,0]; sf=[]
        for m in sorted(masks):
            yes=tuple(x for j,x in enumerate(C.ORDER[4:],4) if m>>j&1)
            no=tuple(x for x in C.ORDER[4:] if x not in yes);s=C.State(p,yes,no); t=rows[str(m)]
            if t['type']=='direct':
                assert set(t)=={'type'} and dead(s); count[0]+=1; continue
            assert not dead(s);k=t['roots']
            if t['type']=='abundance':
                assert set(t)=={'type','roots'} and sorted(set(k))==k
                assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in k)
                def ratio(q,odd):
                    h=max(1,C.valuation(s.D,q));h+=(1-h)%4 if odd else h%2
                    while not C.permitted(q,h,s.bad):h+=4 if odd else 2
                    return Fraction(C.sigma(q,h),q**h)
                terms={q:ratio(q,False) for q in k}; v=Fraction(prod(C.sigma(q,h) for q,h in p),s.X)*prod(terms.values())
                assert min([v,*[v/terms[q]*ratio(q,True) for q in k if not s.fixed_euler and C.euler(q,s.bad)]])>2
                count[1]+=1;continue
            assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
            o,h=t['owners'],t['head']; C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];assert a>B
            certs={str(q):book[str(q)] for q in {z for z,_ in p}|set(k)|set(dict(o)) if q>=2**64}
            b=replay(dict(assigned=p,present=yes,absent=no,leaf=dict(kind='forest',roots=k,owners=o,head=h),ecpp=certs))
            count[2]+=1;sf.append(min(floor10(a),b))
        print('ALL SUPPORT',p,count,'min forest',min(sf,default=None),flush=True)
    def go(p,t):
        s=C.State(p);assert not dead(s)
        if t['type']=='split':
            assert set(t)=={'type','q','cases'} and prime(t['q'])
            z,di,_,_=split(p,t['q']);assert set(z)==set(t['cases'])
            stat[0]+=1;stat[1]+=len(di)
            for e,c in z.items():go(c,t['cases'][e])
        elif t['type']=='forest':
            assert set(t)=={'type','roots','owners','head'};k,o,h=(t[a] for a in ('roots','owners','head'))
            C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];b=exact_leaf(p,k,o,h);assert min(a,b)>B
            stat[2]+=1;floors.append(floor10(min(a,b)))
        elif t['type']=='support':
            assert set(t)=={'type','masks'}
            supported(p,t['masks'])
        else:
            assert t=={'type':'price','targets':[1]} and p==[KEY,(Q,58)]
            ans=excludes(p,s.bad,[1]);assert ans==(0,[21,0,37]);stat[3]+=1
            print('PRICE 58',ans,flush=True)
    if name=='Paths4.json.gz':
        tags=set(); a=512738348529648177663331017165682915269207241; b=66399631; c=2047121
        for key,r in d['paths'].items():
            p=list(map(tuple,r['parts'])); es=tuple(e for q,e in p); assert es not in tags
            assert set(r)=={'parts','targets','receipt'} and key==','.join(map(str,es))
            assert p[:3]==[KEY,(Q,4),(a,4)] and all(prime(q) for q,_ in p)
            if len(p)==4:assert p[-1][0]==b and r['targets']==[0,3]
            else:assert len(p)==5 and p[3]==(b,30) and p[-1][0]==c and r['targets']==[0,4]
            for j in range(1,len(p)):
                live,*_=split(p[:j],p[j][0]);assert live[str(p[j][1])]==p[:j+1]
            v=excludes(p,C.State(p).bad,r['targets']);assert list(v)==r['receipt'];tags.add(es)
            print('PASS 4 CONDITIONAL',es,v,flush=True)
        assert tags=={(310,4,4,j) for j in (52,58,60,64,66)}|{(310,4,4,30,j) for j in (42,46,48)}
        assert used==set(book);print('CONDITIONAL 4 SHA256',sha256(raw).hexdigest(),flush=True);return
    if not expected:
        a,h=d['complete'],d['partial'];assert set(a)=={'parts','forest'} and set(h)=={'parts','masks'}
        for x,ef in [(a,10),(h,16)]:
            p=list(map(tuple,x['parts'])); assert p[:2]==[KEY,(Q,18)] and len(p)==4
            assert p[2]==(707818236468853019281602309439653890995043,2) and p[3]==(385772801143,ef)
            assert all(prime(q) for q,_ in p)
            for j in range(1,len(p)):
                live,*_=split(p[:j],p[j][0]);assert live[str(p[j][1])]==p[:j+1]
            if ef==10:go(p,x['forest']);print('COMPLETE CONDITIONAL',p,'forest floor',floors[-1],flush=True)
            else:supported(p,x['masks'],(8,56,72,120));print('OPEN CONDITIONAL MASKS',[8,56,72,120],flush=True)
        assert used==set(book); print('CONDITIONAL 18 SHA256',sha256(raw).hexdigest(),flush=True);return
    print('DOMAIN',DOMAIN,'direct',len(d0),'incompatible',len(i0),'tail',end,flush=True)
    for e in expected:go(dom[str(e)],d['cases'][str(e)])
    assert used==set(book)
    print('COMPLETE FIBERS',list(expected),'splits/direct/forests/price',stat,'forest minimum',min(floors,default=None),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    assert __debug__
    if sys.argv[1:]==['--deep']:
        packet('Paths18.json.gz',())
    elif sys.argv[1:]==['--deep4']:
        packet('Paths4.json.gz',())
    else:
        assert not sys.argv[1:]
        packet('Minimum31x310.json.gz',(6,58))
        packet('Fiber16.json.gz',(16,))
