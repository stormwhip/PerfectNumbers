"""Run Python parts. Verify Trial.cpp separately as directed in README. Does not rewrite the frozen checkout."""
import sys,json,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from Joint import ROOT
import PrimitiveAudit,Exact,Verify
if __name__=='__main__':
    assert __debug__;PrimitiveAudit.main()
    script=ROOT/'Research/P3I00193Review/VerifyPartial.py';spec=importlib.util.spec_from_file_location('frozenpartial',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    # Intercept its sole write, capturing the JSON in memory instead of modifying the frozen checkout.
    class Sink:
        def __truediv__(self,s):assert s=='PartialResults.json';return self
        def write_text(self,s,encoding):self.value=json.loads(s)
    sink=Sink();m.HERE=sink;m.EXPONENTS=(1162,);m.run();assert sink.value['rows'][0]['e']==1162
    assert Exact.verify_base(verbose=True)==2219
    sys.argv[:]=[str(HERE/'Verify.py'),str(ROOT),'--conditional-2219'];Verify.main();print('PASS all Python parts for (3,1162); separately require Trial.cpp range success',flush=True)
