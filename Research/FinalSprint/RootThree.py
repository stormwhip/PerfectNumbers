"""Replay complete packaged root-three certificates, including the C++ range test."""
from hashlib import sha256
from pathlib import Path,PurePosixPath
import json,os,shutil,subprocess,sys,tempfile,zipfile
H=Path(__file__).resolve().parent

def verify990():
    assert __debug__;name='Root3x990.zip'; raw=H/name; digest=sha256(raw.read_bytes()).hexdigest()
    assert digest=='42df59e33c0d82ae6d876034322ce967bba410321c7746b8396b454bc9ac6f71'
    compiler=os.environ.get('CXX') or shutil.which('g++') or shutil.which('clang++');assert compiler,'C++17 compiler with unsigned __int128 required'
    with tempfile.TemporaryDirectory() as td:
        dest=Path(td)
        with zipfile.ZipFile(raw) as arc:
            manifest=json.loads(arc.read('Manifest.json'));ns=arc.namelist();assert len(ns)==len(set(ns)) and set(ns)==set(manifest)|{'Manifest.json'}
            for s in manifest:
                p=PurePosixPath(s);assert not p.is_absolute() and '..' not in p.parts and ':' not in s and '\\' not in s
                data=arc.read(s);assert sha256(data).hexdigest()==manifest[s];f=dest/s;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
        exe=dest/('range.exe' if os.name=='nt' else 'range');subprocess.run([compiler,'-std=c++17','-O3',dest/'Partial/Base/Trial990.cpp','-o',exe],check=True)
        out=subprocess.check_output([exe],text=True).strip();assert out=='R 9092464640001 survivors tested 208105567; no divisor'
        for args,end in [(['prereq.py',str(H.parents[1])],'PREREQUISITES PASS:'),(['check990.py'],'PASS: all 64+98 branches')]:
            out=subprocess.check_output([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',*args],cwd=dest,text=True)
            assert out.rstrip().splitlines()[-1].startswith(end)
    return dict(actual=[3,990],packet=name,sha256=digest,range_bound=9092464640001,range_candidates=208105567,external_exponents=64,internal_exponents=98)
if __name__=='__main__':print(json.dumps(verify990()))
