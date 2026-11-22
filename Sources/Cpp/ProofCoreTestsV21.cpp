#define main ProofTreeV21Main
#include "ProofTreeV21.cpp"
#undef main
#include <cassert>

int main() {
    const double u3 = lp_prime_abundancy_upper(mpz_class(3));
    assert(u3 > std::log(1.5));
    PREFIX_DUALS[0] = {1.0, 1.0, true, {}, {}};
    ACTIVE_PREFIX_MASK = 0;
    State st;
    st.branched[mpz_class(3)] = {2, false, 0};
    st.log_size_branched = 2.0 * std::log(3.0);
    st.lp_known_abund_upper = u3;
    LOG_BOUND = 3.7;
    assert(!check_state_lp_contradiction(st));
    PREFIX_DUALS[0].removable_gain[3] = 0.3;
    st.forbidden.insert(mpz_class(5));
    LOG_BOUND = 3.7;
    assert(check_state_lp_contradiction(st));
    st.unbranched.insert(mpz_class(7));
    LOG_BOUND = 1.0;
    assert(check_state_lp_contradiction(st));
    st.lp_known_abund_upper = 0.0;
    st.branched.clear();
    st.log_size_branched = 0.0;
    st.forbidden.clear();
    st.unbranched.clear();
    st.unbranched.insert(mpz_class(7));
    PREFIX_DUALS[0] = {1.0, 0.0, true, {}, {}};
    LOG_BOUND = 0.70;
    assert(!check_state_lp_contradiction(st));
    PREFIX_DUALS[0].forced_gain[7] = 0.50;
    assert(check_state_lp_contradiction(st));
    // Counterexample to the old ALPHA=10^8 heuristic:
    // 1009*1013 survives trial division by all primes <=1000.
    // Its two unknown prime factors each contribute positive abundance.
    mpz_class comp = mpz_class(1009) * mpz_class(1013);
    assert(residual_factor_count_upper(comp) == 2);
    double valid_upper = 2.0 * RESIDUAL_ABUND_UPPER;
    double true_abund = std::log(1009.0 / 1008.0) +
                        std::log(1013.0 / 1012.0);
    assert(valid_upper >= true_abund);
    assert(residual_factor_count_upper(mpz_class(1009)) == 1);
    assert(residual_factor_count_upper(mpz_class(1009) * mpz_class(1009)) == 2);
    assert(residual_factor_count_upper(mpz_class(1)) == 0);
    // Small deterministic cutoff product: divisible by 1009 and 1013 only.
    PRIME_CUTOFF_PRODUCT = mpz_class(1009) * mpz_class(1013);
    double bound_bad = certify_sigma_residual_abundance_upper(PRIME_CUTOFF_PRODUCT);
    double actual_bad = std::log(1009.0/1008.0) + std::log(1013.0/1012.0);
    assert(bound_bad >= actual_bad);
    // This synthetic cutoff is *not* the complete 1e8 primorial, so the
    // second test uses only factors above the cutoff's maximum.
    // A synthetic large-prime square certifies the lazy-upgrade accounting:
    // ordinary conservative bound is much weaker, certification replaces
    // it once, and child states preserve the certified residual prefix.
    mpz_class big_prime("100000007");
    mpz_class square = big_prime * big_prime;
    State example;
    example.composites.push_back(square);
    example.log_abund_hi =
        static_cast<double>(residual_factor_count_upper(square)) *
        RESIDUAL_ABUND_UPPER;
    const double weak = example.log_abund_hi;
    strengthen_composite_residuals(example);
    assert(example.certified_residue_count == 1);
    assert(example.log_abund_hi > 0.0 && example.log_abund_hi < weak);
    const double strong = example.log_abund_hi;
    strengthen_composite_residuals(example);
    assert(example.log_abund_hi == strong);
    State fork = example;
    fork.composites.push_back(square);
    fork.log_abund_hi += weak;
    strengthen_composite_residuals(fork);
    assert(fork.certified_residue_count == 2);
    assert(fork.log_abund_hi > strong && fork.log_abund_hi < strong + weak);
    std::cout << "ProofCoreTestsV21: OK" << std::endl;
    return 0;
}
