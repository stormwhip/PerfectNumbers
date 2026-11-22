#include <gmpxx.h>
#include <vector>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <stdexcept>
#include <cmath>
using namespace std;
int main(int argc, char** argv) {
    uint32_t limit = argc > 1 ? static_cast<uint32_t>(strtoul(argv[1], nullptr, 10)) : 1000000U;
    if (limit < 1009 || limit > 100000000) throw runtime_error("limit outside [1009, 100000000]");
    auto start=chrono::steady_clock::now();
    // Deterministic odd-number sieve, independent of probabilistic primality tests.
    vector<unsigned char> composite(limit/2+1, 0);
    for(uint32_t q=3; uint64_t(q)*q<=limit; q+=2) {
        if(composite[q/2]) continue;
        for(uint64_t x=uint64_t(q)*q; x<=limit; x+=2*uint64_t(q))
            composite[static_cast<size_t>(x/2)]=1;
    }
    vector<mpz_class> levels;
    mpz_class block(1);
    uint32_t pc=0, within=0;
    for(uint32_t q=1001; q<=limit; q+=2) {
        if(composite[q/2]) continue;
        mpz_mul_ui(block.get_mpz_t(), block.get_mpz_t(), q);
        ++pc; ++within;
        if(within==1024) {levels.push_back(block);block=1;within=0;}
    }
    if(within) levels.push_back(block);
    if(levels.empty()) throw runtime_error("empty prime set");
    while(levels.size()>1) {
        vector<mpz_class> next;
        next.reserve((levels.size()+1)/2);
        for(size_t i=0;i<levels.size();i+=2) {
            if(i+1<levels.size())next.push_back(levels[i]*levels[i+1]);
            else next.push_back(levels[i]);
        }
        levels.swap(next);
    }
    mpz_class primorial=std::move(levels[0]);
    auto finish=chrono::steady_clock::now();
    double build_s=chrono::duration<double>(finish-start).count();
    cout << "PRIMORIAL_BUILD cutoff="<<limit<<" primes="<<pc
         <<" bits="<<mpz_sizeinbase(primorial.get_mpz_t(),2)
         <<" seconds="<<setprecision(9)<<build_s<<"\n";
    // A composite with both primes just above 1000 must be rejected by the
    // hypothetical 1e8 alpha assumption, and gcd detects it exactly.
    mpz_class bad=mpz_class(1009)*mpz_class(1013),g;
    mpz_gcd(g.get_mpz_t(),bad.get_mpz_t(),primorial.get_mpz_t());
    if(limit>=1013 && g!=bad) throw runtime_error("false exclusion for small composite");
    mpz_class after;
    mpz_nextprime(after.get_mpz_t(),mpz_class(limit).get_mpz_t());
    mpz_gcd(g.get_mpz_t(),after.get_mpz_t(),primorial.get_mpz_t());
    if(g!=1) throw runtime_error("false rejection for prime beyond cutoff");
    cout<<"CUTOFF_CERT_TEST_OK small_composite="<<bad<<" beyond_prime="<<after<<"\n";
    for(int digits : {40,300,1000}) {
        mpz_class rem;
        mpz_ui_pow_ui(rem.get_mpz_t(),10,digits);
        rem+=321;
        const int tries=8;
        auto t0=chrono::steady_clock::now();
        for(int j=0;j<tries;j++) {
            mpz_gcd(g.get_mpz_t(),rem.get_mpz_t(),primorial.get_mpz_t());
            rem+=2;
        }
        auto t1=chrono::steady_clock::now();
        double ms=1000.0*chrono::duration<double>(t1-t0).count()/tries;
        cout<<"CUTOFF_GCD digits="<<digits<<" mean_ms="<<ms<<"\n";
    }
    FILE* out=fopen("PrimeCutoffProduct.bin","wb");
    if(!out)throw runtime_error("cannot write product");
    if(mpz_out_raw(out,primorial.get_mpz_t())==0)throw runtime_error("cannot serialize product");
    fclose(out);
    cout<<"CUTOFF_RESULT=PASS; gcd(R,PrimeCutoffProduct.bin)=1 excludes all primes 1000<p<=cutoff exactly\n";
}
