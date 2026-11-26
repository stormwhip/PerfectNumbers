"""Portable frontend for exact masked-forest certificates. --repo PATH. Packages need ForestMasks.py, selected .json.gz packet and the public RootFiveNext prime checker."""
from pathlib import Path
import os,sys,argparse
assert __debug__;H=Path(__file__).resolve().parent;cli=argparse.ArgumentParser();cli.add_argument('packet',type=Path,nargs='+');cli.add_argument('--repo',type=Path,default=H.parent/'sprint');a=cli.parse_args();os.environ['OPN_REPO']=str(a.repo.resolve());sys.path.insert(0,str(H));from ForestMasks import verify
keys=set()
for f in a.packet:keys.update(verify(f))
print('PASS',len(keys),'conditional support triples',sorted(keys))
