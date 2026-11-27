from pathlib import Path
import hashlib
H=Path(__file__).resolve().parent
for name in 'Domain.py OnePrice.py Special.py Verify.py FinalFibers.py Full882.py Packet12.json.gz Done1.json.gz Done2.json.gz Done4.json.gz Done8.json.gz Proof.md'.split():
 b=(H/name).read_bytes();print(name,len(b),hashlib.sha256(b).hexdigest())
