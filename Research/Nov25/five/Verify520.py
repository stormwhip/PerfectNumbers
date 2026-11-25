"""Complete root-5 exponent 520 exclusion: exact root leaves plus terminal dual."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from functools import cache
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Early520 import verify as early, E, S0
from Late520 import verify as late, SCALE, E as LateE, S0 as LateS0


@cache
def decimal_logs(n,d=1):
    # Decimal.ln is correctly rounded in ROUND_HALF_EVEN. Enclose numerator
    # and denominator separately before directed subtraction and rescaling.
    with localcontext() as ctx:
        ctx.prec=80
        a=Decimal(n).ln(); b=Decimal(d).ln()
        low_n,low_d=a.next_minus(),b.next_plus()
        high_n,high_d=a.next_plus(),b.next_minus()
        ctx.rounding=ROUND_FLOOR
        lo=((low_n-low_d)*SCALE).to_integral_value()
        ctx.rounding=ROUND_CEILING
        hi=((high_n-high_d)*SCALE).to_integral_value()
    return int(lo),int(hi)


def verify(verbose=False):
    if not __debug__:
        raise ValueError('requires assertions; no -O')
    assert (E,S0)==(LateE,LateS0)
    early(verbose=verbose)
    late(verbose=verbose)
    # Independent high-precision directed arithmetic, with common input table
    # assembly and previously checked archive/Pocklington validation.
    late(verbose=verbose,logs=decimal_logs,verify_all=False)
    return {(5,E)}


if __name__=='__main__':
    verify(verbose=True)
