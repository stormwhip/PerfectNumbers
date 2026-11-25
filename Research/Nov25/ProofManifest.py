"""Hash all explicitly registered Nov25 packet files; not a proof replay."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent


def packet_paths():
    # This is a data-only audit of the explicit names tuple, not code execution.
    tree=ast.parse((H/'Ledger.py').read_bytes())
    fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verified_batches')
    stmt=next(n for n in fun.body if isinstance(n,ast.Assign) and
              len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='names')
    paths={'five148':'five/Forest148.json.gz','five520':'five/Late520Dual.json'}
    names=ast.literal_eval(stmt.value)
    if len(names)!=len(set(names)):raise ValueError('duplicate job name')
    for n in names:
        if n in paths:yield H/paths[n]
        elif n.startswith('seven/') and n.count('/')==1 and n.endswith('.pack.json.gz'):yield H/n
        elif Path(n).name==n and n.endswith('.json.gz'):yield H/'Forests'/n
        else:raise ValueError(f'unknown input job {n}')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    opt=ap.add_mutually_exclusive_group(required=True)
    opt.add_argument('--write',action='store_true'); opt.add_argument('--check',action='store_true')
    args=ap.parse_args(); data={}
    for p in sorted(packet_paths()):
        raw=p.read_bytes()
        if p.suffix=='.json':raw=raw.replace(b'\r\n',b'\n')
        data[p.relative_to(H).as_posix()]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    out=H/'ProofManifest.json'
    if args.write:
        out.write_text(json.dumps(data,indent=1)+'\n',encoding='utf-8',newline='\n')
    elif json.loads(out.read_bytes())!=data:
        raise ValueError('proof files or registration differ from manifest')
    print(f'{len(data)} registered packets, {sum(x["bytes"] for x in data.values())} bytes')


if __name__=='__main__':main()
