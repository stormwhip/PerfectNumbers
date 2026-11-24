"""Release manifest only; the mathematical verifier recomputes the claims, not hashes."""
from pathlib import Path
from hashlib import sha256
import json,argparse
H=Path(__file__).resolve().parent
NAMES=['CheckCertificate.py','PrimeCheck.py','Tree.py','DualTree.py','LeafCheck.py','GapDual.py','GapIndependent.py','Shards.py','RootFiveCertificate.json','RootFiveVerified.json','Tests.py','Manifest.py']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args();data={n:sha256((H/n).read_bytes()).hexdigest() for n in NAMES};s=json.dumps(data,indent=1)+'\n';m=H/'ReleaseManifest.json'
 if a.emit:m.write_text(s,encoding='utf8')
 elif json.loads(m.read_text())!=data:raise ValueError('manifest mismatch')
 print('release manifest:',len(data),'files')
