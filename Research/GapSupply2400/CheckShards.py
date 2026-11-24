"""Check three entire divisor shards directly, independent of historical CSV status."""
import json
from pathlib import Path
import Independent as independent


def main():
    if not __debug__:
        raise SystemExit('Do not run with -O.')
    if not all(independent.verify(e) for e in independent.TARGETS):
        raise ValueError('Incomplete exponent proof')
    research=Path(__file__).resolve().parents[1]
    def audit(name):
        return json.loads((research/'TeichmullerValuation'/name).read_text(encoding='utf-8'))
    prior=audit('GeminiBatchAudit2400.json'); ids={s['id'] for s in prior['additions']}
    remaining=[s for s in audit('Audit2400.json')['open_manifest'] if s['id'] not in ids]
    if len(remaining)!=1045 or prior['closed']!=2027:raise ValueError('wrong baseline')
    closed=[]
    for s in remaining:
        if s['root']!=3 or s['exact'] or s['exponent'] not in independent.TARGETS:continue
        d=s['exponent']; nxt=3*(d+1)-1
        # v_3(N) even (3 cannot be Euler); e+1 is an odd multiple of d+1.
        # For e>=nxt, 3^e sigma(3^e)|N and already exceeds B.
        if 3**nxt*((3**(nxt+1)-1)//2)>independent.B:closed.append(s['id'])
    if closed!=['P3_I00212','P3_I00213','P3_I00214']:raise ValueError(closed)
    print('verified shard delta:',closed,'closed:',2027+len(closed),'remaining:',len(remaining)-len(closed))

if __name__=='__main__':main()
