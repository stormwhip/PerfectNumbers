#pragma once
#include <gmpxx.h>
#include <cstdint>

// Independent exact-integer inequalities for an odd-perfect-number factor chain.
// Each inexact exponent a represents a true exponent e >= a with (a+1)|(e+1).
namespace opn {
// For even a, sigma(p^a) is odd, coprime to p, and divides N.
// Thus N >= p^a * sigma(p^a) > p^(2a).
// half_bound = 10^ceil(bound_exponent/2), an integer conservative threshold.
inline bool even_exponent_power_exceeds_half_bound(const mpz_class& p, uint64_t a,
                                                  const mpz_class& half_bound) {
    if (a & 1ULL) return false;
    mpz_class power;
    mpz_pow_ui(power.get_mpz_t(), p.get_mpz_t(), static_cast<unsigned long>(a));
    return power > half_bound;
}

// If every previously selected branch is compatible with N, earlier | N.
// Likewise p^a | N, and the odd part of sigma(p^a) divides N, including
// inexact a because (a+1)|(e+1) implies sigma(p^a)|sigma(p^e)|2N.
// Their least common multiple is therefore a mandatory divisor of N.
// No primality test or factor-database assumption is used in this cut.
inline mpz_class extend_forced_divisor(const mpz_class& earlier,
                                      const mpz_class& p, uint64_t a) {
    mpz_class power, sigma_odd, required;
    mpz_pow_ui(power.get_mpz_t(), p.get_mpz_t(), static_cast<unsigned long>(a));
    sigma_odd = power * p - 1;
    sigma_odd /= p - 1;
    while (mpz_even_p(sigma_odd.get_mpz_t())) sigma_odd >>= 1;
    mpz_lcm(required.get_mpz_t(), earlier.get_mpz_t(), power.get_mpz_t());
    mpz_lcm(required.get_mpz_t(), required.get_mpz_t(), sigma_odd.get_mpz_t());
    return required;
}
}
