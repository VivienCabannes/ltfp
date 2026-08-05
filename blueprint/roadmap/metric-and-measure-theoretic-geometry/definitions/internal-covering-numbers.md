---
kind: node
declaration: definition
mathlib: true
---

# Internal covering numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. The internal covering number of `A` at radius `epsilon` is

`inf {C.encard | C subset A and Metric.IsCover epsilon A C}`,

with the infimum taken in `ENat`. The value may be infinite. Unlike the external covering number, every center is required to lie in the covered set `A`.

When the value is not `top`, Mathlib chooses a finite internal cover `Metric.minimalCover epsilon A` that realizes this cardinality. No compactness or total-boundedness assumption is needed for this implication. If the value is `top`, `minimalCover` is defined to be empty, and the covering and realization theorems do not apply.

## Mathlib

Declarations: `Metric.coveringNumber`, `Metric.IsCover.coveringNumber_le_encard`, `Metric.coveringNumber_anti`, `Metric.minimalCover`, `Metric.minimalCover_subset`, `Metric.finite_minimalCover`, `Metric.isCover_minimalCover`, `Metric.encard_minimalCover`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. Under PseudoEMetricSpace, coveringNumber takes an NNReal radius and is the ENat infimum of encard over IsCover center sets constrained to lie in A. If the value is not top, minimalCover is a finite subset of A, covers A, and realizes the value without compactness or total-boundedness assumptions. If the value is top, minimalCover is empty and the cover/realization theorems require the explicit non-top hypothesis.

## Depends on

- [Extended-metric epsilon-covers](extended-metric-epsilon-covers.md)
