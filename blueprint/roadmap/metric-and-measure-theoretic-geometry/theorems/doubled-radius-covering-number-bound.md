---
kind: node
declaration: theorem
mathlib: true
---

# Doubled-radius covering number bound

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. Then

`Metric.coveringNumber (2 * epsilon) A <= Metric.externalCoveringNumber epsilon A`.

This is the doubled-radius internal-cover estimate obtained by placing the internal covering number below the packing number at radius `2 * epsilon`, then placing that packing number below the external covering number at radius `epsilon`.

## Mathlib

Declarations: `Metric.coveringNumber_two_mul_le_externalCoveringNumber`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. In every PseudoEMetricSpace, coveringNumber (2 * epsilon) A is at most externalCoveringNumber epsilon A. It composes the same-radius covering-packing bound with the doubled-radius packing-external bound and has no finiteness or nonemptiness premise.

## Depends on

- [Covering numbers bounded by packing numbers](covering-numbers-bounded-by-packing-numbers.md)
- [Packing numbers bounded by external covering numbers](packing-numbers-bounded-by-external-covering-numbers.md)
