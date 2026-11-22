#define main ProofTreeV11Main
#include "ProofTreeV11.cpp"
#undef main
#include <sstream>
#include <limits>

int main(int argc, char** argv) {
    const int bound_exp = (argc >= 2) ? std::atoi(argv[1]) : 300;
    omp_set_dynamic(0);
    omp_set_num_threads(1);
    LOG_BOUND = bound_exp * std::log(10.0);
    init_primes(300000);
    if (!db.load("facts.idx", "facts.dat")) {
        std::cerr << "Error: failed to mmap facts.idx / facts.dat\n";
        return 1;
    }

    const size_t n = ROOT_ORDER.size();
    if (n >= 20) {
        std::cerr << "Root set too large for exhaustive subset profiling\n";
        return 2;
    }
    const uint32_t state_count = 1U << n;
    std::cout << "PROFILE_META,exponent," << bound_exp
              << ",roots," << n << ",threads,1\n";
    std::cout << "EDGE,mask,root,branches,seconds,status\n";

    for (uint32_t mask = 0; mask < state_count; ++mask) {
        for (size_t i = 0; i < n; ++i) {
            if (mask & (1U << i)) continue;
            const uint32_t root = ROOT_ORDER[i];
            total_branches.store(0);
            circ_branches.store(0);
            failed_roadblocks.store(0);
            max_rb_b.store(0);
            heavy_rb_printed.store(0);
            outstanding_branch_tasks.store(0);
            fact_cache.clear();

            State initial;
            for (size_t j = 0; j < n; ++j) {
                if (mask & (1U << j)) {
                    initial.forbidden.insert(mpz_class(ROOT_ORDER[j]));
                    initial.forbidden_small.push_back(ROOT_ORDER[j]);
                }
            }
            initial.unbranched.insert(mpz_class(root));

            std::atomic<bool> ok_flag{true};
            bool solved = false;
            const auto t0 = std::chrono::steady_clock::now();
            #pragma omp parallel
            {
                #pragma omp single
                {
                    solved = solve(initial, false, 0, ok_flag);
                }
            }
            const auto t1 = std::chrono::steady_clock::now();
            const double seconds = std::chrono::duration<double>(t1 - t0).count();
            const uint64_t branches = total_branches.load();
            const bool proven = solved && ok_flag.load() && failed_roadblocks.load() == 0;
            std::cout << "EDGE," << mask << "," << root << "," << branches
                      << "," << seconds << "," << (proven ? "PROVEN" : "FAILED")
                      << std::endl;
            if (!proven) {
                std::cerr << "Incomplete edge: mask=" << mask << " root=" << root << "\n";
                return 3;
            }
        }
    }
    std::cout << "PROFILE_COMPLETE," << (n * (state_count / 2))
              << ",edges_expected\n";
    return 0;
}
