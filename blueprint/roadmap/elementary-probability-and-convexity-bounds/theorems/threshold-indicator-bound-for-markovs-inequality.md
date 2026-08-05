---
kind: node
declaration: lemma
statement: formalized
proof: formalized
lean: MeasureTheory.ae_mul_indicator_lt_le_of_ae_nonneg, MeasureTheory.ae_mul_indicator_le_of_ae_nonneg
---

# Threshold indicator bound for Markov's inequality

Let `mu` be a probability measure, let `Y : Omega -> Real` be measurable and nonnegative almost everywhere, and let `epsilon > 0`. Write `1_{Y > epsilon}` for the indicator of the event `{omega | epsilon < Y omega}`. Then

`epsilon * 1_{Y > epsilon}(omega) <= Y omega`

for `mu`-almost every `omega`.

## Proof

Work at a point where `Y omega >= 0`. If `epsilon < Y omega`, the indicator is one, and the desired inequality follows from `epsilon <= Y omega`. Otherwise the indicator is zero, and the desired inequality is `0 <= Y omega`. These two cases cover every point outside the null set on which nonnegativity may fail.

The source-facing assumptions place this lemma in its probability context. The same compiled pointwise argument proves the stronger closed-threshold version with `1_{Y >= epsilon}`. It works for an arbitrary measure and does not use measurability of `Y` or positivity of `epsilon`; those assumptions become relevant when the indicator inequality is integrated to obtain Markov's bound.

### Mathlib status

Mathlib contains the generic set-indicator and almost-everywhere order interfaces used by this argument, but no dedicated declaration for this threshold-indicator inequality was found in the pinned checkout.


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, Exercise 1.9, printed page 9
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.9, printed page 2

## Planning record

Legacy Mathlib assessment: `missing`.

Verified by a compiled direct proof in the pinned checkout and a declaration search. No dedicated theorem states the source's strict-event bound epsilon times the indicator of {epsilon < Y} <= Y; the same argument proves the stronger closed-threshold version. The proof uses generic Set.indicator simplification and Filter.Eventually reasoning. Although the source states a measurable nonnegative random variable on a probability space with epsilon > 0, this lemma itself needs only Y >= 0 almost everywhere under an arbitrary measure. Measurability and threshold positivity enter the subsequent integration and division steps; probability normalization is never needed and is retained only for the source context.

## Depends on

- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/random-variable.md)
