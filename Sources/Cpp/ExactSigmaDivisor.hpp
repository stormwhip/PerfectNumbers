#pragma once
#include <gmpxx.h>
#include <cstdint>

// Exact integer cuts for distinct prime-power branches of a hypothetical OPN.
namespace opn {
inline bool even_exponent_power_exceeds_half_bound(const mpz_class& p, uint64_t a,
                                                  const mpz_class& half_bound) {
    if (a & 1ULL) return false;
    mpz_class power;
    mpz_pow_ui(power.get_mpz_t(), p.get_mpz_t(), static_cast<unsigned long>(a));
    return power > half_bound;
}

struct ExactDivisorProducts {
    mpz_class powers = 1;      // Product of all selected distinct prime powers.
    mpz_class sigma_odds = 1;  // Product of the odd parts of their sigma values.
};

// Each representative a satisfies a+1 | e+1, hence sigma(p^a) | sigma(p^e).
// Since sigma(N) = 2N is a PRODUCT over distinct primes p, the product of
// odd sigma(p^a) values divides N, even when those sigma values share factors.
// Keeping the product is stronger than merely taking the LCM of individual
// sigma factors. Both products divide N, so their LCM divides N exactly.
// This cut uses no factorization or probabilistic primality testing.
inline ExactDivisorProducts extend_forced_products(const ExactDivisorProducts& earlier,
                                                   const mpz_class& p, uint64_t a) {
    ExactDivisorProducts result = earlier;
    mpz_class power, sigma_odd;
    mpz_pow_ui(power.get_mpz_t(), p.get_mpz_t(), static_cast<unsigned long>(a));
    sigma_odd = power * p - 1;
    sigma_odd /= p - 1;
    while (mpz_even_p(sigma_odd.get_mpz_t())) sigma_odd >>= 1;
    result.powers *= power;
    result.sigma_odds *= sigma_odd;
    return result;
}

inline mpz_class mandatory_divisor(const ExactDivisorProducts& products) {
    mpz_class required;
    mpz_lcm(required.get_mpz_t(), products.powers.get_mpz_t(),
            products.sigma_odds.get_mpz_t());
    return required;
}
}
