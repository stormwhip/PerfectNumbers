"""Exact branch-aware outgoing forest; stdlib only. See README for accounting."""
from functools import cache
from math import gcd, prod
from pathlib import Path
import sys

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R/'NightLowRoute/Release'))
from ForestReplay import B, R as ORDER, pc, sigma, valuation, nonsupport
sys.path.remove(str(R/'NightLowRoute/Release'))


def need(value, msg):
    if not value:
        raise ValueError(msg)


def permitted(q, f, bad):
    return all((f+1)%b if q%b==1 else pow(q,f+1,b)!=1 for b in bad)


def euler(q, bad):
    return q%4==1 and all((q+1)%b for b in bad)


def sig_odd(q, f):
    return sigma(q, f)//(2 if f%2 else 1)


class State:
    """All exact components in rows are distinct; p^e is exact, even."""
    def __init__(self, rows, present=(), absent=(), lo=None):
        self.rows = dict(rows)
        self.p, self.e = rows[0]
        self.present = frozenset(present)
        self.bad = tuple(ORDER[:ORDER.index(self.p)]) + tuple(absent)
        self.lo = {} if lo is None else dict(lo)
        self.fixed_euler = any(f%2 for q,f in rows)
        self.X = prod(q**f for q,f in rows)
        self.S = prod(sig_odd(q,f) for q,f in rows)
        self.D = nonsupport(self.S, prod(self.rows))
        self.base = self.X*self.D
        self.conflict = (sum(f%2 for q,f in rows)>1 or
                         any(f%2 and (q%4!=1 or f%4!=1) for q,f in rows) or
                         gcd(self.S*prod(self.rows)*prod(present), prod(self.bad))>1 or
                         any(self.S%q**(f+1)==0 for q,f in rows))

    def possible(self, q, f, v):
        return (f>=v and f>=self.lo.get(q,1) and
                (not f%2 or not self.fixed_euler and f%4==1 and euler(q,self.bad)) and
                permitted(q,f,self.bad))


class Forest:
    """Raw integer proof for a validated forest and a fixed exact-prefix state."""
    def __init__(self, s, roots, owners, head, *, record=False):
        self.s = s
        self.roots = tuple(roots)
        self.owners = dict(owners)
        self.head = head
        K = set(roots)
        self.V = K | set(self.owners)
        self.c = {q:max(1,valuation(s.D,q),s.lo.get(q,0)) for q in roots}
        self.base = s.base//prod(q**valuation(s.D,q) for q in roots)
        self.U = s.X*s.D*prod(self.owners)*prod(set(s.present)-s.rows.keys())
        self.kids = {q:[] for q in self.V}
        for q,z in self.owners.items():
            self.kids[z].append(q)
        self.U2 = {q:prod(self.kids[q]) for q in self.V}
        self.memo = {}
        self.log = {} if record else None

    def node(self,z,h,m):
        # m=0 plain; m=1 optional Euler at z or descendants; m=2 at z;
        # m=3 optional Euler among descendants only.
        key = z,h,m
        if key in self.memo:
            return self.memo[key]
        if m==1:
            ms = ((0,False),) if self.s.fixed_euler else ((3,False),(2,True))
            result = min((self.node(z,h,k),k) for k,sp in ms if not sp or euler(z,self.s.bad))
            self.memo[key] = result[0]
            if self.log is not None:
                self.log[key] = result[1]
            return result[0]
        sp = m==2
        step = 4 if sp else 2
        f = h+((1-h)%4 if sp else h%2)
        best = B+1
        choice = None
        count = 0
        while count<self.head:
            size = z**f
            if size>=best:
                break
            if permitted(z,f,self.s.bad):
                count += 1
                S = sig_odd(z,f)
                C = nonsupport(S,self.U)
                value = size*C
                active = []
                marked = None
                live = gcd(S,self.U2[z])
                for q in self.kids[z] if live>1 else ():
                    if live%q:
                        continue
                    a = valuation(S,q)
                    full = self.node(q,a,0)
                    value *= full
                    active.append((q,a))
                    if m==3:
                        r = full-self.node(q,a,1)
                        if r>0 and marked is None:
                            marked=(q,a,full,r)
                        elif r>0 and r*marked[2]>marked[3]*full:
                            marked=(q,a,full,r)
                if marked is not None:
                    value //= marked[2]
                    value *= marked[2]-marked[3]
                if value<best:
                    best,choice=value,(f,C,active,marked)
            f += step
        # f need not itself be admissible to lower-bound the remaining tail.
        if z**f<best:
            best,choice = z**f,(f,0,[],None)
        self.memo[key] = best
        if self.log is not None:
            self.log[key] = choice
        return best

    def lower(self):
        vals = [self.node(z,h,0) for z,h in self.c.items()]
        w = self.base*prod(vals)
        mark = None
        b = w
        if not self.s.fixed_euler:
            for (z,h),c in zip(self.c.items(),vals):
                v = w//c*self.node(z,h,1)
                if v<b:
                    b,mark=v,z
        return b,mark

    def witness(self,marked):
        def walk(z,c,m):
            if m==1:
                m=self.log[z,c,m]
            f,C,kids,d=self.log[z,c,m]
            if f%2==0:
                assert m!=2
            yield z,f,C
            for q,h in kids:
                yield from walk(q,h,1 if d and q==d[0] else 0)
        for z,h in self.c.items():
            yield from walk(z,h,1 if z==marked else 0)


def validate_forest(s,roots,edges,head,prime):
    parents = dict(edges)
    K = set(roots)
    V = K | set(parents)
    need(type(head)==int and 1<=head<=1024,'head')
    need(len(parents)==len(edges) and len(K)==len(roots) and not K & set(parents),'duplicate')
    need(all(prime(q) and q not in s.rows and q not in s.bad for q in V),'prime/scope')
    need(all(s.D%q==0 or q in s.present for q in K),'root not compelled')
    need(all(q in K for q in s.lo),'tail must be rooted')
    need(all(s.D%q and q not in s.present and z in V for q,z in edges),'owner conflict')
    kids = {q:[] for q in V}
    for q,z in edges:
        kids[z].append(q)
    seen = set()
    queue = list(K)
    while queue:
        z=queue.pop()
        need(z not in seen,'repeated visit')
        seen.add(z)
        queue.extend(kids[z])
    need(seen==V,'unreachable node')
