#include <gmpxx.h>
#include <omp.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstdint>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <chrono>
#include <atomic>
#include <mutex>
#include <utility>
#include <thread>
#include <condition_variable>
#include <array>
#include <fstream>
#include <sstream>
#include <stdexcept>

struct IdxEntry {
    uint64_t h1;
    uint64_t h2;
    uint64_t offset;
    uint32_t len;
};

static inline void hash128(const char* s, size_t n, uint64_t& h1, uint64_t& h2) {
    uint64_t a = 14695981039346656037ULL;
    uint64_t b = 1099511628211ULL ^ 0x9e3779b97f4a7c15ULL;
    for (size_t i = 0; i < n; ++i) {
        uint8_t c = static_cast<uint8_t>(s[i]);
        a ^= c; a *= 1099511628211ULL;
        b ^= c; b *= 0xbf58476d1ce4e5b9ULL;
        b ^= (b >> 31);
    }
    h1 = a; h2 = b;
}

class FactDB {
    const IdxEntry* idx_ptr = nullptr;
    size_t idx_cnt = 0;
    const char* dat_ptr = nullptr;
    size_t dat_sz = 0;
    int fd_idx = -1, fd_dat = -1;

public:
    bool load(const char* idx_path, const char* dat_path) {
        struct stat st;
        fd_idx = open(idx_path, O_RDONLY);
        if (fd_idx < 0 || fstat(fd_idx, &st) < 0) return false;
        idx_cnt = st.st_size / sizeof(IdxEntry);
        idx_ptr = static_cast<const IdxEntry*>(mmap(nullptr, st.st_size, PROT_READ, MAP_PRIVATE, fd_idx, 0));

        fd_dat = open(dat_path, O_RDONLY);
        if (fd_dat < 0 || fstat(fd_dat, &st) < 0) return false;
        dat_sz = st.st_size;
        dat_ptr = static_cast<const char*>(mmap(nullptr, dat_sz, PROT_READ, MAP_PRIVATE, fd_dat, 0));
        return idx_ptr != MAP_FAILED && dat_ptr != MAP_FAILED;
    }

    ~FactDB() {
        if (idx_ptr && idx_ptr != MAP_FAILED) munmap(const_cast<IdxEntry*>(idx_ptr), idx_cnt * sizeof(IdxEntry));
        if (dat_ptr && dat_ptr != MAP_FAILED) munmap(const_cast<char*>(dat_ptr), dat_sz);
        if (fd_idx >= 0) close(fd_idx);
        if (fd_dat >= 0) close(fd_dat);
    }

    std::vector<mpz_class> lookup(const std::string& key) const {
        uint64_t h1, h2;
        hash128(key.data(), key.size(), h1, h2);

        IdxEntry target{h1, h2, 0, 0};
        auto it = std::lower_bound(idx_ptr, idx_ptr + idx_cnt, target, [](const IdxEntry& a, const IdxEntry& b) {
            if (a.h1 != b.h1) return a.h1 < b.h1;
            return a.h2 < b.h2;
        });

        std::vector<mpz_class> res;
        while (it != idx_ptr + idx_cnt && it->h1 == h1 && it->h2 == h2) {
            const char* s = dat_ptr + it->offset;
            const char* end = s + it->len;
            while (s < end) {
                while (s < end && *s == ' ') ++s;
                const char* t = s;
                while (t < end && *t != ' ') ++t;
                if (t > s) res.emplace_back(std::string(s, t - s));
                s = t;
            }
            ++it;
        }
        return res;
    }
};

std::vector<uint32_t> small_primes;
std::vector<double> small_prime_log;
std::vector<double> small_prime_inf_abund;
// 预计算：sigma(q^1)/2 的奇素因子，以及 sigma(q^2) = q^2+q+1 的小素因子（<=1000）
std::vector<std::vector<uint32_t>> sigma1_factors;
std::vector<std::vector<uint32_t>> sigma2_factors;

void init_primes(uint32_t limit) {
    std::vector<uint32_t> spf(limit + 1, 0);
    for (uint32_t i = 2; i <= limit; ++i) {
        if (spf[i] == 0) {
            spf[i] = i;
            small_primes.push_back(i);
            small_prime_log.push_back(std::log(static_cast<double>(i)));
            small_prime_inf_abund.push_back(std::log(static_cast<double>(i) / (i - 1.0)));
        }
        for (uint32_t p : small_primes) {
            if (p > spf[i] || static_cast<uint64_t>(i) * p > limit) break;
            spf[i * p] = p;
        }
    }

    // 预计算用于 sigma(q^2) 试除的素数（3 以及 <= 1000 且 mod 3 == 1 的素数）
    std::vector<uint32_t> s2_divisors = {3};
    for (uint32_t p : small_primes) {
        if (p > 1000) break;
        if (p % 3 == 1) s2_divisors.push_back(p);
    }

    size_t n = small_primes.size();
    sigma1_factors.resize(n);
    sigma2_factors.resize(n);

    for (size_t i = 1; i < n; ++i) { // 跳过 2
        uint32_t q = small_primes[i];
        // 1) 若 q == 1 (mod 4)，分解 (q+1)/2
        if ((q & 3) == 1) {
            uint32_t x = (q + 1) >> 1;
            while (x > 1) {
                uint32_t f = spf[x];
                if (f > 2) sigma1_factors[i].push_back(f);
                while (x % f == 0) x /= f;
            }
        }
        // 2) 提取 q^2 + q + 1 的小素因子（全部 < 10^8，不可能落入未分解合数）
        uint64_t val2 = static_cast<uint64_t>(q) * q + q + 1;
        for (uint32_t r : s2_divisors) {
            if (val2 % r == 0) {
                sigma2_factors[i].push_back(r);
                while (val2 % r == 0) val2 /= r;
            }
        }
    }
}

static inline double mpz_log(const mpz_class& x) {
    long exp;
    double d = mpz_get_d_2exp(&exp, x.get_mpz_t());
    return std::log(d) + exp * std::log(2.0);
}

static inline double ln_sigma_m1(const mpz_class& p, uint64_t a) {
    double lp = mpz_log(p);
    if (lp > 35.0) return std::exp(-lp);
    double pd = p.get_d();
    double term = std::log(pd / (pd - 1.0));
    if (a < 60) {
        double pa1 = std::pow(pd, -static_cast<double>(a + 1));
        if (pa1 > 1e-16) term += std::log1p(-pa1);
    }
    return term;
}

