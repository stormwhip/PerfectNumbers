"""Check rational inequalities in two entire root-11 exponent families. No dependency on the target size or root order."""
from fractions import Fraction

def I(p,e):return Fraction(p**(e+1)-1,(p-1)*p**e)
if __name__=='__main__':
    # For a putative odd perfect N with 11^e||N, 11 not Euler, 5|sigma when 5|e+1; 5²|sigma if 25|e+1 (LTE). If 7|e+1 then 43|sigma because ord_43(11)=7.
    # Assuming 3|N, its exponent is even. If exactly 2, 13|sigma(3²); else it is >=4. Component abundancies increase with actual exponent. If 35|e+1, 43 is never Euler, so exponent >=2.
    if pow(11,7,43)!=1 or 11%43==1 or ((3**3-1)//2)%13 or ((11**25-1)//10)%25:raise ArithmeticError('small exact divisors')
    common=I(11,4)*I(3,2)*I(5,1)*I(13,1)
    a=I(11,4)*I(3,4)*I(5,2); b=I(11,4)*I(3,4)*I(5,1)*I(43,2)
    for name,v in [('v3=2',common),('v3>=4,25|e+1',a),('v3>=4,35|e+1',b)]:
        if v<=2:raise ArithmeticError(name)
        print(name,v,'>2')
    print('If 25 or 35 divides e+1 then 11^e||N forces 3 not dividing N; no unconditional shard claimed.')
