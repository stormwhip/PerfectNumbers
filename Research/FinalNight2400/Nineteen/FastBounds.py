"""Provably rounded logarithm via bit truncation; exact fallback on boundary."""
from functools import cache
# Return exactly floor(512 log2 n), avoiding raising a multi-kilobit n to the 512th power.
@cache
def scaled(n):
    assert n>0
    k=max(0,n.bit_length()-24)
    if not k:return (n**512).bit_length()-1
    m=n>>k
    lo=(m**512).bit_length()-1
    hi=(((m+1)**512)-1).bit_length()-1
    if lo==hi:return 512*k+lo
    # Rare ambiguity: more leading bits then exact fallback.
    j=max(0,n.bit_length()-64);u=n>>j
    a=(u**512).bit_length()-1;b=(((u+1)**512)-1).bit_length()-1
    return 512*j+a if a==b else (n**512).bit_length()-1
