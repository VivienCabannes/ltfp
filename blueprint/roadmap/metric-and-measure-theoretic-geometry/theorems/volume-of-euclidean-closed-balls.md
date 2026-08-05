---
kind: node
declaration: theorem
mathlib: true
---

# Volume of Euclidean closed balls

Let `iota` be a finite nonempty type, set `n = Fintype.card iota`, let `x` belong to `EuclideanSpace Real iota`, and let `r : Real`. For Mathlib's canonical volume measure,

`volume (Metric.closedBall x r)`

is equal to

`ENNReal.ofReal r ^ n * ENNReal.ofReal (Real.sqrt Real.pi ^ n / Real.Gamma (n / 2 + 1))`.

This is the same value as for the open ball. In finite-dimensional nontrivial real normed spaces with additive Haar measure, the boundary sphere has measure zero, so open and closed balls have equal measure. The formula holds for every real radius.

The additive-Haar closed/open equality and sphere-null theorem are in `Mathlib/MeasureTheory/Measure/Lebesgue/EqHaar.lean`; the Euclidean formula is in the primary file below.

## Mathlib

Declarations: `EuclideanSpace.volume_closedBall`, `MeasureTheory.Measure.addHaar_closedBall_eq_addHaar_ball`, `MeasureTheory.Measure.addHaar_sphere`
File: `Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean`.

Verified in the pinned checkout. For Fintype iota with Nonempty iota, volume_closedBall gives the same Gamma-function formula as volume_ball for every real radius. The closed/open equality and boundary-null addHaar_sphere theorem are in Mathlib/MeasureTheory/Measure/Lebesgue/EqHaar.lean.

## Depends on

- [Metric closed balls](../definitions/metric-closed-balls.md)
- [Volume of Euclidean open balls](volume-of-euclidean-open-balls.md)
