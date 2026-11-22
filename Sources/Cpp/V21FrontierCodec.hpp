// Sources/Cpp/V21FrontierCodec.hpp
// Version 2 deterministic state codec for V21:
// - Preserves V21 append-order of forbidden_small (no erroneous ascending requirement)
// - Interprets outer_root_mask strictly via fixed CIRC_ORDER coordinates
// - Preserves composites order and certified_residue_count prefix invariant
#pragma once

#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace opn_v21 {

constexpr uint32_t kStateMagic = 0x324E504Fu; // "OPN2" little-endian
constexpr uint16_t kStateVersion = 2;
constexpr uint16_t kFlagHasFloatHints = 0x0001;
constexpr uint32_t kMaxMpzBytes = 65536;
constexpr uint32_t kMaxCollectionSize = 1000000;

struct BranchedInfoV2 {
    uint64_t exp = 0;
    bool exact = false;
    uint64_t seen_in_sigma = 0; // V21 legacy cumulative field
};

struct SourceVBound {
    mpz_class target_q;
    mpz_class source_p;
    uint64_t lower_bound = 0;
};

struct FloatHints {
    double log_size_branched = 0.0;
    double log_size_comp = 0.0;
    double log_abund_lo = 0.0;
    double log_abund_hi = 0.0;
    double lp_known_abund_upper = 0.0;
};

struct V21State {
    std::set<mpz_class> forbidden;
    std::vector<uint64_t> forbidden_small; // ORDER-PRESERVED (V21 append order, unique odd >= 3)
    std::map<mpz_class, BranchedInfoV2> branched;
    std::set<mpz_class> unbranched;
    std::vector<mpz_class> composites;     // ORDER-PRESERVED (greedy size + prefix certification)
    bool has_special = false;
    uint32_t certified_residue_count = 0;
    uint32_t outer_root_mask = 0;          // Bit i corresponds strictly to circ_order[i]
    std::vector<SourceVBound> source_v_bounds;

    bool has_float_hints = false;
    FloatHints hints{};
};

class ByteWriter {
public:
    void write_u8(uint8_t v) { buf_.push_back(v); }
    void write_u16(uint16_t v) {
        for (int i = 0; i < 2; ++i) buf_.push_back(static_cast<uint8_t>((v >> (8 * i)) & 0xFF));
    }
    void write_u32(uint32_t v) {
        for (int i = 0; i < 4; ++i) buf_.push_back(static_cast<uint8_t>((v >> (8 * i)) & 0xFF));
    }
    void write_u64(uint64_t v) {
        for (int i = 0; i < 8; ++i) buf_.push_back(static_cast<uint8_t>((v >> (8 * i)) & 0xFF));
    }
    void write_f64(double d) {
        uint64_t bits = 0;
        static_assert(sizeof(double) == sizeof(uint64_t));
        std::memcpy(&bits, &d, sizeof(bits));
        write_u64(bits);
    }
    void write_mpz(const mpz_class& z) {
        if (z < 0) throw std::invalid_argument("negative mpz is illegal in V21State");
        if (z == 0) {
            write_u32(0);
            return;
        }
        size_t count = (mpz_sizeinbase(z.get_mpz_t(), 2) + 7) / 8;
        if (count > kMaxMpzBytes) throw std::overflow_error("mpz exceeds kMaxMpzBytes");
        write_u32(static_cast<uint32_t>(count));
        size_t old_size = buf_.size();
        buf_.resize(old_size + count);
        size_t written = 0;
        mpz_export(buf_.data() + old_size, &written, 1, 1, 1, 0, z.get_mpz_t());
        if (written != count) {
            buf_.resize(old_size + written);
            uint32_t w32 = static_cast<uint32_t>(written);
            for (int i = 0; i < 4; ++i) {
                buf_[old_size - 4 + i] = static_cast<uint8_t>((w32 >> (8 * i)) & 0xFF);
            }
        }
    }
    const std::vector<uint8_t>& data() const { return buf_; }

private:
    std::vector<uint8_t> buf_;
};

class ByteReader {
public:
    ByteReader(const uint8_t* data, size_t len) : data_(data), len_(len), pos_(0) {}

