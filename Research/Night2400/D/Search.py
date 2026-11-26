"""Discovery only: greedily extend a valid owner forest along weak witnesses."""
from Explore import *
import argparse, time


def go(f,m,find,rounds,prior,head):
    old,_,_=inputs(); gs=base_graphs(old); a,b=groups(m); s=C.State(feasible(f)[0],a,b); k=roots(s,f)
    p=H/'trials'/f'{m}.json'; p.parent.mkdir(exist_ok=True)
    es=trim(s,k,gs[-1])
    if p.exists():es=json.loads(p.read_bytes())['owners']
    else:
        for other in prior:
            z=p.with_name(f'{other}.json')
            if z.exists():es+=json.loads(z.read_bytes())['owners']
        es=trim(s,k,es)
    considered=set();t=time.monotonic(); best=0
    for ii in range(rounds+1):
        forest=C.Forest(s,k,es,head,record=True); lb,w=forest.lower(); trace=list(forest.witness(w));score=floor10(lb)
        print(m,ii,score,len(es),[(z,g) for z,g,_ in trace[:40]],round(time.monotonic()-t,1),flush=True)
        if lb>best:
            best=lb; p.write_text(json.dumps(dict(roots=k,owners=es,head=head,score=score)),encoding='utf8')
        if lb>B:return True
        if ii==rounds:break
        known=set(k)|dict(es).keys(); new={}
        for z,g,rem in sorted(trace,key=lambda r:r[2].bit_length(),reverse=True):
            if (z,g) in considered or not rem or g*z.bit_length()>15000:continue
            considered.add((z,g));
            for q in find.factors(z,g):
                if q not in known and q not in s.bad and q not in s.rows and s.D%q:new.setdefault(q,z)
        if not new:break
        es+=sorted(new.items())
    return False


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--index',type=Path,required=True);ap.add_argument('--mask',type=int,nargs='+',required=True);ap.add_argument('--rounds',type=int,default=20);ap.add_argument('--smooth',type=int,default=24);ap.add_argument('--head',type=int,default=384); ns=ap.parse_args();
    from Discover import Finder,Bank
    find=Finder(Bank(ns.index),ns.smooth); old,_,missing=inputs(); prev={2:[],4:[]}
    for m in ns.mask:
        assert m in missing; f=next(f for f in branches(m)[0] if f in (2,4)); a,b=groups(m); s=C.State(feasible(f)[0],a,b)
        if bound(s,roots(s,f))[0]>2:print(m,'ABUNDANCE');continue
        go(f,m,find,ns.rounds,prev[f],ns.head);prev[f].append(m)
