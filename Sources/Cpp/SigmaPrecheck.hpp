#pragma once
#include <cstdint>
#include <utility>

// Standalone exact G2/G3 precheck, restored after the PascalCase directory migration.
// Unsupported/overflowing powers return 0, disabling a prune conservatively.
namespace sigma_precheck {

inline bool divisible_by_four(uint64_t p_mod4, uint64_t a) {
    if ((p_mod4 & 1u) == 0u) return false;
    if ((p_mod4 & 3u) == 1u) return (a & 3u) == 3u;
    return (a & 1u) == 1u;
}

inline uint64_t modulus(uint64_t q, uint64_t k, uint64_t limit) {
    if (q < 2 || k == 0) return 0;
    uint64_t m = 1;
    for (uint64_t i = 0; i < k; ++i) {
        if (m > limit / q) return 0;
        m *= q;
    }
    return m;
}

inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t mod) {
    return static_cast<uint64_t>((static_cast<__uint128_t>(a) * b) % mod);
}

inline uint64_t add_mod(uint64_t a, uint64_t b, uint64_t mod) {
    return static_cast<uint64_t>((static_cast<__uint128_t>(a) + b) % mod);
}

inline std::pair<uint64_t, uint64_t> power_sum_mod(uint64_t a, uint64_t n, uint64_t mod) {
    // Return (a^n mod mod, (1+a+...+a^(n-1)) mod mod).
    // Doubling: S_(2n) = S_n * (1+a^n), P_(2n) = P_n^2.
    uint64_t p = 1 % mod, s = 0;
    uint64_t bp = a % mod, bs = 1 % mod;
    while (n) {
        if (n & 1u) {
            s = add_mod(s, mul_mod(p, bs, mod), mod);
            p = mul_mod(p, bp, mod);
        }
        bs = add_mod(bs, mul_mod(bp, bs, mod), mod);
        bp = mul_mod(bp, bp, mod);
        n >>= 1;
    }
    return {p, s};
}

inline bool valuation_at_least(uint64_t p_mod, uint64_t terms, uint64_t q, uint64_t mod) {
    if (terms == 0 || q < 2 || mod < 2 || mod % q != 0) return false;
    return power_sum_mod(p_mod, terms, mod).second == 0;
}

} // namespace sigma_precheck
