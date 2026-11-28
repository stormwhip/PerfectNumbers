"""Separate exact direct progression and rough factor checks of the 3^12 tradeoff."""
from math import gcd,isqrt

p=398581;k=109;D=(p**k-1)//(p-1);X=3**12*797161*p**108
B=10**2400;U=120000000000

def sieve_candidates():
    # Construct one global CRT wheel of selected modulus classes, intersect
    # using exact cyclic multiplication; all discarded residues are impossible.
    allowed=[1];M=8*k;r=next(a for a in range(1,M+1,2*k) if a%8==D%8);allowed=[r]
    for q in (3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        R={x for x in range(q) if any(x*z*z%q==D%q for z in range(q))}
        ss=[]
        for a in allowed:
            for b in R:
                y=a+M*((b-a)*pow(M,-1,q)%q)
                if y<=U:ss.append(y)
        M*=q;allowed=ss
        if M>U:break
    count=0
    for a in sorted(set(allowed)):
        for r in range(a,U+1,M):
            count+=1
            assert D%r or isqrt(D//r)**2!=D//r,(r,M)
    return count,M

if __name__=='__main__':
    print('separate exact wheel',sieve_candidates(),flush=True)
