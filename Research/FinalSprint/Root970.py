"""Use the immutable 990 package for shared prerequisites, then run all 970 domains."""
from pathlib import Path,PurePosixPath
import zipfile,hashlib,json,sys,tempfile,subprocess
H=Path(__file__).resolve().parent

def unpack(dest,name,pin,manifest):
    f=H/name;assert hashlib.sha256(f.read_bytes()).hexdigest()==pin
    with zipfile.ZipFile(f) as z:
        files=json.loads(z.read(manifest));assert len(z.namelist())==len(files)+1 and set(z.namelist())==set(files)|{manifest}
        for n,h in files.items():
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
            v=z.read(n);assert hashlib.sha256(v).hexdigest()==h;d=dest/n;assert not d.exists();d.parent.mkdir(exist_ok=True,parents=True);d.write_bytes(v)

def verify():
    assert __debug__;name='Root3x970Full.zip';pin='c7fb0f0f1b9ce799a0b11782a882585c185252a5d59a9a12fa860b743e7760bc'
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp);unpack(dest,'Root3x990.zip','42df59e33c0d82ae6d876034322ce967bba410321c7746b8396b454bc9ac6f71','Manifest.json');unpack(dest,name,pin,'Manifest970.json');proc=subprocess.run([sys.executable,'-I','-S','-B',str(dest/'next970/check970.py'),str(H.parents[1])],cwd=dest/'next970',check=True,stdout=subprocess.PIPE,text=True);assert proc.stdout.rstrip().splitlines()[-1].startswith('PASS: all 42+42 E3a/E3b supports')
    return dict(actual=[3,970],packet=name,sha256=pin,external_supports=42,internal_supports=42)
if __name__=='__main__':print(json.dumps(verify()))
