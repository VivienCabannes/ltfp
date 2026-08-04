# External covering number bounded by internal covering number

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.externalCoveringNumber epsilon A <= Metric.coveringNumber epsilon A`.

The radii and the closed-ball convention are identical on both sides. The inequality reflects only that an external cover may use any centers in `X`, whereas an internal cover must use centers from `A`.

## Mathlib

Declarations: `Metric.externalCoveringNumber_le_coveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`
