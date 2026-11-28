"""Independent exact sibling/terminal binding for the last (7,438) second fiber."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckSevenForestDomains import split,exact_state
from Check438TwelveMixed import P, MOD,Q,r

piv=752487193
q=50047294070406095227
P0=P+[(r,2)]


def unpack(path,h=None):
    b=(H.parent/path).read_bytes()
    if h is not None: assert sha256(b).hexdigest()==h
    return json.loads(gzip.decompress(b))


def main():
    assert __debug__
    provenance={}
    for tag,hset in (('sub2',{tuple(sorted(P0+[(piv,22),(q,2)]))}),
                     ('price2',{tuple(sorted(P0+[(piv,22),(q,h)])) for h in (10,12)}),
                     ('high2',{tuple(sorted(P0+[(piv,h)])) for h in (46,52)})):
        payload=unpack(f'Propagation/Reserved438x12-{tag}.json.gz')
        actual={tuple(sorted(map(tuple,rec['P']))) for rec in payload['records']}
        assert hset<=actual and not set(provenance)&hset
        for prefix in hset:provenance[prefix]=tag
    packet=unpack('Seven/Forest438t12c.json.gz','2b91c8fbec62e32877df92a3a87e8ab738307203a8049f70693466554dc8d724')
    assert len(packet['records'])==1
    rec=packet['records'][0]; assert list(map(tuple,rec['P']))==P0 and rec['bad']==[19] and not rec['unresolved']
    checked={};found={str(T) for T,h in P0 if T>=2**64}; forest=0; splits=0
    def walk(rows,node):
        nonlocal forest,splits
        x,s,m=exact_state(rows,{19}); assert m and x and s
        assert all(h%2==0 and p%MOD!=Q for p,h in rows)
        kind=node['type']
        if kind=='delegated':
            key=tuple(sorted(rows)); assert key in provenance and key not in checked
            checked[key]=provenance[key]; return
        if kind=='split-q1':
            p=node['q']; assert p%MOD!=Q
            if p>=2**64:found.add(str(p))
            subs,tail=split(rows,{19},p)
            evens={h:rr for h,rr in subs.items() if not h%2}
            assert evens.keys()==set(map(int,node['cases']))
            splits+=1
            for h,rr in evens.items():walk(rr,node['cases'][str(h)])
            return
        assert kind=='reserve';forest+=1
        roots=set(node['roots']); owners=dict(node['owners']); V=roots|owners.keys()
        assert len(V)==len(node['roots'])+len(node['owners']) and all(z%MOD!=Q for z in V)
        assert all(m%z==0 for z in roots) and all(m%z!=0 for z in owners)
        assert all(z not in dict(rows) and z!=19 for z in V)
        found.update(str(z) for z in V if z>=2**64)
        for z in owners:
            vis=set()
            while z not in roots:
                assert z in owners and z not in vis
                vis.add(z);z=owners[z]
    walk(P0,rec['tree'])
    assert checked==provenance and splits==4 and forest==48
    assert found==packet['ecpp'].keys() and len(found)==859
    print('PASS exact final h2 domain: 4 splits, 48 strict-forest scopes, 5 coordinate-identical delegates, 859 reached ECPP labels')

if __name__=='__main__':main()
