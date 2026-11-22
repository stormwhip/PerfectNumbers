#define main ProofTreeProgramMain
#include "ProofTreeV7.cpp"
#undef main

#include <cassert>
#include <cmath>

static bool CoversExponent(uint64_t actual, const std::vector<std::pair<uint64_t, bool>>& exps) {
    for (const auto& [candidate, exact] : exps) {
        if (exact && candidate == actual) return true;
        if (!exact && candidate <= actual && (actual + 1) % (candidate + 1) == 0) return true;
    }
    return false;
}

int main() {
    init_primes(300000);
    LOG_BOUND = 10000.0;
    for (uint32_t p : {3U, 7U, 11U, 13U, 17U}) {
        State st;
        auto exps = get_exponents(st, mpz_class(p));
        for (uint64_t a = 1; a <= 2048; ++a) {
            bool valid = ((a & 1) == 0) || ((p % 4 == 1) && (a % 4 == 1));
            if (valid && !CoversExponent(a, exps)) {
                std::cerr << "Uncovered prime " << p << " exponent " << a << "\n";
                return 1;
            }
        }
    }

    State st;
    st.composites.push_back(mpz_class(15));
    st.composites.push_back(mpz_class(21));
    refresh_composite_size_bound(st);
    assert(std::abs(st.log_size_comp - std::log(15.0)) < 1e-9);

    st.branched[mpz_class(3)] = {2, true, 0};
    refresh_composite_size_bound(st);
    assert(std::abs(st.log_size_comp) < 1e-9);
    st.composites.push_back(mpz_class(25));
    refresh_composite_size_bound(st);
    assert(std::abs(st.log_size_comp - std::log(25.0)) < 1e-9);

    State rb;
    rb.has_special = true;
    assert(compute_roadblock_bound(rb, 1000000.0, 0.01) == 0);
    std::cout << "ProofCoreTestsV7: OK" << std::endl;
    return 0;
}
