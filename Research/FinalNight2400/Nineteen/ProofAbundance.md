# A simple recurring second-valuation obstruction at (19,282)

Fix v_19(N)=282, v_t(N)=10 for t=1735317810514627 and write h=v_r(N), r=8383027. Assume N odd perfect. Then **3∤(h+1)**. Indeed, 23 divides σ(t^10), and if 3|(h+1) then σ(r²)=r²+r+1 divides σ(r^h), forcing 3,7,13,157. These five distinct prime divisors {3,7,13,23,157} are outside the fixed root 19. The primes 3,7,23 are all 3 mod4 so in Euler's form their exponents are at least 2; for 13,157 only require ≥1 (allowing them both as potential Euler only weakens the bound). The divisor of N consisting of 19^282·3²·7²·13·23²·157 has abundancy σ(d)/d≥2.009427>2, evaluated by a strict fraction comparison. Since abundancy is monotone under divisibility, σ(N)/N>2, impossible.

    python -I -S -B Research/FinalNight2400/Nineteen/VerifyAbundance.py

All 17 of the directly live h≡2 mod6 in [2,100] are therefore forbidden, but many repeat earlier forest cases. Beyond the previous 32/50 union, **exactly h=2,8,26** are new (14 already has an independent native forest). This gives 35/50 second assignments excluded, 15 still open. No first-pivot closure or support hypothesis.
