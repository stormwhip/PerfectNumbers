#include <gmpxx.h>
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
#include <algorithm>
#include <iostream>
#include <chrono>

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

    std::vector<mpz_class> lookup(const mpz_class& p, uint64_t q_plus_1) const {
        std::string key = p.get_str() + " " + std::to_string(q_plus_1);
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

// 素数表（用于枚举指数 q-1 和路障绕过）
std::vector<uint32_t> small_primes;
void init_primes(uint32_t limit) {
    std::vector<bool> is_p(limit + 1, true);
    is_p[0] = is_p[1] = false;
    for (uint32_t i = 2; i * i <= limit; ++i)
        if (is_p[i])
            for (uint32_t j = i * i; j <= limit; j += i) is_p[j] = false;
    for (uint32_t i = 2; i <= limit; ++i)
        if (is_p[i]) small_primes.push_back(i);
}

static inline double mpz_log(const mpz_class& x) {
    long exp;
    double d = mpz_get_d_2exp(&exp, x.get_mpz_t());
    return std::log(d) + exp * std::log(2.0);
}

static inline double ln_sigma_m1(const mpz_class& p, uint64_t a) {
    double lp = mpz_log(p);
    if (lp > 35.0) return std::exp(-lp); // p > 1.5e15 时 1/p 足够精确
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

struct BranchedInfo {
    uint64_t exp;
    bool exact;
    uint64_t seen_in_sigma;
};

struct State {
    std::set<mpz_class> forbidden;
    std::map<mpz_class, BranchedInfo> branched;
    std::set<mpz_class> unbranched;
    std::vector<mpz_class> composites;
    bool has_special = false;
    double log_size_branched = 0.0;
    double log_size_comp = 0.0;
    double log_abund_lo = 0.0;
    double log_abund_hi = 0.0;
};

FactDB db;
double LOG_BOUND = 0.0;
const double LN2 = std::log(2.0);
const double ALPHA = 1e8;
const double LN_ALPHA = std::log(ALPHA);
const double LN_ALPHA_RATIO = std::log(ALPHA / (ALPHA - 1.0));

std::vector<uint32_t> S_ORDER = {127, 19, 7, 11, 331, 31, 97, 61, 13, 398581, 1093, 3, 5, 307, 17};

uint64_t total_branches = 0;
uint64_t circ_branches = 0;
uint64_t failed_roadblocks = 0;

// 辅助：计算状态当前大小下界（含未分支素数）与丰度下界
bool check_contradiction(const State& st) {
    double cur_size = st.log_size_branched + st.log_size_comp;
    double cur_abund = st.log_abund_lo;
    double max_spec_deduct = 0.0;

    for (const auto& q : st.unbranched) {
        double lq = mpz_log(q);
        cur_size += 2.0 * lq;
        if (!st.has_special && mpz_tstbit(q.get_mpz_t(), 1) == 0) { // q == 1 (mod 4)
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

bool solve(State& st, bool in_circ);

// 对单个组件 p^a 进行分支
bool branch_component(const State& base, const mpz_class& p, uint64_t a, bool is_exact, bool in_circ) {
    ++total_branches;
    if (in_circ) ++circ_branches;

    double lp = mpz_log(p);
    if (base.log_size_branched + base.log_size_comp + a * lp > LOG_BOUND + 1e-9) return true;

    State st = base;
    st.unbranched.erase(p);
    if (is_exact && a == 1) st.has_special = true;

    st.branched[p] = {a, is_exact, 0};
    st.log_size_branched += a * lp;
    st.log_abund_lo += ln_sigma_m1(p, a);
    st.log_abund_hi += is_exact ? ln_sigma_m1(p, a) : ln_inf_abund(p);

    if (check_contradiction(st)) return true;

    // 计算 sigma(p^a) = (p^{a+1} - 1) / (p - 1)
    mpz_class rem;
    mpz_pow_ui(rem.get_mpz_t(), p.get_mpz_t(), a + 1);
    rem -= 1;
    rem /= (p - 1);

    // 除掉因子 2（只有特殊素数 a=1 时 2 || sigma(p^1)）
    int v2 = mpz_scan1(rem.get_mpz_t(), 0);
    if (v2 >= 2) return true; // 4 | sigma(p^a) 矛盾
    if (v2 == 1) rem >>= 1;

    std::vector<std::pair<mpz_class, uint64_t>> prime_factors;
    auto extract_factor = [&](const mpz_class& f) {
        if (f <= 2 || rem == 1) return;
        uint64_t cnt = 0;
        while (mpz_divisible_p(rem.get_mpz_t(), f.get_mpz_t())) {
            rem /= f;
            ++cnt;
        }
        if (cnt > 0) prime_factors.push_back({f, cnt});
    };

    // 1. 查索引库
    auto db_facts = db.lookup(p, a + 1);
    for (const auto& f : db_facts) extract_factor(f);

    // 2. 对剩余小合数做快速试除（覆盖 3^8, 3^14, 3^24, 7^8 等非素数 a+1）
    if (rem > 1 && mpz_probab_prime_p(rem.get_mpz_t(), 15) == 0) {
        uint64_t trial_lim = (mpz_sizeinbase(rem.get_mpz_t(), 10) <= 13) ? 1000000 : 10000;
        for (uint32_t sp : small_primes) {
            if (sp > trial_lim || rem == 1) break;
            if (mpz_divisible_ui_p(rem.get_mpz_t(), sp)) {
                uint64_t cnt = 0;
                while (mpz_divisible_ui_p(rem.get_mpz_t(), sp)) {
                    rem /= sp;
                    ++cnt;
                }
                prime_factors.push_back({mpz_class(sp), cnt});
            }
        }
    }

    // 3. 若残余本身是素数，直接收入
    if (rem > 1 && mpz_probab_prime_p(rem.get_mpz_t(), 15) > 0) {
        prime_factors.push_back({rem, 1});
        rem = 1;
    }

    // 处理所有素因子
    for (const auto& [f, cnt] : prime_factors) {
        if (st.forbidden.count(f)) return true; // 撞上禁用素数
        auto it = st.branched.find(f);
        if (it != st.branched.end()) {
            it->second.seen_in_sigma += cnt;
            if (it->second.exact && it->second.seen_in_sigma > it->second.exp) {
                return true; // 精确分支幂次溢出矛盾
            }
        } else {
            st.unbranched.insert(f);
        }
    }

    // 处理未分解合数 rem
    if (rem > 1) {
        // 先检查是否与已有合数共享公因子
        bool shared = false;
        for (const auto& c : st.composites) {
            mpz_class g;
            mpz_gcd(g.get_mpz_t(), rem.get_mpz_t(), c.get_mpz_t());
            if (g > 1) { shared = true; break; }
        }
        if (!shared) {
            double lrem = mpz_log(rem);
            st.composites.push_back(rem);
            st.log_size_comp += lrem;
            double max_factors = std::floor(lrem / LN_ALPHA);
            st.log_abund_hi += max_factors * LN_ALPHA_RATIO;
        }
    }

    if (check_contradiction(st)) return true;
    return solve(st, in_circ);
}

// 对素数 p 的所有合法幂次进行分支
bool branch_prime(const State& st, const mpz_class& p, bool in_circ) {
    double lp = mpz_log(p);
    double rem_size = LOG_BOUND - (st.log_size_branched + st.log_size_comp);

    // 1. 若尚未用掉特殊素数且 p == 1 (mod 4)，先尝试精确分支 p^1
    if (!st.has_special && mpz_tstbit(p.get_mpz_t(), 1) == 0) {
        if (!branch_component(st, p, 1, true, in_circ)) return false;
    }

    // 2. 特殊处理 p = 3 和 p = 7 的精确+标准混合分支（论文第 3 节）
    if (p == 3) {
        uint64_t ex_list[] = {2, 4};
        for (uint64_t a : ex_list) {
            if (a * lp > rem_size) break;
            if (!branch_component(st, p, a, true, in_circ)) return false;
        }
        uint64_t extra_std[] = {8, 14, 24};
        for (uint64_t a : extra_std) {
            if (a * lp > rem_size) break;
            if (!branch_component(st, p, a, false, in_circ)) return false;
        }
        for (uint32_t q : small_primes) {
            if (q < 7) continue;
            if ((q - 1) * lp > rem_size) break;
            if (!branch_component(st, p, q - 1, false, in_circ)) return false;
        }
        return true;
    }

    if (p == 7) {
        if (2 * lp <= rem_size) {
            if (!branch_component(st, p, 2, true, in_circ)) return false;
        }
        if (8 * lp <= rem_size) {
            if (!branch_component(st, p, 8, false, in_circ)) return false;
        }
        for (uint32_t q : small_primes) {
            if (q < 5) continue;
            if ((q - 1) * lp > rem_size) break;
            if (!branch_component(st, p, q - 1, false, in_circ)) return false;
        }
        return true;
    }

    // 3. 一般素数：标准分支 p^{q-1}（q >= 3 为素数）
    for (uint32_t q : small_primes) {
        if (q < 3) continue;
        if ((q - 1) * lp > rem_size) break;
        if (!branch_component(st, p, q - 1, false, in_circ)) return false;
    }
    return true;
}

bool solve(State& st, bool in_circ) {
    if (check_contradiction(st)) return true;

    // 正常分支：选当前最大的未分支素因子
    if (!st.unbranched.empty()) {
        mpz_class p = *st.unbranched.rbegin();
        return branch_prime(st, p, in_circ);
    }

    // 遇到路障（Roadblock）
    if (st.log_abund_hi >= LN2 - 1e-12) {
        ++failed_roadblocks;
        return false; // 丰度上界 >= 2，无法绕过
    }

    double rem_size = LOG_BOUND - (st.log_size_branched + st.log_size_comp);
    double abund_gap = LN2 - st.log_abund_hi;

    // 论文原版路障公式：找最小整数 p 使得 (2*t_a(p) - 1)*ln(p) > rem_size
    uint32_t b = 3;
    while (true) {
        double t = std::ceil(abund_gap / std::log(static_cast<double>(b) / (b - 1.0)));
        if ((2.0 * t - 1.0) * std::log(static_cast<double>(b)) > rem_size) break;
        ++b;
        if (b > 200000) { ++failed_roadblocks; return false; }
    }

    // 依次分支 < b 的所有未禁用、未分支素数（优先按 S_ORDER）
    State cur = st;
    std::set<uint32_t> tried;
    auto try_circ_prime = [&](uint32_t q_ui) -> bool {
        if (q_ui >= b || tried.count(q_ui)) return true;
        tried.insert(q_ui);
        mpz_class q(q_ui);
        if (cur.forbidden.count(q) || cur.branched.count(q)) return true;
        if (!branch_prime(cur, q, true)) return false;
        cur.forbidden.insert(q); // 排除后加入当前路障的禁用集
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
    int bound_exp = (argc >= 2) ? std::atoi(argv[1]) : 300;
    LOG_BOUND = bound_exp * std::log(10.0);

    init_primes(200000);
    if (!db.load("facts.idx", "facts.dat")) {
        std::cerr << "Error: failed to mmap facts.idx / facts.dat\n";
        return 1;
    }

    std::cout << "=== OPN Proof Tree Baseline (Target: 10^" << bound_exp << ") ===\n";
    auto t0 = std::chrono::steady_clock::now();

    std::set<mpz_class> global_forbidden;
    for (uint32_t p_ui : S_ORDER) {
        uint64_t b_before = total_branches;
        uint64_t c_before = circ_branches;
        uint64_t f_before = failed_roadblocks;

        State init_st;
        init_st.forbidden = global_forbidden;
        init_st.unbranched.insert(mpz_class(p_ui));

        auto tp0 = std::chrono::steady_clock::now();
        bool ok = solve(init_st, false);
        auto tp1 = std::chrono::steady_clock::now();
        double dt = std::chrono::duration<double>(tp1 - tp0).count();

        std::cout << "Forbid p=" << p_ui
                  << " -> " << (ok ? "PROVEN" : "FAILED")
                  << " | branches=" << (total_branches - b_before)
                  << " (circ=" << (circ_branches - c_before) << ")"
                  << " | failed_rb=" << (failed_roadblocks - f_before)
                  << " | " << dt << "s\n" << std::flush;

        if (!ok) break;
        global_forbidden.insert(mpz_class(p_ui));
    }

    auto t1 = std::chrono::steady_clock::now();
    double total_dt = std::chrono::duration<double>(t1 - t0).count();
    std::cout << "Total branches: " << total_branches
              << " (circ: " << circ_branches << "), failed_rb: " << failed_roadblocks
              << ", elapsed: " << total_dt << "s\n";
    return 0;
}
