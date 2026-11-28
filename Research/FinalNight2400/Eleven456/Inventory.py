from pathlib import Path
import hashlib
H=Path(__file__).resolve().parent
for n in 'Full456.py Kernel.py Joint.py Aux6.py Forest.json.gz Primes.json.gz Proof.md'.split():
 b=(H/n).read_bytes();print(n,len(b),hashlib.sha256(b).hexdigest())
