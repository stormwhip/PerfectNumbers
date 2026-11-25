"""Cheap unit regressions for the simultaneous-output terminal's proof boundary."""
import sys,gzip,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import Joint as J, Audit as A

def reject(fn):
 try:fn()
 except (ValueError,AssertionError,KeyError):return
 raise AssertionError('invalid input accepted')
def main():
 if not __debug__:raise SystemExit('run without -O')
 # Identical output prime is charged with full multiplicity, not only its lcm.
 assert J.sigma(5,2)%31==0 and J.sigma(67,2)%31==0
 # Alternative: 67=5 mod31; two distinct emitters require 31^2 in their joint output.
 z=J.sigma(5,2)*J.sigma(67,2);assert z%961==0
 # Same sink, separate supports, and raw cofactors retaining multiplicity.
 vals=(3,5,7,13,17,19);n=5**7*17*23**3*37
 u,out=A.split(n,vals);assert u==23**3*37 and dict(out)=={5:7,17:1};assert sorted(J.divisors(n,J.tree(vals)))==[5,17]
 fake=2**65+7
 for bank,fn in ((J.data(),J.prime),(A.nominated(),A.trusted)):
  bank['ecpp'][str(fake)]=[];reject(lambda:fn(fake));bank['ecpp'][str(fake)]=[[fake+2,0,1,0,[1,1]]];reject(lambda:fn(fake));del bank['ecpp'][str(fake)]
 assert not J.prime64(2**64) and not J.prime64(1)
 toy=([J.S,J.S],[([(1,-J.S)],0)],{3:[(0,2,True)]},[1]);assert J.weighted(toy,[])==0;reject(lambda:J.weighted(toy,[[0,-1]]));reject(lambda:J.weighted(toy,[[0,J.W+1]]));reject(lambda:J.weighted(toy,[[0,1],[0,1]]))
 frozen=json.loads(gzip.decompress((H/'Accepted.json.gz').read_bytes()));assert [r['e'] for r in frozen]==[6,10,12,16,18,22,28,30,40,42,46,48,52,70];print('PASS shared multiplicity, explicit/rough split, missing/broken ECPP, 64-bit endpoints, malformed weights, excluded unpriced tail, 14 distinct actuals')
if __name__=='__main__':main()
