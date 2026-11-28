# A nineteenth tertiary exclusion at (7,12), v_Q=12

At T^6, S=62936242392988051361, this completes v_S=4. Since σ(S^4) is divisible by 5 and N is odd perfect, 3 cannot divide N: the abundancy ratio of 7^12, 3², 5 already exceeds 2 (3 cannot be Euler). The other forced prime is J=340522774902395416760792885639672290356455394594605085885851976071. Its primality is certified locally by a Lucas chain: the hard n−1 split was discovered by offline ECM at B1=20000, B2=500000, curve 49, yielding 532474235418805439; the actual verifier proves all recursively claimed factors and witnesses. No discovery code or database enters replay.

For j=v_J(N), J≡3 mod4 precludes Euler. Exact enumeration on the compulsory row with both 3 and 19 banned leaves precisely j=2,4; from 12 the elementary size tail is monotone. At both remaining j the sealed forests of Tertiary.md apply with the one extra impossibility of producing 3. A second independent integer arithmetic engine uses the same mask. The two integer lower bounds each strictly exceed 10^2400 *even in the first leaf whose printed decimal floor is only 2400*; the other floor is 2403. The remaining exact S powers after union with Tertiary.md are 1,2,5,6,8,9,10,12, with no full T or Q fiber closure.

    python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/SevenNext/VerifyFour.py
