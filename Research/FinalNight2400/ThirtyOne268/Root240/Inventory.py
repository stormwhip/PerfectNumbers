from pathlib import Path
import hashlib
H=Path(__file__).resolve().parent
for f in 'Full240.py Kernel.py High82.py Forest.json.gz Primes.json.gz Proof.md'.split():
 b=(H/f).read_bytes();print(f,len(b),hashlib.sha256(b).hexdigest())
