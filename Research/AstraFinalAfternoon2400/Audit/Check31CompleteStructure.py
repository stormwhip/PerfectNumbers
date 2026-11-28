"""Independent structural union/domain check for the proposed complete (31,6) packet."""
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import split
from Check31FixedPrice import A
from Check31Joint6 import ROW
D=H.parent/'ThirtyOne'
HASH={'Certificate6Extended.json.gz':'e423c40be321fc55b3033669bce8944f782ee6574cf1fdb776ba48a82baa7f79',
      'Certificate6First72.json.gz':'187675038b42ee59cce728fb8d5871e0d46af2eb898304c40ec684bb1da8d352',
      'Certificate6CompleteJoined.json.gz':'450a80c01c74b098fb858f340c17f4b3be674da4d6cbf8894080e0b5099f3130'}


def read(name):
    raw=(D/name).read_bytes()
    assert sha256(raw).hexdigest()==HASH[name]
    return json.loads(gzip.decompress(raw))


def main():
    assert __debug__
    old,first,current=map(read,HASH)
    assert all((r['e'],r['pivot'])==(6,ROW[1][0]) for r in (old,first,current))
    root,tail=split(((31,6),),ROW[1][0])
    assert len(root)==53 and tail==267
    assert all(d['cases'].keys()=={str(f) for f in root} for d in (old,first,current))
    assert [int(k) for k,v in old['cases'].items() if v is None]==[72]
    assert [int(k) for k,v in first['cases'].items() if v is not None]==[72]
    assert all(v==current['cases'][str(k)] for k,v in old['cases'].items() if k!='72')
    assert current['ecpp'].keys()==old['ecpp'].keys()|first['ecpp'].keys()
    counter=Counter(); tails=Counter()
    def visit(pref,n):
        assert n is not None,pref
        kind=n['type']; counter[kind]+=1
        if kind=='forest':
            assert n.keys()=={'type','roots','owners','head'}
        elif kind=='price6':
            assert pref==A
        elif kind=='joint6':
            assert pref==ROW
        else:
            assert kind=='split' and n.keys()=={'type','q','cases'}
            branches,raw=split(pref,n['q'])
            tails[raw]+=1
            assert n['cases'].keys()=={str(f) for f in branches}
            for f,m in branches.items():
                visit(m,n['cases'][str(f)])
    for f,pref in root.items():
        visit(pref,current['cases'][str(f)])
    assert counter=={'forest':1839,'split':47,'price6':1,'joint6':1}
    print('PASS frozen structural union',len(root),'firsts / raw tail',tail,'leaves',counter,
          '| ECPP subjects',len(current['ecpp']), '| nested tail range',(min(tails),max(tails)),flush=True)


if __name__=='__main__':
    main()
