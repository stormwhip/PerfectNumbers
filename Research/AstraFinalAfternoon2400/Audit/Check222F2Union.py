"""Independent frozen domain and scoped join for the complete first exponent 2 under (19,222)."""
from pathlib import Path
import gzip,json,subprocess,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import BASE,split
from Check222LastJ18 import P,K,W
D=H.parent/'Nineteen'
R=(19,222)


def g(raw):return json.loads(gzip.decompress(raw))

def old(name):return g(subprocess.check_output(['git','show',f'{BASE}:Research/FinalNight2400/Root222/{name}.json.gz']))

def new(name):return g((D/(name+'.json.gz')).read_bytes())


def main():
    assert __debug__
    first,tail=split((R,),P[1][0],())
    assert len(first)==53 and tail==144 and first[2]==P[:2]
    second,st=split(first[2],P[2][0],())
    src=old('TwoForests')['cases']['2']
    accepted={int(h) for h in src}
    assert accepted<=second.keys() and second.keys()-accepted=={2,16,22,46}
    third=old('ThirdForests')['cases']
    rr={}
    for t in (2,16,22):
        d=third[f'2:{t}'];r,tail=split(second[t],d['q'],())
        a={int(h) for h in d['children']};z=set(d['left'])
        assert not a&z and a|z==r.keys()
        rr[t]=z
    assert '2:46' not in third
    inc=[new('Forest222'),new('Forest222Stage2'),new('Forest222Stage3')]
    branches={2:set(),16:{1},22:{1}}
    for pack in inc:
        for k,g in [(f'2:{x}',x) for x in (2,16,22,46)]:
            if k not in pack['windows']:continue
            cert=pack['windows'][k]
            if g==46:
                assert cert['closed']==[None]
                accepted.add(46)
                continue
            add=set(cert['closed'])
            assert add<=rr[g] and not add&branches[g]
            branches[g]|=add
    # Exact inert f2/g16 and f2/g22 impose the same third exponent one.
    # Match the actual prefix of each remaining terminal independent of filenames.
    for h,lab in [(2,'Plain222J2'),(4,'Mask222J4'),(18,'Root222J18'),(28,'Root222J28')]:
        p=new(lab)
        assert tuple(map(tuple,p['prefix']))==(*P[:3],(P[3][0],h))
        assert h in rr[22] and h not in branches[22]
        branches[22].add(h)
        if h==18:
            q=new('Root222J18Low');assert tuple(map(tuple,q['prefix']))==(*P,(K,2))
            assert not q['remaining'] and p['remaining']==[2] and q['pivot']==W
    assert branches==rr and accepted|rr.keys()==second.keys()
    print('PASS exact compositional (19,222), f2 historical+new join; first size tail 144, second',len(second),st,
          'third domains retained from frozen data',rr,flush=True)

if __name__=='__main__':main()
