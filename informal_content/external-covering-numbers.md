# External covering numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. The external covering number of `A` at radius `epsilon` is

`inf {C.encard | Metric.IsCover epsilon A C}`,

where the infimum is taken in the extended natural-number type `ENat`, and `C.encard` is the extended natural cardinality of `C`. The value may be infinite. Centers range over all of `X`; they are not required to lie in `A`.

## Mathlib

Declarations: `Metric.externalCoveringNumber`, `Metric.IsCover.externalCoveringNumber_le_encard`, `Metric.externalCoveringNumber_anti`, `Metric.externalCoveringNumber_mono_set`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`
