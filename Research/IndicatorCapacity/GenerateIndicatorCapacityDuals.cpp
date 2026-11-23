#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using u64 = uint64_t;
using u128 = __uint128_t;

static inline u64 mulmod(u64 a, u64 b, u64 m) {
    return (u64)((u128)a * b % m);
}

static u64 powmod(u64 a, u64 e, u64 m) {
    u64 r = 1 % m;
    a %= m;
    while (e) {
        if (e & 1) r = mulmod(r, a, m);
        a = mulmod(a, a, m);
        e >>= 1;
    }
    return r;
}

static bool is_prime_64(u64 n) {
    if (n < 2) return false;
    static const u64 small_p[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (u64 p : small_p) {
        if (n == p) return true;
        if (n % p == 0) return false;
    }
    u64 d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; ++s; }
    static const u64 bases[] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    for (u64 a : bases) {
        if (a % n == 0) continue;
        u64 x = powmod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool comp = true;
        for (int r = 1; r < s; ++r) {
            x = mulmod(x, x, n);
            if (x == n - 1) { comp = false; break; }
        }
        if (comp) return false;
    }
    return true;
}

static u64 pollard_rho_64(u64 n) {
    if ((n & 1) == 0) return 2;
    if (n % 3 == 0) return 3;
    for (u64 c = 1; c < 64; ++c) {
        u64 x = 2, y = 2, d = 1;
        auto f = [&](u64 v) { return (mulmod(v, v, n) + c) % n; };
        while (d == 1) {
            x = f(x);
            y = f(f(y));
            u64 diff = x > y ? x - y : y - x;
            d = std::gcd(diff, n);
        }
        if (d != n) return d;
    }
    return n;
}

static void factor_64_rec(u64 n, std::vector<u64>& out) {
    if (n <= 1) return;
    if (is_prime_64(n)) {
        out.push_back(n);
        return;
    }
    u64 d = pollard_rho_64(n);
    if (d == n) return;
    factor_64_rec(d, out);
    factor_64_rec(n / d, out);
}

static std::vector<u64> sieve_primes(u64 limit) {
    std::vector<uint8_t> is_p(limit + 1, 1);
    is_p[0] = is_p[1] = 0;
    for (u64 i = 2; i * i <= limit; ++i) {
        if (is_p[i]) {
            for (u64 j = i * i; j <= limit; j += i) is_p[j] = 0;
        }
    }
    std::vector<u64> res;
    for (u64 i = 2; i <= limit; ++i) if (is_p[i]) res.push_back(i);
    return res;
}

static bool sigma_has_forb(u64 r, int f, const std::vector<u64>& forb) {
    for (u64 z : forb) {
        if (r % z == 1) {
            if ((f + 1) % z == 0) return true;
        } else {
            if (powmod(r, (u64)(f + 1), z) == 1) return true;
        }
    }
    return false;
}

static int get_f_min(u64 r, const std::vector<u64>& forb) {
    for (int f = 2; f <= 200; f += 2) {
        if (!sigma_has_forb(r, f, forb)) return f;
    }
    return 200;
}

static u128 sigma_u128(u64 r, int f) {
    u128 s = 1;
    u128 term = 1;
    u128 max_v = ((u128)1 << 126);
    for (int i = 1; i <= f; ++i) {
        if (term > max_v / r) return 0;
        term *= r;
        s += term;
    }
    return s;
}

static std::vector<u64> extract_prime_factors(u128 val, u64 p, u64 W_max, const std::vector<u64>& trial_p) {
    while (val % p == 0) val /= p;
    std::vector<u64> facs;
    for (u64 d : trial_p) {
        if ((u128)d * d > val) break;
        if (val % d == 0) {
            while (val % d == 0) val /= d;
            if (d <= W_max) facs.push_back(d);
        }
    }
    if (val > 1 && val <= (u128)UINT64_MAX) {
        u64 v64 = (u64)val;
        std::vector<u64> tmp;
        factor_64_rec(v64, tmp);
        for (u64 w : tmp) {
            if (w <= W_max) facs.push_back(w);
        }
    }
    std::sort(facs.begin(), facs.end());
    facs.erase(std::unique(facs.begin(), facs.end()), facs.end());
    return facs;
}

struct Opt {
    int f;
    int vp;
    double ab;
    std::vector<int> w_ids;
};

struct Solver {
    u64 p;
    std::vector<u64> forb;
    std::unordered_set<u64> forb_set;
    double target;
    u64 R_act;
    u64 W_max;
    std::vector<u64> all_primes;
    std::vector<u64> trial_p;

