"""Optional discovery packer. GP finds witnesses; Verify130.py decides validity."""
from concurrent.futures import ThreadPoolExecutor
from functools import cache
from hashlib import sha256
import argparse
import gzip
import json
import subprocess

from Verify130 import H, R, C, B, PIVOT, FIBERS, replay


def labels(node):
    if node['type'] == 'open' or node['type'] == 'price':
        return set()
    if node['type'] == 'forest':
        return set(node['roots']) | set(dict(node['owners']))
    return {node['q']}.union(*(labels(x) for x in node['cases'].values()))


def clean(t):
    if t is None:
        return {'type':'open'}
    if t['type'] == 'split':
        return {**t, 'cases': {k:clean(v) for k,v in t['cases'].items()}}
    return t


def load(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def valid(q, c):
    if not isinstance(c, list) or not c:
        return False
    try:
        for rr in c:
            if rr[0] != q:
                return False
            q = C.pc.level(*rr)
        return C.pc.prime64(q)
    except (ValueError, TypeError, IndexError):
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('inputs', nargs='+', help='raw trees; later non-null fiber wins')
    ap.add_argument('--fibers', nargs='+', type=int, required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--gp', required=True)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--timeout', type=int, default=120)
    a = ap.parse_args()
    assert set(a.fibers) <= FIBERS
    cases = {str(f): None for f in sorted(FIBERS)}
    cache_dir = H/'cert'
    cache_dir.mkdir(exist_ok=True)
    for name in a.inputs:
        d = load(H/name)
        assert (d['p'], d['e'], d['tree']['q']) == (7,130,PIVOT)
        for k,v in d['tree']['cases'].items():
            if v is not None and int(k) in a.fibers:
                cases[k] = v
    tree = dict(type='split', q=PIVOT, cases={k:clean(v) for k,v in cases.items()})
    todo = sorted(q for q in labels(tree) if q >= 2**64)
    wanted = {str(q) for q in todo}
    wanted |= {sha256(str(q).encode()).hexdigest()[:24] for q in todo}
    bank = {}
    for directory in ('Session20261126','FinalSprint','Nov25/Forests','Nov25/Seven',
                      'NightSevenForest/Release','NightLowRoute/Release','OrderSupplyNext'):
        for p in (R/directory).glob('*.json.gz'):
            d = load(p)
            if not isinstance(d,dict):continue
            cs = d if p.name=='OrderPrimeProofs.json.gz' else d.get('ecpp',{})
            if isinstance(cs,dict): bank.update((k,v) for k,v in cs.items() if k in wanted)
    print('selected', len(todo), 'archive keys', len(bank), flush=True)

    @cache
    def witness(q):
        key = str(q); dig = sha256(key.encode()).hexdigest()[:24]
        path = cache_dir/(dig+'.json')
        for x in (bank.get(key),bank.get(dig),load(path) if path.is_file() else None):
            if valid(q,x):return x
        data = f'default(parisizemax,1000000000);default(nbthreads,1);\nprint(primecert({q}));\n'
        try:
            r = subprocess.run(['wsl','-d','Ubuntu','--',a.gp,'-fq'],input=data,text=True,encoding='utf-8',
                               errors='replace',capture_output=True,timeout=a.timeout,check=True)
            cs = json.loads(r.stdout)
            if valid(q,cs):
                tmp = path.with_suffix('.tmp')
                tmp.write_text(json.dumps(cs,separators=(',',':')),encoding='utf-8')
                tmp.replace(path)
                return cs
        except (subprocess.SubprocessError, ValueError) as ex:
            print('GP failure',q.bit_length(), key[:20],type(ex).__name__,flush=True)
        return None

    with ThreadPoolExecutor(a.workers) as pool:
        proofs = dict(zip(todo,pool.map(witness,todo)))
    def restrict(t):
        if t['type']=='forest' and any(q>=2**64 and not proofs[q] for q in labels(t)):
            return {'type':'open'}
        if t['type']=='split':
            if t['q']>=2**64 and not proofs[t['q']]:return {'type':'open'}
            return {**t,'cases':{k:restrict(v) for k,v in t['cases'].items()}}
        return t
    tree = restrict(tree)
    ecpp = {str(q):proofs[q] for q in sorted(labels(tree)) if q>=2**64}
    out = dict(p=7,e=130,tree=tree,ecpp=ecpp)
    info = replay(out)
    dest = H/a.name
    dest.write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0))
    print('sealed',dest.name,info['scope'],'complete fibers',info['closed_fibers'],
          'open paths',len(info['open_paths']),'terminal paths',len(info['terminals']), flush=True)


if __name__=='__main__':
    main()
