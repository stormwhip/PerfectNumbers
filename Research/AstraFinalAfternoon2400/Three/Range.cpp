// Exact primitive-factor lower bound for all currently anonymous atoms.
// Usage: Range BASE PRIME_INDEX LAST_K. Check every possible prime r=1+2*d*k.
// No assumption of primality of surviving r values; modular tests are exact.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using U=std::uint64_t; using W=unsigned __int128;
U pw(U a,U n,U m){U v=1;a%=m;for(;n;n>>=1){if(n&1)v=W(v)*a%m;a=W(a)*a%m;}return v;}
int main(int argc,char**argv){
 if(argc!=4)return 2;
 const U p=std::stoull(argv[1]),d=std::stoull(argv[2]),K=std::stoull(argv[3]);
 if(d<3||d%2==0||!K||d>100000||K>10000000000ull)return 2;
 for(U j=3;j*j<=d;j+=2)if(d%j==0)return 2;
 if(p%d==1)return 2; // excludes order-one possibility at the index prime
 constexpr U L=100000,S=1<<22;const U D=2*d;
 std::vector<unsigned char>s(L+1,1),live(S);std::vector<U>P,R;s[0]=s[1]=0;
 for(U q=2;q<=L;++q)if(s[q]){
  for(U k=q*q;k<=L;k+=q)s[k]=0;
  if(D%q){P.push_back(q);R.push_back(q-pw(D,q-2,q));}
 }
 U tried=0;
 for(U b=1;b<=K;b+=S){
  U n=std::min(S,K-b+1);std::fill_n(live.begin(),n,1);
  for(U i=0;i<P.size();++i){U q=P[i],k=b+(R[i]+q-b%q)%q;if(1+D*k==q)k+=q;for(;k<b+n;k+=q)live[k-b]=0;}
  for(U j=0;j<n;++j)if(live[j]){
   U r=1+D*(b+j);
   if(p==3&&r%12!=1&&r%12!=11)continue; // 3 is a square at all odd-order primes
   // The only removed term is checked modulo its square to certify exact
   // multiplicity one in Phi_157(1093), before factoring off this prime.
   if(p==1093&&d==157&&r==2035349){if(pw(p,d,r)!=1||pw(p,d,r*r)==1)return 2;continue;}
   ++tried;
   if(pw(p,d,r)==1){std::cerr<<"possible divisor "<<r<<" at "<<p<<"/"<<d<<"\n";return 1;}
  }
 }
 std::cout<<"PASS "<<p<<" "<<d<<" "<<K<<" "<<(1+D*K)<<" "<<tried<<"\n";
}
