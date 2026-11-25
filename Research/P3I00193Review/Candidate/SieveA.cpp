#include <bits/stdc++.h>
using namespace std;
using u64 = uint64_t;
using u128 = __uint128_t;

static inline u64 mulmod(u64 a, u64 b, u64 m) {
    return (u64)((u128)a * b % m);
}
static inline u64 powmod(u64 a, u64 e, u64 m) {
    u64 res = 1 % m;
    a %= m;
    while (e) {
        if (e & 1) res = mulmod(res, a, m);
        a = mulmod(a, a, m);
        e >>= 1;
    }
    return res;
}
static bool is_prime64(u64 n) {
    if (n < 2) return false;
    for (u64 p : {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,29ULL,31ULL,37ULL}) {
        if (n % p == 0) return n == p;
    }
    u64 d = n - 1;
    int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    for (u64 a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
        if (a % n == 0) continue;
        u64 x = powmod(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool comp = true;
        for (int r = 1; r < s; r++) {
            x = mulmod(x, x, n);
            if (x == n - 1) { comp = false; break; }
        }
        if (comp) return false;
    }
    return true;
}

int main(int argc, char** argv) {
    // Usage: sieve_A <p> <e> <R_max> [mod3_only]
    if (argc < 4) return 1;
    u64 p = stoull(argv[1]);
    u64 e = stoull(argv[2]);
    u64 R_max = stoull(argv[3]);
    int mod3_only = (argc >= 5) ? stoi(argv[4]) : 0;
    u64 d = e + 1;
    u64 step = 2 * d;
    if (mod3_only && (step % 3 != 0)) step *= 3;
    vector<u64> found;
    for (u64 r = 1 + step; r <= R_max; r += step) {
        if (r % 3 == 0 || r % 5 == 0 || r % 7 == 0 || r % 11 == 0 || r % 13 == 0) continue;
        if (powmod(p, d, r) == 1) {
            if (is_prime64(r)) {
                // also check Wieferich r^2 | p^d - 1 if r < 3e9
                found.push_back(r);
            }
        }
    }
    cout << p << " " << e << " " << R_max << " :";
    for (u64 r : found) cout << " " << r;
    cout << "\n";
    return 0;
}
