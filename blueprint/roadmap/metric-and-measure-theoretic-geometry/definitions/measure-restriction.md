---
kind: node
declaration: definition
mathlib: true
---

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


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Restrict.lean`.

Verified in the pinned checkout. Measure.restrict is defined for an arbitrary measure and arbitrary subset. restrict_apply requires the evaluated set measurable; restrict_apply' instead requires the restricting set measurable and allows arbitrary evaluated sets. For arbitrary s, restriction evaluates to mu s on s, is zero iff mu s is zero, lies below mu, and is absolutely continuous with respect to mu. Almost-everywhere concentration on s requires s to be measurable. No probability, finiteness, or sigma-finiteness assumption is used.

## Depends on

- [Measurable spaces and sets](measurable-spaces-and-sets.md)
