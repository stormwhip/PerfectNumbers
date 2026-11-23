// Fast C++17 __uint128_t Brent's Pollard-Rho Factorizer (up to 125-bit integers).
// Used ONLY for candidate factor discovery; all primes are certified by Pratt/trial in Python.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using u64 = uint64_t; using u128 = unsigned __int128;

u128 parse_u128(const std::string& s) {
    u128 v = 0; for (char c : s) if (c >= '0' && c <= '9') v = v * 10 + (c - '0'); return v;
}
std::string to_str(u128 v) {
    if (v == 0) return "0";
    std::string s; while (v > 0) { s.push_back('0' + (int)(v % 10)); v /= 10; }
    std::reverse(s.begin(), s.end()); return s;
}
u128 mul_mod(u128 a, u128 b, u128 m) {
    u128 res = 0; a %= m;
    while (b > 0) { if (b & 1) { res += a; if (res >= m) res -= m; } a <<= 1; if (a >= m) a -= m; b >>= 1; }
    return res;
}
u128 pow_mod(u128 a, u128 e, u128 m) {
    u128 r = 1; a %= m;
    while (e > 0) { if (e & 1) r = mul_mod(r, a, m); a = mul_mod(a, a, m); e >>= 1; }
    return r;
}
u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }
bool is_prime128(u128 n) {
    if (n < 2) return false;
    static const u64 small[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (u64 p : small) { if (n == p) return true; if (n % p == 0) return false; }
    u128 d = n - 1; int s = 0; while ((d & 1) == 0) { d >>= 1; ++s; }
    for (u64 a : small) {
        if ((u128)a >= n) continue;
        u128 x = pow_mod(a, d, n); if (x == 1 || x == n - 1) continue;
        bool comp = true;
        for (int r = 1; r < s; ++r) { x = mul_mod(x, x, n); if (x == n - 1) { comp = false; break; } }
        if (comp) return false;
    }
    return true;
}
u128 brent_rho(u128 n, int max_steps = 40000) {
    if (n % 2 == 0) return 2;
    for (u64 c = 1; c <= 12; ++c) {
        u128 y = 2, r = 1, q = 1, g = 1, ys = 2, x = 2; int steps = 0;
        while (g == 1 && steps < max_steps) {
            x = y; for (u128 i = 0; i < r; ++i) y = (mul_mod(y, y, n) + c) % n;
            u128 k = 0;
            while (k < r && g == 1 && steps < max_steps) {
                ys = y; u128 lim = std::min((u128)128, r - k);
                for (u128 i = 0; i < lim; ++i) {
                    y = (mul_mod(y, y, n) + c) % n;
                    u128 diff = (x > y) ? (x - y) : (y - x); q = mul_mod(q, diff, n);
                }
                g = gcd128(q, n); k += lim; steps += (int)lim;
            }
            r <<= 1;
        }
        if (g == n) {
            do { ys = (mul_mod(ys, ys, n) + c) % n; g = gcd128((x > ys) ? (x - ys) : (ys - x), n); } while (g == 1);
        }
        if (g > 1 && g < n) return g;
    }
    return n;
}
void factor_rec(u128 n, std::vector<u128>& out) {
    if (n <= 1) return;
    if (is_prime128(n)) { out.push_back(n); return; }
    u128 d = brent_rho(n, 25000); if (d == n) return;
    factor_rec(d, out); factor_rec(n / d, out);
}
int main() {
    std::ios::sync_with_stdio(false); std::cin.tie(nullptr);
    std::string line;
    while (std::cin >> line) {
        u128 n = parse_u128(line); std::vector<u128> fac;
        static const u64 sm[] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97};
        for (u64 p : sm) while (n % p == 0) { fac.push_back(p); n /= p; }
        if (n > 1) factor_rec(n, fac);
        std::sort(fac.begin(), fac.end()); fac.erase(std::unique(fac.begin(), fac.end()), fac.end());
        std::cout << fac.size(); for (u128 x : fac) std::cout << " " << to_str(x); std::cout << "\n";
    }
}
