#pragma once

#include "RoadblockPilotArithmetic.hpp"

namespace opn_roadblock {

std::vector<std::pair<Int,Int>> prime_bounds;
std::pair<Int,Int> tail_bounds;
mpz_class trial_product = 1;
Int target_high;
int pilot_mode = 0;
std::atomic<unsigned> trace_count{0};

void init(int exponent) {
    const char* mode = std::getenv("OPN_ROADBLOCK_MODE");
    if (mode && std::string(mode) == "shadow") pilot_mode = 1;
    if (mode && std::string(mode) == "certified") pilot_mode = 2;
    if (!pilot_mode) return;
    target_high = exponent * log_ratio(10).second;
    for (uint32_t q : small_primes) {
        prime_bounds.push_back({log_ratio(q).first, log_ratio(q, q-1).second});
        if (q <= 1000) trial_product *= q;
    }
    const uint32_t tail = small_primes.back() + 1;
    tail_bounds = {log_ratio(tail).first, log_ratio(tail, tail-1).second};
}

Int log_integer_lower(const mpz_class& x) {
    const size_t bits = mpz_sizeinbase(x.get_mpz_t(), 2);
    const size_t shift = bits > 48 ? bits - 48 : 0;
    const mpz_class top = x >> shift;
    return log_ratio(top.get_ui()).first + Int(shift) * log_ratio(2).first;
}

Int prime_abundancy_upper(const mpz_class& p, const BranchedInfo& info) {
    if (mpz_sizeinbase(p.get_mpz_t(), 2) > 48) return 1;
    const uint64_t q = p.get_ui();
    if (info.exact && info.exp == 1) return log_ratio(q + 1, q).second;
    return log_ratio(q, q - 1).second;
}

bool residual_upper(const mpz_class& c, bool strong, Int& upper) {
    thread_local std::unordered_map<std::string, Int> cache;
    if (cache.size() > 4096) cache.clear();
    const std::string key = std::string(strong ? "S" : "W") + c.get_str();
    const auto it = cache.find(key);
    if (it != cache.end()) {
        upper = it->second;
        return true;
    }
    mpz_class g;
    mpz_gcd(g.get_mpz_t(), c.get_mpz_t(), trial_product.get_mpz_t());
    if (g != 1) return false;
    const Int small = log_ratio(1009, 1008).second;
    if (!strong) {
        upper = prime_power_count_upper(c, 1009) * small;
    } else {
        mpz_class rest = c, extracted = 1;
        while (rest > 1) {
            mpz_gcd(g.get_mpz_t(), rest.get_mpz_t(), PRIME_CUTOFF_PRODUCT.get_mpz_t());
            if (g == 1) break;
            extracted *= g;
            rest /= g;
        }
        upper = prime_power_count_upper(extracted, 1009) * small +
                prime_power_count_upper(rest, 100000001) *
                    log_ratio(100000001, 100000000).second;
    }
    cache.emplace(key, upper);
    return true;
}

struct Witness {
    int boundary = 0;
    int64_t multiplier = 0;
    Int numerator = 0;
    unsigned evaluations = 0;
};

Witness select(const State& st, uint32_t legacy) {
    Witness witness;
    Int size = 0, abundance = 0;
    mpz_class counted = 1, g;
    for (const auto& [p, info] : st.branched) {
        size += info.exp * log_integer_lower(p);
        abundance += prime_abundancy_upper(p, info);
        counted *= p;
    }
    for (size_t i = 0; i < st.composites.size(); ++i) {
        const auto& c = st.composites[i];
        Int ab = 0;
        if (!residual_upper(c, i < st.certified_residue_count, ab)) return witness;
        abundance += ab;
        mpz_gcd(g.get_mpz_t(), c.get_mpz_t(), counted.get_mpz_t());
        if (g == 1) {
            counted *= c;
            size += log_integer_lower(c);
        }
    }
    const Int budget = target_high - size;
    if (budget < 0) { witness.boundary = -1; return witness; }
    const Int gap = log_ratio(2).first - abundance;
    if (gap <= 0) return witness;
    const int64_t cap = static_cast<int64_t>(2 * tail_bounds.first * Den / tail_bounds.second);
    const Int lower = ceil_div((budget + 1) * Den, gap);
    if (lower > cap) return witness;

    std::set<uint32_t> forbidden, expanded;
    const auto last = small_primes.back();
    for (const auto& p : st.forbidden)
        if (p.fits_uint_p() && p.get_ui() <= last) forbidden.insert(p.get_ui());
    for (const auto& [p, info] : st.branched)
        if (p.fits_uint_p() && p.get_ui() <= last) expanded.insert(p.get_ui());

    auto try_boundary = [&](uint32_t b) {
        auto blocked = [&](uint32_t r) {
            return forbidden.count(r) || (r < b && !expanded.count(r));
        };
        const auto start = std::lower_bound(small_primes.begin(), small_primes.end(), b);
        auto evaluate = [&](int64_t mu) {
            ++witness.evaluations;
            Dual value(gap, mu);
            if (!st.has_special)
                value.special_gain(tail_bounds.second * mu - tail_bounds.first * Den,
                                   tail_bounds.second);
            for (size_t i = start - small_primes.begin(); i < small_primes.size(); ++i) {
                const auto [lo, hi] = prime_bounds[i];
                if (lo * Den >= hi * mu) break;
                const uint32_t q = small_primes[i];
                if (forbidden.count(q) || expanded.count(q)) continue;
                const bool even4 = std::any_of(sigma2_factors[i].begin(), sigma2_factors[i].end(), blocked);
                const bool sp = !st.has_special && q % 4 == 1 &&
                    std::none_of(sigma1_factors[i].begin(), sigma1_factors[i].end(), blocked);
                value.add(lo, hi, even4 ? 4 : 2, sp, mu);
            }
            if (value.passes(budget)) {
                witness.boundary = b;
                witness.multiplier = mu;
                witness.numerator = value.value - value.gamma;
            }
            return value.supergradient();
        };
        // An inexpensive witness usually wins before the bounded search.
        int64_t lo = static_cast<int64_t>(lower), hi = cap;
        const auto [l, h] = prime_bounds[start - small_primes.begin()];
        const int64_t hint = std::clamp(static_cast<int64_t>(2 * l * Den / h), lo, hi);
        evaluate(hint);
        if (witness.boundary == static_cast<int>(b)) return;
        for (int i = 0; i < 14 && lo <= hi; ++i) {
            const int64_t mid = lo + (hi - lo) / 2;
            const Int slope = evaluate(mid);
            if (witness.boundary == static_cast<int>(b) || slope == 0) return;
            if (slope > 0) lo = mid + 1;
            else hi = mid - 1;
        }
    };

    uint32_t b = legacy ? legacy : 3;
    for (unsigned tries = 0; tries < 12; ++tries) {
        try_boundary(b);
        if (witness.boundary || b == last) return witness;
        b = std::min(last, tries == 10 ? last : 2 * b);
    }
    return witness;
}

Witness run(const State& st, uint32_t legacy, int depth) {
    const auto witness = select(st, legacy);
    if (trace_count.fetch_add(1, std::memory_order_relaxed) < 20) {
        std::lock_guard<std::mutex> lock(print_mtx);
        std::cerr << "RB_PILOT mode=" << pilot_mode << " depth=" << depth
                  << " legacy=" << legacy << " certified=" << witness.boundary
                  << " mu_num=" << witness.multiplier << " evaluations=" << witness.evaluations
                  << " residuals=" << st.composites.size() << '\n';
    }
    return witness;
}

}  // namespace opn_roadblock
