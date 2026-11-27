# Complete r^4 second fiber at (19,282)

Use the [fully proved local absence forest technique](ProofMasked58.md) at exact r=8383027, h=4 under v_19(N)=282 and v_1735317810514627(N)=10. This is a full r^4 branch, not the fourth power of the previous 23773 subpivot. Certified low and high order emission factors allow full exhaustion of 97 nested pivot domains with their infinite size tails. There are 825 strict ordinary and 1125 strict locally masked forest leaves (both integer evaluators checked), and 405 abundance leaves. The 899 ECPP chains prove all oversized prime labels; smaller labels use the deterministic 64-bit test. No unknown prime or root mask is assumed. Exact replay:

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Nineteen/VerifyFourth.py

Exit 0; together with earlier packets 48/50 live r powers are excluded, leaving r^12 and r^22. The root is not yet closed.
