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
