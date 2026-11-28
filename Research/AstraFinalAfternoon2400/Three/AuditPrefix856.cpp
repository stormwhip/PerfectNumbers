// Independent exact recomposition of the new (3,856) Euler wheel certificate.
// GMP integer operations, no discovery or source-prime classification.
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <gmpxx.h>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using Z=mpz_class;
Z pw(const Z& n, unsigned e){ Z r;mpz_pow_ui(r.get_mpz_t(),n.get_mpz_t(),e);return r; }
Z pp(const Z& n,const Z& e,const Z& m){ Z r;mpz_powm(r.get_mpz_t(),n.get_mpz_t(),e.get_mpz_t(),m.get_mpz_t());return r; }
bool prime(int n){for(int k=2;k*k<=n;++k)if(n%k==0)return false;return n>=2;}
std::vector<int> small(int n){std::vector<int>P;for(int p=2;p<=n;++p)if(prime(p))P.push_back(p);return P;}
int mod(const Z& a,int p){return mpz_fdiv_ui(a.get_mpz_t(),p);}
Z pm(const Z&a,const Z&b){return a<b?b:a;}
std::vector<Z> tariff(){
 std::vector<int>bans={7,11,13,19,31};const Z cap=15000*15000;
 std::vector<Z>L(856,cap),V{1};
 for(int p:small(15000))if(p%3==1&&std::find(bans.begin(),bans.end(),p)==bans.end()){
  for(int n=3,f=0;;n*=3){
   Z w=pw(Z(p),n-1-f); if(w>=cap)break;
   bool good=true;Z sum=(pw(Z(p),n)-1)/(p-1);
   for(int q:bans)if(mod(sum,q)==0){good=false;break;}
   if(!good)break;
   L.push_back(w); f=n-1;
  }
 }
 std::sort(L.begin(),L.end());for(int j=0;j<856;++j)V.push_back(V.back()*L[j]); return V;
}
int main(int argc,char**argv){
 assert(argc==3);int s=atoi(argv[1]),mode=atoi(argv[2]);assert((s==697&&mode==0)||(s==679&&mode==1));
 auto M=tariff();const Z B=pw(Z(10),2400),X=pw(Z(3),856),W=3*X,A=(W-1)/2,R("100097600002"),Y=pw(Z(3),s);int k=856-s;
 Z C=0, X0;int H;
 std::vector<Z>RR;for(int i=0;i<=k;++i)RR.push_back(pw(R,2*i));
 if(!mode){
  for(int i=0;i<=k;++i){ Z m=M[k-i]*pm(A*R,RR[i]); if(!C||m<C)C=m; }
  X0=X*C;Z t=3*B/(2*X0),ss;mpz_sqrt(ss.get_mpz_t(),t.get_mpz_t());t=(ss+1)/(2*Y);H=t.get_si();assert(H==114235);
 }else{
  auto feasible=[&](int m){Z q=2*Y*m-1, den=pm(W,q)*(W/Y+4);for(int i=0;i<=k;++i){Z h=X*q*M[k-i];
     if(h*pm(A*R,RR[i])<=B&&2*h*q*RR[i]<=3*B&&h*q*Y*pm(A,RR[i])<=B*den)return true;}
    return false;};
  int lo=1,hi=1;while(feasible(hi))hi*=2;
  while(lo+1<hi){int t=(lo+hi)/2;if(feasible(t))lo=t;else hi=t;}
  H=lo;assert(H==1689429);X0=X*M[k];
 }
 // Recompute up to global d from the bare ordinary source cap.
 Z C0=B/X0,L=mode?R:Z(5),limit=C0/(2*Y-1),ex=L*L*L*L;std::vector<std::pair<int,Z>>ds;
 for(int d=5;ex<=limit;d+=2,ex*=L*L)if(d%3)ds.emplace_back(d,ex);
 std::vector<int> sb=small(600),bans={3,7,11,13,19,31};int count=0,fermat=0;
 for(int m=1;m<=H;m+=2){
  if(std::any_of(bans.begin(),bans.end(),[&](int p){return m%p==0;}))continue;
  Z q=2*Y*m-1;
  if(std::any_of(sb.begin(),sb.end(),[&](int p){return mod(q,p)==0;}))continue;
  Z room=C0/q;std::vector<int>v;
  for(const auto &de:ds)if(de.second<=room&&mod(q-1,de.first)==0)v.push_back(de.first);
  if(v.empty())continue;
  ++count; if(pp(Z(2),q-1,q)!=1||pp(Z(3),q-1,q)!=1)continue;
  ++fermat;
  for(int d:v){
   assert(pw(q,d-1)>room);
   // May choose a different generator from the Python proof; every primitive
   // power in the cyclic subgroup is checked. If the candidate modulus is
   // composite, it is irrelevant; if prime these powers exhaust its roots.
   std::vector<int>factor;for(int t:small(d))if(d%t==0)factor.push_back(t);
   Z z=0;for(int a=2;a<150;++a){
    Z g=pp(Z(a),(q-1)/d,q);
    if(pw(g,d)%q!=1)continue;
    if(std::any_of(factor.begin(),factor.end(),[&](int t){return pw(g,d/t)%q==1;}))continue;
    z=g;break;}
   assert(z!=0);
   Z r=1;
   for(int j=1;j<d;++j){r=(r*z)%q;if(std::gcd(j,d)!=1)continue;
    if(r<L||mod(r,2)==0)continue;
    if(mode&&(mod(r,1714)!=1||(mod(r,12)!=1&&mod(r,12)!=11)||A%r!=0))continue;
    assert(pw(r,d-1)>room);
   }
  }
 }
 assert(count==(mode?60008:4796)&&fermat==(mode?860:77));
 std::cout<<"PASS "<<mode<<" "<<s<<" "<<H<<" "<<count<<" "<<fermat<<"\n";
}
