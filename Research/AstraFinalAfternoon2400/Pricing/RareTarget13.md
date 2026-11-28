# Third-target price in the last supplier-13 window

Frozen baseline: `495c59f55456a70994ce7848487e0c4e262c1984`. Suppose `N≤10^2400` is odd perfect and the exact prefix is `19^276,1176672733^1,1109^2,13^276` (the remaining window of [H2LocalPricing.md](H2LocalPricing.md)). Set `r=44119464395283956806299428681`. Its primality is proved by Pocklington, with the two trial-certified factors `15539196401,1578110473` of `r−1` and witness 2. The fixed outgoing product supplies exactly one `r` factor; `r` is not fixed. Euler is already fixed, so `r^h||N` with even `h≥2`.

## Zero-loss rare-target price `77/20`

Let `X0` be the fixed-prefix product. For any external ordinary source `b^f` under the stronger prefix including `r^h`, `L=f+1` is odd and at most 5031. Order 1 at `r` cannot supply and no LTE increment exists, because `r>5031`. The complete list of possible nontrivial odd orders dividing `r−1` and `L` is `5,71,277,355,1385,2287`. For each order, the verifier constructs an element of the claimed exact order and takes all of its primitive powers. Each residue's least positive odd representative gives a lower bound for **all** odd positive bases in its class.

- Orders 71, 355, 1385, 2287 all force `X0 r^2 b^(o−1)>10^2400` by the least representative. No primality proxy is needed.
- At order 277, the same bound forces `b<r`; the only in-range odd representatives are `13,169,2197,28561,371293`. Base 13 is already fixed and the larger four are divisible by 13, so none can be an external prime.
- At order 5, use Hensel roots modulo `r^z`, and the least odd representative in each class. For each in-size layer, the smallest of these representatives satisfies `b^80≥r^(77z)`, hence every possible base in that layer satisfies it. At the first layer whose smallest odd representative forces `X0 r² b^4>10^2400`, all deeper lifts are impossible as well. The cutoff is driven by size, not by assuming the root was the actual base.

Thus every external positive `r` supply `u=v_r(σ(b^f))` is paid with four exponent units: `b^80≥r^(77u)`. This is exact and has zero loss. It covers all valuations, not only those for a particular `h`.

## Adding the rare price to the existing 19/13 price

The supports of all effective 19/13 lengths are contained in `{3,13,19}`. `gcd(19·13·9,r(r−1))=1`, so `5` is coprime to the effective combined 19/13 length `A`. For a jointly supplying component, `5A|L`, and `(A−1)+4≤L−1`. This allocates the full, already audited 19/13 joint price on the component of length `A` plus four separate units for the order-5 rare target. To see why the old price applies to the smaller length `A`: take `A` to be the least common multiple of the independently selected effective lengths which preserve the target valuations by LTE. Apply the 19/13 proof to this length, not the original `L`. The same per-base deficit table applies, because it is indexed only by primitive orders, capped valuations, and fixed-prefix exclusions. If `A=1` both old target valuations are zero.

For precision, the 19/13 price raises quantities to power 10 and weights both incoming valuations by `19/10`. When both orders are cubic, two exponent units suffice for the joint CRT deficit; on this order pair the CRT modulus is the product of the two prime-power divisibility requirements and crosses the weight threshold since `20≥19`. If both nontrivial orders are not cubic, the 19-side order is 9 and at least four base units fit separately. Order-one and LTE add supply via factors `19^i,13^j`; application of exact individual lower bounds gives their payment. See [Net13.py](../Nineteen/Net13.py) for complete residue/loss replay; the new verifier pins that dependency.

The six compulsory bases `67,967,8311,11621,50627,392233` are distinctly certified and forced by exact outgoing divisibility. They are order-5 inactive at `r`, so no `r` supply is double charged in their per-base credit. The fixed `r` component does not supply itself. For those seven selected primes, replace their baseline deficit factors by minima of the exact normalized prices including the original factor (`Net13.atom` and `Net13.gain`). Every other source retains its bound. As a result all remaining `h−1` rare units still enter with exact price `r^(77(h−1))` after squaring the tenth-power inequality. No anonymous compulsory mass is multiplied into this price. The verifier recomputes every even exponent until the strict raw tail `X0 r^h>B`, and checks each terminal by exact cross-products.

```sh
python -I -S -B Research/AstraFinalAfternoon2400/Pricing/RareTarget13.py
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Pricing/Verify13Upper.py
```

This proof is only the complement to `r²`. It does not independently close the full supplier-13 window. Its exact uniform lemma and quantified inactivity test can be used when refining `r²` into descendants.