static inline double ln_inf_abund(const mpz_class& p) {
    double lp = mpz_log(p);
    if (lp > 35.0) return std::exp(-lp);
    double pd = p.get_d();
    return std::log(pd / (pd - 1.0));
}

static inline uint64_t pow_mod_u64(uint64_t base, uint64_t exp, uint64_t mod) {
    uint64_t res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (static_cast<__uint128_t>(res) * base) % mod;
        base = (static_cast<__uint128_t>(base) * base) % mod;
        exp >>= 1;
    }
    return res;
}

static inline bool small_prime_divides_sigma(const mpz_class& p, uint64_t a, uint32_t s) {
    uint64_t r = mpz_fdiv_ui(p.get_mpz_t(), s);
    if (r == 1) return ((a + 1) % s) == 0;
    if (r == 0) return false;
    return pow_mod_u64(r, a + 1, s) == 1;
}

struct SigmaFact {
    bool div_by_4 = false;
    std::vector<std::pair<mpz_class, uint64_t>> primes;
    mpz_class comp_rem = 1;
    double comp_log = 0.0;
    double certified_comp_abund_upper = 0.0;
};

// Exact product of primes from 1009 through 100,000,000, built by
// PrimeCutoffCert.cpp with a deterministic sieve. A gcd=1 proves that
// a residual has no such small prime divisor.
mpz_class PRIME_CUTOFF_PRODUCT;
std::atomic<uint64_t> screened_composites{0};
std::atomic<uint64_t> with_low_primes{0};
std::atomic<uint64_t> cutoff_gcd_nanoseconds{0};

bool load_prime_cutoff_product(const char* path) {
    FILE* f = std::fopen(path, "rb");
    if (!f) return false;
    const size_t count = mpz_inp_raw(PRIME_CUTOFF_PRODUCT.get_mpz_t(), f);
    std::fclose(f);
    return count > 0 && PRIME_CUTOFF_PRODUCT > 1;
}
static inline uint64_t prime_power_count_upper(mpz_class n, uint64_t minfactor) {
    uint64_t count = 0;
    while (n >= minfactor) {
        n /= minfactor;
        ++count;
    }
    return count;
}
double certify_sigma_residual_abundance_upper(const mpz_class& composite) {
    if (PRIME_CUTOFF_PRODUCT <= 1) {
        throw std::runtime_error("prime cutoff certificate not loaded");
    }
    screened_composites.fetch_add(1, std::memory_order_relaxed);
    auto time_start = std::chrono::steady_clock::now();
    mpz_class rem = composite, extracted = 1, common;
    bool found_small = false;
    while (rem > 1) {
        mpz_gcd(common.get_mpz_t(), rem.get_mpz_t(),
                PRIME_CUTOFF_PRODUCT.get_mpz_t());
        if (common == 1) break;
        found_small = true;
        extracted *= common;
        rem /= common;
    }
    if (found_small) with_low_primes.fetch_add(1, std::memory_order_relaxed);
    auto time_end = std::chrono::steady_clock::now();
    cutoff_gcd_nanoseconds.fetch_add(static_cast<uint64_t>(
        std::chrono::duration_cast<std::chrono::nanoseconds>(
             time_end - time_start).count()), std::memory_order_relaxed);
    // Both pieces are exact positive integers. The first has all prime
    // factors in [1009,1e8], whereas rem has none <=1e8; its factors are
    // therefore >=100000001. Each factor contributes at most q/(q-1).
    const uint64_t n_small = prime_power_count_upper(extracted, 1009);
    const uint64_t n_large = prime_power_count_upper(rem, 100000001);
    const double small_upper =
        std::nextafter(std::log1p(1.0 / 1008.0) + 1e-14,
                       std::numeric_limits<double>::infinity());
    const double large_upper =
        std::nextafter(std::log1p(1.0/100000000.0) + 1e-14,
                       std::numeric_limits<double>::infinity());
    return std::nextafter(
        static_cast<double>(n_small)*small_upper +
        static_cast<double>(n_large)*large_upper + 1e-12,
        std::numeric_limits<double>::infinity());
}

FactDB db;
thread_local std::unordered_map<std::string, SigmaFact> fact_cache;

const SigmaFact& get_sigma_fact(const mpz_class& p, uint64_t a) {
    std::string key = p.get_str() + " " + std::to_string(a + 1);
    auto it = fact_cache.find(key);
    if (it != fact_cache.end()) return it->second;

    if (fact_cache.size() > 150000) fact_cache.clear();

    SigmaFact res;
    mpz_class rem;
    mpz_pow_ui(rem.get_mpz_t(), p.get_mpz_t(), a + 1);
    rem -= 1;
    rem /= (p - 1);

    int v2 = mpz_scan1(rem.get_mpz_t(), 0);
    if (v2 >= 2) {
        res.div_by_4 = true;
        return fact_cache.emplace(std::move(key), std::move(res)).first->second;
    }
    if (v2 == 1) rem >>= 1;

    auto db_facts = db.lookup(key);
    for (const auto& f : db_facts) {
        if (f <= 2 || rem == 1) continue;
        uint64_t cnt = 0;
        while (mpz_divisible_p(rem.get_mpz_t(), f.get_mpz_t())) {
            rem /= f;
            ++cnt;
        }
        if (cnt > 0) res.primes.push_back({f, cnt});
    }

    if (rem > 1 && mpz_probab_prime_p(rem.get_mpz_t(), 5) == 0) {
        size_t digits = mpz_sizeinbase(rem.get_mpz_t(), 10);
        uint32_t trial_lim = (digits <= 10) ? 10000 : 1000;
        for (uint32_t sp : small_primes) {
            if (sp > trial_lim || rem == 1) break;
            if (digits <= 10 && mpz_cmp_ui(rem.get_mpz_t(), static_cast<uint64_t>(sp) * sp) < 0) break;
            if (mpz_divisible_ui_p(rem.get_mpz_t(), sp)) {
                uint64_t cnt = 0;
                while (mpz_divisible_ui_p(rem.get_mpz_t(), sp)) {
                    rem /= sp;
                    ++cnt;
                }
                res.primes.push_back({mpz_class(sp), cnt});
            }
        }
    }

    if (rem > 1) {
        if (mpz_probab_prime_p(rem.get_mpz_t(), 5) > 0) {
            res.primes.push_back({rem, 1});
            rem = 1;
        } else {
            res.comp_rem = rem;
            res.comp_log = mpz_log(rem);
            // The large gcd is deliberately DEFERRED until a weak safe
            // residual bound would cause an unresolved roadblock.
        }
    }

    return fact_cache.emplace(std::move(key), std::move(res)).first->second;
}

