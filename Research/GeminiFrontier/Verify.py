#!/usr/bin/env python3
"""Reviewed increment only. SubmittedVerify is a preserved, partly unaccepted candidate."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

assert __debug__
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
B = 10**2400
HASHES = {
    "SubmittedProof.md": "0a85ab736a5d520c1dd149490c2d4d92538d6b1815c1d7f27d12708d7ac2fb59",
    "SubmittedResults.json": "b5826969b6ea0541d968f2576f14f22d53be7a3ed7a0d071526927ae35439962",
    "SubmittedVerify.py": "39657ee6eafdd632f800597247b587a0f7d236fe8e8258723ca8cd0676c07469",
}
for name, digest in HASHES.items():
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest
v = runpy.run_path(str(HERE / "SubmittedVerify.py"))
for p in v["PRATT_CERTS"]:
    v["verify_prime"](p)
# For the actual single-target uses, higher multiples k of an odd order
# cannot increase the deficit over f=o-1: k-1 >= (p-1)*v_p(k).
for p, n, d, orders in [(7,19,10,[3]),(13,19,10,[3]),(19,99,50,[3,9])]:
    assert n > d and (2*p+1)**(d*(p-1)) > p**n
    for o in orders:
        assert d*(o-1) >= n and 3**(d*o*(p-1)) >= p**n
v["verify_full_key_13_508"]()
v["verify_7_438_f22_f18"]()
v["verify_19_618_independent"]()
# Repair: the author's s_1=0 bound applies only to a=1. For every
# high even pivot, exclude a>=5 separately, without assuming p-supply
# comes from q+1 and without charging the potentially shared block A.
state, sigma, odd, val = (v[k] for k in ("state_eval","sigma","odd","val"))
t = 2477
for f in range(70,122,2):
    X,S,D = state({19:618,t:f},set())
    A = odd(sigma(19,618))//t
    C = odd(sigma(t,f))
    C //= 19**val(C,19)
    assert D == A*C
    Q = 2*t**(f-val(S,t))-1
    assert v["prove_q_not_dividing_block"](C,Q,2*(Q+1))
    assert X*C*Q**5 > B
X,S,D = state({19:618},set())
live = [f for f in range(1,243) if state({19:618,t:f},set()) is not None]
assert live == sorted([1,*range(2,121,2),*range(5,122,4)])
assert X*(D//t)*t**243 > B
assert X*(D//t)*t**242 <= B
print("PASS 19x618 high Euler repair, 56/91 live fibers, tail 243")
# Historical union: pin the registered proof packets, not the author's
# textual assertion. Default run includes their complete local replay.
history = ROOT/"Research"/"Night2400"/"G8"
for name, digest in {
    "Thirteen508.json.gz":"d798580b1e3e4760bcb67da93e5f9c37611ef1997d543e4a6d904a0d722c9680",
    "Resume6.json.gz":"bd46c808e0a830d9f6d1e498a7daa57a2bbc55525a97491955a33e54779b4248",
}.items():
    assert hashlib.sha256((history/name).read_bytes()).hexdigest()==digest
if "--arithmetic-only" not in sys.argv:
    subprocess.run([sys.executable,"-I","-S","-B","-X","int_max_str_digits=0",str(history/"ResumeVerify.py")],cwd=ROOT,check=True)
else:
    print("NOTE: historical arithmetic not replayed by this invocation")
raw = (ROOT/"Research"/"Night2400"/"ShardToKeys.json").read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="230650784273e7d2734ab4562e903bef5076a4fc"
old = json.loads(raw)
assert len(old)==69 and len({tuple(k) for ks in old.values() for k in ks})==79
assert old["P13_I00096"]==[[13,508]]
updated = {s:[k for k in ks if k!=[13,508]] for s,ks in old.items()}
closed = [s for s,ks in updated.items() if not ks]
updated = {s:ks for s,ks in updated.items() if ks}
assert closed==["P13_I00096"]
assert updated==json.loads((HERE/"ShardToKeys.json").read_text())
inverse = {}
for s,ks in updated.items():
    for p,e in ks:
        inverse.setdefault(f"{p},{e}",[]).append(s)
assert {k:sorted(s) for k,s in inverse.items()}==json.loads((HERE/"KeyToShards.json").read_text())
assert len(updated)==68 and len(inverse)==78
assert sum(len(ks)==1 for ks in updated.values())==60
d = json.loads((HERE/"Delta.json").read_text())
assert (d["closed"],d["open"],d["distinct_keys"],d["singleton_shards"])==(3004,68,78,60)
assert d["new_keys"]==[[13,508]] and d["new_closed"]==closed
print("PASS registered projection: 3004/3072 closed, 68 shards, 78 keys, 60 singletons")
print("Unaccepted submissions (7,882) f=72 and (19,432) f=22 are not replayed or credited.")
