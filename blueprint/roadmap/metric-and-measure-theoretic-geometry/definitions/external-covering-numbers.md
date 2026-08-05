---
kind: node
declaration: definition
mathlib: true
---

# External covering numbers

Let `X` be a pseudoemetric space, let `epsilon : NNReal`, and let `A` be a subset of `X`. The external covering number of `A` at radius `epsilon` is

`inf {C.encard | Metric.IsCover epsilon A C}`,

where the infimum is taken in the extended natural-number type `ENat`, and `C.encard` is the extended natural cardinality of `C`. The value may be infinite. Centers range over all of `X`; they are not required to lie in `A`.

## Mathlib

Declarations: `Metric.externalCoveringNumber`, `Metric.IsCover.externalCoveringNumber_le_encard`, `Metric.externalCoveringNumber_anti`, `Metric.externalCoveringNumber_mono_set`
File: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Verified in the pinned checkout. Under PseudoEMetricSpace, externalCoveringNumber takes an NNReal radius and is the ENat infimum of encard over all IsCover center sets, without requiring centers to lie in the covered set. It may be top. The API gives the expected antitonicity in radius and monotonicity in the covered set; no finiteness, compactness, or measurability premise is present.

## Depends on

- [Extended-metric epsilon-covers](extended-metric-epsilon-covers.md)
