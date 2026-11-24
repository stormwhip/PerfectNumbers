"""Independent shared-block tail audit; deliberately NOT a claim that a shard closes."""
import json,sys,math
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'RootFiveNext'));from PrimeCheck import prime64
ORDER=(19,7,11,31,13,3,5,17);B=10**2400

def check(rows):
    baseline=json.loads((R/'EveningMerge/Audit.json').read_text()); pending={p:{e for r in baseline['remaining_shards'] if r['root']==p for e in r['remaining_actuals']} for p in (3,5)}; closed=set(); stats=[]
    for row in rows:
        p,h,fs=row['p'],row['h'],row['fs'];assert p in pending and h>=3 and h%2==1 and len(set(fs))==len(fs)
        A=(p**h-1)//(p-1);ban=ORDER[:ORDER.index(p)]; M=A;savings=[1];
        for z in fs:
            if not prime64(z) or z<=2 or A%z:raise ValueError('not a certified odd prime divisor')
            c=0;u=A
            while u%z==0:c+=1;u//=z
            def ok(f):return all(pow(z,f+1,r*(z-1))!=1 for r in ban)
            m=c+c%2
            while not ok(m):m+=2
            M*=z**(m-c)
            if z%4==1 and all((z+1)%r for r in ban):
                o=c+(1-c)%4
                while o<m and not ok(o):o+=4
                savings.append(z**max(0,m-o))
        charge=M//max(savings);k=0
        while p**k*charge<=B:k+=1
        target=sorted(e for e in pending[p] if (e+1)%h==0);hits=[e for e in target if e>=k]; closed.update((p,e) for e in hits)
        stats.append(dict(p=p,h=h,threshold=k,targets=target,extra_factor_bits=(charge//A).bit_length()-1,excluded=hits))
    return stats,closed

if __name__=='__main__':
    d=json.loads((H/'Shared64.json').read_text());rs,c=check(d);print('verified common blocks',len(rs),'new exponents',sorted(c));print('max price gain',max(x['extra_factor_bits'] for x in rs));print('top reusable',sorted(rs,key=lambda x:-x['extra_factor_bits'])[:3]);
