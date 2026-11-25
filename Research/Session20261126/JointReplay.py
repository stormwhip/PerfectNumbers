"""Full 3x1162 proof: compile the exact range verifier from tracked source, then run all Python obligations. Requires GCC or Clang with unsigned __int128."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent/'Joint';ROOT=H.parents[2]

def verify():
    cc=os.environ.get('CXX') or shutil.which('g++') or shutil.which('clang++')
    if not cc:raise RuntimeError('3x1162 requires a C++17 compiler (g++ or clang++) for the complete finite progression sweep')
    with tempfile.TemporaryDirectory() as tmp:
        exe=Path(tmp)/('Trial.exe' if os.name=='nt' else 'Trial');subprocess.run([cc,'-std=c++17','-O3',str(H/'Trial.cpp'),'-o',str(exe)],check=True)
        msg=subprocess.check_output([str(exe)],text=True).strip();assert msg=='R 10670571520001 survivors tested 208445632; no divisor',msg
    p=subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(H/'Complete.py'),str(ROOT)],check=True,stdout=subprocess.PIPE,text=True);answers=[json.loads(l) for l in p.stdout.splitlines() if l.startswith('{"excluded"')];answer,=answers
    assert answer['all_joint_subdomains'] and answer['conditional_on_parity_2219'] and answer['excluded']==[list(range(42)),list(range(42))]
    assert 'PASS all Python parts for (3,1162)' in p.stdout and 'PASS uniform e>=824;' in p.stdout
    files=sorted(f for f in H.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix in ('.cpp','.py','.json'))
    manifest=hashlib.sha256();
    for f in files:
        manifest.update(f.relative_to(H).as_posix().encode()+b'\0'+hashlib.sha256(f.read_bytes().replace(b'\r\n',b'\n')).digest())
    return dict(seed=[3,1162],actuals=[1162],packet='Joint/Complete.py',sha256=hashlib.sha256((H/'Complete.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),joint_files_sha256_lf=manifest.hexdigest(),source_leaves=[42,42],range_bound=10670571520001,range_survivors_tested=208445632)
if __name__=='__main__':
    if not __debug__:raise SystemExit('no -O')
    print(json.dumps(verify(),sort_keys=True))
