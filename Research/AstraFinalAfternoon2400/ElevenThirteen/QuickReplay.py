"""Rebuild package scope and check total disjointness; no global projection side effects."""
from pathlib import Path
import argparse, subprocess, sys, json, gzip
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Coverage import require

PROVED={
 (11,16):(10,13,25,26),(11,18):(9,),(11,48):(14,24,26,32),(13,6):(124,150),
}


def cmd(file,*args):
    subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(H/file),*map(str,args)],check=True)


def summary():
    d=json.loads((H/'ForestCoverage.json').read_bytes());n=sum(len(v['accepted']) for v in d.values());require(n==212,'base forest count')
    extra={(p,e,f) for (p,e),fs in PROVED.items() for f in fs};require(len(extra)==11,'nested count')
    paths=[]
    for p,e,f in sorted(extra):
        path=H/f'Second-{p}-{e}-{f}.json.gz';r=json.loads(gzip.decompress(path.read_bytes()))['row']
        require((r['p'],r['e'],r['f'])==(p,e,f),'nested scope');paths.append(path)
    extra.add((11,48,36));require(len(extra)==12,'disjoint supplemental shapes')
    require(all(f in d[f'{p}:{e}']['remaining'] for p,e,f in extra),'incompatible or overlapping first fiber')
    for k,v in sorted(d.items()):
        p,e=map(int,k.split(':')); left=set(v['remaining'])-{f for a,b,f in extra if (a,b)==(p,e)}
        require(bool(left),'this packet does not contain a whole key')
        print(k,len(v['accepted'])+len(v['remaining'])-len(left),'accepted total, live remaining:',len(left),flush=True)
    print('PASS exact first-fiber partition',n+len(extra),'complete conditional fibers, zero whole keys',flush=True)
    return paths

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--local-arithmetic',action='store_true');a=parser.parse_args();p=summary()
    if a.local_arithmetic:
        cmd('Coverage.py');cmd('ForestPacket.py');cmd('SecondTree.py','--verify',*p);cmd('PivotPrice48Depth.py');cmd('AllLifts.py')
