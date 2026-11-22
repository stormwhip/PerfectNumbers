#define main ProofTreeV16Main
#include "ProofTreeV16.cpp"
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
    std::cout << "ProofCoreTestsV16: OK" << std::endl;
    return 0;
}
