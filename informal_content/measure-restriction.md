# Measure restriction

Let `alpha` be a measurable space, let `mu` be a measure on `alpha`, and let `s` be an arbitrary subset of `alpha`. The restriction `mu.restrict s` is a measure on the same measurable space whose measurable evaluations are obtained by intersecting with `s`.

The restricting set need not be measurable for the definition. If `t` is measurable, then

`(mu.restrict s) t = mu (t intersection s)`.

Alternatively, if `s` is measurable, the same equality holds for every set `t`, with measure application on arbitrary sets interpreted through the associated outer measure. These are distinct evaluation lemmas: one assumes measurability of the evaluated set and the other assumes measurability of the restricting set.

For arbitrary `s`, restriction still satisfies

`(mu.restrict s) s = mu s`,

`mu.restrict s = 0` exactly when `mu s = 0`, `mu.restrict s <= mu`, and `mu.restrict s` is absolutely continuous with respect to `mu`. If a measurable `t` is disjoint from arbitrary `s`, then its restricted measure is zero. If `s` itself is measurable, the same conclusion holds for every disjoint `t`, and almost every point under `mu.restrict s` belongs to `s`. That almost-everywhere concentration statement must not be asserted for a general nonmeasurable restricting set.

## Mathlib

Declarations: `MeasureTheory.Measure.restrict`, `MeasureTheory.Measure.restrict_apply`, `MeasureTheory.Measure.restrict_apply'`, `MeasureTheory.Measure.restrict_apply_self`, `MeasureTheory.Measure.restrict_eq_zero`, `MeasureTheory.Measure.restrict_le_self`, `MeasureTheory.Measure.absolutelyContinuous_restrict`, `MeasureTheory.ae_restrict_mem`
File: `Mathlib/MeasureTheory/Measure/Restrict.lean`
