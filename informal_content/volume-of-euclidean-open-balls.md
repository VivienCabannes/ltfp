# Volume of Euclidean open balls

Let `iota` be a finite nonempty type, set `n = Fintype.card iota`, let `x` belong to `EuclideanSpace Real iota`, and let `r : Real`. For Mathlib's canonical volume measure,

`volume (Metric.ball x r)`

is equal to

`ENNReal.ofReal r ^ n * ENNReal.ofReal (Real.sqrt Real.pi ^ n / Real.Gamma (n / 2 + 1))`,

where the occurrences of `n` inside the gamma-function expression are coerced to real numbers. The normalization is the one transported from product Lebesgue measure by the standard coordinate isometry. The formula holds for every real radius, including nonpositive radii; `ENNReal.ofReal r` then vanishes.

The coordinate volume-preservation declarations are in `Mathlib/MeasureTheory/Measure/Haar/InnerProductSpace.lean`; the formula itself is in the primary file below.

## Mathlib

Declarations: `EuclideanSpace.volume_ball`, `EuclideanSpace.volume_preserving_symm_measurableEquiv_toLp`, `PiLp.volume_preserving_toLp`
File: `Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean`
