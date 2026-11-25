"""Standalone entry point: cold-verify all six numeric packets; close each Boolean theorem.
Dependency: the published [3,5,7] theorem. --baseline independently cold replays that too.
Uses only published archives / deterministic arithmetic, no nomination database, LP or scorer.
"""
import json,gzip,sys,hashlib,itertools,argparse,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(H));from Audit import replay,W,logs,split,primeproduct,chunks
from Common import bank

def cases():
 common=[3,5,11,13];Q=[17,19,23]
 for a,b in itertools.combinations(Q,2):
  no=common+[a,b];yield 'Cut-0-0-'+'-'.join(map(str,no))+'.json.gz',no,[],{(17,19):2524,(17,23):2457,(19,23):2438}[a,b]
 for a in Q:yield f'New-Drop{a}.json.gz',common+[a],[7,*[b for b in Q if b!=a]],{17:2459,19:2462,23:2426}[a]

def main():
 if not __debug__:raise SystemExit('Do not use -O')
 ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
 if args.baseline:
  subprocess.run([sys.executable,'-I','-S','-B',str(R/'NightUniform/ThreeHittingWitness.py'),str(R/'NightUniform/ThreeAvoid.json')],check=True,cwd=R.parent)
 print('Prior: published {3,5,7} hitting theorem. Optional bases:',len(bank()),flush=True);cuts=[({3,5,7},set())];u=W*logs(10)[1]
 for fn,no,yes,expected in cases():
  raw=(H/fn).read_bytes();d=json.loads(gzip.decompress(raw));assert d['root']==d['e']==0 and d['x']==[] and d['extra']==no and d['lower']==[[p,1] for p in yes];b,*_=replay(**d);assert b>2400*u and b//u==expected;cuts.append((set(no),set(yes)));print(fn,hashlib.sha256(raw).hexdigest(),b//u,flush=True)
  # A previous varying base can otherwise occupy large caches. Numeric logs shared.
  split.cache_clear();primeproduct.cache_clear();chunks.cache_clear()
 U=sorted(set.union(*[no|yes for no,yes in cuts]));remaining=[]
 for bits in itertools.product((0,1),repeat=len(U)):
  active={p for p,b in zip(U,bits) if b}
  if not any(not (no&active) and yes<=active for no,yes in cuts):remaining.append(active)
 for p in (17,19,23):
  hit={3,5,11,13,p};assert all(active&hit for active in remaining);print('PROVED hitting set',sorted(hit),flush=True)
 assert all(not ({3,5,11,13}.isdisjoint(active)) or {7,17,19,23}<=active for active in remaining);print('Corollary: absent 3,5,11,13 => present 7,17,19,23. Complete exponents/shards credited: 0/0.',flush=True)
if __name__=='__main__':main()
