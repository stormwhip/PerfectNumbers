# Final source of the 7^862, t^30 double-seed branch (conditional interface)

Assume the preceding cut certificate gives s=v7(q+1)≥160, q Euler with exponent one, q dividing neither A=σ(7^862) nor S=σ(t^30), where t=683845718669 and t^30||N. Let C=A/t. The independent certificate checks gcd(C,S)=gcd(t,C S)=gcd(7,C S)=1, and M=7^862 t^30 C S divides N. Put Y=7^160, Q=2Y−1. The already verified Teichmüller profile has k=2 and U(862)=579125. Two distinct ordinary components may pay their actual ratios while covering all remaining deficits by U: if r^f is an ordinary source of q, then r≠7,t by q∤A S, and

    N ≥ [7^(3·862)t^30/U] · [q/7^(2s)] · [r^f/7^(2b)],  b=v7(σ(r^f)).

This uses v7(σ(t^30))=0; retaining an unclipped ratio instead of its max with one is always conservative. Since q·7^b divides the odd σ(r^f), r^f>(2/3)q7^b. Since q/7^s≥2−7^(−s)≥Q/Y, the above implies

    N > 2·7^(3·862)t^30 Q² / (3U Y² 7^b).

The exact test at b=159 exceeds 10^2400, forcing b≥160. Also r^f≤10^2400 makes f<9999, j=v7(f+1)≤4. For r≡1 mod 7 LTE would give b=j; all r of even multiplicative order mod 7 give b=0 since f even. The only possible r mod7 are 2,4, both order 3, with b=v7(r³−1)+j by LTE. Therefore r³≡1 mod 7^154 and r is one of the two Hensel classes a=x_2 or x_4, generated as x_i=i^(7^153) mod 7^154. The elementary root uniqueness follows from gcd(3r²,7)=1. Both least positive representatives satisfy M Q x_i>10^2400 by integer check. Put c=v_r(C S). If f>c, then M Q r≤N (rather, M q r divides N and q≥Q), contradicting the preceding inequality. Thus f=c≥2, implying r²|C or r²|S, never both. This conclusion itself excludes emitters outside C S. The optional 10^13 rough screens are *not used* in this reduction.

The remainder is precisely four square-divisor exclusion problems: C or S and x_2 or x_4 mod 7^154. For C (resp. S) every prime divisor is 1 mod 2·863 (resp. 2·31), by the known order of 7 (resp. t) and exclusion of the exceptional index prime. Check endpoints and combine congruences by CRT; the cut-lab small-root certificates operate on v_r(C),v_r(S)≥2. Running `python -I -S -B parity-lab/Teich862.py` checks all threshold and representative comparisons without any dependence on FLINT. This source reduction alone is not a claim that all exponents at t or all (7,862) leaves have been eliminated.
