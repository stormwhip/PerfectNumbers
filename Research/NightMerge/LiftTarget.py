"""Fail-closed adapter: only a concrete integer bound above B for the claimed target counts."""
from pathlib import Path
import sys,json,gzip
R=Path(__file__).resolve().parents[1];H=R/'NightFiveReview/ForestLift';sys.path.insert(0,str(H));import Target as T

def main():
    if not __debug__:raise SystemExit('Run without -O')
    name,p,e=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);pack=json.loads(gzip.decompress((H/name).read_bytes()));found=[]
    for row in pack['rows']:
        if row['p']!=p or 'extra' in row:raise ValueError('incorrect ordinary root scope')
        found.extend(T.certify(row,pack['ecpp'],[e]))
    if not found or any(v[0]!=e for v in found):raise ValueError('target not excluded')
    print('PASS exact rooted seed extension',p,found,flush=True)
if __name__=='__main__':main()
