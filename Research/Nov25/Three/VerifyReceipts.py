"""Validate preserved root-three negative experiment metadata, not an OPN proof."""
import hashlib
import json
from pathlib import Path
import re
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from SourceUnit import frontier, E, test


def require(t, msg):
    if not t:
        raise ValueError(msg)


def verify_ecm():
    n=E.sigma(3,1162)
    require(pow(2,n-1,n)!=1,'expected composite witness for full input')
    digest=hashlib.sha256(str(n).encode()).hexdigest()
    used=set()
    for stem, total, b1,b2 in (('Root1162ECM',128,250000,128992510),
                               ('Root1162ECMStrong',64,1000000,1045563762)):
        row=json.loads((H/(stem+'.json')).read_bytes());text=(H/(stem+'.log')).read_text(encoding='ascii')
        runs=re.findall(r'Using B1=(\d+), B2=(\d+), polynomial \w+\(\d+\), sigma=(\d+:\d+)',text)
        require(row['sigma_sha256']==digest and row['e']==1162 and row['root']==3 and row['status']==0,'ECM input mismatch')
        require(row['requested_curves']==row['completed']==total and row['b1']==b1,'ECM count mismatch')
        require(len(runs)==text.count('Step 2 took')==total and all((int(x),int(y))==(b1,b2) for x,y,_ in runs),'log count mismatch')
        require(f'Input number is {n} ({len(str(n))} digits)' in text,'ECM logged a different input')
        require(not row['factors'] and not any(1<q<n and n%q==0 for w in re.findall(r'\b[0-9]{1,555}\b',text) for q in (int(w),)), 'proper divisor warrants investigation')
        for _,_,seed in runs:
            require(seed not in used,'duplicate curve seed'); used.add(seed)
    return len(used)


def compare_sample():
    stored=json.loads((H/'SourceUnitSample.json').read_bytes())
    require([r['e'] for r in stored]==[1162,1108,990,970,856] and set(r['e'] for r in stored)<=frontier(),'sample set mismatch')
    actual=[test(r['e'],4096,4096,sample=True) for r in stored]
    require(actual==stored,'source sample mismatch')
    return sum(2*r['tested']-len(r['left']) for r in actual)


if __name__=='__main__':
    print('curves logged',verify_ecm(),'excluded (s, tag) sample cells',compare_sample(),
          '; 0 new exact-exponent or shard claims')
