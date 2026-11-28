// Read-only scan of all serialized factor strings, not just indexed matches.
#include <gmpxx.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstdio>
#include <string>
#include <vector>
#include <cassert>
#include <ctime>
using namespace std; using UL=unsigned long;
const unsigned char* load(const char* name,UL &size){int fd=open(name,O_RDONLY);assert(fd>=0);struct stat st;assert(fstat(fd,&st)==0);size=st.st_size;auto ans=(const unsigned char*)mmap(0,size,PROT_READ,MAP_PRIVATE,fd,0);assert(ans!=MAP_FAILED);return ans;}
struct Rec{UL h1,h2,pos;unsigned len,pad;};
int main(int argc,char**v){assert(argc==2);mpz_class n(v[1]),prod=1;UL nidx,ndat;auto ix=(const Rec*)load("/home/storm/opn/facts.idx",nidx);auto dat=load("/home/storm/opn/facts.dat",ndat);assert(sizeof(Rec)==32 && nidx%32==0);vector<unsigned char> flag(ndat/8+1);for(UL i=0;i<nidx/32;i++){UL p=ix[i].pos;assert(p+ix[i].len<=ndat);flag[p/8]|=1<<(p%8);}UL count=0,large=0;vector<mpz_class> batch;
auto flush=[&](){mpz_class g;mpz_gcd(g.get_mpz_t(),prod.get_mpz_t(),n.get_mpz_t());if(g!=1){for(auto &p:batch){mpz_gcd(g.get_mpz_t(),p.get_mpz_t(),n.get_mpz_t());if(g>1)gmp_printf("factor %Zd from %Zd\n",g.get_mpz_t(),p.get_mpz_t());}}batch.clear();prod=1;};auto step=[&](UL lo,UL hi){if(hi<=lo)return;count++;if(hi-lo<11)return;large++;mpz_class x(string((const char*)dat+lo,hi-lo));batch.push_back(x);prod*=x;prod%=n;if(batch.size()==512)flush();};UL lo=0;for(UL j=0;j<ndat;j++){if(dat[j]==' '){step(lo,j);lo=j+1;}else if(flag[j/8]&(1<<(j%8))){step(lo,j);lo=j;}}step(lo,ndat);flush();printf("rows=%lu tokens=%lu length>=11=%lu cpu_seconds=%.2f\n",nidx/32,count,large,(double)clock()/CLOCKS_PER_SEC);}
