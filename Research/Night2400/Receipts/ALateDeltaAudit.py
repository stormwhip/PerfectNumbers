"""Exact scope and delta-only replay for the late A first-fiber packets."""
from collections import Counter
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from math import gcd,prod
import gzip,json,subprocess,sys

old_source='c3219ae160f6b4f604fdf906c8f227b9fb109b14:Research/Night2400/ReceiptsA/A79DeltaAudit.py'
G={}
exec(subprocess.check_output(['git','show',old_source]),G)
P=G['P']; Q=G['Q']; ROOT=G['ROOT']; B=G['B']
decode=G['decode'];state=G['state']; branch=G['branch'];sigma=G['sigma']; val=G['val']; modes=G['modes']
R=((7,12),)
U=(3,5,11,13,17,31)
EXPECTED={'Exact1x2':R+((Q,1),(110563,2)),
          'SupportLeaf12':R+((Q,1),(110563,2),(226741,2)),
          'SupportLeaf2':R+((Q,2),(200741603328100897,1))}


def support(parts,obj):
    totals=Counter(); fkeys=set()
    assert sum(e%2 for q,e in parts)==1
    for i in range(64):
        yes={p for j,p in enumerate(U) if i>>j&1}; no=(19,*sorted(set(U)-yes))
        X,S,D,dead=state(parts,no)
        if dead:totals['direct']+=1;continue
        x=Fraction(S,X)
        for q in yes:
            h=max(1,val(D,q));h+=h%2
            while q**h<=B and gcd(sigma(q,h),prod(no))>1:h+=2
            assert q**h<=B
            x*=Fraction(sigma(q,h),q**h)
        if x>2:totals['abundance']+=1;continue
        fkeys.add(str(i));totals['forest']+=1
        assert yes<=set(obj['masks'][str(i)]['roots'])
    assert fkeys==obj['masks'].keys() and totals=={'direct':32,'abundance':23,'forest':9}
    print('SUPPORT',parts,dict(totals),sorted(map(int,fkeys)),flush=True)


def main(base,fs,selected):
    p=P/'Fibers12.json.gz';raw=p.read_bytes();d=decode(raw)
    old=decode(subprocess.check_output(['git','show',f'{base}:{p.as_posix()}']))
    print('PROVENANCE',base,'packet',sha256(raw).hexdigest(),'commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),flush=True)
    assert d['pivot']==old['pivot']==Q and d['pair']==old['pair']==[7,12]
    assert all(d['cases'][k]==a for k,a in old['cases'].items())
    assert all(d['ecpp'][k]==a for k,a in old['ecpp'].items())
    fs=set(fs)
    assert d['cases'].keys()-old['cases'].keys()=={str(f) for f in fs}
    live,direct=branch(ROOT,Q,(19,)); assert (len(live),direct)==(83,84)
    print('COMBINED OPEN',sorted(live-set(map(int,d['cases']))),flush=True)
    stats=Counter(); cert=set(); used_wrappers=[]
    def add(z,seen):
        if z>=2**64:seen.add(str(z))
    def walk(parts,t,ban,seen):
        typ=t['type'];stats[typ]+=1
        X,S,D,dead=state(parts,ban);assert not dead
        if typ=='forest':
            for p in [*t['roots'],*(p for p,q in t['owners'])]:add(p,seen)
        elif typ=='split':
            q=t['q'];add(q,seen)
            keys,n=branch(parts,q,ban);stats['direct']+=n
            assert set(map(str,keys))==t['cases'].keys()
            for f in sorted(keys):walk(parts+((q,f),),t['cases'][str(f)],ban,seen)
        elif typ in ('no-three','no-five'):
            q,r=(3,5) if typ=='no-three' else (5,3)
            assert ban==(19,) and (r in dict(parts) or D%r==0) and q not in dict(parts)
            assert Fraction(sigma(7,12),7**12)*Fraction(13,9)*Fraction(6,5)>2
            if not state(parts,ban+(q,))[3]:walk(parts,t['tree'],ban+(q,),seen)
        elif typ=='abundance':
            qs=t['forced'];assert qs and len(set(qs))==len(qs) and all(D%q==0 for q in qs)
            for q in qs:add(q,seen)
            stats['abundance_modes']+=modes(parts,ban,qs)
        elif typ=='support-abundance':
            for mask in range(64):
                yes={q for i,q in enumerate(U) if mask>>i&1};no=tuple(set(ban)|(set(U)-yes))
                if not state(parts,no)[3]:stats['support_modes']+=modes(parts,no,sorted(yes-set(dict(parts))))
        elif typ in ('exact-packet','support-packet'):
            assert ban==(19,) and set(t)=={'type','name'}
            key=t['name']; raw=(P/(key+'.json.gz')).read_bytes();obj=decode(raw)
            expected=EXPECTED.get(key)
            if key.startswith('Exact42x'):
                expected=ROOT+((Q,42),(173,int(key.removeprefix('Exact42x'))))
            assert parts==expected==tuple(map(tuple,obj['prefix']))
            used_wrappers.append((key,parts,sha256(raw).hexdigest(),len(obj['ecpp'])))
            if typ=='exact-packet':
                assert set(obj)=={'pair','pivot','ecpp','prefix','tree'} and obj['pivot']==Q and obj['pair']==[7,12]
                childcert=set()
                for j,(q,f) in enumerate(parts[2:],2):
                    assert f in branch(parts[:j],q,ban)[0]
                    add(q,childcert)
                walk(parts,obj['tree'],ban,childcert)
                assert childcert==obj['ecpp'].keys()
            else:support(parts,obj)
        else:raise RuntimeError(typ)
    for f in sorted(selected):walk(ROOT+((Q,f),),d['cases'][str(f)],(19,),cert)
    if fs==set(selected): assert d['ecpp'].keys()-old['ecpp'].keys()<=cert
    assert cert<=d['ecpp'].keys()
    print('DELTA',dict(stats),'outer ECPP',len(cert),'scoped',used_wrappers,flush=True)
    sys.path.insert(0,str(P.resolve()))
    import Verify
    given=dict(pair=d['pair'],pivot=d['pivot'],cases={str(f):d['cases'][str(f)] for f in selected},ecpp={k:d['ecpp'][k] for k in cert})
    assert set(Verify.verify(G['InMemoryPacket'](given)))==live-set(selected)

if __name__=='__main__':
    assert __debug__ and len(sys.argv)==4
    main(sys.argv[1],list(map(int,sys.argv[2].split(','))),list(map(int,sys.argv[3].split(','))))
