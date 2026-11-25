"""Independent pure-integer forced-divisor leaf for the new 507-digit prime."""
from pathlib import Path
import sys,json,gzip
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'RootFiveNext'))
import PrimeCheck as PC
B=10**2400;BAD=(3,7,11,13,19,31)
def prime(p,rows):
 t=p
 for row in rows:
  if row[0]!=t:raise ValueError('unbound chain')
  t=PC.level(*row)
 if not PC.prime64(t):raise ValueError('chain tail')
def main():
 e=48;f=18;a=227376585863531112677002031251;s=(5**49-1)//4;assert s%a==0;roots=json.loads(gzip.decompress((H/'Seeds.json.gz').read_bytes()));prime(a,roots['ecpp'][str(a)]);extra=json.loads(gzip.decompress((H/'Extra48.json.gz').read_bytes()));p=max(map(int,extra));prime(p,extra[str(p)]);z=(a**19-1)//(a-1);assert z%p==0 and p%4==3
 blocked={h:[r for r in BAD if sum(pow(p,k,r) for k in range(h+1))%r==0] for h in [2,4]};assert all(blocked.values()) and 5**e*a**f*p**6>B
 print('EXCLUDED e=48, v_anchor=18; digits',len(str(p)),'ECPP links',len(extra[str(p)]),'blocked',blocked,'floor',len(str(5**e*a**f*p**6))-1)
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 main()
