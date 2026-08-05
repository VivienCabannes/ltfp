---
kind: node
declaration: theorem
mathlib: true
---

# Packing numbers bounded by external covering numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.packingNumber (2 * epsilon) A <= Metric.externalCoveringNumber epsilon A`.

Thus every set whose distinct points are more than `2 * epsilon` apart injects into any cover by closed balls of radius `epsilon`. Both sides are extended-natural cardinal values, so the theorem includes finite and infinite cases.

## Mathlib

Declarations: `Metric.packingNumber_two_mul_le_externalCoveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. In every PseudoEMetricSpace, packingNumber (2 * epsilon) A is at most externalCoveringNumber epsilon A. Strict separation and the triangle inequality make a chosen covering-center map injective; no nearest-center existence is assumed. The ENat theorem includes top-valued cases.

## Depends on

- [Packing numbers](../definitions/packing-numbers.md)
- [External covering numbers](../definitions/external-covering-numbers.md)
