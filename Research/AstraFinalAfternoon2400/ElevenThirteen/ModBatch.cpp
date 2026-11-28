// Optional GMP accelerator for exact modular exponentiations. No PRP library calls.
#include <gmp.h>
#include <iostream>
#include <sstream>
#include <string>
#include <cassert>
int main(){
  std::string line; mpz_t n, e, a, r;
  mpz_inits(n,e,a,r,nullptr);
  while(std::getline(std::cin,line)){
    std::istringstream input(line); std::string word,tail;
    if(!(input>>word) || input>>tail) return 2;
    if(mpz_set_str(n,word.c_str(),16)!=0 || mpz_cmp_ui(n,5)<=0 || mpz_even_p(n)) return 3;
    mpz_sub_ui(e,n,1);
    mpz_set_ui(a,2);mpz_powm(r,a,e,n);
    if(mpz_cmp_ui(r,1)!=0){std::cout<<"2\n";continue;}
    mpz_set_ui(a,3);mpz_powm(r,a,e,n);
    std::cout<<(mpz_cmp_ui(r,1)==0?0:3)<<'\n';
  }
  mpz_clears(n,e,a,r,nullptr);
  return std::cin.eof()?0:4;
}