struct BranchedInfo {
    uint64_t exp;
    bool exact;
    uint64_t seen_in_sigma;
};

struct State {
    std::set<mpz_class> forbidden;
    std::vector<uint32_t> forbidden_small;
    std::map<mpz_class, BranchedInfo> branched;
    std::set<mpz_class> unbranched;
    std::vector<mpz_class> composites;
    bool has_special = false;
    double log_size_branched = 0.0;
    double log_size_comp = 0.0;
    double log_abund_lo = 0.0;
    double log_abund_hi = 0.0;
    double lp_known_abund_upper = 0.0;
    size_t certified_residue_count = 0; // Invariant: [0,count) uses the strong certified bound.
};

double LOG_BOUND = 0.0;
const double LN2 = std::log(2.0);
// Every still-composite sigma residual was trial-divided by all odd primes
// through 1000. Its least (unextracted) prime divisor is >=1009.
// The older ALPHA=1e8 was not justified by the actual runtime trial bound.
const uint64_t RESIDUAL_MIN_PRIME = 1009;
const double RESIDUAL_ABUND_UPPER =
    std::nextafter(std::log1p(1.0 / (RESIDUAL_MIN_PRIME - 1.0)) + 1e-14,
                   std::numeric_limits<double>::infinity());

static inline uint64_t residual_factor_count_upper(mpz_class rem) {
    // Exact integer bound: if all prime factors are >=1009, their count
    // with multiplicity is at most floor(log_1009(rem)).
    uint64_t count = 0;
    while (rem >= RESIDUAL_MIN_PRIME) {
        rem /= RESIDUAL_MIN_PRIME;
        ++count;
    }
    return count;
}

// Root order is optimized independently from the fixed circular partition order.
std::vector<uint32_t> ROOT_ORDER = {19, 7, 11, 31, 13, 3, 5, 17};
const std::vector<uint32_t> CIRC_ORDER = {19, 7, 11, 31, 13, 3, 5, 17};

struct PrefixDualBound {
    double lambda0_lower = 0.0;
    double intercept_lower = 0.0;
    bool valid = false;
    std::unordered_map<uint64_t, double> removable_gain;
    std::unordered_map<uint64_t, double> forced_gain;
};
std::array<PrefixDualBound, 256> PREFIX_DUALS;
uint32_t ACTIVE_PREFIX_MASK = 0;
std::atomic<uint64_t> state_lp_prunes{0};
std::atomic<uint64_t> state_lp_early_prunes{0};

