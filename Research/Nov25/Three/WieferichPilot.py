"""Optional literature-assisted sensitivity: not used in the standalone proof ledger."""
import argparse
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
import SourceUnit as S

# Dorais–Klyve (JIS 14 (2011), Art. 11.9.2), Other applications and The Computation.
# Use the exact product printed in the paper, then a conservatively strict bound.
CUTOFF=6469693230*150000
KNOWN=(11,1006003)


def run(e):
    a=S.E.sigma(3,e); m=e+1
    if not (S.E.mr(m) and all(a%r for r in KNOWN)):
        raise ValueError('not a prime-index block or known Wieferich exception divides A')
    low=S.strip_lower(a,m,4096); gift,_=S.free_levels(a,m,low)
    prices=S.reserve_items(a,e,low,(S.I.T+1)**2)
    cells,high=S.J.audit(e,[])
    if high or min(cells)<=0:
        raise ValueError('Euler branches remain')
    results=[]
    for s in sorted({min(cells),min(cells)+1,cells[len(cells)//2],max(cells)}):
        for tag in (1,2):
            q=S.euler_least(s,tag); old={}; new={}
            before=S.int_possible(a,e,s,tag,q,prices,gift,low,witness=old)
            # If r^2|A, then r^2|(3^m-1), m|r-1, hence r is base-3 Wieferich.
            after=S.int_possible(a,e,s,tag,q,prices,gift,low,repeat_lower=CUTOFF,witness=new)
            results.append(dict(s=s,tag=tag,before=before,after=after,old=old,new=new))
    return dict(e=e,repeat_lower=CUTOFF,source='Dorais–Klyve JIS 14 11.9.2',results=results)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',action='store_true');args=p.parse_args()
    rows=[run(1162),run(1108)]
    for row in rows:
        print(row['e'], 'possible before/after', sum(x['before'] for x in row['results']),
              sum(x['after'] for x in row['results']),flush=True)
    if args.out:
        (H/'WieferichPilot.json').write_text(json.dumps(rows,indent=1,ensure_ascii=False)+'\n',encoding='utf8')


if __name__=='__main__':
    main()
