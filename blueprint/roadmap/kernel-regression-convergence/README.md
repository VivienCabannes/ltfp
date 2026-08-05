---
kind: roadmap
status: mapped
---

# Kernel-regression convergence

Convolution-based bias and variance analysis and nonasymptotic bandwidth rates for Nadaraya-Watson regression.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Generic local-smoother bias and variance](../generic-local-smoother-bias-and-variance/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Bounded differences and Bernstein concentration](../bounded-differences-and-bernstein-concentration/README.md)

## Candidate contents

- Kernel-density bandwidth scaling
- Convolution smoothing identity
- Asymptotic Nadaraya-Watson variance
- Asymptotic Nadaraya-Watson bias
- Kernel-regression bandwidth balance
- Nadaraya-Watson convergence theorem
- Normalization constant
- Bounded-normalization-constant exercise (Exercise 6.4)

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.3.3, printed pages 170-174

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `MeasureTheory.convolution`
- `MeasureTheory.convolution_def`
- `MeasureTheory.dist_convolution_le`
- `MeasureTheory.convolution_tendsto_right`

Primary file: `Mathlib/Analysis/Convolution.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: Convolution smoothing identity. Assembly ingredients and limits: Mathlib defines function convolution by the required integral and proves that normalized nonnegative kernels approximate a target through dist_convolution_le and convolution_tendsto_right. It has no Nadaraya-Watson ratio estimator, stochastic numerator/denominator analysis, asymptotic variance or bias formula, bandwidth balance, normalization-constant bound, or kernel-regression convergence theorem. Source issue: the printed theorem types the kernel as real-valued while its setup and proof require nonnegativity; that hypothesis must be resolved before splitting. Materially uncovered members: Kernel-density bandwidth scaling; Asymptotic Nadaraya-Watson variance; Asymptotic Nadaraya-Watson bias; Kernel-regression bandwidth balance; Nadaraya-Watson convergence theorem; Normalization constant; Bounded-normalization-constant exercise.
