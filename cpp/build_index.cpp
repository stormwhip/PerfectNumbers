#include <zlib.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>

struct IdxEntry {
    uint64_t h1;
    uint64_t h2;
    uint64_t offset;
    uint32_t len;
};

// 128-bit FNV-1a / SplitMix 混合哈希，用于 (p, q+1) 键
static inline void hash128(const char* s, size_t n, uint64_t& h1, uint64_t& h2) {
    uint64_t a = 14695981039346656037ULL;
    uint64_t b = 1099511628211ULL ^ 0x9e3779b97f4a7c15ULL;
    for (size_t i = 0; i < n; ++i) {
        uint8_t c = static_cast<uint8_t>(s[i]);
        a ^= c;
        a *= 1099511628211ULL;
        b ^= c;
        b *= 0xbf58476d1ce4e5b9ULL;
        b ^= (b >> 31);
    }
    h1 = a;
    h2 = b;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <path_to_checkfacts.txt.gz>\n";
        return 1;
    }

    gzFile gz = gzopen(argv[1], "rb");
    if (!gz) {
        std::cerr << "Error: cannot open " << argv[1] << "\n";
        return 1;
    }
    gzbuffer(gz, 1 << 20); // 1 MB 读缓冲

    FILE* fdat = fopen("facts.dat", "wb");
    if (!fdat) {
        std::cerr << "Error: cannot create facts.dat\n";
        return 1;
    }
    static char out_buf[1 << 20];
    setvbuf(fdat, out_buf, _IOFBF, sizeof(out_buf));

    std::vector<IdxEntry> index;
    index.reserve(10000000);

    std::string cur_key;
    std::string cur_vals;
    uint64_t cur_offset = 0;
    uint64_t line_cnt = 0;

    auto flush_group = [&]() {
        if (cur_key.empty()) return;
        uint64_t h1, h2;
        hash128(cur_key.data(), cur_key.size(), h1, h2);
        fwrite(cur_vals.data(), 1, cur_vals.size(), fdat);
        index.push_back({h1, h2, cur_offset, static_cast<uint32_t>(cur_vals.size())});
        cur_offset += cur_vals.size();
        cur_vals.clear();
    };

    std::vector<char> line_buf(1 << 20);
    while (gzgets(gz, line_buf.data(), static_cast<int>(line_buf.size()))) {
        char* s = line_buf.data();
        // 找到第 1 个和第 2 个空格: "p q+1 f"
        char* sp1 = strchr(s, ' ');
        if (!sp1) continue;
        char* sp2 = strchr(sp1 + 1, ' ');
        if (!sp2) continue;

        size_t key_len = static_cast<size_t>(sp2 - s);
        char* f_start = sp2 + 1;
        char* f_end = f_start;
        while (*f_end && *f_end != '\n' && *f_end != '\r' && *f_end != ' ') ++f_end;
        size_t f_len = static_cast<size_t>(f_end - f_start);
        if (f_len == 0) continue;

        if (cur_key.size() == key_len && memcmp(cur_key.data(), s, key_len) == 0) {
            cur_vals.push_back(' ');
            cur_vals.append(f_start, f_len);
        } else {
            flush_group();
            cur_key.assign(s, key_len);
            cur_vals.assign(f_start, f_len);
        }

        if (++line_cnt % 5000000 == 0) {
            std::cout << "Processed " << (line_cnt / 1000000) << "M lines, "
                      << index.size() << " groups...\n" << std::flush;
        }
    }
    flush_group();
    gzclose(gz);
    fclose(fdat);

    std::cout << "Total lines: " << line_cnt << ", total groups: " << index.size() << "\n";
    std::cout << "Sorting index...\n" << std::flush;

    std::sort(index.begin(), index.end(), [](const IdxEntry& a, const IdxEntry& b) {
        if (a.h1 != b.h1) return a.h1 < b.h1;
        return a.h2 < b.h2;
    });

    FILE* fidx = fopen("facts.idx", "wb");
    if (!fidx) {
        std::cerr << "Error: cannot create facts.idx\n";
        return 1;
    }
    fwrite(index.data(), sizeof(IdxEntry), index.size(), fidx);
    fclose(fidx);

    std::cout << "Done! Generated facts.dat (" << cur_offset << " bytes) and facts.idx ("
              << (index.size() * sizeof(IdxEntry)) << " bytes).\n";
    return 0;
}
