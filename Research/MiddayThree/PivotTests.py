"""Negative coverage checks on registered proof data; no temporary files.
Syntactic tampering must not benefit from the ECPP cache used on nearby leaves.
"""
import sys,json,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from IndependentForest import checkdata
from Forest import measure

def test():
 data=json.loads(gzip.decompress((H/'Forest342.json.gz').read_bytes()));n=checkdata(data);m=measure(data['row'],data['ecpp'])[0];assert n==m
 q=next(iter(data['ecpp']));v=data['ecpp'][q][0][0];data['ecpp'][q][0][0]=v+2
 for fn in (lambda:checkdata(data),lambda:measure(data['row'],data['ecpp'])):
  try:fn()
  except ValueError:continue
  raise AssertionError('mutated chain accepted under warmed cache')
 data['ecpp'][q][0][0]=v;data['row']['edges'].append(data['row']['edges'][0]);
 try:checkdata(data)
 except ValueError:pass
 else:raise AssertionError('duplicate owner')
 print('PASS tamper: elliptic-chain binding after cache warming (both); duplicate owner')
if __name__=='__main__':test()
