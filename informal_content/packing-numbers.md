# Packing numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. The packing number of `A` at radius `epsilon` is

`sup {C.encard | C subset A and Metric.IsSeparated epsilon C}`,

with the supremum taken in `ENat`. The `NNReal` radius is coerced to `ENNReal` in the separation predicate. The value may be `top`, and separation uses the strict inequality `epsilon < edist x y` for distinct points. A top value can record arbitrarily large finite separated subsets without asserting that one infinite separated subset realizes the supremum.

When the value is not `top`, Mathlib chooses a finite separated subset `Metric.maximalSeparatedSet epsilon A` that realizes it. This chosen maximal separated set is also an `epsilon`-cover of `A`; neither conclusion needs compactness or total boundedness. If the packing number is `top`, the definition chooses the empty set and the realization and cover theorems do not apply.

## Mathlib

Declarations: `Metric.packingNumber`, `Metric.IsSeparated.encard_le_packingNumber`, `Metric.maximalSeparatedSet`, `Metric.maximalSeparatedSet_subset`, `Metric.isSeparated_maximalSeparatedSet`, `Metric.encard_maximalSeparatedSet`, `Metric.isCover_maximalSeparatedSet`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`
