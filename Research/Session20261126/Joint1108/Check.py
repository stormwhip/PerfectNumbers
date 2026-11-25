"""Fixed all-domain certificate for canonical (3,1108). Trusted sources are the checked-in archive and fixed mathematical dependencies; never execute a remote program or read a cached receipt."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
H=Path(__file__).resolve().parent;REPO=H.parents[2];PIN='8a58ee47bbeb50c597205f88426800464a9ee04fb3c1e29385a45f958bb5a753'

def verify():
    if not __debug__:raise ValueError('no -O')
    raw=H/'Proof.zip';m=json.loads((H/'Manifest.json').read_bytes());assert hashlib.sha256(raw.read_bytes()).hexdigest()==m['archive_sha256']==PIN
    cc=os.environ.get('CXX') or shutil.which('g++') or shutil.which('clang++');assert cc,'compiler with unsigned __int128 required'
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(raw) as z:
            names=z.namelist();assert len(names)==len(set(names)) and set(names)==set(m['files'])
            for name in names:
                assert not PurePosixPath(name).is_absolute() and not {'..','.'}.intersection(PurePosixPath(name).parts) and '\\' not in name and ':' not in name
                f=root/name;data=z.read(name);assert hashlib.sha256(data).hexdigest()==m['files'][name];f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(data)
        exe=root/('Trial.exe' if os.name=='nt' else 'Trial');subprocess.run([cc,'-std=c++17','-O3',str(root/'Base/Trial1108.cpp'),'-o',str(exe)],check=True);assert subprocess.check_output([str(exe)],text=True).strip()=='R 10175119360001 survivors tested 208340693; no divisor'
        proc=subprocess.Popen([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(root/'Complete.py'),str(REPO)],stdout=subprocess.PIPE,text=True);end=''
        for line in proc.stdout:print(line,end='',flush=True);end=line.strip()
        assert proc.wait()==0 and end.startswith('PASS all Python parts: e=1108; require separate Trial1108.cpp range check')
    return dict(packet='Joint1108/Proof.zip',sha256=PIN,seed=[3,1108],actuals=[1108],source_leaves=[42,42],base_digits=[2122,2089],range_bound=10175119360001,range_survivors_tested=208340693)
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
