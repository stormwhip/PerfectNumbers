"""Remove stray factor 2 from discovery trees and retest affected leaves."""
import argparse
import json
from Verify130 import H, C, B


def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('input');a.add_argument('out');p=a.parse_args()
    d=json.loads((H/p.input).read_bytes());changes=[0,0]
    def walk(n, path):
        if n is None:return n
        if n['type']=='split':
            q=n['q']
            if q==2:changes[0]+=1;return None
            n['cases']={p:walk(v,path+[(q,int(p))]) for p,v in n['cases'].items()};return n
        if n['type']!='forest':return n
        o=dict(n['owners']); roots=n['roots']; bad={2};V=set(o)|set(roots)
        if not bad&V:return n
        while True:
            k=len(bad);bad.update(q for q,z in o.items() if z in bad)
            if len(bad)==k:break
        roots=[q for q in roots if q not in bad];o=sorted((q,z) for q,z in o.items() if q not in bad);h=n['head']
        if C.Forest(C.State(path),roots,o,h).lower()[0]<=B:changes[0]+=1;return None
        changes[1]+=1;return dict(type='forest',roots=roots,owners=o,head=h)
    d['tree']=walk(d['tree'],[(d['p'],d['e'])]);print('dropped/safe replacements',changes)
    (H/p.out).write_text(json.dumps(d,separators=(',',':')),encoding='utf8')


if __name__=='__main__':main()
