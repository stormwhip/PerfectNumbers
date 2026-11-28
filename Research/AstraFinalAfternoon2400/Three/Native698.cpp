// Native independent s=698 exterior-source wheel; all arithmetic exact GMP.
#include <algorithm>
#include <atomic>
#include <cassert>
#include <cstdlib>
#include <gmpxx.h>
#include <iostream>
#include <mutex>
#include <numeric>
#include <thread>
#include <vector>
using Z=mpz_class;
Z pw(const Z&b,int n){Z o;mpz_pow_ui(o.get_mpz_t(),b.get_mpz_t(),n);return o;}
Z pp(const Z&b,const Z&e,const Z&m){Z o;mpz_powm(o.get_mpz_t(),b.get_mpz_t(),e.get_mpz_t(),m.get_mpz_t());return o;}
int md(const Z&n,int d){return mpz_fdiv_ui(n.get_mpz_t(),d);}
bool pr(int n){for(int q=2;q*q<=n;++q)if(n%q==0)return false;return n>1;}
int inv(int a,int m){for(int i=1;i<m;++i)if((a*i)%m==1)return i;return 0;}
// Greedy minimum marginal factors; report establishes why this is conservative.
std::vector<Z> U(){std::vector<Z>L(856,225000000),V{1};for(int p=4;p<=15000;++p)if(p%3==1&&pr(p)&&p!=7&&p!=13&&p!=19&&p!=31){
 for(int d=3,j=0;;d*=3){Z a=pw(Z(p),d-1-j);if(a>=225000000)break;Z n=(pw(Z(p),d)-1)/(p-1);bool yes=true;for(int q:{7,11,13,19,31})if(md(n,q)==0)yes=false;if(!yes)break;L.push_back(a);j=d-1;}}
 std::sort(L.begin(),L.end());for(int j=0;j<856;++j)V.push_back(V.back()*L[j]);return V;}
int main(int argc,char**argv){
 assert(argc==2);auto M=U();const int s=698,k=856-s;const Z B=pw(Z(10),2400),X=pw(Z(3),856),Y=pw(Z(3),s),D=(3*X-1)/2,R("100097600002"),K("13000000000001");
 Z c=0;for(int i=0;i<=k;++i){Z a=D*K,b=pw(R,2*i),m=M[k-i]*(a>b?a:b);if(!c||m<c)c=m;} Z F=X*c;
 Z h=3*B/(2*F),rt;mpz_sqrt(rt.get_mpz_t(),h.get_mpz_t());h=(1+rt)/(2*Y);int H=h.get_si();assert(H==15199714);
 std::vector<unsigned char>good(H+1,1),orders(H+1,0);for(int d:{2,3,7,11,13,19,31})for(int i=0;i<=H;i+=d)good[i]=0;
 for(int p=5;p<=600;++p)if(pr(p)){int a=inv(md(2*Y,p),p);assert(a);for(int m=a;m<=H;m+=p)good[m]=0;}
 struct Row{int d;Z pow;std::vector<int> factors;};std::vector<Row> lib;const Z C=B/F; Z l=C/(2*Y-1);
 for(int d=5;pw(Z(5),d-1)<=l;d+=2)if(d%3){
   const Z z=pw(Z(5),d-1);int a=inv(md(Y,d),d);assert(a);
   if(a%2==0)a+=d; Z u=(1+C/z)/(2*Y);int cap=std::min(long(H),u.get_si());
   for(int m=a;m<=cap;m+=2*d)orders[m]=1;
   Row row{d,z,{}};for(int p=2;p<=d;++p)if(d%p==0&&pr(p))row.factors.push_back(p);
   lib.push_back(std::move(row));
 }
 std::vector<int> pts;for(int m=1;m<=H;m+=2)if(good[m]&&orders[m])pts.push_back(m);
 std::cout<<"candidate count "<<pts.size()<<std::endl;
 std::atomic<unsigned>cursor{0},cand{0},unresolved{0};std::mutex mu;
 auto run=[&](){for(unsigned j;(j=cursor.fetch_add(1))<pts.size();){
  int m=pts[j];Z q=2*Y*m-1;
  if(pp(Z(2),q-1,q)!=1||pp(Z(3),q-1,q)!=1)continue;
  cand.fetch_add(1);Z room=C/q;assert(q*q>room);
  for(const auto &v:lib)if(v.pow<=room&&md(q-1,v.d)==0){
   int d=v.d;Z g=0;for(int a=2;a<100;++a){Z z=pp(Z(a),(q-1)/d,q);if(pw(z,d)%q!=1)continue;
      bool good=true;for(int t:v.factors)if(pw(z,d/t)%q==1)good=false;if(good){g=z;break;}}
   if(!g){std::lock_guard<std::mutex> lock(mu);std::cout<<"generator open "<<m<<" "<<d<<"\n";++unresolved;continue;}
   Z z=1;for(int a=1;a<d;++a){z=z*g%q;if(std::gcd(a,d)>1||z<5||md(z,2)==0)continue;
    if(pw(z,d-1)<=room){std::lock_guard<std::mutex> lock(mu);std::cout<<"source open "<<m<<" "<<d<<"\n";++unresolved;break;}}
  }
 }};
 std::vector<std::thread>T;unsigned threads=std::stoul(argv[1]);assert(threads>0&&threads<=32);for(unsigned i=0;i<threads;++i)T.emplace_back(run);for(auto& t:T)t.join();
 std::cout<<"FINAL "<<H<<" "<<pts.size()<<" "<<cand.load()<<" "<<unresolved.load()<<"\n";
 assert(pts.size()==648244&&cand.load()==9481&&unresolved.load()==0);
 return 0;
}
