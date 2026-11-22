#pragma once

#include <algorithm>
#include <cstdint>
#include <utility>

namespace opn_roadblock {

using Int = __int128_t;
constexpr int64_t Scale = int64_t{1} << 40;
constexpr int64_t Den = int64_t{1} << 24;

inline Int ceil_div(Int n, Int d) {
    return n / d + (n % d != 0);
}

// 20 positive terms of the atanh series with directed integer arithmetic.
// The remaining tail after multiplication by two is bounded by 3*z^41.
inline std::pair<Int, Int> unit_log(Int n, Int d) {
    const Int zl = Scale * (n - d) / (n + d);
    const Int zh = ceil_div(Scale * (n - d), n + d);
    const Int scale2 = Int(Scale) * Scale;
    Int pl = zl, ph = zh, lo = 0, hi = 0;
    for (int i = 1; i <= 39; i += 2) {
        lo += pl / i;
        hi += ceil_div(ph, i);
        pl = pl * zl * zl / scale2;
        ph = ceil_div(ph * zh * zh, scale2);
    }
    return {2 * lo, 2 * hi + 3 * ph};
}

inline std::pair<Int, Int> log_ratio(uint64_t num, uint64_t den = 1) {
    const auto ln2 = unit_log(2, 1);
    Int n = num, d = den;
    int shift = 0;
    while (2 * d <= n) {
        d *= 2;
        ++shift;
    }
    const auto core = unit_log(n, d);
    return {core.first + shift * ln2.first, core.second + shift * ln2.second};
}

struct Dual {
    Int value;
    Int slope;
    Int gamma = 0;
    Int gamma_slope = 0;

    Dual(Int gap, int64_t mu) : value(gap * mu), slope(gap) {}

    void special_gain(Int gain, Int derivative) {
        if (gain > gamma) {
            gamma = gain;
            gamma_slope = derivative;
        }
    }

    void add(Int log_low, Int abund_high, int exponent, bool special, int64_t mu) {
        const Int cost = log_low * Den;
        const Int reward = abund_high * mu;
        const Int ordinary = exponent * cost - reward;
        if (ordinary < 0) {
            value += ordinary;
            slope -= abund_high;
        }
        if (special) {
            special_gain(std::min<Int>(0, ordinary) + reward - cost,
                         ordinary >= 0 ? abund_high : 0);
        }
    }

    bool passes(Int budget) const { return value - gamma >= (budget + 1) * Den; }
    Int supergradient() const { return slope - gamma_slope; }
};

}  // namespace opn_roadblock
