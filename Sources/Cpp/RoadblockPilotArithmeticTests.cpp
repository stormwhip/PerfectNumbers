#include "RoadblockPilotArithmetic.hpp"

#include <cassert>
#include <iostream>

int main() {
    using namespace opn_roadblock;
    // Known exact rational identities, checked using interval addition.
    const auto a = log_ratio(2), b = log_ratio(3), c = log_ratio(6);
    assert(c.first <= a.second+b.second && c.second >= a.first+b.first);
    assert(a.first < a.second && a.second-a.first < 100);
    Int previous_log = 0, previous_abund = Scale;
    for (uint32_t q = 3; q <= 300000; q += 2) {
        const auto log_q = log_ratio(q).first;
        const auto abund = log_ratio(q,q-1).second;
        assert(log_q >= previous_log && abund <= previous_abund);
        previous_log = log_q;
        previous_abund = abund;
    }

    // At an even kink the special alternative is active with its own slope.
    Dual at_kink(7, Den);
    at_kink.add(3, 6, 2, true, Den);
    assert(at_kink.value-at_kink.gamma == 4*Den);
    assert(at_kink.supergradient() == 1);
    assert(at_kink.passes(3) && !at_kink.passes(4));
    Dual with_tail(7, Den);
    with_tail.special_gain(2*Den, 5);
    assert(with_tail.supergradient() == 2 && with_tail.passes(4));
    std::cout << "fixed-point endpoint monotonicity and strict dual comparisons passed\n";
}
