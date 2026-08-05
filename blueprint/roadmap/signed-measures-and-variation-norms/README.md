---
kind: roadmap
status: mapped
---

# Signed measures and variation norms

Signed and vector measures, total variation, Bochner integration, and quotient norms used to define infinite-width variation spaces.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Signed measures
- Jordan decomposition
- Total variation measure and norm
- Integration against signed measures
- Vector measures
- Quotient infimum norms

## Sources

- `sources/ltfp_book.pdf` — Chapter 9, Section 9.3.2, printed pages 257-259
- `sources/ltfp_book.pdf` — Chapter 9, Section 9.5.1, printed pages 271-273

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `MeasureTheory.SignedMeasure`
- `MeasureTheory.VectorMeasure.variation`
- `MeasureTheory.SignedMeasure.toJordanDecomposition`
- `MeasureTheory.SignedMeasure.toSignedMeasure_toJordanDecomposition`
- `MeasureTheory.VectorMeasure.integral`

Primary file: `Mathlib/MeasureTheory/VectorMeasure/Integral.lean`.

Pinned Mathlib provides signed and vector measures, total variation as a measure, Jordan decomposition, and integration of vector-valued functions against signed or vector measures. The neural representation quotient and its infimum norm remain project-specific.
