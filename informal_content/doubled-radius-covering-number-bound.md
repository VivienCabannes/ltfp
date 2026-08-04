# Doubled-radius covering number bound

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.coveringNumber (2 * epsilon) A <= Metric.externalCoveringNumber epsilon A`.

This is the doubled-radius internal-cover estimate obtained by placing the internal covering number below the packing number at radius `2 * epsilon`, then placing that packing number below the external covering number at radius `epsilon`.

## Mathlib

Declarations: `Metric.coveringNumber_two_mul_le_externalCoveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`
