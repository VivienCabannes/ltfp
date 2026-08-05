---
kind: roadmap
status: detailed
---

# Deterministic quadrature error

Trapezoidal approximation of expectations under differentiability or periodicity assumptions.

## Planning status

This milestone is decomposed into 12 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Uniform-grid trapezoidal estimator
- Piecewise-affine integral identity
- Exact trapezoidal error decomposition
- Second-derivative error bound
- Affine interpolation and local error (Exercise 1.26)
- First-derivative error rate (Exercise 1.27)
- Periodic smooth-function error rate (Exercise 1.28)

## Detailed nodes

- [Uniform-grid trapezoidal estimator](definitions/uniform-grid-trapezoidal-estimator.md)
- [Affine panel interpolant](definitions/affine-panel-interpolant.md)
- [Affine panel integral identity](theorems/affine-panel-integral-identity.md)
- [Piecewise-affine integral identity](theorems/piecewise-affine-integral-identity.md)
- [Exact trapezoidal error decomposition](theorems/exact-trapezoidal-error-decomposition.md)
- [Affine interpolation local error (Exercise 1.26)](theorems/affine-interpolation-local-error-exercise-1-26.md)
- [Second-derivative trapezoidal error bound](theorems/second-derivative-trapezoidal-error-bound.md)
- [First-derivative error rate (Exercise 1.27)](theorems/first-derivative-error-rate-exercise-1-27.md)
- [Periodic Bernoulli-kernel trapezoidal identity](theorems/periodic-bernoulli-kernel-trapezoidal-identity.md)
- [Periodic smooth-function error rate (Exercise 1.28)](theorems/periodic-smooth-function-error-rate-exercise-1-28.md)
- [Affine line maps](definitions/affine-line-maps.md)
- [Rolle's theorem for real derivatives](theorems/rolles-theorem-for-real-derivatives.md)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed pages 18-19

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `trapezoidal_integral`
- `trapezoidal_error`
- `trapezoidal_integral_one`
- `sum_trapezoidal_integral_adjacent_intervals`
- `sum_trapezoidal_error_adjacent_intervals`
- `trapezoidal_error_le`
- `trapezoidal_error_le_of_c2`
- `AffineMap.lineMap`
- `AffineMap.lineMap_apply_ring`

Primary file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`.

Pinned Mathlib has a dedicated uniform-grid trapezoidal-rule definition, its signed error, the one-panel endpoint formula, exact decomposition into adjacent-panel errors, and the sharp C2 bound |error| <= |b-a|^3*zeta/(12*N^2). The book's [0,1] estimator and L/(12*n^2) result are direct specializations (Mathlib defines error with the opposite sign, immaterial under absolute value). AffineMap.lineMap_apply_ring gives the explicit affine interpolant formula, but its integral identity still needs assembly from elementary interval integrals. No public theorem was found for the pointwise L*x*(1-x)/2 interpolation error, the O(1/n) first-derivative-only rate, or the O(1/n^s) periodic smooth-function rate.
