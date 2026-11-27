"""Isolated, offline replay of a partial SECOND-pivot packet. No factor DB."""
import gzip,json,sys
from pathlib import Path
from math import gcd,prod
from functools import cache
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'Session20261126'))
from PivotCheck import B,C,exact_leaf,floor10

def main():
    assert __debug__;p,e,t,r=19,282,1735317810514627,8383027
    pack=json.loads(gzip.decompress((P/'Packet282.json.gz').read_bytes()));assert set(pack)=={'cases','ecpp'}
    used=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2;y=z
        if z>=2**64:
            used.add(str(z))
            for row in pack['ecpp'][str(z)]:assert row[0]==y;y=C.pc.level(*row)
        assert C.pc.prime64(y);return True
    assert all(prime(z) for z in (p,t,r));assert C.valuation(C.sigma(p,e),t)==1
    prefix=[(p,e),(t,10)];s=C.State(prefix);assert not s.conflict and C.valuation(s.D,r)==1
    domain=[]; h=1;cases={int(k):v for k,v in pack['cases'].items()};floors={}
    assert set(map(str,cases))==set(pack['cases']) and cases
    while s.base//r*r**h<=B:
        if s.possible(r,h,1):
            rows=prefix+[(r,h)];child=C.State(rows)
            if not child.conflict and child.base<=B and prod(C.sigma(z,k) for z,k in rows)<=2*child.X:
                domain.append(h)
                if h in cases:
                    node=cases[h];assert set(node)=={'roots','owners','head'};k,o,H=node['roots'],node['owners'],node['head'];C.validate_forest(child,k,o,H,prime)
                    x=C.Forest(child,k,o,H).lower()[0];y=exact_leaf(rows,k,o,H);assert min(x,y)>B;floors[h]=floor10(min(x,y))
        h+=1
    assert domain==list(range(2,101,2)) and set(cases)<=set(domain) and set(pack['ecpp'])==used
    print('19^282, t^10: r=8383027; original secondary domain',domain,'size tail',h,'closed',sorted(floors),'remaining',sorted(set(domain)-set(cases)),'min decimal floor',min(floors.values()),'ECPP',len(used),flush=True)
if __name__=='__main__':main()
