#define main ProofTreeProgramMain
#include "ProofTreeReduced.cpp"
#undef main
#include <cassert>
int main() {
    const std::vector<uint32_t> expected = {19, 7, 11, 31, 13, 3, 5, 17};
    assert(S_ORDER == expected);
    init_primes(300000);
    LOG_BOUND = 300.0 * std::log(10.0);
    for (uint32_t p : S_ORDER) {
        State st;
        auto options = get_exponents(st, mpz_class(p));
        assert(!options.empty());
    }
    std::cout << "ReducedRootTests: OK" << std::endl;
    return 0;
}
