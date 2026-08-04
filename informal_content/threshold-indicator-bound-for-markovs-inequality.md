# Threshold indicator bound for Markov's inequality

Let `mu` be a probability measure, let `Y : Omega -> Real` be measurable and nonnegative almost everywhere, and let `epsilon > 0`. Write `1_{Y > epsilon}` for the indicator of the event `{omega | epsilon < Y omega}`. Then

`epsilon * 1_{Y > epsilon}(omega) <= Y omega`

for `mu`-almost every `omega`.

## Proof

Work at a point where `Y omega >= 0`. If `epsilon < Y omega`, the indicator is one, and the desired inequality follows from `epsilon <= Y omega`. Otherwise the indicator is zero, and the desired inequality is `0 <= Y omega`. These two cases cover every point outside the null set on which nonnegativity may fail.

The source-facing assumptions place this lemma in its probability context. The same compiled pointwise argument proves the stronger closed-threshold version with `1_{Y >= epsilon}`. It works for an arbitrary measure and does not use measurability of `Y` or positivity of `epsilon`; those assumptions become relevant when the indicator inequality is integrated to obtain Markov's bound.

### Mathlib status

Mathlib contains the generic set-indicator and almost-everywhere order interfaces used by this argument, but no dedicated declaration for this threshold-indicator inequality was found in the pinned checkout.
