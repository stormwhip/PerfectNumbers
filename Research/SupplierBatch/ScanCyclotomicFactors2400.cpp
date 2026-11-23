#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

std::uint64_t Power(std::uint64_t p, int exponent, std::uint64_t q) {
    std::uint64_t value = 1;
    while (exponent) {
        if (exponent & 1) value = value * p % q;
        exponent >>= 1;
        if (exponent) p = p * p % q;
    }
    return value;
}

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    const int cutoff = std::stoi(argv[1]);
    if (cutoff < 3 || cutoff > 2000000000) return 1;
    std::vector<bool> composite(cutoff / 2 + 1);
    for (int p = 3; p <= cutoff / p; p += 2) {
        if (composite[p / 2]) continue;
        for (int q = p * p; q <= cutoff; q += 2 * p) composite[q / 2] = true;
    }
    int p, exponent;
    while (std::cin >> p >> exponent) {
        const int m = exponent + 1;
        if (m <= p || (m & 1) == 0 || m > cutoff || composite[m / 2]) continue;
        const int step = 2 * m;
        for (int q = step + 1; q <= cutoff; q += step) {
            if (!composite[q / 2] && Power(p, m, q) == 1)
                std::cout << p << '\t' << exponent << '\t' << q << '\n';
        }
    }
}
