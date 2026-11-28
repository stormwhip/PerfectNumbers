"""Produce or cold-check a conditional first-pivot forest packet; verifier needs no discovery input."""
from functools import cache
from hashlib import sha256
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R/'Session20261126')]
from Coverage import FACTORS,PIVOTS,ORDER,POCK,B,domain,prime,prime64,require
from PivotCheck import C,exact_leaf,floor10
PACK=H/'Forests.json.gz'


def packed():
    rows={};cert={}
    for f in sorted(H.glob('TrialForest-*-None-*.json')):
        _,sp,se,_,*_=f.stem.split('-');p,e=int(sp),int(se)
        row=rows.setdefault(f'{p}:{e}',{})
        for h,d in json.loads(f.read_bytes()).items():
            if 'floor' not in d:continue
            if h not in row or len(d['owners'])+len(d['roots'])<sum(len(row[h][k]) for k in ('owners','roots')):
                row[h]={k:d[k] for k in ('roots','owners','head')}
    for key,d in rows.items():
        for leaf in d.values():
            for z in (*leaf['roots'],*(q for q,_ in leaf['owners'])):
                if z<2**64 or z in POCK or str(z) in cert:continue
                path=R/'NightOrder/ECPP'/(sha256(str(z).encode()).hexdigest()[:24]+'.json.gz')
                cert[str(z)]=json.loads(gzip.decompress(path.read_bytes()))
    return dict(rows=rows,ecpp=cert)


def verify(d,verbose=True):
    require(set(d)=={'rows','ecpp'},'packet layout');used=set(); allfs=0;result={}
    @cache
    def certified(z):
        require(type(z)==int and z>2,'invalid vertex')
        if z<2**64:return prime64(z)
        if str(z) not in d['ecpp'] and z in POCK:return prime(z)
        used.add(str(z));q=z
        for step in d['ecpp'][str(z)]:
            require(step[0]==q,'ECPP subject');q=C.pc.level(*step)
        return prime64(q)
    for key,item in sorted(d['rows'].items()):
        p,e=map(int,key.split(':'));require(key==f'{p}:{e}' and (p,e) in FACTORS,'unregistered key');q=PIVOTS[p,e];values=set(domain(p,e)[0]);hits=[];least=None
        for sf,leaf in sorted(item.items(),key=lambda pair:int(pair[0])):
            f=int(sf);require(sf==str(f) and f in values,'extra fiber'); rows=[(p,e),(q,f)]; s=C.State(rows)
            require(not s.conflict and s.base<=B and tuple(C.ORDER)==ORDER,'wrong state')
            require(set(leaf)=={'roots','owners','head'},'leaf fields')
            a,o,h=(leaf[k] for k in ('roots','owners','head'));C.validate_forest(s,a,o,h,certified)
            z=min(C.Forest(s,a,o,h).lower()[0],exact_leaf(rows,a,o,h));require(z>B,('insufficient leaf',key,f))
            x=floor10(z);least=x if least is None else min(least,x); hits.append(f)
        remaining=sorted(values-set(hits));result[key]=dict(pivot=q,accepted=hits,remaining=remaining,min_floor=least);allfs+=len(hits)
        if verbose:print(key,'pivot',q,'covered',len(hits),'of',len(values),'remaining',remaining,'minimum floor',least,flush=True)
    require(used==set(d['ecpp']),'unneeded ECPP');print('PASS',allfs,'complete conditional first-pivot fibers;',len(used),'ECPP certificates; full keys',[k for k,v in result.items() if not v['remaining']],flush=True)
    return result

if __name__=='__main__':
    if not __debug__:raise SystemExit('assertions are required in frozen second verifier')
    if sys.argv[1:]==['--pack']:
        data=packed();report=verify(data)
        PACK.write_bytes(gzip.compress((json.dumps(data,separators=(',',':'),sort_keys=True)+'\n').encode(),mtime=0))
        (H/'ForestCoverage.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8')
    elif not sys.argv[1:]:
        data=json.loads(gzip.decompress(PACK.read_bytes()));report=verify(data)
        require(report==json.loads((H/'ForestCoverage.json').read_bytes()),'receipt discrepancy')
    else:raise SystemExit('usage: ForestPacket.py [--pack]')
