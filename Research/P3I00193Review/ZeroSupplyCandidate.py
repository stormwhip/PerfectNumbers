"""Conditional b=0 Euler-base experiment; no acceptance and no new trial-division claim."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ReplayCandidate import HERE,INPUT,load_model


def run():
    m=load_model();scope=m.verify_euler_bounds.__globals__
    source=(INPUT/'VerifyP31162.py').read_text()
    source=source[source.index('def verify_euler_bounds'):source.index('def verify_not_euler_source')]
    source=source.replace('range(0, 7)','range(0, 1)').replace('    def extra_ord_full(U):','    @cache\n    def extra_ord_full(U):')
    exec(compile(source,'candidate_b0','exec'),scope)
    rows=[]
    for e,ra in [(1108,10**11),(1162,5*10**9)]:
        v=scope['verify_euler_bounds'](e,ra)
        rows.append({'e':e,'assumed_R_A':ra,'b0_euler_base_digits':str(min(v[3:5])/m.LN10_HI),
                     's_min_candidate_b0':v[5],'status':'CANDIDATE_BASE_ONLY'})
    (HERE/'ZeroSupplyCandidate.json').write_text(json.dumps({'accepted_actuals':[],'rows':rows},indent=2)+'\n',encoding='utf-8')
    print(rows)


if __name__=='__main__':run()
