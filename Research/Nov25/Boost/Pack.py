"""Canonical low forest packet or exact sorted list of unavailable prime proofs."""
import argparse, gzip, hashlib, json, sys
from functools import cache
from pathlib import Path
from BoostScore import H,R,ROOT,HIST,PIN,B,pc,proof,load

CACHE=ROOT/'NightCache'
DIRS=(H/'cert',HIST/'CertCache',CACHE/'ecpp-local',R/'NightOrder/ECPP',R/'EveningTree/ECPP',R/'NightLowRoute/CertCache',ROOT/'upstream/Research/OrderSupplyNext/certs',HIST.parent/'NightOrder/ECPP',HIST.parent/'EveningTree/ECPP')

def read(f):
    data=f.read_bytes();return json.loads(gzip.decompress(data) if f.suffix=='.gz' else data)

def verify_chain(q,rows):
    if not isinstance(rows,list) or not rows:return False
    try:
        for r in rows:
            if r[0]!=q:return False
            q=pc.level(*r)
        return pc.prime64(q)
    except (TypeError,ValueError,IndexError,OverflowError):return False

@cache
def database():
    db={}
    files=[*PIN.glob('Forest*.gz'),*H.parent.joinpath('Forests').glob('*.gz'),*R.joinpath('NightSevenForest/Release').glob('*.gz'),R/'RootFiveNext/RootFiveCertificate.json']
    for f in files:
        if f.is_file():db.update(read(f).get('ecpp',{}))
    f=R/'OrderSupplyNext/OrderPrimeProofs.json.gz'
    if f.is_file():db.update(read(f))
    return db

@cache
def known(q):
    if q<2**64:return pc.prime64(q)
    h=hashlib.sha256(str(q).encode()).hexdigest()[:24]
    db=database();return str(q) in db or h in db or any((d/n).is_file() for d in DIRS for n in (h+'.json',h+'.json.gz','Prime'+h+'.json'))

@cache
def chain(q):
    h=hashlib.sha256(str(q).encode()).hexdigest()[:24]
    for key in (str(q),h):
        rows=database().get(key)
        if verify_chain(q,rows):return rows
    for d in DIRS:
        for n in (h+'.json',h+'.json.gz','Prime'+h+'.json'):
            f=d/n
            if f.is_file():
                rows=read(f)
                if verify_chain(q,rows):return rows
    return None

def pack(path):
    r=load(path); names=set(r['roots'])|dict(r['owners']).keys(); missing=[]; cs={}
    for q in sorted(names):
        if q<2**64:
            if not pc.prime64(q):raise ValueError(f'composite small node {q}')
        elif (rows:=chain(q)) is not None:cs[str(q)]=rows
        else:missing.append(q)
    if missing:
        f=H/(path.stem+'.missing.json');f.write_text(json.dumps(missing)+'\n',encoding='utf8'); print('MISSING',path.name,len(missing),[(q,q.bit_length()) for q in missing],flush=True);return
    vals=proof(r,cs);den=r.get('den',1);v=min(vals.values());passed=v>B**den
    if passed:
        f=H/(path.stem+'.pack.json.gz');f.write_bytes(gzip.compress(json.dumps(dict(rows=[r],ecpp=cs),separators=(',',':')).encode(),mtime=0))
    # Both the decision and floor are exact; avoid Python 3.11 digit limits.
    k=(v.bit_length()-1)*30103//100000//den
    while v>=10**((k+1)*den):k+=1
    while v<10**(k*den):k-=1
    print('PASS' if passed else 'OPEN','exact',path.name,'floor',k,'modes',len(vals),'nodes',len(names),'ECPP',len(cs),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--cache',type=Path,action='append',default=[]);ap.add_argument('paths',nargs='+',type=Path);a=ap.parse_args()
    DIRS=(*a.cache,*DIRS)
    for s in a.paths:pack(s)
