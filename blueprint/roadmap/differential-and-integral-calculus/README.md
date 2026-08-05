---
kind: roadmap
status: detailed
---

# Differential and integral calculus

Mathlib foundations for Frechet derivatives, higher derivatives, Taylor estimates, and Bochner and interval integration.

## Planning status

This milestone is decomposed into 12 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

This milestone has no coarse prerequisites.

## Candidate contents

- Frechet derivative
- Gradient and Hessian
- Taylor expansion
- Bochner integral
- Interval integral

## Detailed nodes

- [Frechet derivative](definitions/frechet-derivative.md)
- [Gradient in a complete inner product space](definitions/gradient-in-a-complete-inner-product-space.md)
- [Frechet Taylor derivative jet](definitions/frechet-taylor-derivative-jet.md)
- [Iterated Frechet derivative](definitions/iterated-frechet-derivative.md)
- [Taylor polynomial on a set](definitions/taylor-polynomial-on-a-set.md)
- [Taylor expansion with little-o remainder](theorems/taylor-expansion-with-little-o-remainder.md)
- [Taylor remainder bound](theorems/taylor-remainder-bound.md)
- [Taylor formula with integral remainder](theorems/taylor-formula-with-integral-remainder.md)
- [Bochner integral](definitions/bochner-integral.md)
- [Interval integrability](definitions/interval-integrability.md)
- [Interval integral](definitions/interval-integral.md)
- [Fundamental theorem of calculus for interval integrals](theorems/fundamental-theorem-of-calculus-for-interval-integrals.md)

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `in-mathlib`.

Relevant declarations:

- `HasFDerivAt`
- `fderiv`
- `HasGradientAt`
- `gradient`
- `iteratedFDeriv`
- `iteratedFDerivWithin`
- `HasFTaylorSeriesUpTo`
- `taylor_isLittleO`
- `taylor_mean_remainder_bound`
- `map_add_eq_sum_add_integral_iteratedFDeriv`
- `MeasureTheory.integral`
- `intervalIntegral.integral_eq_sub_of_hasDerivAt`

Primary file: `Mathlib/Analysis/Calculus/FDeriv/Defs.lean`.

Verified in the pinned checkout. HasFDerivAt and fderiv are defined in Mathlib/Analysis/Calculus/FDeriv/Defs.lean; gradients are in Analysis/Calculus/Gradient/Basic.lean. No standalone Hessian declaration was found, so the fine graph must use iteratedFDeriv at order two or introduce a proved bridge. HasFTaylorSeriesUpTo records derivative jets and is not itself a Taylor formula; actual expansions and bounds include taylor_isLittleO and taylor_mean_remainder_bound in Analysis/Calculus/Taylor.lean and map_add_eq_sum_add_integral_iteratedFDeriv in TaylorIntegral.lean. Bochner integration is under MeasureTheory/Integral/Bochner, and the interval fundamental theorem is in MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean.
