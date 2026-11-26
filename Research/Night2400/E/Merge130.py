"""Merge overlapping discovery trials without replacing known closed leaves."""
import argparse
import json

from Verify130 import H, FIBERS, PIVOT


def stats(t):
    if t is None or t['type']=='open':return 0,1
    if t['type'] in ('forest','price'):return 1,0
    vals=list(map(stats,t['cases'].values()))
    return sum(x for x,_ in vals),sum(y for _,y in vals)


def merge(a,b):
    if b is None or b['type']=='open':return a
    if a is None or a['type']=='open':return b
    if a['type']!='split':return a
    if b['type']!='split':return b
    if a['q']!=b['q']:
        score=lambda x: (not stats(x)[1],stats(x)[0],-stats(x)[1])
        return max((a,b),key=score)
    assert a['cases'].keys()==b['cases'].keys()
    return {**a,'cases':{k:merge(v,b['cases'][k]) for k,v in a['cases'].items()}}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('inputs',nargs='+');ap.add_argument('--out',required=True)
    a=ap.parse_args()
    cases={str(f):None for f in sorted(FIBERS)}
    for name in a.inputs:
        d=json.loads((H/name).read_bytes());assert (d['p'],d['e'],d['tree']['q'])==(7,130,PIVOT)
        for k,v in d['tree']['cases'].items():cases[k]=merge(cases[k],v)
    tree=dict(type='split',q=PIVOT,cases=cases)
    print({k:stats(v) for k,v in cases.items()},flush=True)
    (H/a.out).write_text(json.dumps(dict(p=7,e=130,tree=tree),separators=(',',':')),encoding='utf8')


if __name__=='__main__':main()