    std::vector<u64> node_p;
    std::unordered_map<u64, int> p_to_id;
    std::vector<int> node_fmin;
    std::vector<int> node_fcap;
    std::vector<std::vector<Opt>> node_opts;
    std::vector<std::vector<std::pair<int, int>>> rev;

    int get_or_add_node(u64 q) {
        auto it = p_to_id.find(q);
        if (it != p_to_id.end()) return it->second;
        int id = (int)node_p.size();
        p_to_id[q] = id;
        node_p.push_back(q);
        node_fmin.push_back(get_f_min(q, forb));
        node_fcap.push_back(0);
        node_opts.emplace_back();
        rev.emplace_back();
        return id;
    }

    std::vector<u64> expand_node(u64 r, int f_cap) {
        int rid = get_or_add_node(r);
        if (node_fcap[rid] >= f_cap) return {};
        node_fcap[rid] = f_cap;
        node_opts[rid].clear();
        std::vector<u64> discovered;
        for (int f = 2; f < f_cap; f += 2) {
            if (sigma_has_forb(r, f, forb)) continue;
            int vp = 0;
            if (r % p == 1) {
                int t = f + 1;
                while (t % (int)p == 0) { t /= (int)p; ++vp; }
            }
            double ab = std::log((double)r / (double)(r - 1));
            double rf1 = std::pow((double)r, -(double)(f + 1));
            if (rf1 < 0.5) ab += std::log1p(-rf1);

            u128 val = sigma_u128(r, f);
            std::vector<int> w_ids;
            if (val > 0) {
                auto ws = extract_prime_factors(val, p, W_max, trial_p);
                for (u64 w : ws) {
                    if (w == r || w == p || forb_set.count(w)) continue;
                    int wid = get_or_add_node(w);
                    w_ids.push_back(wid);
                    discovered.push_back(w);
                }
            }
            node_opts[rid].push_back(Opt{f, vp, ab, std::move(w_ids)});
        }
        return discovered;
    }

    void build_graph(u64 r_act, u64 w_max, int expand_hop2_limit_r, u64 hop2_max_w) {
        R_act = r_act;
        W_max = w_max;
        forb_set.clear();
        for (u64 z : forb) forb_set.insert(z);
        target = std::log(2.0) - std::log((double)p / (double)(p - 1));
        all_primes = sieve_primes(std::max<u64>(R_act, 200000));
        trial_p.clear();
        for (u64 q : all_primes) {
            if (q <= 10000) trial_p.push_back(q);
            else break;
        }

        std::vector<u64> hop2_candidates;
        for (u64 r : all_primes) {
            if (r <= 2 || r == p || forb_set.count(r)) continue;
            if (r > R_act) break;
            int fc = 10;
            if (r <= 80) fc = 64;
            else if (r <= 300) fc = 42;
            else if (r <= 1500) fc = 26;
            else if (r <= 6000) fc = 18;
            else if (r <= 20000) fc = 14;
            else fc = 10;
            auto ws = expand_node(r, fc);
            if ((int)r <= expand_hop2_limit_r) {
                for (u64 w : ws) {
                    if (w > R_act && w <= hop2_max_w) hop2_candidates.push_back(w);
                }
            }
        }
        std::sort(hop2_candidates.begin(), hop2_candidates.end());
        hop2_candidates.erase(std::unique(hop2_candidates.begin(), hop2_candidates.end()), hop2_candidates.end());

        for (u64 w : hop2_candidates) {
            int fm = get_f_min(w, forb);
            int fc = std::min(16, fm + 8);
            expand_node(w, fc);
        }

        for (auto& v : rev) v.clear();
        for (int rid = 0; rid < (int)node_p.size(); ++rid) {
            if (node_fcap[rid] == 0) continue;
            for (int i = 0; i < (int)node_opts[rid].size(); ++i) {
                for (int wid : node_opts[rid][i].w_ids) {
                    rev[wid].push_back({rid, i});
                }
            }
        }
        std::cerr << "Root p=" << p << " graph built: total_nodes=" << node_p.size()
                  << " hop2_expanded=" << hop2_candidates.size() << "\n";
    }

    struct DualResult {
        double val_log10;
        double mu;
        double lam_r;
        double delta_src_log10;
        int used_nodes;
        std::vector<std::tuple<u64, int, u64, int64_t>> flows_scaled; // flow * 10^6 (integer!)
    };

