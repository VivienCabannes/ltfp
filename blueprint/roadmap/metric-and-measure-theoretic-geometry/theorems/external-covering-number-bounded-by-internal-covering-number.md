---
kind: node
declaration: lemma
mathlib: true
---

# External covering number bounded by internal covering number

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.externalCoveringNumber epsilon A <= Metric.coveringNumber epsilon A`.

The radii and the closed-ball convention are identical on both sides. The inequality reflects only that an external cover may use any centers in `X`, whereas an internal cover must use centers from `A`.

## Mathlib

Declarations: `Metric.externalCoveringNumber_le_coveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. For every PseudoEMetricSpace, NNReal radius, and subset, the external ENat infimum is at most the internal ENat infimum because every internal cover is an admissible external cover. No finiteness or nonemptiness assumption is needed.

## Depends on

- [External covering numbers](../definitions/external-covering-numbers.md)
- [Internal covering numbers](../definitions/internal-covering-numbers.md)
