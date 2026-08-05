---
kind: node
declaration: theorem
mathlib: true
---

# Covering numbers bounded by packing numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.coveringNumber epsilon A <= Metric.packingNumber epsilon A`.

The internal covering number and the packing number use the same radius. The statement remains valid when either extended-natural cardinal is infinite.

## Mathlib

Declarations: `Metric.coveringNumber_le_packingNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. In every PseudoEMetricSpace, coveringNumber epsilon A is at most packingNumber epsilon A at the same NNReal radius. The proof uses the realizing maximal separated cover below top and handles the top case separately, so no finiteness assumption appears in the theorem.

## Depends on

- [Internal covering numbers](../definitions/internal-covering-numbers.md)
- [Packing numbers](../definitions/packing-numbers.md)
