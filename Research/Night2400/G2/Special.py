"""Optional discovery of the forced-five mask 113 forest; not a verifier."""
from pathlib import Path
import argparse
from Search import state, P, E, Q, H, catalog, seed, build


def main():
    from Discover import Finder, Bank
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--db',type=Path,required=True)
    ns=a.parse_args()
    m,f=113,16
    s=state([(P,E),(Q,f),(5,1)],m)
    finder=Finder(Bank(ns.db),26)
    cat,_=catalog()
    roots=sorted((set(s.present)|set(finder.factors(Q,f)))-set(s.bad)-s.rows.keys())
    return build(s,roots,seed(s,roots,cat,7,1550),finder,85,384,H/'trials/Special.json',(m,f,5,1))


if __name__=='__main__':
    raise SystemExit(0 if main() else 1)
