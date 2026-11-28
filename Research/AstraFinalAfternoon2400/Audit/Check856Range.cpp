// Independent range verification; no sieve or copied class-index arithmetic.
#include <cstdint>
#include <iostream>
using U=uint64_t;
using W=unsigned __int128;
int main() {
 constexpr U cut=100097600001, mod=1714, e=857;
 U tested=0;
 // Check every integer candidate in the necessary prime progression, including
 // all composites. 3 is a quadratic residue for odd order, so r=+-1 mod 12.
 for (U r=1+mod;r<=cut;r+=mod) {
  if (r%12!=1 && r%12!=11) continue;
  U p=1;
  for (U a=3,b=e;b;b>>=1) {
   if (b&1) p=U(W(p)*a%r);
   a=U(W(a)*a%r);
  }
  if (p==1) { std::cerr<<"Root candidate "<<r<<'\n'; return 1; }
  ++tested;
 }
 std::cout<<"PASS independent unsieved candidate range through "<<cut<<"; "<<tested<<" entries\n";
}
