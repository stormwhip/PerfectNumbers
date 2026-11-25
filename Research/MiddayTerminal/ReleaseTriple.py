"""Fully universal 3/5/11 hitting theorem, conditional only on N<=10^2400.
Offline independent replay; numbers count support theorems, not canonical shards.
"""
import sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from AuditLarge import check

def main():
 if not __debug__:raise SystemExit('Do not use -O')
 a=sys.argv[1:];assert a in ([],['--baseline'],['--only-new'])
 if a!=['--only-new']:subprocess.run([sys.executable,'-I','-S','-B',str(H/'ReleaseAlternates.py'),*a],check=True)
 d,b=check('PackNewLocalTriple.json.gz');assert d['extra']==[3,5,11] and d['x']==[] and d['lower']==[[q,1] for q in (7,13,17,19,23)] and not d.get('parity',False) and b==2511
 print('For odd perfect N <= 10^2400, absence of 3,5,11 forces 7,13,17,19,23 by the preceding support theorems, contradicting this packet. PROVED hitting set {3,5,11}; combined with {3,5,7}, absence of 3 and 5 forces BOTH 7 and 11. Canonical exact-exponent/shard credit: 0/0.',flush=True)
if __name__=='__main__':main()
