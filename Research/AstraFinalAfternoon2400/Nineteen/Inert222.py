"""Self-contained integer certificate for two frozen root-222 deep cuts."""
from math import isqrt,prod,gcd
from functools import cache
from pathlib import Path
import json

B=10**2400
P,T,R,U,Q=19,7579985624053,3705121363,2032322226061,339512567

@cache
def prime(n):
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,isqrt(n)+1,2))

def sigma(p,h):return (p**(h+1)-1)//(p-1)

def vp(n,p):
    assert n>0 and p>1
    v=0
    while n%p==0:n//=p;v+=1
    return v

def main():
    assert __debug__
    assert 3**5030<=B<3**5031
    assert all(prime(p) for p in [P,T,R,U,Q])
    z=json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))
    assert z['frozen']=='495c59f55456a70994ce7848487e0c4e262c1984'
    assert (z['B_power10'],z['order_cap'],z['obstruction_prime'],z['q_minus_one'])==(2400,5031,Q,Q-1)
    a=sigma(P,222); b=sigma(T,2); c=sigma(U,1)
    assert a%(T*R)==z['root_sigma_mod_t_times_r']==0 and b%U==z['t_sigma_mod_u']==0 and c%(2*Q)==0
    assert T%2==1 and U%4==1 and Q not in (P,T,R,U)
    assert Q>5031 and all((Q-1)%d for d in range(3,5032,2))
    assert len(z['cases'])==2
    for g,w in zip((16,22),z['cases']):
        assert w['prefix']==[[P,222],[T,2],[R,g],[U,1]]
        assert w['frozen_deep_pivot_exponents']==[1,2,4,18,28] and w['remaining_deep_pivot_exponents']==[2,4,18,28]
        X=P**222*T**2*R**g*U
        parts=[a,b,sigma(R,g),c//2]; S=prod(parts)
        assert [d%Q**2 for d in parts]==w['individual_odd_sigma_mod_q2']
        assert S%Q**2==w['odd_sigma_product_mod_q2']
        assert S%2==1 and vp(S,Q)==w['incoming_valuation']==1
        assert all(vp(S,p)<=h for p,h in [(P,222),(T,2),(R,g),(U,1)])
        D=S//gcd(X,S)
        assert gcd(X,D)==1 and X*D<=B and S<=X
        print(f'PASS [19^222,{T}^2,{R}^{g},{U}^1]: v_{Q}(S)=1; all external sources impossible')

if __name__=='__main__':main()
