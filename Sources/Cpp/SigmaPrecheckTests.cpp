#include "SigmaPrecheck.hpp"
#include <gmpxx.h>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

static void require(bool v, const char* what) {
    if (!v) throw std::runtime_error(what);
}

int main() {
    unsigned long long checked = 0;
    const std::vector<uint64_t> primes = {3, 5, 7, 11, 13, 17};
    for (uint64_t p = 3; p <= 35; p += 2) {
        for (uint64_t a = 1; a <= 70; ++a) {
            mpz_class power;
            mpz_ui_pow_ui(power.get_mpz_t(), p, a + 1);
            mpz_class sigma = (power - 1) / (p - 1);
            require(sigma_precheck::divisible_by_four(p % 4, a) ==
                    (mpz_fdiv_ui(sigma.get_mpz_t(), 4) == 0),
                    "divisibility by 4 mismatch");
            for (uint64_t q : primes) {
                for (uint64_t k = 1; k <= 5; ++k) {
                    uint64_t m = sigma_precheck::modulus(q, k, 1000000000ULL);
                    if (m == 0) continue;
                    bool actual = mpz_fdiv_ui(sigma.get_mpz_t(), m) == 0;
                    bool evaluated = sigma_precheck::valuation_at_least(p % m, a + 1, q, m);
                    require(actual == evaluated, "sigma valuation mismatch");
                    ++checked;
                }
            }
        }
    }

    const uint64_t large_q = 4294967291ULL;
    const uint64_t large_m = sigma_precheck::modulus(large_q, 2, UINT64_MAX);
    require(large_m > (UINT64_MAX / 2), "large modulus construction failed");
    require(sigma_precheck::modulus(large_q, 3, UINT64_MAX) == 0,
            "overflowing modulus must disable precheck");
    for (uint64_t p : {3ULL, 7ULL, 9876543219876543ULL,
                       18446744073709551557ULL}) {
        for (uint64_t count = 1; count <= 100; ++count) {
            mpz_class source(p), power;
            mpz_pow_ui(power.get_mpz_t(), source.get_mpz_t(), count);
            mpz_class sigma = (power - 1) / (source - 1);
            const bool actual = mpz_divisible_ui_p(sigma.get_mpz_t(), large_m) != 0;
            const bool evaluated = sigma_precheck::valuation_at_least(
                p % large_m, count, large_q, large_m);
            require(actual == evaluated, "large-modulus sigma valuation mismatch");
            ++checked;
        }
    }
    std::cout << "SigmaPrecheckTests: PASS " << checked
              << " exact GMP comparisons" << std::endl;
}
