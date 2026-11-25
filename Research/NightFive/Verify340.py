"""Separate entry point sharing both standard-library factor-tree replays."""
from VerifyChain import H,run,json
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 a=run(json.loads((H/'ChainPacket340.json').read_text()));assert a[0]==340;print('verified',a)
