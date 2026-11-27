"""Accepted partial forests only; enforce packet identities and both partitions."""
import hashlib,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent;hist=here.parent/'Night2400'
for name,sha,checks in [('Thirteen262.json.gz','23e91a724829cac6f849993452067010df3bb66d9d4bc8b4f07ad105b08b7f21',[('G6/Verify.py','--packet')]),('Root31x310F18.json.gz','680539a9f43d372b26816eab8a110e741db2ba2c5b461418bb270d9c3986374d',[('FrontierTree.py',),('Receipts/FiberPartition.py',)])]:
    file=here/'Others'/name;assert hashlib.sha256(file.read_bytes()).hexdigest()==sha
    for script,*args in checks:subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(hist/script),*args,str(file)],check=True)
