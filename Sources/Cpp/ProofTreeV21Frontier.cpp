// Sources/Cpp/ProofTreeV21Frontier.cpp (Audited & Fixed)
// - Fixes B-1: properly handles root shards pruned immediately at step 0 (e.g. root 7, d=2 with 19 forbidden)
// - Fixes B-2: writes <prefix>_meta.json in split-state and returns exit code 10 on SPLIT_ALL_CLOSED
// - Fixes B-3: restores full G2/G3 quota precheck, OPN_ROOT_ORDER parsing, and bounded OpenMP barrier
// - Fixes B-4: cleans up hash128() typo

#include "V21FrontierCodec.hpp"
#include "../../Experimental/SigmaPrecheck.hpp"

#include <gmpxx.h>
#include <omp.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <csignal>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

volatile std::sig_atomic_t g_stop_signal = 0;
extern "C" void handle_stop_signal(int) { g_stop_signal = 1; }
inline bool stop_requested() { return g_stop_signal != 0; }

struct IdxEntry { uint64_t h1, h2, offset; uint32_t len; };

inline void hash128(const char* s, size_t n, uint64_t& h1, uint64_t& h2) {
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
    bool loaded = false;

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
        loaded = (idx_ptr != MAP_FAILED && dat_ptr != MAP_FAILED);
        return loaded;
    }
    bool is_loaded() const { return loaded; }
    ~FactDB() {
        if (idx_ptr && idx_ptr != MAP_FAILED) munmap(const_cast<IdxEntry*>(idx_ptr), idx_cnt * sizeof(IdxEntry));
        if (dat_ptr && dat_ptr != MAP_FAILED) munmap(const_cast<char*>(dat_ptr), dat_sz);
        if (fd_idx >= 0) close(fd_idx);
        if (fd_dat >= 0) close(fd_dat);
    }
    std::vector<mpz_class> lookup(const std::string& key) const {
        if (!loaded) return {};
        uint64_t h1, h2;
        hash128(key.data(), key.size(), h1, h2);
        IdxEntry target{h1, h2, 0, 0};
        auto it = std::lower_bound(idx_ptr, idx_ptr + idx_cnt, target, [](const IdxEntry& a, const IdxEntry& b) {
            return (a.h1 != b.h1) ? (a.h1 < b.h1) : (a.h2 < b.h2);
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
const std::vector<uint32_t> CIRC_ORDER = {19, 7, 11, 31, 13, 3, 5, 17};
std::vector<uint32_t> ROOT_ORDER = {19, 7, 11, 31, 13, 3, 5, 17};
double LOG_BOUND = 0.0;
const double LN2 = std::log(2.0);
const uint64_t RESIDUAL_MIN_PRIME = 1009;
const double RESIDUAL_ABUND_UPPER =
    std::nextafter(std::log1p(1.0 / (RESIDUAL_MIN_PRIME - 1.0)) + 1e-14,
                   std::numeric_limits<double>::infinity());

FactDB g_db;
bool g_has_cutoff = false;
bool g_reuse_prp = true;     // DEFAULT: G1 enabled
bool g_use_precheck = false; // DEFAULT: G2 off

std::atomic<uint64_t> g_branches{0};
std::atomic<uint64_t> g_prp_calls{0};
std::atomic<uint64_t> g_fact_hits{0};
std::atomic<uint64_t> g_fact_misses{0};
std::atomic<uint64_t> g_leaves_size{0};
std::atomic<uint64_t> g_leaves_forb{0};
std::atomic<uint64_t> g_leaves_quota{0};
std::atomic<uint64_t> g_unresolved{0};
std::atomic<int> g_outstanding_tasks{0};

void init_primes(uint32_t limit) {
    std::vector<uint32_t> spf(limit + 1, 0);
    for (uint32_t i = 2; i <= limit; ++i) {
        if (spf[i] == 0) { spf[i] = i; small_primes.push_back(i); }
        for (uint32_t p : small_primes) {
            if (p > spf[i] || static_cast<uint64_t>(i) * p > limit) break;
            spf[i * p] = p;
        }
    }
}

void parse_root_order_env() {
    const char* text = std::getenv("OPN_ROOT_ORDER");
    if (!text || !*text) return;
    std::stringstream ss(text);
    std::vector<uint32_t> parsed;
    std::string token;
    while (std::getline(ss, token, ',')) {
        if (token.empty()) throw std::runtime_error("empty token in OPN_ROOT_ORDER");
        char* end = nullptr;
        unsigned long p = std::strtoul(token.c_str(), &end, 10);
        if (*end != '\0' || p > 300000) throw std::runtime_error("invalid prime in OPN_ROOT_ORDER");
        parsed.push_back(static_cast<uint32_t>(p));
    }
    auto lhs = parsed, rhs = CIRC_ORDER;
    std::sort(lhs.begin(), lhs.end());
    std::sort(rhs.begin(), rhs.end());
    if (lhs != rhs) throw std::runtime_error("OPN_ROOT_ORDER must permute CIRC_ORDER");
    ROOT_ORDER = std::move(parsed);
}

inline double mpz_log(const mpz_class& x) {
    long exp;
    double d = mpz_get_d_2exp(&exp, x.get_mpz_t());
    return std::log(d) + exp * std::log(2.0);
}

inline double ln_sigma_m1(const mpz_class& p, uint64_t a) {
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

inline double ln_inf_abund(const mpz_class& p) {
    double lp = mpz_log(p);
    if (lp > 35.0) return std::exp(-lp);
    double pd = p.get_d();
    return std::log(pd / (pd - 1.0));
}

inline uint64_t pow_mod_u64(uint64_t base, uint64_t exp, uint64_t mod) {
    uint64_t res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (static_cast<__uint128_t>(res) * base) % mod;
        base = (static_cast<__uint128_t>(base) * base) % mod;
        exp >>= 1;
    }
    return res;
}

inline bool small_prime_divides_sigma(const mpz_class& p, uint64_t a, uint64_t s) {
    uint64_t r = mpz_fdiv_ui(p.get_mpz_t(), static_cast<unsigned long>(s));
    if (r == 1) return ((a + 1) % s) == 0;
    if (r == 0) return false;
    return pow_mod_u64(r, a + 1, s) == 1;
}

inline uint64_t residual_factor_count_upper(mpz_class rem) {
    uint64_t count = 0;
    while (rem >= RESIDUAL_MIN_PRIME) { rem /= RESIDUAL_MIN_PRIME; ++count; }
    return count;
}

struct SigmaFact {
    bool div_by_4 = false;
    std::vector<std::pair<mpz_class, uint64_t>> primes;
    mpz_class comp_rem = 1;
};

thread_local std::unordered_map<std::string, SigmaFact> tls_fact_cache;

int call_prp(const mpz_class& val) {
    g_prp_calls.fetch_add(1, std::memory_order_relaxed);
    return mpz_probab_prime_p(val.get_mpz_t(), 5);
}

const SigmaFact& get_sigma_fact(const mpz_class& p, uint64_t a) {
    std::string key = p.get_str() + " " + std::to_string(a + 1);
    auto it = tls_fact_cache.find(key);
    if (it != tls_fact_cache.end()) {
        g_fact_hits.fetch_add(1, std::memory_order_relaxed);
        return it->second;
    }
    g_fact_misses.fetch_add(1, std::memory_order_relaxed);
    if (tls_fact_cache.size() > 150000) tls_fact_cache.clear();

    SigmaFact res;
    mpz_class rem;
    mpz_pow_ui(rem.get_mpz_t(), p.get_mpz_t(), a + 1);
    rem -= 1;
    rem /= (p - 1);

    int v2 = mpz_scan1(rem.get_mpz_t(), 0);
    if (v2 >= 2) {
        res.div_by_4 = true;
        return tls_fact_cache.emplace(std::move(key), std::move(res)).first->second;
    }
    if (v2 == 1) rem >>= 1;

    if (g_db.is_loaded()) {
        auto db_facts = g_db.lookup(key);
        for (const auto& f : db_facts) {
            if (f <= 2 || rem == 1) continue;
            uint64_t cnt = 0;
            while (mpz_divisible_p(rem.get_mpz_t(), f.get_mpz_t())) {
                rem /= f;
                ++cnt;
            }
            if (cnt > 0) res.primes.push_back({f, cnt});
        }
    }

    int primality = (rem > 1) ? call_prp(rem) : 0;
    bool changed = false;
    if (rem > 1 && primality == 0) {
        size_t digits = mpz_sizeinbase(rem.get_mpz_t(), 10);
        uint32_t trial_lim = (digits <= 10) ? 10000 : 1000;
        for (uint32_t sp : small_primes) {
            if (sp > trial_lim || rem == 1) break;
            if (digits <= 10 && mpz_cmp_ui(rem.get_mpz_t(), static_cast<uint64_t>(sp) * sp) < 0) break;
            if (mpz_divisible_ui_p(rem.get_mpz_t(), sp)) {
                changed = true;
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
        if (!g_reuse_prp || changed) primality = call_prp(rem);
        if (primality > 0) {
            res.primes.push_back({rem, 1});
            rem = 1;
        } else {
            res.comp_rem = rem;
        }
    }
    return tls_fact_cache.emplace(std::move(key), std::move(res)).first->second;
}

void refresh_composite_size_bound(opn_v21::V21State& st) {
    st.hints.log_size_comp = 0.0;
    std::vector<const mpz_class*> chosen;
    for (const auto& c : st.composites) {
        bool indep = true;
        for (const auto& [p, _] : st.branched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { indep = false; break; }
        }
        if (!indep) continue;
        for (const auto& p : st.unbranched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { indep = false; break; }
        }
        if (!indep) continue;
        for (const auto* d : chosen) {
            mpz_class g;
            mpz_gcd(g.get_mpz_t(), c.get_mpz_t(), d->get_mpz_t());
            if (g > 1) { indep = false; break; }
        }
        if (indep) {
            st.hints.log_size_comp += mpz_log(c);
            chosen.push_back(&c);
        }
    }
}

void rebuild_float_hints(opn_v21::V21State& st) {
    if (st.certified_residue_count > 0 && !g_has_cutoff) {
        throw std::runtime_error("cannot restore certified_residue_count > 0 without PrimeCutoffProduct.bin");
    }
    st.hints = {};
    for (const auto& [p, info] : st.branched) {
        st.hints.log_size_branched += info.exp * mpz_log(p);
        st.hints.log_abund_lo += ln_sigma_m1(p, info.exp);
        st.hints.log_abund_hi += info.exact ? ln_sigma_m1(p, info.exp) : ln_inf_abund(p);
    }
    for (const auto& c : st.composites) {
        st.hints.log_abund_hi += static_cast<double>(residual_factor_count_upper(c)) * RESIDUAL_ABUND_UPPER;
    }
    refresh_composite_size_bound(st);
    st.has_float_hints = true;
}

bool check_contradiction(const opn_v21::V21State& st, std::string* reason = nullptr) {
    double cur_size = st.hints.log_size_branched + st.hints.log_size_comp;
    double cur_abund = st.hints.log_abund_lo;
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
    if (cur_size > LOG_BOUND + 1e-9) {
        g_leaves_size.fetch_add(1, std::memory_order_relaxed);
        if (reason) *reason = "SIZE_EXCEEDS_BOUND";
        return true;
    }
    if (cur_abund > LN2 + 1e-12) {
        if (reason) *reason = "ABUNDANCE_EXCEEDS_TWO";
        return true;
    }
    return false;
}

std::vector<std::pair<uint64_t, bool>> get_exponents(const opn_v21::V21State& st, const mpz_class& p) {
    std::vector<std::pair<uint64_t, bool>> exps;
    double lp = mpz_log(p);
    double rem_size = LOG_BOUND - (st.hints.log_size_branched + st.hints.log_size_comp);
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

bool apply_branch_step(const opn_v21::V21State& base, const mpz_class& p, uint64_t a, bool is_exact,
                       opn_v21::V21State& out_child, bool& pruned_immediately, std::string& prune_reason) {
    pruned_immediately = false;
    prune_reason.clear();
    double lp = mpz_log(p);
    if (base.hints.log_size_branched + base.hints.log_size_comp + a * lp > LOG_BOUND + 1e-9) {
        g_leaves_size.fetch_add(1, std::memory_order_relaxed);
        pruned_immediately = true;
        prune_reason = "SIZE_EXCEEDS_BOUND";
        return true;
    }
    for (uint64_t s : base.forbidden_small) {
        if (small_prime_divides_sigma(p, a, s)) {
            g_leaves_forb.fetch_add(1, std::memory_order_relaxed);
            pruned_immediately = true;
            prune_reason = "FORBIDDEN_FACTOR";
            return true;
        }
    }
    if (g_use_precheck) {
        if (sigma_precheck::divisible_by_four(mpz_fdiv_ui(p.get_mpz_t(), 4), a)) {
            pruned_immediately = true;
            prune_reason = "V2_EXCEEDS_ONE";
            return true;
        }
        for (const auto& [q, info] : base.branched) {
            if (!info.exact || !q.fits_ulong_p()) continue;
            if (info.seen_in_sigma > info.exp) {
                g_leaves_quota.fetch_add(1, std::memory_order_relaxed);
                pruned_immediately = true;
                prune_reason = "EXACT_QUOTA_EXCEEDED";
                return true;
            }
            const uint64_t qu = q.get_ui();
            const uint64_t m = sigma_precheck::modulus(
                qu, info.exp - info.seen_in_sigma + 1, std::numeric_limits<unsigned long>::max());
            if (m && sigma_precheck::valuation_at_least(
                    mpz_fdiv_ui(p.get_mpz_t(), static_cast<unsigned long>(m)), a + 1, qu, m)) {
                g_leaves_quota.fetch_add(1, std::memory_order_relaxed);
                pruned_immediately = true;
                prune_reason = "EXACT_QUOTA_EXCEEDED";
                return true;
            }
        }
    }

    const SigmaFact& sf = get_sigma_fact(p, a);
    if (sf.div_by_4) {
        pruned_immediately = true;
        prune_reason = "V2_EXCEEDS_ONE";
        return true;
    }
    for (const auto& [f, cnt] : sf.primes) {
        if (base.forbidden.count(f)) {
            g_leaves_forb.fetch_add(1, std::memory_order_relaxed);
            pruned_immediately = true;
            prune_reason = "FORBIDDEN_FACTOR";
            return true;
        }
        auto it = base.branched.find(f);
        if (it != base.branched.end() && it->second.exact && it->second.seen_in_sigma + cnt > it->second.exp) {
            g_leaves_quota.fetch_add(1, std::memory_order_relaxed);
            pruned_immediately = true;
            prune_reason = "EXACT_QUOTA_EXCEEDED";
            return true;
        }
    }

    out_child = base;
    out_child.unbranched.erase(p);
    if (is_exact && a == 1) out_child.has_special = true;
    out_child.branched[p] = {a, is_exact, 0};
    out_child.hints.log_size_branched += a * lp;
    out_child.hints.log_abund_lo += ln_sigma_m1(p, a);
    out_child.hints.log_abund_hi += is_exact ? ln_sigma_m1(p, a) : ln_inf_abund(p);
    for (const auto& [f, cnt] : sf.primes) {
        auto it = out_child.branched.find(f);
        if (it != out_child.branched.end()) it->second.seen_in_sigma += cnt;
        else out_child.unbranched.insert(f);
    }
    if (sf.comp_rem > 1) {
        out_child.composites.push_back(sf.comp_rem);
        out_child.hints.log_abund_hi += static_cast<double>(residual_factor_count_upper(sf.comp_rem)) * RESIDUAL_ABUND_UPPER;
    }
    refresh_composite_size_bound(out_child);
    if (check_contradiction(out_child, &prune_reason)) {
        pruned_immediately = true;
        return true;
    }
    return true;
}

bool solve_subtree(const opn_v21::V21State& st, int depth, std::atomic<bool>& ok_flag) {
    if (!ok_flag.load(std::memory_order_relaxed) || stop_requested()) return false;
    if (check_contradiction(st)) return true;
    if (st.unbranched.empty()) {
        g_unresolved.fetch_add(1, std::memory_order_relaxed);
        return false;
    }
    mpz_class p = *st.unbranched.rbegin();
    auto exps = get_exponents(st, p);
    const int max_tasks = 4 * omp_get_max_threads();

    if (depth < 6 && exps.size() > 1 && omp_get_num_threads() > 1) {
        for (auto [a, is_exact] : exps) {
            if (!ok_flag.load(std::memory_order_relaxed) || stop_requested()) break;
            int cur = g_outstanding_tasks.load(std::memory_order_relaxed);
            bool reserved = false;
            while (cur < max_tasks) {
                if (g_outstanding_tasks.compare_exchange_weak(cur, cur + 1, std::memory_order_relaxed)) {
                    reserved = true;
                    break;
                }
            }
            if (reserved) {
                #pragma omp task firstprivate(st, p, a, is_exact, depth) shared(ok_flag)
                {
                    if (ok_flag.load(std::memory_order_relaxed) && !stop_requested()) {
                        g_branches.fetch_add(1, std::memory_order_relaxed);
                        opn_v21::V21State child;
                        bool pruned = false;
                        std::string reason;
                        apply_branch_step(st, p, a, is_exact, child, pruned, reason);
                        if (!pruned && !solve_subtree(child, depth + 1, ok_flag)) {
                            ok_flag.store(false, std::memory_order_relaxed);
                        }
                    }
                    g_outstanding_tasks.fetch_sub(1, std::memory_order_relaxed);
                }
            } else {
                g_branches.fetch_add(1, std::memory_order_relaxed);
                opn_v21::V21State child;
                bool pruned = false;
                std::string reason;
                apply_branch_step(st, p, a, is_exact, child, pruned, reason);
                if (!pruned && !solve_subtree(child, depth + 1, ok_flag)) {
                    ok_flag.store(false, std::memory_order_relaxed);
                    break;
                }
            }
        }
        #pragma omp taskwait
        return ok_flag.load(std::memory_order_relaxed) && !stop_requested();
    }

    for (auto [a, is_exact] : exps) {
        if (!ok_flag.load(std::memory_order_relaxed) || stop_requested()) return false;
        g_branches.fetch_add(1, std::memory_order_relaxed);
        opn_v21::V21State child;
        bool pruned = false;
        std::string reason;
        apply_branch_step(st, p, a, is_exact, child, pruned, reason);
        if (!pruned && !solve_subtree(child, depth + 1, ok_flag)) return false;
    }
    return true;
}

struct RootShardInit {
    bool pruned_immediately = false;
    std::string prune_reason;
    opn_v21::V21State state;
};

RootShardInit build_root_shard_state(uint32_t root_p, size_t shard_idx) {
    opn_v21::V21State init;
    uint32_t mask = 0;
    bool found_root = false;
    for (uint32_t r : ROOT_ORDER) {
        if (r == root_p) { found_root = true; break; }
        init.forbidden.insert(mpz_class(r));
        init.forbidden_small.push_back(r);
        auto it = std::find(CIRC_ORDER.begin(), CIRC_ORDER.end(), r);
        if (it != CIRC_ORDER.end()) mask |= (1u << static_cast<unsigned>(it - CIRC_ORDER.begin()));
    }
    if (!found_root) throw std::invalid_argument("root_p not in ROOT_ORDER");
    init.outer_root_mask = mask;
    init.unbranched.insert(mpz_class(root_p));
    rebuild_float_hints(init);
    auto exps = get_exponents(init, mpz_class(root_p));
    if (shard_idx >= exps.size()) throw std::out_of_range("shard_idx out of range");

    RootShardInit res;
    apply_branch_step(init, mpz_class(root_p), exps[shard_idx].first, exps[shard_idx].second,
                      res.state, res.pruned_immediately, res.prune_reason);
    return res;
}

void write_bytes(const std::string& path, const std::vector<uint8_t>& bytes) {
    std::ofstream out(path, std::ios::binary);
    if (!out) throw std::runtime_error("cannot open for write: " + path);
    out.write(reinterpret_cast<const char*>(bytes.data()), static_cast<std::streamsize>(bytes.size()));
    if (!out) throw std::runtime_error("write failed: " + path);
}

std::vector<uint8_t> read_bytes(const std::string& path) {
    std::ifstream in(path, std::ios::binary | std::ios::ate);
    if (!in) throw std::runtime_error("cannot open for read: " + path);
    auto sz = in.tellg();
    in.seekg(0);
    std::vector<uint8_t> buf(static_cast<size_t>(sz));
    in.read(reinterpret_cast<char*>(buf.data()), sz);
    return buf;
}

} // namespace

int main(int argc, char** argv) {
    std::signal(SIGTERM, handle_stop_signal);
    std::signal(SIGINT, handle_stop_signal);
    if (argc < 3) {
        std::cerr << "Usage:\n"
                  << "  ProofTreeV21Frontier export-root <B_exp> <root> <shard_idx> <out.bin>\n"
                  << "  ProofTreeV21Frontier split-state <B_exp> <in.bin> <out_prefix>\n"
                  << "  ProofTreeV21Frontier solve-state <B_exp> <in.bin> [--no-db] [--mode=G1|G0|G2|G3]\n"
                  << "  ProofTreeV21Frontier bench-nodb <B_exp> <root> <shard_idx> [--mode=G1|G0|G2|G3]\n";
        return 2;
    }
    const std::string cmd = argv[1];
    const int bound_exp = std::atoi(argv[2]);
    LOG_BOUND = bound_exp * std::log(10.0);
    init_primes(300000);

    bool no_db = (cmd == "bench-nodb");
    for (int i = 3; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--no-db") no_db = true;
        else if (arg == "--mode=G0") { g_reuse_prp = false; g_use_precheck = false; }
        else if (arg == "--mode=G1") { g_reuse_prp = true;  g_use_precheck = false; }
        else if (arg == "--mode=G2") { g_reuse_prp = false; g_use_precheck = true;  }
        else if (arg == "--mode=G3") { g_reuse_prp = true;  g_use_precheck = true;  }
    }
    if (!no_db) g_db.load("facts.idx", "facts.dat");

    try {
        parse_root_order_env();

        if (cmd == "export-root") {
            uint32_t root = static_cast<uint32_t>(std::stoul(argv[3]));
            size_t shard = static_cast<size_t>(std::stoull(argv[4]));
            auto init_res = build_root_shard_state(root, shard);
            if (init_res.pruned_immediately) {
                std::cout << "ROOT_SHARD_PRUNED_IMMEDIATELY root=" << root
                          << " shard=" << shard << " reason=" << init_res.prune_reason << "\n";
                return 0;
            }
            write_bytes(argv[5], opn_v21::serialize_state(init_res.state, CIRC_ORDER, false));
            std::cout << "EXPORTED root=" << root << " shard=" << shard
                      << " unbranched=" << init_res.state.unbranched.size() << "\n";
            return 0;
        }

        if (cmd == "split-state") {
            auto raw = read_bytes(argv[3]);
            auto st = opn_v21::deserialize_state(raw.data(), raw.size(), CIRC_ORDER, false);
            rebuild_float_hints(st);
            if (st.unbranched.empty()) {
                std::cerr << "SPLIT_UNSUPPORTED: empty unbranched set (roadblock split required)\n";
                return 4;
            }
            mpz_class p = *st.unbranched.rbegin();
            auto exps = get_exponents(st, p);
            std::string prefix = argv[4];
            size_t open_cnt = 0, closed_cnt = 0;

            std::ostringstream meta;
            meta << "{\"branch_prime\":\"" << p.get_str() << "\",\"total_edges\":" << exps.size()
                 << ",\"edges\":[";
            for (size_t i = 0; i < exps.size(); ++i) {
                opn_v21::V21State child;
                bool pruned = false;
                std::string reason;
                apply_branch_step(st, p, exps[i].first, exps[i].second, child, pruned, reason);
                if (i > 0) meta << ",";
                meta << "{\"ordinal\":" << i << ",\"exp\":" << exps[i].first
                     << ",\"exact\":" << (exps[i].second ? "true" : "false");
                if (pruned) {
                    ++closed_cnt;
                    meta << ",\"status\":\"CLOSED\",\"reason\":\"" << reason << "\"}";
                } else {
                    std::string child_file = prefix + "_edge_" + std::to_string(i) + ".bin";
                    write_bytes(child_file, opn_v21::serialize_state(child, CIRC_ORDER, false));
                    ++open_cnt;
                    meta << ",\"status\":\"OPEN\",\"state_file\":\"" << child_file << "\"}";
                }
            }
            meta << "],\"open_count\":" << open_cnt << ",\"closed_count\":" << closed_cnt << "}\n";
            std::ofstream meta_out(prefix + "_meta.json");
            meta_out << meta.str();
            if (!meta_out) throw std::runtime_error("failed to write split meta json");

            if (open_cnt == 0) {
                std::cout << "SPLIT_ALL_CLOSED branch_prime=" << p.get_str()
                          << " total_edges=" << exps.size() << "\n";
                return 10; // Caller must submit leaf/closed subtree via finish(), NOT empty split
            }
            std::cout << "SPLIT_OK branch_prime=" << p.get_str()
                      << " total_edges=" << exps.size()
                      << " open=" << open_cnt << " closed=" << closed_cnt << "\n";
            return 0;
        }

        if (cmd == "solve-state" || cmd == "bench-nodb") {
            auto t0 = std::chrono::steady_clock::now();
            bool solved = false;
            std::atomic<bool> ok{true};
            bool pruned_at_root = false;
            std::string root_reason;

            if (cmd == "solve-state") {
                auto raw = read_bytes(argv[3]);
                auto st = opn_v21::deserialize_state(raw.data(), raw.size(), CIRC_ORDER, false);
                rebuild_float_hints(st);
                #pragma omp parallel
                {
                    #pragma omp single
                    { solved = solve_subtree(st, 1, ok); }
                }
            } else {
                auto init_res = build_root_shard_state(static_cast<uint32_t>(std::stoul(argv[3])),
                                                       static_cast<size_t>(std::stoull(argv[4])));
                if (init_res.pruned_immediately) {
                    pruned_at_root = true;
                    root_reason = init_res.prune_reason;
                    solved = true;
                } else {
                    #pragma omp parallel
                    {
                        #pragma omp single
                        { solved = solve_subtree(init_res.state, 1, ok); }
                    }
                }
            }

            auto t1 = std::chrono::steady_clock::now();
            double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
            const char* outcome = stop_requested() ? "INTERRUPTED"
                                : (solved && ok.load() ? "PROVEN_UNAUDITED" : "UNRESOLVED");
            std::cout << "{\"event\":\"TASK_END\",\"outcome\":\"" << outcome
                      << "\",\"pruned_at_root\":" << (pruned_at_root ? "true" : "false")
                      << ",\"root_reason\":\"" << root_reason
                      << "\",\"mode\":\"" << (g_reuse_prp ? (g_use_precheck ? "G3" : "G1")
                                                          : (g_use_precheck ? "G2" : "G0"))
                      << "\",\"no_db\":" << (no_db ? "true" : "false")
                      << ",\"wall_ms\":" << ms
                      << ",\"branches\":" << g_branches.load()
                      << ",\"prp_calls\":" << g_prp_calls.load()
                      << ",\"fact_misses\":" << g_fact_misses.load()
                      << ",\"fact_hits\":" << g_fact_hits.load()
                      << ",\"leaves_size\":" << g_leaves_size.load()
                      << ",\"leaves_forb\":" << g_leaves_forb.load()
                      << ",\"leaves_quota\":" << g_leaves_quota.load()
                      << ",\"unresolved\":" << g_unresolved.load() << "}\n";
            return (solved && ok.load()) ? 0 : (stop_requested() ? 130 : 3);
        }
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << "\n";
        return 1;
    }
    return 2;
}
