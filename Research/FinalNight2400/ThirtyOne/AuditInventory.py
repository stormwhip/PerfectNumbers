import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
names=['First16.md','Verify16.py','AtomPrice.py','Forest16.json','Cert16.json','First22.md','Window.py','EulerForest.py','Verify22.py','Packet22.json','Cert22.json','VerifyDeep.py','DeepPacket.json','CertDeep.json','DeepExtras.json','Full31x16.py'];print('complete integration set (baselines imported separately)');
for name in names:
 b=(H/name).read_bytes();print(name,len(b),hashlib.sha256(b).hexdigest());
