#define main ProofTreeV12Main
#include "ProofTreeV12.cpp"
#undef main
#include <cassert>

int main() {
    const double u3 = lp_prime_abundancy_upper(mpz_class(3));
    const double u5 = lp_prime_abundancy_upper(mpz_class(5));
    assert(u3 > std::log(1.5));
    assert(u5 > std::log(1.25));

    PREFIX_DUALS[0] = {1.0, 1.0, true};
    ACTIVE_PREFIX_MASK = 0;
    State st;
    st.branched[mpz_class(3)] = {2, false, 0};
    st.log_size_branched = 2.0 * std::log(3.0);
    st.lp_known_abund_upper = u3;
    LOG_BOUND = 3.4;
    assert(check_state_lp_contradiction(st));
    LOG_BOUND = 3.7;
    assert(!check_state_lp_contradiction(st));
    st.unbranched.insert(mpz_class(5));
    LOG_BOUND = 1.0;
    assert(!check_state_lp_contradiction(st));
    std::cout << "ProofCoreTestsV12: OK" << std::endl;
    return 0;
}
