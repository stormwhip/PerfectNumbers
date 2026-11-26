"""Fail-closed regression tests using the small archived conditional packet."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from Verify130 import H, PIVOT, replay


def reject(d, mutation):
    bad = deepcopy(d)
    mutation(bad)
    try:
        replay(bad)
    except (AssertionError, ValueError, KeyError):
        return
    raise AssertionError('corrupted certificate accepted')


def main():
    x = json.loads(gzip.decompress((H/'Conditional7x130-128910.json.gz').read_bytes()))
    r = replay(x)
    assert r['scope']=='CONDITIONAL_ONLY' and r['closed_fibers']==[1,2,8,9,10]
    assert r['open_paths']==[[(PIVOT,4)],[(PIVOT,6)]]
    assert set(r['partial_fibers'])=={4,6} and not set(r['closed_fibers']) & set(r['partial_fibers'])
    for f in r['partial_fibers']:
        assert r['partial_fibers'][f]==dict(open_paths=[[(PIVOT,f)]],excluded_leaves=[])
    assert r['splits'][0]['tail']==21
    reject(x,lambda d:d['tree']['cases'].pop('4'))
    reject(x,lambda d:d['tree']['cases'].__setitem__('21',{'type':'open'}))
    reject(x,lambda d:d['tree'].__setitem__('q',PIVOT+2))
    reject(x,lambda d:d['tree']['cases'].__setitem__('4',{'type':'forest','roots':[],'owners':[],'head':64}))
    reject(x,lambda d:d['ecpp'][str(PIVOT)][0].__setitem__(0,PIVOT+2))
    reject(x,lambda d:d['ecpp'].__setitem__('17',[]))
    print('PASS conditional accounting and six negative mutations')


if __name__=='__main__':main()