    uint8_t read_u8() { require(1); return data_[pos_++]; }
    uint16_t read_u16() {
        require(2);
        uint16_t v = 0;
        for (int i = 0; i < 2; ++i) v |= static_cast<uint16_t>(data_[pos_++]) << (8 * i);
        return v;
    }
    uint32_t read_u32() {
        require(4);
        uint32_t v = 0;
        for (int i = 0; i < 4; ++i) v |= static_cast<uint32_t>(data_[pos_++]) << (8 * i);
        return v;
    }
    uint64_t read_u64() {
        require(8);
        uint64_t v = 0;
        for (int i = 0; i < 8; ++i) v |= static_cast<uint64_t>(data_[pos_++]) << (8 * i);
        return v;
    }
    double read_f64() {
        uint64_t bits = read_u64();
        double d = 0.0;
        std::memcpy(&d, &bits, sizeof(d));
        return d;
    }
    mpz_class read_mpz() {
        uint32_t count = read_u32();
        if (count > kMaxMpzBytes) throw std::runtime_error("mpz byte length exceeds limit");
        require(count);
        mpz_class z(0);
        if (count > 0) {
            if (data_[pos_] == 0) throw std::runtime_error("non-canonical leading zero in mpz");
            mpz_import(z.get_mpz_t(), count, 1, 1, 1, 0, data_ + pos_);
            pos_ += count;
        }
        return z;
    }
    size_t remaining() const { return len_ - pos_; }

private:
    void require(size_t n) const {
        if (pos_ + n > len_) throw std::runtime_error("truncated V21State buffer");
    }
    const uint8_t* data_;
    size_t len_;
    size_t pos_;
};

inline uint32_t crc32_ieee(const uint8_t* data, size_t len) {
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; ++i) {
        crc ^= data[i];
        for (int b = 0; b < 8; ++b) {
            crc = (crc & 1u) ? ((crc >> 1) ^ 0xEDB88320u) : (crc >> 1);
        }
    }
    return ~crc;
}

inline void validate_state_invariants(const V21State& st,
                                      const std::vector<uint32_t>& circ_order) {
    if (st.certified_residue_count > st.composites.size()) {
        throw std::runtime_error("certified_residue_count exceeds composites.size()");
    }
    if (circ_order.empty() || circ_order.size() > 30) {
        throw std::runtime_error("invalid circ_order size");
    }
    if (st.outer_root_mask >= (1u << circ_order.size())) {
        throw std::runtime_error("outer_root_mask has invalid bits beyond circ_order");
    }

    // forbidden_small preserves V21 append order; enforce uniqueness, odd >= 3, and presence in forbidden
    std::unordered_set<uint64_t> fs_set;
    fs_set.reserve(st.forbidden_small.size());
    for (uint64_t p : st.forbidden_small) {
        if (p < 3 || (p & 1ULL) == 0) {
            throw std::runtime_error("forbidden_small entry must be odd >= 3");
        }
        if (!fs_set.insert(p).second) {
            throw std::runtime_error("duplicate entry in forbidden_small");
        }
        if (!st.forbidden.count(mpz_class(static_cast<unsigned long>(p)))) {
            throw std::runtime_error("forbidden_small entry missing from forbidden set");
        }
    }

    // Interpret outer_root_mask strictly in fixed CIRC_ORDER coordinates
    for (size_t i = 0; i < circ_order.size(); ++i) {
        if ((st.outer_root_mask >> i) & 1u) {
            uint64_t root_p = circ_order[i];
            if (!fs_set.count(root_p) || !st.forbidden.count(mpz_class(circ_order[i]))) {
                throw std::runtime_error("outer_root_mask bit (CIRC_ORDER) missing from forbidden");
            }
        }
    }

    size_t committed_special_count = 0;
    for (const auto& [p, info] : st.branched) {
        if (p <= 2 || mpz_even_p(p.get_mpz_t())) {
            throw std::runtime_error("branched key must be odd integer > 2");
        }
        if (info.exp == 0) throw std::runtime_error("branched exp must be >= 1");
        if (st.unbranched.count(p)) throw std::runtime_error("prime in both branched and unbranched");
        if (st.forbidden.count(p)) throw std::runtime_error("branched prime is forbidden");
        if (info.exact && (info.exp & 1ULL) == 1ULL) {
            if (mpz_fdiv_ui(p.get_mpz_t(), 4) != 1 || (info.exp % 4) != 1) {
                throw std::runtime_error("odd exact exponent requires p==1 (mod 4) and exp==1 (mod 4)");
            }
            ++committed_special_count;
        } else if (!info.exact && (info.exp & 1ULL) == 1ULL) {
            throw std::runtime_error("standard branch exponent must be even");
        }
    }
    if (st.has_special && committed_special_count != 1) {
        throw std::runtime_error("has_special==true requires exactly one committed special prime");
    }
    if (!st.has_special && committed_special_count != 0) {
        throw std::runtime_error("has_special==false conflicts with committed special prime");
    }
    for (const auto& q : st.unbranched) {
        if (q <= 2 || mpz_even_p(q.get_mpz_t())) {
            throw std::runtime_error("unbranched key must be odd integer > 2");
        }
        if (st.forbidden.count(q)) throw std::runtime_error("unbranched prime is forbidden");
    }
    for (const auto& c : st.composites) {
        if (c <= 1 || mpz_even_p(c.get_mpz_t())) {
            throw std::runtime_error("composite residue must be odd integer > 1");
        }
    }
    std::set<std::pair<mpz_class, mpz_class>> seen_sv;
    for (const auto& sb : st.source_v_bounds) {
        if (sb.target_q <= 2 || mpz_even_p(sb.target_q.get_mpz_t())) {
            throw std::runtime_error("source_v_bounds target_q must be odd integer > 2");
        }
        if (!st.branched.count(sb.source_p)) {
            throw std::runtime_error("source_v_bounds source_p missing from branched");
        }
        if (sb.lower_bound == 0) {
            throw std::runtime_error("source_v_bounds lower_bound must be >= 1");
        }
        if (!seen_sv.emplace(sb.target_q, sb.source_p).second) {
            throw std::runtime_error("duplicate (target_q, source_p) in source_v_bounds");
        }
    }

}

