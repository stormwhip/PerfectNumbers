# Canonical 19×312 — independent scope-only receipt

Clean detached `83206fb12af98d39c4088d8c36d5331ca97a4168` in `E:\PerfectNumbers-Night2400-reviewa`; sparse excludes only `Research/NightOrder/ECPP/`; no author cache or reserved folder used. Python 3.11.9. Packet SHA-256 `f2dda153eb0b063dab3820f44b7414e700b499cedd41fe58cc529d556fb6ed32`, verifier SHA-256 `7f652874ac1c3bef9f7da6b2c230b471f438e7163c83af583129f3db5dafe080`.

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers19x312.json.gz
```

2026-11-27 04:06:01.9004726 → 04:06:21.8807357 UTC+08:00, stopwatch 19.966809 seconds, exit 0. Exact first pivot `1481866508237449`, 32/40 closed, open `[1,2,8,10,12,16,22,36]`, first size tail 107. 136 forests, 6 inner splits, 154 direct exclusions, no prices, 554 ECPP.

Independent domain checks rebuilt the outer and all six inner sibling sets with the same standalone integer routine as the previous short proofs, fetched via the reviewer snapshot (not candidate imports). Reproduce from the repository root using this Python stdin body with `python -I -S -B -X int_max_str_digits=0 -`:

```python
import gzip,json,subprocess
script='Research/Night2400/ReceiptsA/ShortFiberScope.py'
s={}
exec(subprocess.check_output(['git','show','2a0f5152dd796dbf1a2dfdcd291b54ef6ae0389c:'+script]),s)
with gzip.open('Research/Night2400/Fibers19x312.json.gz','rt') as f:
    d=json.load(f,object_pairs_hook=s['unique'])
assert (d['p'],d['e'])==(19,312)
p=((19,312),);q=d['pivot']; live,tail,dead=s.get('domain')(p,q,1)
a=set(map(int,d['cases']));assert a<=live
assert (len(a),len(live),tail,sorted(live-a))==(32,40,107,[1,2,8,10,12,16,22,36])
from collections import Counter
c=Counter(direct=dead); tails=[]
def walk(p,t):
    c[t['type']]+=1
    if t['type']=='split':
        x=t['q'];kids,end,n=s.get('domain')(p,x,1);c['direct']+=n;tails.append(end)
        assert set(map(str,kids))==t['cases'].keys()
        for e in kids:walk(p+((x,e),),t['cases'][str(e)])
    else:assert t['type']=='forest'
for e in sorted(a):walk(p+((q,e),),d['cases'][str(e)])
assert c=={'forest':136,'split':6,'direct':154}
assert tails==[50,23,93,106,79,67]
```

No root exponent or shard closure.
