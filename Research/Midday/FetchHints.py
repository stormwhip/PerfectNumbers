"""Optional discovery only. Query the public FactorDB endpoint sequentially with pacing.
Nothing in a FactorDB response is a primality or divisibility certificate.
"""
import argparse,json,time,urllib.request,urllib.parse
from pathlib import Path
H=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('out',type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    rows=json.loads((H.parent/'Nov25/Delta.json').read_bytes())['remaining_shards']; pairs={(r['root'],e) for r in rows for e in r['remaining_actuals']}
    for p,e in sorted(pairs,key=lambda pe:-pe[1]*__import__('math').log(pe[0])):
        out=a.out/f'{p}x{e}.json'; expr=f'{p}^{e+1}-1'
        if out.is_file():continue
        try:
            with urllib.request.urlopen('https://factordb.com/api?'+urllib.parse.urlencode({'query':expr}),timeout=15) as f: d=json.load(f)
            pairs2=[(int(q),int(v)) for q,v in d['factors']]; assert all(q>1 and v>0 for q,v in pairs2) and __import__('math').prod(q**v for q,v in pairs2)==p**(e+1)-1
            out.write_text(json.dumps(pairs2),encoding='utf8');print(p,e,[(len(str(q)),v) for q,v in pairs2],flush=True)
        except Exception as exc:
            print(expr,'failed',repr(exc),flush=True)
            if getattr(exc,'code',None) in (403,429):break
        time.sleep(1.25)
if __name__=='__main__': main()