bool load_prefix_duals(const char* path, const char* gain_path, const char* forced_path) {
    std::ifstream in(path);
    if (!in) return false;
    std::string line;
    if (!std::getline(in, line)) return false;
    size_t count = 0;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::array<std::string, 4> fields;
        for (size_t i = 0; i < fields.size(); ++i) {
            if (!std::getline(ss, fields[i], ',')) return false;
        }
        const unsigned mask = static_cast<unsigned>(std::stoul(fields[0]));
        if (mask >= PREFIX_DUALS.size() || PREFIX_DUALS[mask].valid) return false;
        PREFIX_DUALS[mask].lambda0_lower = std::stod(fields[1]);
        PREFIX_DUALS[mask].intercept_lower = std::stod(fields[2]);
        PREFIX_DUALS[mask].valid = true;
        ++count;
    }
    if (count != PREFIX_DUALS.size()) return false;
    std::ifstream gains_in(gain_path);
    if (!gains_in) return false;
    if (!std::getline(gains_in, line)) return false;
    while (std::getline(gains_in, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string mask_text, prime_text, gain_text;
        if (!std::getline(ss, mask_text, ',') ||
            !std::getline(ss, prime_text, ',') ||
            !std::getline(ss, gain_text, ',')) return false;
        const unsigned mask = static_cast<unsigned>(std::stoul(mask_text));
        const uint64_t prime = static_cast<uint64_t>(std::stoull(prime_text));
        const double gain = std::stod(gain_text);
        if (mask >= PREFIX_DUALS.size() || !PREFIX_DUALS[mask].valid || !(gain > 0.0)) return false;
        PREFIX_DUALS[mask].removable_gain[prime] = gain;
    }

    std::ifstream forced_in(forced_path);
    if (!forced_in || !std::getline(forced_in, line)) return false;
    while (std::getline(forced_in, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string mask_text, prime_text, gain_text;
        if (!std::getline(ss, mask_text, ',') ||
            !std::getline(ss, prime_text, ',') ||
            !std::getline(ss, gain_text, ',')) return false;
        const unsigned mask = static_cast<unsigned>(std::stoul(mask_text));
        const uint64_t prime = static_cast<uint64_t>(std::stoull(prime_text));
        const double gain = std::stod(gain_text);
        if (mask >= PREFIX_DUALS.size() || !PREFIX_DUALS[mask].valid ||
            !std::isfinite(gain) || !(gain > 0.0)) return false;
        PREFIX_DUALS[mask].forced_gain[prime] = gain;
    }
    return true;
}

static inline double lp_prime_abundancy_upper(const mpz_class& p) {
    const double lp = mpz_log(p);
    if (lp < 30.0) {
        const double pd = p.get_d();
        return std::nextafter(std::log(pd / (pd - 1.0)) + 1e-12,
                              std::numeric_limits<double>::infinity());
    }
    const double inv = std::exp(-lp);
    if (inv == 0.0) return 2e-323;
    return std::nextafter(1.50001 * inv,
                          std::numeric_limits<double>::infinity());
}

std::atomic<uint64_t> total_branches{0};
std::atomic<uint64_t> circ_branches{0};
std::atomic<uint64_t> failed_roadblocks{0};
std::atomic<uint32_t> max_rb_b{0};
std::atomic<int> heavy_rb_printed{0};
std::mutex print_mtx;

// Conservative composite size accounting: count only pairwise coprime residuals
// that are also coprime to every known prime divisor of the candidate.
void refresh_composite_size_bound(State& st) {
    st.log_size_comp = 0.0;
    std::vector<const mpz_class*> chosen;
    for (const auto& c : st.composites) {
        bool independent = true;
        for (const auto& [p, info] : st.branched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { independent = false; break; }
        }
        if (!independent) continue;
        for (const auto& p : st.unbranched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { independent = false; break; }
        }
        if (!independent) continue;
        for (const auto* d : chosen) {
            mpz_class g;
            mpz_gcd(g.get_mpz_t(), c.get_mpz_t(), d->get_mpz_t());
            if (g > 1) { independent = false; break; }
        }
        if (independent) {
            st.log_size_comp += mpz_log(c);
            chosen.push_back(&c);
        }
    }
}

bool check_state_lp_contradiction(const State& st) {
    // Forced but not-yet-branched primes remain represented by the residual LP.
    // Relaxing their mandatory presence is safe and allows earlier cuts.
    if (ACTIVE_PREFIX_MASK >= PREFIX_DUALS.size()) return false;
    const PrefixDualBound& cert = PREFIX_DUALS[ACTIVE_PREFIX_MASK];
    if (!cert.valid) return false;
    const double count = static_cast<double>(st.branched.size() + 1);
    const double known_abund_upper = st.lp_known_abund_upper + 1e-10 * count;
    const double required_log_abund = LN2 - known_abund_upper;
    if (!(required_log_abund > 0.0)) return false;
    double removable_gain = 0.0;
    std::set<uint64_t> removed_primes;
    auto add_removal_gain = [&](const mpz_class& p) {
        if (!p.fits_ulong_p()) return;
        const uint64_t q = static_cast<uint64_t>(p.get_ui());
        if (!removed_primes.insert(q).second) return;
        const auto it = cert.removable_gain.find(q);
        if (it != cert.removable_gain.end()) {
            removable_gain = std::nextafter(
                removable_gain + it->second,
                -std::numeric_limits<double>::infinity()
            );
        }
    };
    for (const auto& p : st.forbidden) add_removal_gain(p);
    for (const auto& [p, info] : st.branched) add_removal_gain(p);

    // The residual LP permits zero or one option for each prime. If a prime q
    // is already forced in N but has no chosen exponent, its residual
    // variables must sum to one. The dual lower-bound penalty for q
    // strengthens from sum_i min(0, rc_i) to min_i(rc_i).
    // Gains are interval-certified and applied only to disjoint unbranched q.
    double forced_gain = 0.0;
    for (const auto& q : st.unbranched) {
        if (!q.fits_ulong_p()) continue;
        const auto it = cert.forced_gain.find(static_cast<uint64_t>(q.get_ui()));
        if (it != cert.forced_gain.end()) {
            forced_gain = std::nextafter(
                forced_gain + it->second,
                -std::numeric_limits<double>::infinity()
            );
        }
    }

    const double known_size_lower = st.log_size_branched - 1e-8 * count;
    const double residual_size_lower =
        cert.intercept_lower + cert.lambda0_lower * required_log_abund + removable_gain + forced_gain;
    const double total_lower = known_size_lower + residual_size_lower - 1e-7 * count;
    if (total_lower > LOG_BOUND + 1e-7) {
        state_lp_prunes.fetch_add(1, std::memory_order_relaxed);
        if (!st.unbranched.empty()) state_lp_early_prunes.fetch_add(1, std::memory_order_relaxed);
        return true;
    }
    return false;
}

bool check_contradiction(const State& st) {
    double cur_size = st.log_size_branched + st.log_size_comp;
    double cur_abund = st.log_abund_lo;
    double max_spec_deduct = 0.0;

    for (const auto& q : st.unbranched) {
        double lq = mpz_log(q);
        cur_size += 2.0 * lq;
        if (!st.has_special && mpz_tstbit(q.get_mpz_t(), 1) == 0) {
            if (lq > max_spec_deduct) max_spec_deduct = lq;
            cur_abund += ln_sigma_m1(q, 1);
        } else {
            cur_abund += ln_sigma_m1(q, 2);
        }
    }
    cur_size -= max_spec_deduct;

    if (cur_size > LOG_BOUND + 1e-9) return true;
    if (cur_abund > LN2 + 1e-12) return true;
    return false;
}

bool solve(State& st, bool in_circ, int depth, std::atomic<bool>& ok_flag);

bool branch_component(const State& base, const mpz_class& p, uint64_t a, bool is_exact, bool in_circ, int depth, std::atomic<bool>& ok_flag) {
    if (!ok_flag.load(std::memory_order_relaxed)) return false;

    total_branches.fetch_add(1, std::memory_order_relaxed);
    if (in_circ) circ_branches.fetch_add(1, std::memory_order_relaxed);

    double lp = mpz_log(p);
    if (base.log_size_branched + base.log_size_comp + a * lp > LOG_BOUND + 1e-9) return true;

    for (uint32_t s : base.forbidden_small) {
        if (small_prime_divides_sigma(p, a, s)) return true;
    }

    const SigmaFact& sf = get_sigma_fact(p, a);
    if (sf.div_by_4) return true;

    for (const auto& [f, cnt] : sf.primes) {
        if (base.forbidden.count(f)) return true;
        auto it = base.branched.find(f);
        if (it != base.branched.end() && it->second.exact && it->second.seen_in_sigma + cnt > it->second.exp) {
            return true;
        }
    }

    State st = base;
    st.unbranched.erase(p);
    if (is_exact && a == 1) st.has_special = true;

    st.branched[p] = {a, is_exact, 0};
    st.log_size_branched += a * lp;
    st.log_abund_lo += ln_sigma_m1(p, a);
    st.log_abund_hi += is_exact ? ln_sigma_m1(p, a) : ln_inf_abund(p);
    st.lp_known_abund_upper += lp_prime_abundancy_upper(p);

    for (const auto& [f, cnt] : sf.primes) {
        auto it = st.branched.find(f);
        if (it != st.branched.end()) {
            it->second.seen_in_sigma += cnt;
        } else {
            st.unbranched.insert(f);
        }
    }

    if (sf.comp_rem > 1) {
        // Even overlapping residuals may contain additional prime factors.
        // Add their optimistic abundance contribution; double counting is safe.
        st.composites.push_back(sf.comp_rem);
        const uint64_t count = residual_factor_count_upper(sf.comp_rem);
        st.log_abund_hi += static_cast<double>(count) * RESIDUAL_ABUND_UPPER;
    }
    refresh_composite_size_bound(st);

    if (check_contradiction(st)) return true;
    return solve(st, in_circ, depth, ok_flag);
}

std::vector<std::pair<uint64_t, bool>> get_exponents(const State& st, const mpz_class& p) {
    std::vector<std::pair<uint64_t, bool>> exps;
    double lp = mpz_log(p);
    double rem_size = LOG_BOUND - (st.log_size_branched + st.log_size_comp);

    if (!st.has_special && mpz_tstbit(p.get_mpz_t(), 1) == 0) {
        if (lp <= rem_size) exps.push_back({1, true});
    }

    if (p == 3) {
        for (uint64_t a : {2ULL, 4ULL}) if (a * lp <= rem_size) exps.push_back({a, true});
        for (uint64_t a : {8ULL, 14ULL, 24ULL}) if (a * lp <= rem_size) exps.push_back({a, false});
        for (uint32_t q : small_primes) {
            if (q < 7) continue;
            if ((q - 1) * lp > rem_size) break;
            exps.push_back({q - 1, false});
        }
    } else if (p == 7) {
        if (2 * lp <= rem_size) exps.push_back({2, true});
        if (8 * lp <= rem_size) exps.push_back({8, false});
        for (uint32_t q : small_primes) {
            if (q < 5) continue;
            if ((q - 1) * lp > rem_size) break;
            exps.push_back({q - 1, false});
        }
    } else {
        for (uint32_t q : small_primes) {
            if (q < 3) continue;
            if ((q - 1) * lp > rem_size) break;
            exps.push_back({q - 1, false});
        }
    }
    return exps;
}

// Bound the number of outstanding tasks while allowing deep work stealing.
std::atomic<int> outstanding_branch_tasks{0};

bool branch_prime(const State& st, const mpz_class& p, bool in_circ, int depth, std::atomic<bool>& ok_flag) {
    auto exps = get_exponents(st, p);
    const int max_tasks = 8 * omp_get_max_threads();
    if (depth < 12 && exps.size() > 1 && omp_get_num_threads() > 1) {
        for (auto [a, is_exact] : exps) {
            if (!ok_flag.load(std::memory_order_relaxed)) break;
            int current = outstanding_branch_tasks.load(std::memory_order_relaxed);
            bool reserved = false;
            while (current < max_tasks) {
                if (outstanding_branch_tasks.compare_exchange_weak(
                        current, current + 1, std::memory_order_relaxed)) {
                    reserved = true;
                    break;
                }
            }
            if (reserved) {
                #pragma omp task firstprivate(st, p, a, is_exact, in_circ, depth) shared(ok_flag)
                {
                    if (ok_flag.load(std::memory_order_relaxed) &&
                        !branch_component(st, p, a, is_exact, in_circ, depth + 1, ok_flag)) {
                        ok_flag.store(false, std::memory_order_relaxed);
                    }
                    outstanding_branch_tasks.fetch_sub(1, std::memory_order_relaxed);
                }
            } else if (!branch_component(st, p, a, is_exact, in_circ, depth + 1, ok_flag)) {
                ok_flag.store(false, std::memory_order_relaxed);
                break;
            }
        }
        #pragma omp taskwait
        return ok_flag.load(std::memory_order_relaxed);
    }

    for (auto [a, is_exact] : exps) {
        if (!branch_component(st, p, a, is_exact, in_circ, depth + 1, ok_flag)) return false;
    }
    return true;
}

// 升级版 v5 路障函数：按效率双指针归并 a=2 与 a=4 流 + 合法 a=1 特殊素数
uint32_t compute_roadblock_bound(const State& st, double rem_size, double abund_gap) {
    static thread_local std::vector<uint32_t> mark_forb(300005, 0);
    static thread_local std::vector<uint32_t> mark_bran(300005, 0);
    static thread_local uint32_t stamp = 0;
    if (++stamp == 0) {
        std::fill(mark_forb.begin(), mark_forb.end(), 0);
        std::fill(mark_bran.begin(), mark_bran.end(), 0);
        stamp = 1;
    }
    for (const auto& x : st.forbidden) if (x.fits_uint_p()) { uint32_t v = x.get_ui(); if (v <= 300000) mark_forb[v] = stamp; }
    for (const auto& [x, _] : st.branched) if (x.fits_uint_p()) { uint32_t v = x.get_ui(); if (v <= 300000) mark_bran[v] = stamp; }

    size_t n = small_primes.size();
    // Every omitted prime q is at least tail_q. The infinite even-exponent
    // tail is relaxed to unbounded fractional knapsack capacity.
    const double tail_q = static_cast<double>(small_primes.back()) + 1.0;
    const double tail_abund = -std::log1p(-1.0 / tail_q);
    const double tail_eff = tail_abund / (2.0 * std::log(tail_q));
    auto exceeds = [&](size_t start_idx) -> bool {
        uint32_t min_p = small_primes[start_idx];
        // Grant the possible omitted special prime's entire maximum abundance
        // for free, even if a finite special prime is also used: a safe relaxation.
        const double effective_gap = std::max(0.0, abund_gap - (st.has_special ? 0.0 : tail_abund));
        auto is_eff_forbidden = [&](uint32_t r) -> bool {
            if ((mark_forb[r] == stamp)) return true;
            if (r < min_p && !(mark_bran[r] == stamp)) return true;
            return false;
        };

        // 找第一个合法的 a=1 特殊素数（若尚未用掉特殊素数）
        size_t spec_idx = n;
        if (!st.has_special) {
            for (size_t i = start_idx; i < n; ++i) {
                uint32_t q = small_primes[i];
                if ((mark_forb[q] == stamp) || (mark_bran[q] == stamp)) continue;
                if ((q & 3) != 1) continue;
                bool ok1 = true;
                for (uint32_t f : sigma1_factors[i]) {
                    if (is_eff_forbidden(f)) { ok1 = false; break; }
                }
                if (ok1) { spec_idx = i; break; }
            }
        }

        auto is_a4 = [&](size_t i) -> bool {
            for (uint32_t f : sigma2_factors[i]) {
                if (is_eff_forbidden(f)) return true;
            }
            return false;
        };

        // 双指针分别扫 a=2 流（i2）和 a=4 流（i4），按效率递减归并
        size_t i2 = start_idx, i4 = start_idx;
        auto advance_i2 = [&]() {
            while (i2 < n) {
                uint32_t q = small_primes[i2];
                if (i2 != spec_idx && !(mark_forb[q] == stamp) && !(mark_bran[q] == stamp) && !is_a4(i2)) break;
                ++i2;
            }
        };
        auto advance_i4 = [&]() {
            while (i4 < n) {
                uint32_t q = small_primes[i4];
                if (i4 != spec_idx && !(mark_forb[q] == stamp) && !(mark_bran[q] == stamp) && is_a4(i4)) break;
                ++i4;
            }
        };
        advance_i2();
        advance_i4();

        bool spec_avail = (spec_idx < n);
        double acc_abund = 0.0;
        double acc_size = 0.0;

        while (true) {
            // 比较 spec_idx (a=1), i2 (a=2), i4 (a=4) 的效率
            int pick = 0; // 1=spec, 2=i2, 4=i4
            double best_eff = -1.0;

            if (spec_avail) {
                double e1 = small_prime_inf_abund[spec_idx] / small_prime_log[spec_idx];
                best_eff = e1; pick = 1;
            }
            if (i2 < n) {
                double e2 = small_prime_inf_abund[i2] / (2.0 * small_prime_log[i2]);
                if (e2 > best_eff) { best_eff = e2; pick = 2; }
            }
            if (i4 < n) {
                double e4 = small_prime_inf_abund[i4] / (4.0 * small_prime_log[i4]);
                if (e4 > best_eff) { best_eff = e4; pick = 4; }
            }
            // The infinite tail may be cheaper than the remaining finite
            // a=4 options. Stop when its optimistic efficiency dominates.
            if (pick == 0 || best_eff <= tail_eff) {
                acc_size += std::max(0.0, effective_gap - acc_abund) / tail_eff;
                return acc_size > rem_size + 1e-9;
            }

            double da, ds;
            if (pick == 1) {
                da = small_prime_inf_abund[spec_idx];
                ds = small_prime_log[spec_idx];
                spec_avail = false;
            } else if (pick == 2) {
                da = small_prime_inf_abund[i2];
                ds = 2.0 * small_prime_log[i2];
                ++i2; advance_i2();
            } else {
                da = small_prime_inf_abund[i4];
                ds = 4.0 * small_prime_log[i4];
                ++i4; advance_i4();
            }

            if (acc_abund + da >= effective_gap) {
                // 分数背包精确截断，保证严格下界
                double frac = std::max(0.0, effective_gap - acc_abund) / da;
                acc_size += frac * ds;
                return acc_size > rem_size + 1e-9;
            }
            acc_abund += da;
            acc_size += ds;
            if (acc_size > rem_size + 1e-9) return true;
        }
    };

    size_t lo = 1, hi = n - 1;
    if (!exceeds(hi)) return 0;
    while (lo < hi) {
        size_t mid = (lo + hi) / 2;
        if (exceeds(mid)) hi = mid;
        else lo = mid + 1;
    }
    return small_primes[lo];
}

// Upgrade only unproved residuals whose conservative contribution is
// obstructing further search. All earlier residuals are certified exactly
// once per State lineage; forked States inherit the certified count.
std::atomic<uint64_t> lazy_triggered_states{0};
std::atomic<uint64_t> lazy_cache_hits{0};
thread_local std::unordered_map<std::string,double> lazy_residual_cache;

void strengthen_composite_residuals(State& st) {
    if (st.certified_residue_count >= st.composites.size()) return;
    lazy_triggered_states.fetch_add(1, std::memory_order_relaxed);
    if (lazy_residual_cache.size() > 10000) lazy_residual_cache.clear();
    while (st.certified_residue_count < st.composites.size()) {
        const mpz_class& rem = st.composites[st.certified_residue_count];
        const std::string key = rem.get_str();
        double certified = 0.0;
        auto it = lazy_residual_cache.find(key);
        if (it != lazy_residual_cache.end()) {
            certified = it->second;
            lazy_cache_hits.fetch_add(1, std::memory_order_relaxed);
        } else {
            certified = certify_sigma_residual_abundance_upper(rem);
            lazy_residual_cache.emplace(key, certified);
        }
        const uint64_t n = residual_factor_count_upper(rem);
        const double weak = static_cast<double>(n) * RESIDUAL_ABUND_UPPER;
        st.log_abund_hi = std::nextafter(
            st.log_abund_hi - weak + certified + 1e-10,
            std::numeric_limits<double>::infinity());
        ++st.certified_residue_count;
    }
}

bool solve(State& st, bool in_circ, int depth, std::atomic<bool>& ok_flag) {
    if (!ok_flag.load(std::memory_order_relaxed)) return false;
    if (check_contradiction(st)) return true;
    if (check_state_lp_contradiction(st)) return true;

    if (!st.unbranched.empty()) {
        mpz_class p = *st.unbranched.rbegin();
        return branch_prime(st, p, in_circ, depth, ok_flag);
    }

    if (st.log_abund_hi >= LN2 - 1e-12) {
        strengthen_composite_residuals(st);
        if (st.log_abund_hi >= LN2 - 1e-12) {
            failed_roadblocks.fetch_add(1, std::memory_order_relaxed);
            return false;
        }
    }

    double rem_size = LOG_BOUND - (st.log_size_branched + st.log_size_comp);
    double abund_gap = LN2 - st.log_abund_hi;

    uint32_t b = compute_roadblock_bound(st, rem_size, abund_gap);
    if (b == 0 && st.certified_residue_count < st.composites.size()) {
        strengthen_composite_residuals(st);
        if (st.log_abund_hi < LN2 - 1e-12) {
            abund_gap = LN2 - st.log_abund_hi;
            b = compute_roadblock_bound(st, rem_size, abund_gap);
        }
    }
    if (b == 0) { failed_roadblocks.fetch_add(1, std::memory_order_relaxed); return false; }

    uint32_t prev_max = max_rb_b.load(std::memory_order_relaxed);
    while (b > prev_max && !max_rb_b.compare_exchange_weak(prev_max, b, std::memory_order_relaxed));

    // 诊断重型路障（b > 5000，每个顶层素数最多打印 5 条）
    if (b > 5000 && heavy_rb_printed.load(std::memory_order_relaxed) < 5 &&
        heavy_rb_printed.fetch_add(1, std::memory_order_relaxed) < 5) {
        std::lock_guard<std::mutex> lk(print_mtx);
        std::cout << "  [HEAVY RB] b=" << b
                  << " | rem_log10=" << (rem_size / std::log(10.0))
                  << " | abund_hi=" << std::exp(st.log_abund_hi)
                  << " | spec=" << st.has_special
                  << " | comps=" << st.composites.size()
                  << " | branched={";
        for (const auto& [bp, info] : st.branched) {
            if (bp.fits_uint_p()) std::cout << bp.get_ui() << "^" << info.exp << (info.exact ? "(E) " : " ");
        }
        std::cout << "}\n" << std::flush;
    }

    // Partition the circular prime cases by their first new prime.
    // Every task receives exactly the forbidden prefix of earlier cases.
    // These disjoint branches can be checked independently.
    if (b > 2000 && omp_get_max_threads() > 1) {
        std::vector<uint32_t> candidates;
        std::set<uint32_t> seen;
        auto append_candidate = [&](uint32_t q) {
            if (q >= b || !seen.insert(q).second) return;
            const mpz_class p(q);
            if (st.forbidden.count(p) || st.branched.count(p)) return;
            candidates.push_back(q);
        };
        for (uint32_t q : CIRC_ORDER) append_candidate(q);
        for (uint32_t q : small_primes) {
            if (q == 2) continue;
            if (q >= b) break;
            append_candidate(q);
        }

        if (candidates.size() >= 256) {
            const size_t workers = static_cast<size_t>(omp_get_max_threads());
            const size_t block_size = std::max<size_t>(64, (candidates.size() + workers * 4 - 1) / (workers * 4));
            const size_t outstanding_limit = std::max<size_t>(2, workers * 2);
            State prefix = st;
            size_t launched = 0;
            #pragma omp taskgroup
            {
                for (size_t start = 0; start < candidates.size(); start += block_size) {
                    if (!ok_flag.load(std::memory_order_relaxed)) break;
                    size_t end = std::min(start + block_size, candidates.size());
                    State snapshot = prefix;
                    for (size_t j = start; j < end; ++j) {
                        mpz_class q(candidates[j]);
                        prefix.forbidden.insert(q);
                        prefix.forbidden_small.push_back(candidates[j]);
                    }
                    #pragma omp task firstprivate(snapshot, start, end, depth) shared(candidates, ok_flag)
                    {
                        State local = std::move(snapshot);
                        for (size_t j = start; j < end && ok_flag.load(std::memory_order_relaxed); ++j) {
                            uint32_t q_ui = candidates[j];
                            if (!branch_prime(local, mpz_class(q_ui), true, depth + 1, ok_flag)) {
                                ok_flag.store(false, std::memory_order_relaxed);
                                break;
                            }
                            local.forbidden.insert(mpz_class(q_ui));
                            local.forbidden_small.push_back(q_ui);
                        }
                    }
                    ++launched;
                    if (launched % outstanding_limit == 0) {
                        #pragma omp taskwait
                    }
                }
            }
            return ok_flag.load(std::memory_order_relaxed);
        }
    }

    State cur = st;
    std::set<uint32_t> tried;
    auto try_circ_prime = [&](uint32_t q_ui) -> bool {
        if (q_ui >= b || tried.count(q_ui)) return true;
        tried.insert(q_ui);
        mpz_class q(q_ui);
        if (cur.forbidden.count(q) || cur.branched.count(q)) return true;
        if (!branch_prime(cur, q, true, depth + 1, ok_flag)) return false;
        cur.forbidden.insert(q);
        cur.forbidden_small.push_back(q_ui);
        return true;
    };

    for (uint32_t q : CIRC_ORDER) {
        if (!try_circ_prime(q)) return false;
    }
    for (uint32_t q : small_primes) {
        if (q == 2) continue;
        if (q >= b) break;
        if (!try_circ_prime(q)) return false;
    }
    return true;
}

int main(int argc, char** argv) {
    int bound_exp = (argc >= 2) ? std::atoi(argv[1]) : 1500;
    uint32_t only_p = (argc >= 3) ? static_cast<uint32_t>(std::atoi(argv[2])) : 0;
    const bool shard_listing = argc >= 4 && std::string(argv[3]) == "list";
    const bool shard_single = argc >= 4 && !shard_listing;
    long long chosen_shard = -1;
    if (shard_single) {
        char* end = nullptr;
        chosen_shard = std::strtoll(argv[3], &end, 10);
        if (end == argv[3] || *end || chosen_shard < 0 || only_p == 0) {
            std::cerr << "Usage: ProofTreeV20 2400 root [list|nonnegative-shard-index]\\n";
            return 2;
        }
    }
    if (shard_listing && only_p == 0) {
        std::cerr << "A root prime is required to list its shards\\n";
        return 2;
    }
    LOG_BOUND = bound_exp * std::log(10.0);
    // A validated permutation changes only the outer root-case partition.
    // CIRC_ORDER remains fixed, as does its bit layout for all 256 LP masks.
    if (const char* text = std::getenv("OPN_ROOT_ORDER")) {
        std::stringstream ss(text);
        std::vector<uint32_t> parsed;
        std::string token;
        while (std::getline(ss, token, ',')) {
            if (token.empty()) { std::cerr << "Invalid root-order token\n"; return 2; }
            char* end = nullptr;
            unsigned long p = std::strtoul(token.c_str(), &end, 10);
            if (*end != '\0' || p > 300000) {
                std::cerr << "Invalid root-order prime: " << token << "\n";
                return 2;
            }
            parsed.push_back(static_cast<uint32_t>(p));
        }
        auto lhs = parsed;
        auto rhs = CIRC_ORDER;
        std::sort(lhs.begin(), lhs.end());
        std::sort(rhs.begin(), rhs.end());
        if (lhs != rhs) {
            std::cerr << "OPN_ROOT_ORDER must permute the fixed eight primes\n";
            return 2;
        }
        ROOT_ORDER = std::move(parsed);
    }

    init_primes(300000);
    if (!load_prime_cutoff_product("PrimeCutoffProduct.bin")) {
        std::cerr << "Error: PrimeCutoffProduct.bin unavailable or invalid\\n";
        return 2;
    }
    if (!db.load("facts.idx", "facts.dat")) {
        std::cerr << "Error: failed to mmap facts.idx / facts.dat\n";
        return 1;
    }
    if (!load_prefix_duals("PrefixDualBounds.csv", "PrefixDualVariableGains.csv", "PrefixDualForcedGains.csv")) {
        std::cerr << "Error: failed to load 256 affine LP certificates\n";
        return 1;
    }

    std::cout << "=== OPN Proof Tree v21 (Lazy Residual Bounds and Restartable Shards, Target: 10^"
              << bound_exp << ", threads=" << omp_get_max_threads() << ") ===\n";
    auto t0 = std::chrono::steady_clock::now();

    std::set<mpz_class> global_forbidden;
    std::vector<uint32_t> global_forbidden_small;

    uint32_t prefix_mask = 0;
    bool any_failure = false;
    bool matched_root = false;
    for (uint32_t p_ui : ROOT_ORDER) {
        ACTIVE_PREFIX_MASK = prefix_mask;
        if (only_p != 0 && p_ui != only_p) {
            global_forbidden.insert(mpz_class(p_ui));
            global_forbidden_small.push_back(p_ui);
            const auto it = std::find(CIRC_ORDER.begin(), CIRC_ORDER.end(), p_ui);
            if (it != CIRC_ORDER.end()) prefix_mask |= (1U << static_cast<unsigned>(it - CIRC_ORDER.begin()));
            continue;
        }

        uint64_t b_before = total_branches.load();
        uint64_t c_before = circ_branches.load();
        uint64_t f_before = failed_roadblocks.load();
        uint64_t lp_before = state_lp_prunes.load();
        uint64_t early_before = state_lp_early_prunes.load();
        max_rb_b.store(0);
        heavy_rb_printed.store(0);

        matched_root = true;
        State init_st;
        init_st.forbidden = global_forbidden;
        init_st.forbidden_small = global_forbidden_small;
        mpz_class p(p_ui);
        init_st.unbranched.insert(p);
        const auto root_exponents = get_exponents(init_st, p);
        if (shard_listing) {
            std::cout << "SHARD_COUNT root=" << p_ui
                      << " count=" << root_exponents.size() << "\n";
            for (size_t i = 0; i < root_exponents.size(); ++i) {
                const auto& [a, exact] = root_exponents[i];
                std::cout << "SHARD root=" << p_ui << " index=" << i
                          << " exponent=" << a << " exact=" << (exact ? 1 : 0) << "\n";
            }
            return 0;
        }
        if (shard_single && static_cast<size_t>(chosen_shard) >= root_exponents.size()) {
            std::cerr << "Invalid shard index: " << chosen_shard << "\n";
            return 2;
        }

        std::atomic<bool> all_ok{true};
        auto tp0 = std::chrono::steady_clock::now();
        // Flush progress independently of the search so that bounded jobs
        // leave useful diagnostic evidence when the process is terminated.
        std::mutex progress_mutex;
        std::condition_variable progress_cv;
        bool finished = false;
        std::thread reporter([&]() {
            std::unique_lock<std::mutex> guard(progress_mutex);
            while (!progress_cv.wait_for(guard, std::chrono::seconds(10), [&] { return finished; })) {
                auto now = std::chrono::steady_clock::now();
                double elapsed = std::chrono::duration<double>(now - tp0).count();
                std::cerr << "[PROGRESS] p=" << p_ui
                          << " | branches=" << (total_branches.load(std::memory_order_relaxed) - b_before)
                          << " | circ=" << (circ_branches.load(std::memory_order_relaxed) - c_before)
                          << " | failed_rb=" << (failed_roadblocks.load(std::memory_order_relaxed) - f_before)
                          << " | max_b=" << max_rb_b.load(std::memory_order_relaxed)
                          << " | lp_prunes=" << state_lp_prunes.load(std::memory_order_relaxed)
                          << " | cutoff_screened=" << screened_composites.load(std::memory_order_relaxed)
                          << " | cutoff_small=" << with_low_primes.load(std::memory_order_relaxed)
                          << " | lazy_states=" << lazy_triggered_states.load(std::memory_order_relaxed)
                          << " | gcd_seconds=" << (cutoff_gcd_nanoseconds.load(std::memory_order_relaxed) * 1e-9)
                          << " | lp_early=" << state_lp_early_prunes.load(std::memory_order_relaxed)
                          << " | elapsed=" << elapsed << "s" << std::endl;
            }
        });
        bool solved = false;
        #pragma omp parallel
        {
            #pragma omp single
            {
                if (shard_single) {
                    const auto& [a, exact] = root_exponents[static_cast<size_t>(chosen_shard)];
                    // The unsharded solve first branches on the root p and
                    // invokes branch_component at depth=1 for each option.
                    solved = branch_component(init_st, p, a, exact, false, 1, all_ok);
                } else {
                    solved = solve(init_st, false, 0, all_ok);
                }
            }
        }
        {
            std::lock_guard<std::mutex> guard(progress_mutex);
            finished = true;
        }
        progress_cv.notify_all();
        reporter.join();
        auto tp1 = std::chrono::steady_clock::now();
        double dt = std::chrono::duration<double>(tp1 - tp0).count();

        bool ok = solved && all_ok.load();
        if (!ok) any_failure = true;
        std::cout << "Forbid p=" << p_ui;
        if (shard_single) {
            std::cout << " branch=" << chosen_shard << "/" << root_exponents.size();
        }
        std::cout << " -> " << (ok ? "PROVEN" : "FAILED")
                  << " | branches=" << (total_branches.load() - b_before)
                  << " (circ=" << (circ_branches.load() - c_before) << ", max_b=" << max_rb_b.load() << ")"
                  << " | failed_rb=" << (failed_roadblocks.load() - f_before)
                  << " | lp_prunes=" << (state_lp_prunes.load() - lp_before)
                  << " | lp_early=" << (state_lp_early_prunes.load() - early_before)
                  << " | " << dt << "s\n" << std::flush;

        if (!ok || only_p != 0) break;
        global_forbidden.insert(p);
        global_forbidden_small.push_back(p_ui);
        const auto root_it = std::find(CIRC_ORDER.begin(), CIRC_ORDER.end(), p_ui);
        if (root_it != CIRC_ORDER.end()) prefix_mask |= (1U << static_cast<unsigned>(root_it - CIRC_ORDER.begin()));
    }

    auto t1 = std::chrono::steady_clock::now();
    double total_dt = std::chrono::duration<double>(t1 - t0).count();
    std::cout << "LAZY_STATS states=" << lazy_triggered_states.load()
              << " cache_hits=" << lazy_cache_hits.load() << std::endl;
    std::cout << "CUTOFF_STATS screened=" << screened_composites.load()
              << " has_factors_le_1e8=" << with_low_primes.load()
              << " gcd_seconds=" << (cutoff_gcd_nanoseconds.load() * 1e-9)
              << std::endl;
    std::cout << "Total branches: " << total_branches.load()
              << " (circ: " << circ_branches.load() << "), failed_rb: " << failed_roadblocks.load()
              << ", lp_prunes: " << state_lp_prunes.load() << ", elapsed: " << total_dt << "s\n";
    if ((only_p != 0 && !matched_root) || (shard_single && !matched_root)) return 2;
    return any_failure ? 3 : 0;
}
