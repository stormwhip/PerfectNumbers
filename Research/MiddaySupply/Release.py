"""Runtime-generated source interval audit. No hardcoded historical survival mask."""
from pathlib import Path
import sys,json,argparse,hashlib
D=Path(__file__).resolve().parent;R=D.parent;sys.path.insert(0,str(D));import Joint as J,Independent as I,DigitReplay as DR,Digits as DG

def release(p,first,last,kind):
    if not __debug__:raise ValueError('do not use optimized Python')
    p,e,rs=next(x for x in J.CASES if x[0]==p);assert I.CASES[p]==(e,tuple(rs));assert 0<=first<=last<=e
    obligations=json.loads((R/'Nov25/Delta.json').read_bytes())['remaining_shards'];assert any(r['root']==p and e in r['remaining_actuals'] for r in obligations)
    ctl=J.old.run(p,e,rs,min_s=first,max_s=last);assert ctl['guard'] is None
    live={s:(ext,hit) for s,ext,hit in ctl['open']};out=[];I.DIGIT=DR.verifier
    for s in range(first,last+1):
        if s not in live:continue
        ext,hit=live[s]
        if s==0 or (hit and hit[0]=='known'):out.append([s,'zero or known']);continue
        # Do not import search packets or take their candidate lower bounds on faith.
        Q=J.euler_floor(p,s,J.U.O.tb.forbidden(p),128);mult=(Q+1)//(2*p**s)
        if ext:
            if kind=='independent':
                from ExteriorReplay import possible
                outside=possible(p,s,mult)
            else:
                from OuterDigits import run_ext
                outside=run_ext(p,e,rs,s)
            if outside:out.append([s,'external']);continue
        if kind=='independent':w=I.check(p,s,mult,65)
        else:
            old=J.short;J.short=lambda *a:DG.digit(*a[:-1],128) and old(*a)
            try:w=J.run(p,e,tuple(rs),s,128,cap=65)['first']
            finally:J.short=old
        if w:out.append([s,'rough'])
    return {'p':p,'e':e,'domain':[first,last],'kind':kind,'open':out,'count':last-first+1-len(out)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('first',type=int);ap.add_argument('last',type=int);ap.add_argument('--kind',choices=['primary','independent'],default='independent');ap.add_argument('--require-complete',action='store_true');a=ap.parse_args();row=release(a.p,a.first,a.last,a.kind);print(json.dumps(row),flush=True)
 if a.require_complete and (row['open'] or a.first!=0 or a.last!=row['e']):raise SystemExit('incomplete domain or open branches')
