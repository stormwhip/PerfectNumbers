"""One frozen dual, many complementary forbidden-prime scenarios."""
import json,gzip,sys
from pathlib import Path
from math import gcd,prod
H=Path(__file__).resolve().parents[2];D=H/'FinalSprint/Support'
sys.path.insert(0,str(H/'MiddayTerminal'))
import Audit,Common
base=json.load(gzip.open(H/'MiddayTerminal/PackNewTriple3513.json.gz'));Common.dataset=lambda:{'ecpp':base['ecpp'],'rows':{}}
bad,need,L,cut,add,w,old=json.loads((D/'Side1931.json').read_bytes());assert bad==[3,5,19,31] and need==[7,11,13,17]
required={*need,23,29,37,47}; ext={q:c for q,c in base['args']['extend'] if q not in bad};ext.update({q:max(c,ext.get(q,0)) for q,c in add})
_,V,pr=Common.init(0,0,bad,True);ps=sorted((set(Audit.primes(L))|V|set(pr)|set(ext)|set(need))-set(bad));stop=2+len(ps)+len(need)
w=[(i,a) for i,a in w if i<2 or i>=stop];u,r,G,_=Audit.replay(root=0,e=0,extra=bad,x=[],lower=need and [[p,1] for p in need],L=L,T=3*L,cut=cut,cap=cut,wide=True,extend=sorted(ext.items()),parity=True,weights=w);assert list(G)==ps
scale=Audit.W*Audit.logs(10)[1]
S=tuple(q for q in Audit.primes(180) if q not in required and q not in bad);P=prod(S)
# Build the small-prime obstruction mask once per column. An unbounded even tail
# is not removed for its nominal index; every odd tail emits q+1.
opts={}; refund=u
for q,g in G.items():
    refund-=min([0]+[r[i] for i,e,x in g]); col=[]
    for i,e,x in g:
        z=Audit.geom(q,e) if x else q+1 if e%2 else 1
        z=gcd(z,P); mask=sum(1<<j for j,b in enumerate(S) if z%b==0) if z>1 else 0
        col.append((r[i],mask,e%2))
    opts[q]=col

def score(banned):
    mask=sum(1<<S.index(b) for b in banned);v=refund;disc=0
    for q,col in opts.items():
        if q in banned:continue
        a=None if q in required else 0;o=None
        for c,m,k in col:
            if m&mask:continue
            if k:
                if o is None or c<o:o=c
            elif a is None or c<a:a=c
        assert a is not None
        v+=a
        if o is not None:disc=min(disc,o-a)
    return (v+disc)//scale

if __name__=='__main__':
    assert __debug__ and required<=set(G) and set(S)<=set(G)
    for row,bound in [((53,59),2403),((53,41,73),2411),((53,41,137),2412),((53,73,137),2410)]:
        assert score(row)==bound and bound>2400
        print('PASS absent',bad,'and',row,'lower floor',bound,flush=True)
