// Sieve candidate r=h*k+1, then test the exact n. Requires 64-bit unsigned long.
#include <gmpxx.h>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <chrono>
using UL=unsigned long;
int main(int argc,char**v){static_assert(sizeof(UL)==8);if(argc!=5)return 1;mpz_class n(v[1]);UL h=strtoul(v[2],0,10), hi=strtoul(v[3],0,10), known=strtoul(v[4],0,10);UL cap=sqrt((long double)hi)+1,K=(hi-1)/h;std::vector<char> sieve(cap+1),seg(1<<20);std::vector<UL> ps,rx;for(UL p=2;p<=cap;p++)if(!sieve[p]){if(p<=cap/p)for(UL j=p*p;j<=cap;j+=p)sieve[j]=1;if(h%p==0)continue;mpz_class H=h,P=p,X; if(!mpz_invert(X.get_mpz_t(),H.get_mpz_t(),P.get_mpz_t()))return 2;ps.push_back(p);rx.push_back(p-X.get_ui());}
UL hit=0,test=0;auto st=std::chrono::steady_clock::now();for(UL a=1;a<=K;a+=seg.size()){UL b=std::min<UL>(a+seg.size(),K+1);std::fill(seg.begin(),seg.end(),0);for(UL i=0;i<ps.size();i++){UL p=ps[i],k=a+(rx[i]+p-a%p)%p;if(h*k+1==p)k+=p;for(;k<b;k+=p)seg[k-a]=1;}for(UL k=a;k<b;k++)if(!seg[k-a]){UL r=h*k+1;test++;if(mpz_divisible_ui_p(n.get_mpz_t(),r)){printf("factor %lu\n",r);fflush(stdout);hit++;}}}
printf("h=%lu maximum=%lu tests=%lu found=%lu seconds=%.3f\n",h,hi,test,hit,std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count());return hit==known?0:3;}
