"""Three independently sealed direct-forest packets cover the exact 30103 domain. No nested-109 candidate used."""
from pathlib import Path
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from VerifyFive import main
if __name__=='__main__':
 assert __debug__;seen=set();D=None
 for path in ['FiveAnchor.json.gz','FiveAdd.json.gz','FiveLast.json.gz']:
  z=json.load(gzip.open(H/path));xs=set(map(int,z['nodes']));assert not seen&xs
  dd=set(main(xs,path));assert D is None or D==dd;D=dd;seen|=xs
 assert set(seen)==D and len(D)==45 and 30 in seen
 print('PASS complete exact 173^5 under 7^12, Q^42: all 45 ordinary-anchor assignments and monotone size tail eliminated.')
