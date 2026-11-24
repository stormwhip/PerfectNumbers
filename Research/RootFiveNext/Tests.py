"""Boundary and adversarial checks; no network or third-party package."""
from copy import deepcopy
from itertools import product
from math import prod
import json
from Tree import F,PR,cost,minf,ok
from LeafCheck import valuation
from DualTree import units
from PrimeCheck import prime64,level,H,check

def must_reject(fn):
 try:fn()
 except (ValueError,ZeroDivisionError,TypeError):return
 raise AssertionError('corrupt proof was accepted')

def main():
 n=0
 for p,f in product(PR[:80],range(1,100)):
  if f%2 and (p%4!=1 or f%4!=1):continue
  s=(p**(f+1)-1)//(p-1);check(ok(p,f)==all(s%v for v in F),'forbidden');v=0
  while not s%5:s//=5;v+=1
  check(v==units(p,f)==valuation(p,f),'LTE round trip');n+=1
 for eu in (False,True):
  for triple in ([17,23,29],[37,41,47],[53,59,61]):
   cs=dict(zip(triple,[1,2,3])); price,_=cost(cs,eu);m=None
   opts=[[f for f in range(c,26) if (not f%2 or (not eu and f%4==p%4==1)) and ok(p,f)] for p,c in cs.items()]
   for fs in product(*opts):
    if sum(f%2 for f in fs)>1:continue
    t=prod(p**f for p,f in zip(cs,fs));m=min(m or t,t)
   check(m==price,'one-Euler cost')
 for x in [1,9,25,2047,3215031751,341550071728321,3825123056546413051,2**64+13]:check(not prime64(x),'fake 64-bit prime')
 rows=next(iter(json.loads((H/'RootFiveCertificate.json').read_text())['ecpp'].values()));row=rows[0];q=level(*row);check(q==(row[0]+1-row[1])//row[2],'corrupt factor'); r=deepcopy(row);r[2]=0;must_reject(lambda:level(*r));r=deepcopy(row);r[3]=0;r[4]=[0,0];must_reject(lambda:level(*r));r=deepcopy(row);r[1]=r[0];must_reject(lambda:level(*r));print('passed',n,'sigma/LTE comparisons, six parity oracles, eight composite/range checks and three corrupted ECPP levels')
if __name__=='__main__':main()
