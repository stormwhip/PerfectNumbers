"""Independent exact masked-forest recurrence."""
from functools import cache
from math import gcd,prod
from Verify import B,sig as sigma,val,trim

def legal(q,f,banned):return all(pow(q,f+1,b*(q-1))!=1 for b in banned)

def second(rows,need,banned,roots,edges,head):
    """Independent recurrence with states deriving ordinary and one optional Euler cost."""
    fixed=dict(rows); s=prod(sigma(q,f)//(1+f%2) for q,f in rows)
    d=trim(s,prod(fixed)); x=prod(q**f for q,f in rows)
    parent=dict(edges); kids={q:[] for q in (*roots,*parent)}
    for q,z in edges:kids[z].append(q)
    children_product={p:prod(zs) for p,zs in kids.items()}
    pool=x*d*prod(parent)*prod(set(need)-fixed.keys()); locked=any(f%2 for f in fixed.values())
    # Alternate arithmetic recognizes bans from a congruence, not Compose.permitted.
    @cache
    def allowed(p,f):return legal(p,f,banned)
    @cache
    def costs(q,h):
        even,flex= B+1,B+1
        for odd in (0,1):
            if odd and (locked or q%4!=1 or not allowed(q,1)):continue
            step=2+2*odd; f=h+((1-h)%4 if odd else h%2); remaining=head
            while remaining and q**f<(flex if odd else even):
                if allowed(q,f):
                    remaining-=1; z=sigma(q,f)//(1+odd)
                    common=gcd(z,children_product[q])
                    subs=[costs(p,val(z,p)) for p in kids[q] if common%p==0] if common>1 else []
                    n=q**f*trim(z,pool)*prod(a for a,_ in subs)
                    if not odd:
                        even=min(even,n);n=min([n]+[n//a*b for a,b in subs])
                    flex=min(flex,n)
                f+=step
            tail=q**f
            if not odd:even=min(even,tail)
            flex=min(flex,tail)
        return even,flex
    heights=[(q,val(d,q)) for q in roots];children=[costs(q,max(1,v)) for q,v in heights]
    n=x*(d//prod(q**v for q,v in heights))*prod(a for a,_ in children)
    return min([n]+[n//a*b for a,b in children])
