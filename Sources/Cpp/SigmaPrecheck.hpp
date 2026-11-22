#pragma once

#include <cstdint>
#include <limits>

namespace sigma_precheck {

inline bool divisible_by_four(unsigned p_mod_four, uint64_t d) {
    return (d & 1) && (p_mod_four == 3 || (d & 3) == 3);
}

// Zero means the requested prime power does not fit the configured modulus.
inline uint64_t modulus(uint64_t q, uint64_t exponent, uint64_t limit) {
    uint64_t result = 1;
    for (uint64_t i = 0; i < exponent; ++i) {
        if (result > limit / q) return 0;
        result *= q;
    }
    return result;
}

// q is an odd prime and prime_power is q^k. base is p reduced modulo q^k.
inline bool valuation_at_least(uint64_t base, uint64_t dp1, uint64_t q,
                               uint64_t prime_power) {
    if (base % q == 0) return false;
    if (base % q == 1) return dp1 % prime_power == 0;
    uint64_t value = 1;
    while (dp1) {
        if (dp1 & 1) value = static_cast<__uint128_t>(value) * base % prime_power;
        base = static_cast<__uint128_t>(base) * base % prime_power;
        dp1 >>= 1;
    }
    return value == 1;
}

}  // namespace sigma_precheck
