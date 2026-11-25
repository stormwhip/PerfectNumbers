"""Small fail-closed tests; no external cache or optimizer."""
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Replay import proof
from SupportRules import rules
from IndependentTerminal import run


def rejected(call,name):
    try:
        call()
    except (ValueError,KeyError):
        return
    raise AssertionError(name+' should be rejected')


def main():
    assert rules(10)==rules(54)==rules(76)==(2092943,2052296,2045072)
    rejected(lambda:rules(12),'wrong seed class')
    P=H/'Branches/T13x10Mask0F0.json.gz'
    x=json.loads(gzip.decompress(P.read_bytes()))
    rejected(lambda:proof(x),'conditional packet submitted as a complete pair')
    weak={**x,'leaf':{**x['leaf'],'weights':[]}}
    rejected(lambda:proof(weak,conditional=True),'empty terminal dual')
    rejected(lambda:run(weak),'empty independent terminal dual')
    corrupt={**x,'leaf':{**x['leaf'],'edges':[*x['leaf']['edges'],x['leaf']['edges'][0]]}}
    rejected(lambda:proof(corrupt,conditional=True),'duplicate source target')
    rejected(lambda:run(corrupt),'duplicate independent source target')
    from Compose import State,valuation
    q=150332843;s=State([(31,10)],(5,),(3,13,17));v=valuation(s.D,q)
    assert v==1 and [f for f in range(1,22) if s.possible(q,f,v)]==[2,4,6,12,14,16,18,20]
    incomplete={'p':31,'e':10,'ecpp':{},'tree':{'kind':'exp','q':q,'cut':2,'cells':{},'tail':{'kind':'direct'}}}
    rejected(lambda:proof(incomplete),'missing finite exact split cell')
    print('PASS support lifts, first-anchor head, and fail-closed negative controls')

if __name__=='__main__':main()