    DualResult solve_one(double mu, double lam_r, bool save_flows = false, double max_theta_cap = 1e9) {
        double lp = std::log((double)p);
        double lam = lam_r * lp;
        int f_p1 = (int)p - 1;
        if (lam > f_p1 * std::log((double)R_act) - mu / (double)(R_act - 1)) {
            return {-1e9, mu, lam_r, 0.0, 0, {}};
        }

        int N = (int)node_p.size();
        std::vector<double> cap(N, 0.0);
        for (int w = 0; w < N; ++w) {
            u64 pw = node_p[w];
            double c = node_fmin[w] * std::log((double)pw)
                     - ((pw % p == 1) ? lam : 0.0)
                     - mu * std::log((double)pw / (double)(pw - 1));
            cap[w] = std::min(max_theta_cap, std::max(0.0, c));
        }

        std::vector<int> order(N);
        std::iota(order.begin(), order.end(), 0);
        std::sort(order.begin(), order.end(), [&](int a, int b) { return node_p[a] > node_p[b]; });

        std::vector<std::vector<double>> pen(N);
        for (int r = 0; r < N; ++r) pen[r].assign(node_opts[r].size(), 0.0);
        std::vector<double> theta_used(N, 0.0);
        std::vector<std::tuple<u64, int, u64, int64_t>> flows_scaled;

        auto compute_tail_rc = [&](int r) {
            u64 pr = node_p[r];
            double lr = std::log((double)pr);
            double ab_max = std::log((double)pr / (double)(pr - 1));
            int fc = node_fcap[r];
            double trc = fc * lr - mu * ab_max;
            if (pr % p == 1) {
                u64 pb = p;
                for (int b = 1; b <= 6; ++b) {
                    int fb = (int)pb - 1;
                    if (fb >= fc) {
                        trc = std::min(trc, fb * lr - b * lam - mu * ab_max);
                    }
                    pb *= p;
                }
            }
            return trc;
        };

        int rounds = 7;
        for (int rnd = 0; rnd < rounds; ++rnd) {
            if (rnd > 0) {
                for (int w : order) {
                    if (node_fcap[w] == 0) continue;
                    u64 pw = node_p[w];
                    double lw = std::log((double)pw);
                    double cur_min = compute_tail_rc(w);
                    for (int i = 0; i < (int)node_opts[w].size(); ++i) {
                        const auto& o = node_opts[w][i];
                        double v = o.f * lw + pen[w][i] - lam * o.vp - mu * o.ab;
                        if (v < cur_min) cur_min = v;
                    }
                    cap[w] = std::min(max_theta_cap, std::max(0.0, cur_min));
                }
            }
            for (int r = 0; r < N; ++r) std::fill(pen[r].begin(), pen[r].end(), 0.0);
            std::fill(theta_used.begin(), theta_used.end(), 0.0);
            if (save_flows && rnd == rounds - 1) flows_scaled.clear();

            std::vector<std::vector<double>> r_rcs(N);
            for (int r = 0; r < N; ++r) {
                if (node_fcap[r] == 0) continue;
                double lr = std::log((double)node_p[r]);
                r_rcs[r].resize(node_opts[r].size());
                for (int i = 0; i < (int)node_opts[r].size(); ++i) {
                    const auto& o = node_opts[r][i];
                    r_rcs[r][i] = o.f * lr - lam * o.vp - mu * o.ab;
                }
            }

            for (int w : order) {
                double c = cap[w];
                if (c <= 1e-9 || rev[w].empty()) continue;
                std::vector<std::tuple<double, int, int>> needy;
                for (auto [r, i] : rev[w]) {
                    double cur = r_rcs[r][i] - theta_used[r];
                    if (cur < -1e-9) needy.push_back({cur, r, i});
                }
                if (needy.empty()) continue;
                std::sort(needy.begin(), needy.end());
                double rem = c;
                for (auto [_, r, i] : needy) {
                    if (rem <= 1e-9) break;
                    double cur = r_rcs[r][i] - theta_used[r];
                    double need = -cur;
                    if (need <= 1e-9) continue;
                    double give = std::min(rem, need);
                    // quantize down to 10^-6 so exact rational sum <= cap[w] strictly!
                    int64_t q_give = (int64_t)std::floor(give * 1e6);
                    if (q_give <= 0) continue;
                    double d_give = q_give * 1e-6;
                    pen[r][i] += d_give;
                    r_rcs[r][i] += d_give;
                    theta_used[w] += d_give;
                    rem -= d_give;
                    if (save_flows && rnd == rounds - 1) {
                        flows_scaled.push_back({node_p[r], node_opts[r][i].f, node_p[w], q_give});
                    }
                }
            }
        }

        double total_neg = 0.0;
        double delta_src = 0.0;
        int used_cnt = 0;
        for (int w = 0; w < N; ++w) {
            double best_rc = 0.0;
            if (node_fcap[w] > 0) {
                double lw = std::log((double)node_p[w]);
                best_rc = compute_tail_rc(w) - theta_used[w];
                for (int i = 0; i < (int)node_opts[w].size(); ++i) {
                    const auto& o = node_opts[w][i];
                    double rc = o.f * lw + pen[w][i] - theta_used[w] - lam * o.vp - mu * o.ab;
                    if (rc < best_rc) best_rc = rc;
                }
                if (best_rc < 0.0) total_neg += best_rc;
            }
            if (theta_used[w] > 1e-9) {
                ++used_cnt;
                double ab_max = std::log((double)node_p[w] / (double)(node_p[w] - 1));
                double d_w = theta_used[w] + mu * ab_max + std::min(0.0, best_rc);
                if (d_w > delta_src) delta_src = d_w;
            }
        }
        double val = (mu * (target - 0.001) + total_neg) / std::log(10.0);
        return {val, mu, lam_r, delta_src / std::log(10.0), used_cnt, std::move(flows_scaled)};
    }
};

