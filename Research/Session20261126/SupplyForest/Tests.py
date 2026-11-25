"""Exact floor-sum microtests and adversarial packet mutations; pass Research as first arg outside tree."""
import sys,os,tempfile,random,json,gzip
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
H=Path(__file__).resolve().parent
spec=spec_from_file_location('vc',H/'VerifyCut.py');V=module_from_spec(spec);spec.loader.exec_module(V)
if not __debug__:raise RuntimeError('assertions required')
rng=random.Random(2889)
for _ in range(4096):
 n=rng.randrange(50);m=rng.randrange(1,70);a=rng.randrange(-100,101);b=rng.randrange(-100,101);assert V.floors(n,m,a,b)==sum((a*i+b)//m for i in range(n))
# C=13*7, Y=7: q=13 (admissible class), C=9*7, Y=5: q=9 (even composites must not be assumed absent).
for C,Y in [(13*3,7),(9*7,5),(21*17,11)]:
 try:V.internal(C,Y)
 except AssertionError:pass
 else:raise AssertionError('true modulus hit disappeared')
base=H/'Cut19x660.json.gz';orig=base.read_bytes()
with tempfile.TemporaryDirectory() as folder:
 def reject(mut,name):
  packet=json.loads(gzip.decompress(orig));mut(packet);f=Path(folder)/'bad.json.gz';f.write_bytes(gzip.compress(json.dumps(packet).encode()));
  try:V.verify(f)
  except (AssertionError,ValueError,KeyError):return
  raise AssertionError(name+' was accepted')
 reject(lambda d:d['row'].__setitem__('rough',3),'remove essential roughness')
 reject(lambda d:d['row'].__setitem__('weighted',False),'remove mixed ledger')
 reject(lambda d:d['row'].__setitem__('cut',0),'missing s=0')
 reject(lambda d:d['row']['owners'].append(d['row']['owners'][0]),'double ownership')
 reject(lambda d:next(iter(d['ecpp'].values()))[0].__setitem__(0,15),'broken ECPP')
print('PASS 4096 signed floor sums, 3 true rectangle hits, 5 corrupted packets rejected')
