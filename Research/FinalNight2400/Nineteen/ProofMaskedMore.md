# r^18, r^24 and r^60 excluded at (19,282), t^10

These are three further full second-pivot fibers under the hypotheses of [Proof282.md](Proof282.md). Use the same checked local absence lemma and strict masked-forest arithmetic as in [ProofMasked58.md](ProofMasked58.md), not a stronger assumed global support mask. At r^24 a severe final branch had 2984231898295102876968635389872588356150804497 as a compulsory prime; native ECM split the 182-digit residual of its exponent-four emission into two factors (24 and 159 digits), subsequently proven prime. The final packet relies only on strict divisibility and the embedded ECPP evidence, not on the ECM result alone. Neither package assumes a leftover composite cofactor prime.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyMasked24.py
    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyMaskedMore.py

Both cold commands returned 0. r^24: 8 exhaustive internal splits, 87 ordinary + 27 conditional-absence forest terminals and 13 abundance terminals, 76 ECPP. r^18 and r^60 together: 42 internal splits, 364 ordinary +165 conditional-absence terminals, 45 abundance terminals, 171 ECPP. The exact h count rises from 39 to 42 of the 50 initial r powers. Remaining h = 4,6,12,22,36,40,42,52. No root or first-pivot closure yet.
