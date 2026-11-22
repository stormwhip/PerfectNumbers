// Sources/Cpp/V21FrontierCodecTests.cpp
#include "V21FrontierCodec.hpp"
#include <cassert>
#include <iostream>

int main() {
    using namespace opn_v21;
    const std::vector<uint32_t> circ_order = {19, 7, 11, 31, 13, 3, 5, 17};

    // 1. Non-ascending forbidden_small {19, 7} + CIRC_ORDER mask (bits 0 and 1 -> 0b11 = 3)
    V21State st;
    st.forbidden = {mpz_class(7), mpz_class(19)};
    st.forbidden_small = {19, 7}; // Append order, NOT ascending
    st.outer_root_mask = 3;       // circ_order[0]=19, circ_order[1]=7
    st.branched[mpz_class(11)] = {2, false, 0};
    st.composites = {mpz_class(1019) * mpz_class(1021), mpz_class(1009) * mpz_class(1013)};
    st.certified_residue_count = 1;
    st.source_v_bounds = {{mpz_class(3), mpz_class(11), 1}};

    auto bytes = serialize_state(st, circ_order, false);
    auto rt = deserialize_state(bytes.data(), bytes.size(), circ_order, false);
    assert(rt.forbidden_small == st.forbidden_small); // Exact append order preserved
    assert(rt.composites == st.composites);           // Exact composite order preserved
    assert(rt.outer_root_mask == 3);

    // 2. Permuted ROOT_ORDER (e.g. 7 first, then 19): if 7 excluded (circ_order[1]), mask is 0b10 = 2
    V21State st_perm;
    st_perm.forbidden = {mpz_class(7)};
    st_perm.forbidden_small = {7};
    st_perm.outer_root_mask = 2; // bit 1 in CIRC_ORDER
    auto bytes_p = serialize_state(st_perm, circ_order, false);
    auto rt_p = deserialize_state(bytes_p.data(), bytes_p.size(), circ_order, false);
    assert(rt_p.outer_root_mask == 2);

    // 3. Negative test: wrong mask bit (bit 0 = 19 not in forbidden) must throw
    bool threw = false;
    try {
        st_perm.outer_root_mask = 1;
        serialize_state(st_perm, circ_order, false);
    } catch (const std::runtime_error&) { threw = true; }
    assert(threw);

    // 4. Negative test: invalid source_v_bounds (source_p not in branched) must throw
    threw = false;
    try {
        st.source_v_bounds.push_back({mpz_class(5), mpz_class(97), 1});
        serialize_state(st, circ_order, false);
    } catch (const std::runtime_error&) { threw = true; }
    assert(threw);

    std::cout << "V21FrontierCodecTests: ALL ORDER, MASK, AND INVARIANT TESTS PASSED\n";
    return 0;
}
