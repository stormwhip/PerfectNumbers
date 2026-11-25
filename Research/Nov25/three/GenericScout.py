"""Bounded discovery against the unchanged generic ThreeChainNext replay."""
import argparse
import json
from pathlib import Path
import sys
from time import monotonic

sys.path.insert(0,str(Path(__file__).resolve().parent))
from ChainScout import EdgeProbe, StopSearch, HERE, E, frontier, roots


def run(e, args):
    # E.replay builds its own dict; feed candidate edges iteratively from the exact
    # visit callback instead of editing verifier code. Candidate only.
    fs=roots(e)
    ep=EdgeProbe(args.bits,args.requests,monotonic()+args.seconds)
    old=E.proven
    E.proven=lambda _: True
    code=E.replay.__code__
    walk_code=next(c for c in code.co_consts if getattr(c,'co_name','')=='walk')
    depth=0; nodes=0
    def trace(fr,event,arg):
        nonlocal depth,nodes
        if event=='call' and fr.f_code is walk_code:
            v=fr.f_locals
            nodes+=1; depth=max(depth,v['depth'])
            r,f=v['ex'][-1]
            if r!=3:
                children=ep.get((r,f))
                v['edges'].setdefault((r,f),set()).update(children)
        return trace if fr.f_code is walk_code or fr.f_code is code else None
    sys.settrace(trace)
    try:
        res=E.replay(dict(e=e,root=list(map(str,fs)),edges=[]),cap=args.requests)
        ok=True; info=res
    except (ValueError,StopSearch) as ex:
        ok=False; info=str(ex)
    finally:
        sys.settrace(None); E.proven=old
    out=dict(e=e,ok=ok,status=info,depth=depth,nodes=nodes,edges=len(ep.edges),root=list(map(str,fs)))
    row=dict(e=e,root=out['root'],edges=[[str(r),f,str(z)] for (r,f),zs in sorted(ep.edges.items()) for z in sorted(zs)],generic=True) if ok else None
    return out,row


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only',nargs='+',type=int,required=True)
    p.add_argument('--seconds',type=float,default=10)
    p.add_argument('--requests',type=int,default=5000)
    p.add_argument('--bits',type=int,default=290)
    a=p.parse_args()
    if not set(a.only)<=frontier():
        raise ValueError('outside fixed frontier')
    rows=[]; candidates=[]
    for e in a.only:
        r,c=run(e,a);rows.append(r);print(e,r['ok'],r['status'],r['nodes'],r['edges'],flush=True)
        (HERE/'GenericScout.json').write_text(json.dumps(rows,indent=1)+'\n',encoding='utf8')
        if c:
            candidates.append(c)
            (HERE/'GenericScoutCandidates.json').write_text(json.dumps(candidates,separators=(',',':'))+'\n',encoding='utf8')


if __name__=='__main__':
    main()
