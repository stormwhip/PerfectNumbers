"""Release-only regressions: no cache, external binary, or third-party library."""
from pathlib import Path
import gzip,json,unittest,sys
from copy import deepcopy
sys.path.insert(0,str(Path(__file__).resolve().parent))
import VerifyOrderSupply as v

class TestOrder(unittest.TestCase):
    def test_ecc_corruption(self):
        with gzip.open(v.H/'OrderPrimeProofs.json.gz','rt',encoding='utf-8') as f:proofs=json.load(f)
        r=min(map(int,proofs)); c=proofs[str(r)];v.verify_cert(r,c)
        for name,mutate in [('root',lambda x:x[0].__setitem__(0,r+2)),('trace',lambda x:x[0].__setitem__(1,0)),('cofactor',lambda x:x[0].__setitem__(2,0)),('point',lambda x:x[0].__setitem__(4,[0,0]))]:
            d=deepcopy(c);mutate(d)
            with self.subTest(name=name),self.assertRaises(ValueError):v.verify_cert(r,d)
        with self.assertRaises(ValueError):v.verify_cert(341,None)
    def test_progressions(self):
        for p in v.roots:
            for s in (1,2):
                y=p**s
                for n in range(1,900):
                    for lo,hi in [(2,n),(2*y,4*y),(max(2,2*y-3),2*y+1)]:
                        if any(n%q==0 for q in range(2*y-1,hi+1,4*y) if lo<=q):self.assertTrue(v.possible_factor(n,s,y,lo,hi))
    def test_forbidden_price(self):
        for p in v.roots:
            k=v.tb.kappa(p)
            for r in (3,5,7,11,13,17,29,31):
                if r==p:continue
                for c in (1,3,7):
                    lo=v.price(p,k,r,c)
                    for f in range(c+c%2,34,2):
                        z=v.tb.sigma(r,f)
                        if not any(z%t==0 for t in v.tb.forbidden(p)):self.assertLessEqual(lo,v.Fraction(r**f,p**(k*v.G.val(z,p))))
    def test_at_least_two_actual_exponents(self):
        stored=json.loads((v.H/'Audit.json').read_text());self.assertTrue(any(len(es)>1 for _,p,es in stored['closed']))
        self.assertEqual(len({(p,e) for p,e in stored['new']}),len(stored['new']))
    def test_the_small_case_stays_open(self):
        self.assertIsNone(v.independent_chain(7,2,[]));self.assertFalse(v.pair_rule(7,2,[],[]))

if __name__=='__main__':unittest.main()
