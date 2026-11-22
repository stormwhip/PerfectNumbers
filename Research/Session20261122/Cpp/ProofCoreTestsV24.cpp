#define main ProofTreeV24Main
#include "ProofTreeV24.cpp"
#undef main
#include <cassert>
#include <random>
// Independent reference implementation from V21's original composite-size logic.
static double reference_composite_size(const State& state) {
    double result = 0.0;
    std::vector<const mpz_class*> chosen;
    for (const auto& c : state.composites) {
        bool independent = true;
        for (const auto& [p, info] : state.branched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { independent = false; break; }
        }
        if (!independent) continue;
        for (const auto& p : state.unbranched) {
            if (mpz_divisible_p(c.get_mpz_t(), p.get_mpz_t())) { independent = false; break; }
        }
        if (!independent) continue;
        for (const auto* d : chosen) {
            mpz_class g;
            mpz_gcd(g.get_mpz_t(), c.get_mpz_t(), d->get_mpz_t());
            if (g > 1) { independent = false; break; }
        }
        if (independent) {
            result += mpz_log(c);
            chosen.push_back(&c);
        }
    }
    return result;
}


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
    // Exhaustive finite verification of actual get_exponents() covering
    // every admissible Euler/ordinary exponent within the 10^2400 size bound.
    // A nonexact branch a covers e whenever (a+1)|(e+1) and a<=e,
    // since sigma(p^a) then divides sigma(p^e).
    init_primes(300000);
    LOG_BOUND = 2400.0 * std::log(10.0);
    State empty;
    uint64_t covered_cases = 0;
    for (uint32_t q : ROOT_ORDER) {
        const auto choices = get_exponents(empty, mpz_class(q));
        const int emax = static_cast<int>(std::ceil(LOG_BOUND / std::log(q))) + 2;
        for (int e = 1; e <= emax; ++e) {
            const bool ordinary = (e % 2 == 0);
            const bool euler = (q % 4 == 1 && e % 4 == 1);
            if ((!ordinary && !euler) ||
                e * std::log(static_cast<double>(q)) >= LOG_BOUND) continue;
            bool found = false;
            for (const auto& [a, exact] : choices) {
                if (exact && a == static_cast<uint64_t>(e)) found = true;
                if (!exact && a <= static_cast<uint64_t>(e) &&
                    (static_cast<uint64_t>(e) + 1) % (a + 1) == 0) found = true;
            }
            assert(found);
            ++covered_cases;
        }
    }
    assert(covered_cases > 10000);
    // Randomized differential test against the original V21 implementation.
    std::mt19937_64 rng(24001122ULL);
    const uint32_t test_primes[] = {3,5,7,11,13,17,19,23,29,31,37,41,43,47};
    for (int trial = 0; trial < 4000; ++trial) {
        State state;
        for (int j = 0; j < 14; ++j) {
            uint64_t decision = rng() % 7;
            if (decision == 0) state.branched[mpz_class(test_primes[j])] = {2,false,0};
            else if (decision == 1) state.unbranched.insert(mpz_class(test_primes[j]));
        }
        for (int j = 0, count = static_cast<int>(rng() % 24); j < count; ++j) {
            mpz_class residual = 1;
            for (int k = 0, len = 1 + static_cast<int>(rng() % 5); k < len; ++k) {
                residual *= static_cast<unsigned long>(test_primes[rng() % 14]);
            }
            state.composites.push_back(residual);
        }
        double expected = reference_composite_size(state);
        refresh_composite_size_bound(state);
        assert(expected == state.log_size_comp);
    }
    // Include a large residual that shares a small factor with a known prime.
    State special_state;
    special_state.branched[mpz_class(13)] = {2,false,0};
    special_state.composites.push_back(mpz_class("100000000000000000000000000000000003"));
    special_state.composites.push_back(mpz_class(13) * mpz_class("100000000000000000000000000000000003"));
    special_state.composites.push_back(mpz_class("100000000000000000000000000000000019"));
    const double expected_large = reference_composite_size(special_state);
    refresh_composite_size_bound(special_state);
    assert(expected_large == special_state.log_size_comp);
    std::cout << "ProofCoreTestsV24: OK" << std::endl;
    return 0;
}
