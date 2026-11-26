"""Seal discovery forests into one deterministic packet; not used by cold verification."""
from Explore import *
from hashlib import sha256
import subprocess


def main():
    old, _, missing = inputs()
    cases = {}
    primes = {Q}
    for m in missing:
        fs = set(branches(m)[0]) - {row['f'] for row in old['rows']}
        assert len(fs) == 1
        f, = fs
        a,b = groups(m)
        s = C.State(feasible(f)[0],a,b)
        if m == 59:
            k = roots(s,f); assert bound(s,k)[0] > 2
            cases[str(m)] = dict(f=f, kind='abundance', roots=k)
        else:
            row = json.loads((H/'trials'/f'{m}.json').read_bytes())
            assert C.Forest(s,row['roots'],row['owners'],row['head']).lower()[0] > B
            cases[str(m)] = dict(f=f, kind='forest', **{k: row[k] for k in ('roots','owners','head')})
            primes.update(dict(row['owners']))
        primes.update(cases[str(m)]['roots'])
    known = seed()
    wanted = sorted(z for z in primes if z >= 2**64)
    for q in wanted:
        if str(q) in known:continue
        key = sha256(str(q).encode()).hexdigest()[:24]
        obj = f'49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec:Research/NightOrder/ECPP/{key}.json.gz'
        proc = subprocess.run(['git','cat-file','blob',obj],capture_output=True,cwd=REPO)
        if proc.returncode == 0:
            known[str(q)] = json.loads(gzip.decompress(proc.stdout))
    todo = [q for q in wanted if str(q) not in known]
    print('ECPP labels',len(wanted),'generate',len(todo),flush=True)
    if todo:
        cmd = ['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-f','-q','-s','128M']
        ask = 'default(nbthreads,1);\n' + ''.join(f'print(primecert({q}));\n' for q in todo)
        proc = subprocess.run(cmd, input=ask.encode(),capture_output=True,cwd=REPO,timeout=900,check=True)
        ans = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
        assert len(ans) == len(todo), proc.stderr
        known.update({str(q):c for q,c in zip(todo,ans)})
    assert all(prime_chain(z,known) for z in primes)
    cases_str = json.dumps(dict(cases=cases,ecpp={str(z):known[str(z)] for z in wanted}),separators=(',',':'),sort_keys=True).encode()
    packet=H/'Pivot316Residual.json.gz';packet.write_bytes(gzip.compress(cases_str,mtime=0))
    print(packet,sha256(packet.read_bytes()).hexdigest(),flush=True)

if __name__ == '__main__': main()
