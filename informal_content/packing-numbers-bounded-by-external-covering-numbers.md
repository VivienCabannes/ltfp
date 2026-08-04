# Packing numbers bounded by external covering numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.packingNumber (2 * epsilon) A <= Metric.externalCoveringNumber epsilon A`.

Thus every set whose distinct points are more than `2 * epsilon` apart injects into any cover by closed balls of radius `epsilon`. Both sides are extended-natural cardinal values, so the theorem includes finite and infinite cases.

## Mathlib

Declarations: `Metric.packingNumber_two_mul_le_externalCoveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`
