import json,gzip,sys,tempfile
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
H=Path(__file__).resolve().parent
sp=spec_from_file_location('v',H/'VerifyBranch.py');v=module_from_spec(sp);sp.loader.exec_module(v)
if not __debug__:raise RuntimeError('assertions mandatory')
f=H/'Branch7x928.json.gz'
with tempfile.TemporaryDirectory() as td:
 def check(fn):
  p=json.loads(gzip.decompress(f.read_bytes()));fn(p);bad=Path(td)/'bad.json.gz';bad.write_bytes(gzip.compress(json.dumps(p).encode()))
  try:v.verify(bad)
  except (AssertionError,ValueError,KeyError):return
  raise RuntimeError('forgery accepted')
 check(lambda p:p['rows'].pop(0));check(lambda p:p['rows'].append(p['rows'][0]));check(lambda p:p['seed'].__setitem__(2,5));check(lambda p:p['rows'][0]['owners'].extend(p['rows'][0]['owners'][:1]));check(lambda p:next(iter(p['ecpp'].values()))[0].__setitem__(0,9))
print('PASS 5 negative controls: missing and duplicate exact exponent, false pivot, duplicate owner, broken prime chain')
