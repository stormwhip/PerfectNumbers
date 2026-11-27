"""Bounded witness-led private forest discovery (no proof result without cold replay)."""
from Domain import *
import argparse, time


def search(s,k,o,find,rounds,head,path,tag):
    seen=set(); best=0; begin=time.monotonic(); path.parent.mkdir(exist_ok=True)
    for i in range(rounds+1):
        ff=C.Forest(s,k,o,head,record=True);lb,w=ff.lower();wit=list(ff.witness(w));fl=floor10(lb)
        print(tag,i,fl,len(o),[(q,f) for q,f,_ in wit[:30]],round(time.monotonic()-begin,1),flush=True)
        if lb>best:
            path.write_text(json.dumps(dict(roots=k,owners=o,head=head,score=fl)),encoding='utf8');best=lb
        if lb>B:return True
        if i==rounds:break
        known=set(k)|dict(o).keys();add={}
        for q,f,r in sorted(wit,key=lambda x:x[2].bit_length(),reverse=True):
            if (q,f) in seen or not r or f*q.bit_length()>15000:continue
            seen.add((q,f))
            for z in find.factors(q,f):
                if z not in known and z not in s.bad and z not in s.rows and s.D%z:add.setdefault(z,q)
        if not add:break
        o+=sorted(add.items())
    return False


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--db',type=Path,required=True);ap.add_argument('--mask',type=int,nargs='+',required=True);ap.add_argument('--rounds',type=int,default=24);ap.add_argument('--smooth',type=int,default=24);ap.add_argument('--head',type=int,default=512);ap.add_argument('--phase',default='base');ns=ap.parse_args()
    from Discover import Finder,Bank
    find=Finder(Bank(ns.db),ns.smooth)
    prior=[]
    for m in ns.mask:
        assert m in range(2,256,4)
        s=st([(P,E)],m); path=H/'trials'/f'{ns.phase}-{m}.json'
        es=(json.loads(path.read_bytes())['owners'] if path.exists() else [])+OLD['row']['owners']+prior
        if ns.phase != 'base':
            es += [edge for p in sorted((H/'trials').glob('base-*.json')) for edge in json.loads(p.read_bytes())['owners']]
        k,o=shape(s,SEEDS,es)
        search(s,k,o,find,ns.rounds,ns.head,path,m);prior+=json.loads(path.read_bytes())['owners']