inline std::vector<uint8_t> serialize_state(const V21State& st,
                                            const std::vector<uint32_t>& circ_order,
                                            bool include_float_hints = false) {
    validate_state_invariants(st, circ_order);
    ByteWriter w;
    w.write_u32(kStateMagic);
    w.write_u16(kStateVersion);
    uint16_t flags = (include_float_hints && st.has_float_hints) ? kFlagHasFloatHints : 0;
    w.write_u16(flags);

    w.write_u8(st.has_special ? 1 : 0);
    w.write_u32(st.certified_residue_count);
    w.write_u32(st.outer_root_mask);

    // forbidden_small (ORDER PRESERVED)
    w.write_u32(static_cast<uint32_t>(st.forbidden_small.size()));
    for (uint64_t p : st.forbidden_small) w.write_u64(p);

    // forbidden (sorted ascending)
    w.write_u32(static_cast<uint32_t>(st.forbidden.size()));
    for (const auto& z : st.forbidden) w.write_mpz(z);

    // branched (sorted ascending)
    w.write_u32(static_cast<uint32_t>(st.branched.size()));
    for (const auto& [p, info] : st.branched) {
        w.write_mpz(p);
        w.write_u64(info.exp);
        w.write_u8(info.exact ? 1 : 0);
        w.write_u64(info.seen_in_sigma);
    }

    // unbranched (sorted ascending)
    w.write_u32(static_cast<uint32_t>(st.unbranched.size()));
    for (const auto& q : st.unbranched) w.write_mpz(q);

    // composites (ORDER PRESERVED)
    w.write_u32(static_cast<uint32_t>(st.composites.size()));
    for (const auto& c : st.composites) w.write_mpz(c);

    // source_v_bounds
    w.write_u32(static_cast<uint32_t>(st.source_v_bounds.size()));
    for (const auto& sb : st.source_v_bounds) {
        w.write_mpz(sb.target_q);
        w.write_mpz(sb.source_p);
        w.write_u64(sb.lower_bound);
    }

    if (flags & kFlagHasFloatHints) {
        w.write_f64(st.hints.log_size_branched);
        w.write_f64(st.hints.log_size_comp);
        w.write_f64(st.hints.log_abund_lo);
        w.write_f64(st.hints.log_abund_hi);
        w.write_f64(st.hints.lp_known_abund_upper);
    }

    uint32_t crc = crc32_ieee(w.data().data(), w.data().size());
    w.write_u32(crc);
    return w.data();
}