void export_certs(const std::string& filename, u64 root, const std::vector<u64>& forb,
                  u64 R_act, u64 W_max, int hop2_r, u64 hop2_w,
                  const std::vector<double>& lams, const std::vector<double>& mus, double theta_cap_digits) {
    Solver S;
    S.p = root;
    S.forb = forb;
    S.build_graph(R_act, W_max, hop2_r, hop2_w);

    std::ofstream out(filename);
    out << "{\n";
    out << "  \"root\": " << root << ",\n";
    out << "  \"forbidden\": [";
    for (size_t i = 0; i < forb.size(); ++i) out << (i ? ", " : "") << forb[i];
    out << "],\n";
    out << "  \"R_act\": " << R_act << ",\n";
    out << "  \"W_max\": " << W_max << ",\n";
    out << "  \"flow_scale\": 1000000,\n";
    out << "  \"duals\": [\n";

    bool first = true;
    for (double lam_r : lams) {
        Solver::DualResult best{-1e9, 0, lam_r, 0, 0, {}};
        for (double mu : mus) {
            auto res = S.solve_one(mu, lam_r, false, theta_cap_digits * std::log(10.0));
            if (res.val_log10 > best.val_log10) best = std::move(res);
        }
        if (best.val_log10 < -1e8) continue;
        // Re-solve with save_flows = true
        best = S.solve_one(best.mu, lam_r, true, theta_cap_digits * std::log(10.0));
        std::cout << std::fixed << std::setprecision(2)
                  << "p=" << root << " lam_r=" << std::setw(4) << lam_r
                  << " mu=" << std::setw(6) << best.mu
                  << " const=" << std::setw(7) << best.val_log10
                  << " delta_src=" << std::setw(5) << best.delta_src_log10
                  << " flows=" << best.flows_scaled.size() << "\n";

        if (!first) out << ",\n";
        first = false;
        out << "    {\n";
        out << "      \"mu_num\": " << (int64_t)std::llround(best.mu) << ",\n";
        out << "      \"mu_den\": 1,\n";
        out << "      \"lam_p_num\": " << (int64_t)std::llround(lam_r) << ",\n";
        out << "      \"lam_p_den\": 1,\n";
        out << "      \"float_const_log10\": " << std::fixed << std::setprecision(4) << best.val_log10 << ",\n";
        out << "      \"flows\": [";
        for (size_t i = 0; i < best.flows_scaled.size(); ++i) {
            auto [r, f, w, q] = best.flows_scaled[i];
            if (i) out << ",";
            out << "[" << r << "," << f << "," << w << "," << q << "]";
        }
        out << "]\n";
        out << "    }";
    }
    out << "\n  ]\n}\n";
    out.close();
}

int main() {
    export_certs("CandidateDualP5.json", 5, {19, 7, 11, 31, 13, 3},
                 120000, 1000000000000000000ULL - 1, 5000, 100000000ULL,
                 {0, 4, 8, 12, 16, 20, 24, 28},
                 {6000, 7500, 9000, 10500, 12000}, 20.0);
    export_certs("CandidateDualP3.json", 3, {19, 7, 11, 31, 13},
                 150000, 1000000000000000000ULL - 1, 4000, 80000000ULL,
                 {0, 5, 10, 15, 20, 21},
                 {0, 50, 150, 250, 350}, 6.0);
    return 0;
}
