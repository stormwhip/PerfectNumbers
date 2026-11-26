from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
import sys,json,gzip,tempfile
H=Path(__file__).resolve().parent;spec=spec_from_file_location('d',H/'Domain.py');d=module_from_spec(spec);spec.loader.exec_module(d)
assert __debug__
raw=(H/'Recursive7x856.json.gz').read_bytes()
with tempfile.TemporaryDirectory() as tmp:
 def reject(f):
  x=json.loads(gzip.decompress(raw));f(x);out=Path(tmp)/'broken.gz';out.write_bytes(gzip.compress(json.dumps(x).encode()));
  try:d.verify(out)
  except (AssertionError,KeyError,ValueError):pass
  else:raise AssertionError('invalid recursive packet accepted')
 reject(lambda x:x['states'].pop(''));reject(lambda x:x['states'].__setitem__('',5));reject(lambda x:x['states'].pop(str(x['states'][''])+':1'));reject(lambda x:x.__setitem__('seed',[9,856]));
print('PASS 4 corrupted recursive state/prime/exponent/seed packets rejected')
