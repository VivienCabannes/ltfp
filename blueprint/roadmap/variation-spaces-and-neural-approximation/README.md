---
kind: roadmap
status: mapped
---

# Variation spaces and neural approximation

Infinite-width variation-norm spaces and norm bounds from curvature, Fourier-Barron smoothness, Sobolev regularity, and latent dimension.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Shallow ReLU models and norm-controlled estimation](../shallow-relu-models-and-norm-controlled-estimation/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Lipschitz kernel learning and smoothness adaptation](../lipschitz-kernel-learning-and-smoothness-adaptation/README.md)
- [Signed measures and variation norms](../signed-measures-and-variation-norms/README.md)
- [Fourier analysis and Sobolev approximation](../fourier-analysis-and-sobolev-approximation/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)

## Candidate contents

- Exact ReLU representation of piecewise-affine functions
- One-dimensional and multidimensional universal approximation
- Signed-measure representation of networks
- Variation norm gamma1
- Function space F1
- Variation norm and Lipschitz property
- Banach-space completeness obligation
- One-dimensional piecewise-affine variation bound
- Twice-differentiable Taylor variation bound
- Minimum-variation interpolant (Exercise 9.3)
- Fourier-Barron variation bound
- Step-activation variation norm (Exercise 9.4)
- Sobolev-to-variation norm bound
- Latent-variable norm contraction and dimension adaptation

## Sources

- `sources/ltfp_book.pdf` — Chapter 9, Sections 9.3.1-9.3.5, printed pages 256-266

## Mathlib assessment

Legacy assessment: `missing`.

Completeness of F1 is asserted but not proved in the source and must be a separate obligation.
