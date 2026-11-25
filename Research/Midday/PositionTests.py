"""Offline structural regression tests for position/support covers; no solver, no network."""
from pathlib import Path
import sys,json,gzip,copy
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import ModeCheck as M

def reject(fn):
    try:fn()
    except (AssertionError,ValueError,KeyError,TypeError):return
    raise ValueError('corrupted packet accepted')

def main():
    raw=json.loads(gzip.decompress((H/'Euler7x700.json.gz').read_bytes()));p,e,f=M.replay(raw);assert (p,e)==(7,700) and len(f)==5
    # When a named exemption is lost from the manifest, it returns to the general
    # case. A sound checker must then fail, not silently retain the old ban.
    q=next(iter(raw['special']));omit=copy.deepcopy(raw);del omit['special'][q];reject(lambda:M.replay(omit))
    mis=copy.deepcopy(raw);mis['special'][q]['e']=702;reject(lambda:M.replay(mis))
    dup=copy.deepcopy(raw);dup['general']['owners']+=dup['general']['owners'][:1];reject(lambda:M.replay(dup))
    cert=copy.deepcopy(raw);k=next(iter(cert['ecpp']));cert['ecpp'][k]=[];reject(lambda:M.replay(cert))
    print('PASS four incompatible Euler-cover mutations and authentic reconstruction')
if __name__=='__main__':
    if not __debug__:raise SystemExit('no -O')
    main()
