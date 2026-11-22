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

void init_primes(uint32_t limit) {
    std::vector<bool> is_p(limit + 1, true);
    is_p[0] = is_p[1] = false;
    for (uint32_t i = 2; i * i <= limit; ++i)
        if (is_p[i])
            for (uint32_t j = i * i; j <= limit; j += i) is_p[j] = false;
    for (uint32_t i = 2; i <= limit; ++i) {
        if (is_p[i]) {
            small_primes.push_back(i);
            small_prime_log.push_back(std::log(static_cast<double>(i)));
            small_prime_inf_abund.push_back(std::log(static_cast<double>(i) / (i - 1.0)));
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
};

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

    // 轻量试除：大数试除到 1000（168个素数），小数试除到 10000
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
};

double LOG_BOUND = 0.0;
const double LN2 = std::log(2.0);
const double ALPHA = 1e8;
const double LN_ALPHA = std::log(ALPHA);
const double LN_ALPHA_RATIO = std::log(ALPHA / (ALPHA - 1.0));

std::vector<uint32_t> S_ORDER = {127, 19, 7, 11, 331, 31, 97, 61, 13, 398581, 1093, 3, 5, 307, 17};

std::atomic<uint64_t> total_branches{0};
std::atomic<uint64_t> circ_branches{0};
std::atomic<uint64_t> failed_roadblocks{0};
std::atomic<uint32_t> max_rb_b{0};

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

    for (const auto& [f, cnt] : sf.primes) {
        auto it = st.branched.find(f);
        if (it != st.branched.end()) {
            it->second.seen_in_sigma += cnt;
        } else {
            st.unbranched.insert(f);
        }
    }

    if (sf.comp_rem > 1) {
        bool shared = false;
        for (const auto& c : st.composites) {
            mpz_class g;
            mpz_gcd(g.get_mpz_t(), sf.comp_rem.get_mpz_t(), c.get_mpz_t());
            if (g > 1) { shared = true; break; }
        }
        if (!shared) {
            st.composites.push_back(sf.comp_rem);
            st.log_size_comp += sf.comp_log;
            double max_factors = std::floor(sf.comp_log / LN_ALPHA);
            st.log_abund_hi += max_factors * LN_ALPHA_RATIO;
        }
    }

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

bool branch_prime(const State& st, const mpz_class& p, bool in_circ, int depth, std::atomic<bool>& ok_flag) {
    auto exps = get_exponents(st, p);
    // 前 3 层用 OpenMP Task 动态切分，彻底消除 32 核长尾负载不均
    if (depth < 3 && exps.size() > 1) {
        for (auto [a, is_exact] : exps) {
            #pragma omp task firstprivate(st, p, a, is_exact, in_circ, depth) shared(ok_flag)
            {
                if (ok_flag.load(std::memory_order_relaxed)) {
                    if (!branch_component(st, p, a, is_exact, in_circ, depth + 1, ok_flag)) {
                        ok_flag.store(false, std::memory_order_relaxed);
                    }
                }
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

uint32_t compute_roadblock_bound(const State& st, double rem_size, double abund_gap) {
    std::set<uint32_t> skip_ui;
    for (const auto& x : st.forbidden) if (x.fits_uint_p()) skip_ui.insert(x.get_ui());
    for (const auto& [x, _] : st.branched) if (x.fits_uint_p()) skip_ui.insert(x.get_ui());

    size_t lo = 1, hi = small_primes.size() - 1;
    auto exceeds = [&](size_t start_idx) -> bool {
        double acc_abund = 0.0;
        double acc_size = 0.0;
        bool used_spec = st.has_special;
        for (size_t i = start_idx; i < small_primes.size(); ++i) {
            uint32_t q = small_primes[i];
            if (skip_ui.count(q)) continue;
            acc_abund += small_prime_inf_abund[i];
            if (!used_spec && (q & 3) == 1) {
                acc_size += small_prime_log[i];
                used_spec = true;
            } else {
                acc_size += 2.0 * small_prime_log[i];
            }
            if (acc_size > rem_size + 1e-9) return true;
            if (acc_abund >= abund_gap) return false;
        }
        return true;
    };

    if (!exceeds(hi)) return 0;
    while (lo < hi) {
        size_t mid = (lo + hi) / 2;
        if (exceeds(mid)) hi = mid;
        else lo = mid + 1;
    }
    return small_primes[lo];
}

bool solve(State& st, bool in_circ, int depth, std::atomic<bool>& ok_flag) {
    if (!ok_flag.load(std::memory_order_relaxed)) return false;
    if (check_contradiction(st)) return true;

    if (!st.unbranched.empty()) {
        mpz_class p = *st.unbranched.rbegin();
        return branch_prime(st, p, in_circ, depth, ok_flag);
    }

    if (st.log_abund_hi >= LN2 - 1e-12) {
        failed_roadblocks.fetch_add(1, std::memory_order_relaxed);
        return false;
    }

    double rem_size = LOG_BOUND - (st.log_size_branched + st.log_size_comp);
    double abund_gap = LN2 - st.log_abund_hi;

    uint32_t b = compute_roadblock_bound(st, rem_size, abund_gap);
    if (b == 0) { failed_roadblocks.fetch_add(1, std::memory_order_relaxed); return false; }

    uint32_t prev_max = max_rb_b.load(std::memory_order_relaxed);
    while (b > prev_max && !max_rb_b.compare_exchange_weak(prev_max, b, std::memory_order_relaxed));

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

    for (uint32_t q : S_ORDER) {
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
    int bound_exp = (argc >= 2) ? std::atoi(argv[1]) : 1000;
    LOG_BOUND = bound_exp * std::log(10.0);

    init_primes(200000);
    if (!db.load("facts.idx", "facts.dat")) {
        std::cerr << "Error: failed to mmap facts.idx / facts.dat\n";
        return 1;
    }

    std::cout << "=== OPN Proof Tree v4 (TaskPool 32T + FastRB, Target: 10^"
              << bound_exp << ", threads=" << omp_get_max_threads() << ") ===\n";
    auto t0 = std::chrono::steady_clock::now();

    std::set<mpz_class> global_forbidden;
    std::vector<uint32_t> global_forbidden_small;

    for (uint32_t p_ui : S_ORDER) {
        uint64_t b_before = total_branches.load();
        uint64_t c_before = circ_branches.load();
        uint64_t f_before = failed_roadblocks.load();
        max_rb_b.store(0);

        State init_st;
        init_st.forbidden = global_forbidden;
        init_st.forbidden_small = global_forbidden_small;
        mpz_class p(p_ui);
        init_st.unbranched.insert(p);

        std::atomic<bool> all_ok{true};
        auto tp0 = std::chrono::steady_clock::now();
        #pragma omp parallel
        {
            #pragma omp single
            {
                solve(init_st, false, 0, all_ok);
            }
        }
        auto tp1 = std::chrono::steady_clock::now();
        double dt = std::chrono::duration<double>(tp1 - tp0).count();

        bool ok = all_ok.load();
        std::cout << "Forbid p=" << p_ui
                  << " -> " << (ok ? "PROVEN" : "FAILED")
                  << " | branches=" << (total_branches.load() - b_before)
                  << " (circ=" << (circ_branches.load() - c_before) << ", max_b=" << max_rb_b.load() << ")"
                  << " | failed_rb=" << (failed_roadblocks.load() - f_before)
                  << " | " << dt << "s\n" << std::flush;

        if (!ok) break;
        global_forbidden.insert(p);
        global_forbidden_small.push_back(p_ui);
    }

    auto t1 = std::chrono::steady_clock::now();
    double total_dt = std::chrono::duration<double>(t1 - t0).count();
    std::cout << "Total branches: " << total_branches.load()
              << " (circ: " << circ_branches.load() << "), failed_rb: " << failed_roadblocks.load()
              << ", elapsed: " << total_dt << "s\n";
    return 0;
}
