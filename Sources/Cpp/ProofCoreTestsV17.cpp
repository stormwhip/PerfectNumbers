#define main ProofTreeV17Main
#include "ProofTreeV17.cpp"
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
    // V17 deliberately replaces V16's independent forced_gain with option costs.
    PREFIX_DUALS[0].euler_costs[7] = {0.50, 0.0, 0.0, false};
    assert(check_state_lp_contradiction(st));
    State coupled;
    coupled.unbranched.insert(mpz_class(5));
    coupled.unbranched.insert(mpz_class(13));
    PREFIX_DUALS[0] = {1.0, 0.0, true, {}, {}, {}};
    EulerOptionCosts costs = {1.0, -2.0, -2.0, true};
    PREFIX_DUALS[0].euler_costs[5] = costs;
    PREFIX_DUALS[0].euler_costs[13] = costs;
    const double gain = euler_coupled_gain_lower(coupled, PREFIX_DUALS[0]);
    assert(gain > 2.99999999 && gain <= 3.0);
    LOG_BOUND = 2.0;
    assert(check_state_lp_contradiction(coupled));
    coupled.has_special = true;
    const double no_slot_gain = euler_coupled_gain_lower(coupled, PREFIX_DUALS[0]);
    assert(no_slot_gain > 5.99999999 && no_slot_gain <= 6.0);
    std::cout << "ProofCoreTestsV17: OK" << std::endl;
    return 0;
}
