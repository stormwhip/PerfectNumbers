# Add two full (19,282) second-pivot values 82,88

Keep v_19(N)=282 and v_1735317810514627(N)=10. With the same compulsory r=8383027, the two exact valuations 82 and 88 are impossible. This application is disjoint from the 24 initial values and the extra r^28. Use exactly the [forest invariant](Proof282.md): the verifier independently derives the full r domain and its tail 202, visits the two stated fibers, tests primalities, and checks the domain of the one interior split before requiring the strict minimum >10^2400 with both integer evaluators on all 16 leaves. Twenty embedded ECPP chains, no extra exclusions or support assumptions. Thus 27/50 r-valuations have now been excluded in union with the earlier packets. No closure of the first t fiber.

    python -I -S -B Research/FinalNight2400/Nineteen/VerifyHigh.py
