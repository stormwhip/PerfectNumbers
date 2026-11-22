#include "SigmaPrecheck.hpp"

#include <cassert>
#include <iostream>

int main() {
    using namespace sigma_precheck;
    const uint64_t primes[] = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 127};
    uint64_t checks = 0;
    for (uint64_t p : primes) {
        for (uint64_t d = 1; d <= 16; ++d) {
            __uint128_t sigma = 1, power = 1;
            for (uint64_t i = 0; i < d; ++i) {
                power *= p;
                sigma += power;
            }
            assert(divisible_by_four(p % 4, d) == (sigma % 4 == 0));
            for (uint64_t q : primes) {
                for (uint64_t k = 1; k <= 5; ++k) {
                    const uint64_t m = modulus(q, k, UINT64_MAX);
                    const bool direct = sigma % m == 0;
                    assert(valuation_at_least(p % m, d + 1, q, m) == direct);
                    ++checks;
                }
            }
        }
    }
    assert(valuation_at_least(127 % 9, 9, 3, 9));
    assert(valuation_at_least(11, 21, 7, 49));
    assert(modulus(3, 40, UINT64_MAX) != 0);
    assert(modulus(3, 41, UINT64_MAX) == 0);
    std::cout << "SigmaPrecheckTests: " << checks << " exact valuation comparisons passed\n";
}
