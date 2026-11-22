#define main ProofTreeV22Main
#include "ProofTreeV22.cpp"
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
    // Independent exact arithmetic proof of a bound on even exponents.
    mpz_ui_pow_ui(EXACT_INTEGER_CAP.get_mpz_t(), 10, 2400);
    mpz_ui_pow_ui(EXACT_HALF_CAP.get_mpz_t(), 10, 1200);
    mpz_class small_half;
    mpz_ui_pow_ui(small_half.get_mpz_t(), 10, 3);
    assert(!opn::even_exponent_power_exceeds_half_bound(mpz_class(19), 2, small_half));
    assert(opn::even_exponent_power_exceeds_half_bound(mpz_class(19), 4, small_half));
    assert(!opn::even_exponent_power_exceeds_half_bound(mpz_class(19), 1, small_half));

    // Exact divisor product: sigma factors of DIFFERENT selected primes
    // multiply, including common prime factors.
    opn::ExactDivisorProducts products;
    products = opn::extend_forced_products(products, mpz_class(3), 2);
    assert(opn::mandatory_divisor(products) == 117);
    products = opn::extend_forced_products(products, mpz_class(7), 2);
    assert(opn::mandatory_divisor(products) == 108927);
    assert(mpz_divisible_ui_p(opn::mandatory_divisor(products).get_mpz_t(), 117));
    opn::ExactDivisorProducts special;
    special = opn::extend_forced_products(special, mpz_class(5), 1);
    assert(opn::mandatory_divisor(special) == 15);
    assert(mpz_divisible_ui_p(mpz_class(3906).get_mpz_t(), 31));
    opn::ExactDivisorProducts inexact;
    inexact = opn::extend_forced_products(inexact, mpz_class(5), 2);
    assert(opn::mandatory_divisor(inexact) == 775);
    // sigma(3^2)=13, sigma(61^2)=3783=3*13*97.
    // Taking LCM over individual sigmas loses a required factor of 13.
    opn::ExactDivisorProducts overlapping;
    overlapping = opn::extend_forced_products(overlapping, mpz_class(3), 2);
    overlapping = opn::extend_forced_products(overlapping, mpz_class(61), 2);
    const mpz_class full_required = opn::mandatory_divisor(overlapping);
    assert(full_required == 548985177);
    mpz_class naive = 1, s3 = 13, s61 = 3783, p3 = 9, p61 = 3721;
    mpz_lcm(naive.get_mpz_t(), naive.get_mpz_t(), p3.get_mpz_t());
    mpz_lcm(naive.get_mpz_t(), naive.get_mpz_t(), s3.get_mpz_t());
    mpz_lcm(naive.get_mpz_t(), naive.get_mpz_t(), p61.get_mpz_t());
    mpz_lcm(naive.get_mpz_t(), naive.get_mpz_t(), s61.get_mpz_t());
    assert(naive == 42229629);
    assert(full_required == naive * 13);

    // An exact, arithmetic-only test of how many top-level exponent options
    // can be discarded before sigma factorization: 1382 of 3072 at 2400.
    uint64_t all_options = 0, directly_impossible = 0;
    for (uint32_t q : ROOT_ORDER) {
        const auto choices = get_exponents(empty, mpz_class(q));
        for (const auto& [a, exact] : choices) {
            ++all_options;
            if (opn::even_exponent_power_exceeds_half_bound(
                    mpz_class(q), a, EXACT_HALF_CAP)) ++directly_impossible;
        }
    }
    assert(all_options == 3072);
    assert(directly_impossible == 1382);
    std::cout << "ProofCoreTestsV22: OK" << std::endl;
    return 0;
}
