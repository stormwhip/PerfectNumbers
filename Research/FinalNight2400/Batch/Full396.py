"""Complete canonical (11,396); check packet disjointness and all source prices in one interpreter."""
from pathlib import Path
import sys,importlib.util,runpy
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Hybrid

def load(name):
    sp=importlib.util.spec_from_file_location('batch_'+name,H/(name+'.py'));v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);return v

if __name__=='__main__':
    assert __debug__
    import json
    G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());ks=json.loads((G/'KeyToShards.json').read_bytes())
    assert [(s,k) for s,k in sh.items() if [11,396] in k]==[('P11_I00076',[[11,396]])] and ks['11,396']==['P11_I00076']
    high,rest=load('Verify').run();assert high==list(range(150,233,2)) and rest==list(range(2,150,2))
    missing=load('Low').verify();ordinary=set(rest)-missing
    from TwoTrees import replay
    split=[{112,136},{36,70,78,82},{22}];mixed=[]
    for name,exps in [('HybridFour',{96,106,126,138}),('HybridSmall',{4,6,12,24}),('HybridTwentySix',{26}),('HybridTwo',{2}),('HybridEight',{8})]:
        Hybrid.verify(name+'.json.gz',exps);mixed.append(exps)
    parts=[set(high),ordinary,*split,*mixed];assert len(set.union(*parts))==sum(map(len,parts))==116 and set.union(*parts)==set(range(2,233,2))
    print('FULL canonical 11^396; 42 + 56 + 7 + 4 + 4 + 1 + 1 + 1 = 116; raw tail 468',flush=True)
