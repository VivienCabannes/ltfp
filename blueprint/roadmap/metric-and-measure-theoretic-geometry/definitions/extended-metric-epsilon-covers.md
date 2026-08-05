---
kind: node
declaration: definition
mathlib: true
---

# Extended-metric epsilon-covers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `s` and `N` be subsets of `X`. The set `N` is an `epsilon`-cover of `s` when every `x` in `s` is within extended distance at most `epsilon` of some center in `N`:

`forall x in s, exists y in N, edist x y <= epsilon`.

Equivalently, `s` is contained in the union of the extended closed balls of radius `epsilon` centered at points of `N`. If `X` is a pseudometric space, the same predicate is equivalent to containment in the corresponding union of real-valued closed balls. Covers therefore use closed balls and a non-strict inequality. The centers need not belong to `s`.

The radius is finite because it lies in `NNReal`, even though distances may take the value `infinity`. In a genuine emetric space a zero-cover is exactly set containment `s subset N`. In a pseudoemetric space a zero-cover may instead use distinct centers at zero extended distance.

## Mathlib

Declarations: `Metric.IsCover`, `Metric.isCover_iff_subset_iUnion_closedEBall`, `Metric.isCover_iff_subset_iUnion_closedBall`, `Metric.isCover_zero`
File: `Mathlib/Topology/MetricSpace/Cover.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/Cover.lean`.

Verified in the pinned checkout. Under PseudoEMetricSpace, IsCover takes an NNReal radius and uses edist and closedEBall. Under PseudoMetricSpace it is also characterized by real closedBall unions. The EMetricSpace theorem isCover_zero identifies zero-covering with set containment; this need not hold without separation. No compactness or measurability is assumed.

## Depends on

- [Extended pseudometric distance and balls](extended-pseudometric-distance-and-balls.md)
- [Metric closed balls](metric-closed-balls.md)
