"""Discovery only: reusable historical edges and witness-led branch refinements."""
from Domain import *
from collections import defaultdict
import argparse, time


def catalog():
    # Do not read any sparse ECPP directory, external worktree, or agent workspace.
    groups=['Session20261126','FinalSprint','Midday','MiddayDirected','MiddayForest','Night2400/D','Night2400/D2','Night2400/G']
    by_parent=defaultdict(list); seen=set(); proof={}
    def walk(obj):
        if type(obj)==dict:
            if 'owners' in obj:
                for a,b in obj['owners']:
                    if (a,b) not in seen:
                        seen.add((a,b));by_parent[b].append(a)
            if 'ecpp' in obj:
                for k,v in obj['ecpp'].items():
                    if type(v)==list and v and type(v[0])==list and len(v[0])>=5 and type(v[0][0])==int:
                        proof.setdefault(str(v[0][0]),v)
            for k,v in obj.items():
                if k not in {'owners','ecpp'}:walk(v)
        elif type(obj)==list:
            for v in obj:walk(v)
    for d in groups:
        for p in sorted((R/d).rglob('*.json.gz')):
            if p.stat().st_size>6_000_000:continue
            # Mainline prime stores live elsewhere; restrict archive names to forest/tree proofs.
            if not p.name.startswith(('Forest','Pivot','Directed','JointTree','Tree','Seven28','Eleven358')):continue
            walk(json.loads(gzip.decompress(p.read_bytes())))
    print('CATALOG',len(by_parent),len(seen),len(proof),flush=True)
    return by_parent,proof


def seed(s,roots,cat,depth,limit):
    z=sorted(set(roots)); reach=set(z); es=[]
    for _ in range(depth):
        level=[]
        for p in z:
            for q in cat.get(p,()):
                if q not in reach and q not in s.bad and q not in s.rows and s.D%q:
                    reach.add(q);es.append((q,p));level.append(q)
                    if len(es)>=limit:return es
        z=level
        if not z:break
    return es


def build(s,k,o,find,rounds,head,path,counter):
    now=time.monotonic();old=0;tried=set();path.parent.mkdir(exist_ok=True)
    for i in range(rounds+1):
        F=C.Forest(s,k,o,head,record=True); lb,w=F.lower();trace=[] if lb>B else list(F.witness(w));fl=floor10(lb)
        print(counter,i,fl,len(o),[(q,h) for q,h,r in trace[:30]],round(time.monotonic()-now,1),flush=True)
        if lb>old:
            old=lb; tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(dict(roots=k,owners=o,head=head,score=fl)),encoding='utf8');tmp.replace(path)
        if lb>B:return True
        if i==rounds:break
        d={};seen=set(k)|dict(o).keys()
        for q,h,r in sorted(trace,key=lambda t:t[2].bit_length(),reverse=True):
            if not r or (q,h) in tried or h*q.bit_length()>13000:continue
            tried.add((q,h));
            for v in find.factors(q,h):
                if v not in seen and v not in s.bad and v not in s.rows and s.D%v:d.setdefault(v,q)
        if not d:break
        o+=sorted(d.items())
    return False


def main():
    from Discover import Finder,Bank
    a=argparse.ArgumentParser();a.add_argument('--db',type=Path,required=True);a.add_argument('--f',type=int,nargs='+',required=True);a.add_argument('--mask',type=int,nargs='+',required=True);a.add_argument('--smooth',type=int,default=24);a.add_argument('--rounds',type=int,default=25);a.add_argument('--head',type=int,default=384);a.add_argument('--depth',type=int,default=7);a.add_argument('--limit',type=int,default=1600);a.add_argument('--phase',default='base');a.add_argument('--anchor',type=int,nargs='*',default=[]);ns=a.parse_args()
    finder=Finder(Bank(ns.db),ns.smooth);cat,proof=catalog();
    # Warm discovery with existing successful trials (not used by the proof checker).
    for p in sorted((H/'trials').glob('*.json')):
        try: row=json.loads(p.read_bytes())
        except ValueError: continue
        if row.get('score',0)<2400:continue
        for z,q in row['owners']:
            if z not in cat[q]:cat[q].append(z)
    for f in ns.f:
        for m in ns.mask:
            assert m in ALL
            if f not in expand([(P,E)],Q,m)[0]:continue
            s=state([(P,E),(Q,f)],m)
            k=sorted((set(s.present)|set(finder.factors(Q,f))|set(ns.anchor))-s.rows.keys()-set(s.bad));assert all(s.D%z==0 or z in s.present for z in k)
            value=abundance(s,k)
            if value>2: print('ABUNDANCE',m,f,float(value),flush=True);continue
            o=seed(s,k,cat,ns.depth,ns.limit);path=H/'trials'/f'{ns.phase}-{m}-{f}.json'
            if path.exists():o=json.loads(path.read_bytes())['owners']
            build(s,k,o,finder,ns.rounds,ns.head,path,(m,f))
            for z,q in json.loads(path.read_bytes())['owners']:
                if z not in cat[q]:cat[q].append(z)

if __name__=='__main__':main()
