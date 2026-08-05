---
kind: roadmap
status: mapped
---

# Hierarchical sparse priors

Heavy-tailed and hierarchical priors for sparse parameters, including Gaussian scale mixtures and their induced penalties.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Likelihood and prior modeling foundations](../likelihood-and-prior-modeling-foundations/README.md)
- [Likelihood-loss and MAP-regularization correspondences](../likelihood-loss-and-map-regularization-correspondences/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)

## Candidate contents

- Generalized-Gaussian sparse prior
- Student prior
- Spike-and-slab Gaussian mixture prior
- Gaussian scale-mixture representation
- Laplace prior as a Gaussian scale mixture
- Super-Gaussian density
- Scale mixtures are super-Gaussian (Exercise 14.4)
- Hierarchical variance prior
- Marginalization over latent scales
- Sparse MAP penalty from hierarchical priors

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.1.3 and Exercise 14.4, printed pages 412-413

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: ProbabilityTheory.multivariateGaussian, ProbabilityTheory.gammaMeasure, ProbabilityTheory.expMeasure, Dirac measures, measure addition/scaling, and MeasureTheory.Measure.bind can encode Gaussian components and latent-scale mixing. Mathlib has no generalized-Gaussian, Student-t, inverse-Gamma, Laplace, spike-and-slab, super-Gaussian, or named hierarchical sparse-prior API, and no Gaussian-mixture identities or induced sparse-MAP theorem. Materially uncovered members: Generalized-Gaussian sparse prior; Student prior; Spike-and-slab Gaussian mixture prior; Gaussian scale-mixture representation; Laplace prior as a Gaussian scale mixture; Super-Gaussian density; Scale mixtures are super-Gaussian (Exercise 14.4); Hierarchical variance prior; Marginalization over latent scales; Sparse MAP penalty from hierarchical priors.