inline V21State deserialize_state(const uint8_t* data,
                                  size_t len,
                                  const std::vector<uint32_t>& circ_order,
                                  bool trust_float_hints = false) {
    if (len < 12) throw std::runtime_error("buffer too small for V21State");
    uint32_t expected_crc = crc32_ieee(data, len - 4);
    ByteReader tail(data + len - 4, 4);
    if (tail.read_u32() != expected_crc) throw std::runtime_error("V21State CRC32 mismatch");

    ByteReader r(data, len - 4);
    if (r.read_u32() != kStateMagic) throw std::runtime_error("invalid V21State magic");
    if (r.read_u16() != kStateVersion) throw std::runtime_error("unsupported V21State version");
    uint16_t flags = r.read_u16();

    V21State st;
    uint8_t sp = r.read_u8();
    if (sp > 1) throw std::runtime_error("invalid boolean for has_special");
    st.has_special = (sp == 1);
    st.certified_residue_count = r.read_u32();
    st.outer_root_mask = r.read_u32();

    auto read_count = [&]() -> uint32_t {
        uint32_t n = r.read_u32();
        if (n > kMaxCollectionSize) throw std::runtime_error("collection exceeds limit");
        return n;
    };

    uint32_t n_fs = read_count();
    st.forbidden_small.reserve(n_fs);
    for (uint32_t i = 0; i < n_fs; ++i) st.forbidden_small.push_back(r.read_u64());

    uint32_t n_fb = read_count();
    mpz_class prev_fb(0);
    for (uint32_t i = 0; i < n_fb; ++i) {
        mpz_class z = r.read_mpz();
        if (i > 0 && z <= prev_fb) throw std::runtime_error("forbidden set not strictly sorted");
        prev_fb = z;
        st.forbidden.insert(z);
    }

    uint32_t n_br = read_count();
    mpz_class prev_br(0);
    for (uint32_t i = 0; i < n_br; ++i) {
        mpz_class p = r.read_mpz();
        if (i > 0 && p <= prev_br) throw std::runtime_error("branched map not strictly sorted");
        prev_br = p;
        BranchedInfoV2 info;
        info.exp = r.read_u64();
        uint8_t ex = r.read_u8();
        if (ex > 1) throw std::runtime_error("invalid boolean for exact");
        info.exact = (ex == 1);
        info.seen_in_sigma = r.read_u64();
        st.branched.emplace(std::move(p), info);
    }

    uint32_t n_ub = read_count();
    mpz_class prev_ub(0);
    for (uint32_t i = 0; i < n_ub; ++i) {
        mpz_class q = r.read_mpz();
        if (i > 0 && q <= prev_ub) throw std::runtime_error("unbranched set not strictly sorted");
        prev_ub = q;
        st.unbranched.insert(q);
    }

    uint32_t n_cp = read_count();
    st.composites.reserve(n_cp);
    for (uint32_t i = 0; i < n_cp; ++i) st.composites.push_back(r.read_mpz());

    uint32_t n_sv = read_count();
    st.source_v_bounds.reserve(n_sv);
    for (uint32_t i = 0; i < n_sv; ++i) {
        SourceVBound sb;
        sb.target_q = r.read_mpz();
        sb.source_p = r.read_mpz();
        sb.lower_bound = r.read_u64();
        st.source_v_bounds.push_back(std::move(sb));
    }

    if (flags & kFlagHasFloatHints) {
        FloatHints h;
        h.log_size_branched = r.read_f64();
        h.log_size_comp = r.read_f64();
        h.log_abund_lo = r.read_f64();
        h.log_abund_hi = r.read_f64();
        h.lp_known_abund_upper = r.read_f64();
        if (trust_float_hints) {
            st.has_float_hints = true;
            st.hints = h;
        }
    }
    if (r.remaining() != 0) throw std::runtime_error("trailing bytes in V21State");

    validate_state_invariants(st, circ_order);
    return st;
}

} // namespace opn_v21
