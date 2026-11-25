// Independent C++17 range certificate. GCC/Clang unsigned __int128.
#include <algorithm>
#include <iostream>
#include <vector>
#include <cstdint>
using U=std::uint64_t; using W=unsigned __int128;
constexpr U D=2326,N=65536ull*70000,S=1<<22,L=200000;
U power(U a,U h,U p){U v=1;for(;h;h>>=1){if(h&1)v=W(v)*a%p;a=W(a)*a%p;}return v;}
int main(){std::vector<unsigned char> sieve(L+1,1),alive(S);std::vector<U> pp,roots;
 for(U p=2;p<=L;++p)if(sieve[p]){for(U k=p*p;k<=L;k+=p)sieve[k]=0;if(D%p){pp.push_back(p);roots.push_back(p-power(D,p-2,p));}}
 U tried=0; for(U a=1;a<=N;a+=S){U n=std::min(S,N-a+1);std::fill_n(alive.begin(),n,1);
 for(U j=0;j<pp.size();++j){U p=pp[j],k=a+(roots[j]+p-a%p)%p;if(D*k+1==p)k+=p;for(;k<a+n;k+=p)alive[k-a]=0;}
 for(U i=0;i<n;++i)if(alive[i]){U t=D*(a+i)+1;if(t%12!=1 && t%12!=11)continue; ++tried;if(power(3,1163,t)==1){std::cerr<<"unexpected divisor candidate "<<t<<"\n";return 1;}}}
 std::cout<<"R "<<D*N+1<<" survivors tested "<<tried<<"; no divisor\n";}
