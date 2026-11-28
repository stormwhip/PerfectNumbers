// Candidate square-kernel lower endpoint for anonymous cyclotomic values.
// Scan every K that could be a squarefree kernel below an explicit threshold.
#include <cstdint>
#include <cstdlib>
#include <algorithm>
#include <iostream>
#include <vector>
#include <gmpxx.h>
using U=uint64_t;using Z=mpz_class;
int main(int argc,char**argv){
 if(argc!=4)return 2;U p=std::stoull(argv[1]),d=std::stoull(argv[2]),H=std::stoull(argv[3]);
 Z A;mpz_ui_pow_ui(A.get_mpz_t(),p,d);A=(A-1)/(p-1);
 constexpr U LEN=1<<20;std::vector<unsigned char> T(LEN);
 if(p<2||d<3||d%2==0||p%d==1)return 2;
 for(U j=3;j*j<=d;j+=2)if(d%j==0)return 2;
 if(mpz_fdiv_ui(A.get_mpz_t(),d)==0||mpz_fdiv_ui(A.get_mpz_t(),2)==0)return 2;
 U D=8*d,m=mpz_fdiv_ui(A.get_mpz_t(),8),base=1;while(base%8!=m)base+=2*d;
 if(H<base)return 2;
 U ymax=(H-base)/D;
 std::vector<std::pair<U,std::vector<U>>> wheel;
 // K*h²=A implies K is in one of a finite set of residue classes mod q.
 // This does not presume K invertible; include any residue that could work.
 for(U q=3;q<100;++q){bool prime=true;for(U j=2;j*j<=q;++j)if(q%j==0){prime=false;break;}if(!prime)continue;
   std::vector<U> forbid;U a=mpz_fdiv_ui(A.get_mpz_t(),q);
   for(U k=0;k<q;++k){U r=(base+D*k)%q;bool ok=false;for(U z=0;z<q;++z)if((r*z*z)%q==a){ok=true;break;}if(!ok)forbid.push_back(k);}
   wheel.emplace_back(q,std::move(forbid));
 }
 U n=0;for(U s=0;s<=ymax;s+=LEN){U cap=std::min(LEN,ymax-s+1);std::fill_n(T.begin(),cap,1);
  for(auto &[q,V]:wheel)for(U r:V)for(U k=(r+q-s%q)%q;k<cap;k+=q)T[k]=0;
  for(U j=0;j<cap;++j)if(T[j]){U x=base+D*(s+j);++n;
   if(mpz_divisible_ui_p(A.get_mpz_t(),x)){Z Q=A/x;if(mpz_perfect_square_p(Q.get_mpz_t())){std::cout<<"hit "<<x<<"\n";return 1;}}
  }
 }
 std::cout<<"PASS "<<p<<" "<<d<<" "<<H<<" "<<n<<"\n";
}
