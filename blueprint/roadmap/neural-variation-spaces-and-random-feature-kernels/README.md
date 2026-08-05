---
kind: roadmap
status: mapped
---

# Neural variation spaces and random-feature kernels

Comparison of the Banach variation space F1 with a random-feature RKHS F2 and the extra smoothness imposed by frozen features.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Nystrom and random-feature kernel approximations](../nystrom-and-random-feature-kernel-approximations/README.md)
- [Structured sparsity and low-rank regularization](../structured-sparsity-and-low-rank-regularization/README.md)
- [Variation spaces and neural approximation](../variation-spaces-and-neural-approximation/README.md)

## Candidate contents

- F2 and gamma2
- gamma1 bounded by gamma2 and F2 contained in F1
- Random-ReLU RKHS characterization
- Random-feature interpretation
- Optimized input weights as kernel learning
- Variation norm as kernel learning (Exercise 9.9)
- One-dimensional ReLU kernel
- All-dimensional ReLU kernel
- Step-activation kernel (Exercise 9.10)
- One-dimensional gamma2 upper bound
- All-dimensional Sobolev upper bound for gamma2

## Sources

- `sources/ltfp_book.pdf` — Chapter 9, Section 9.5, printed pages 271-276

## Mathlib assessment

Legacy assessment: `missing`.

The sharper gamma2 Sobolev exponent is cited rather than proved and needs an external proof source.
