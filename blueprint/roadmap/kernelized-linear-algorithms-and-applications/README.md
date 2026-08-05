---
kind: roadmap
status: mapped
---

# Kernelized linear algorithms and applications

Algorithms expressible through inner products admit kernelized forms, including principal components, clustering, quadrature, and nearest-centroid classification.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Hilbert-space covariance operators and probability](../hilbert-space-covariance-operators-and-probability/README.md)
- [Principal components and low-rank regression](../principal-components-and-low-rank-regression/README.md)
- [Local-averaging estimator constructions](../local-averaging-estimator-constructions/README.md)

## Candidate contents

- Kernelization of linear algorithms
- Kernel principal components (Exercise 7.17)
- Kernel K-means (Exercise 7.18)
- Kernel quadrature (Exercise 7.19)
- Kernel nearest-centroid classification (Exercise 7.20)

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Section 7.4.6 and Exercises 7.17-7.20, printed pages 201-202

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib searches found RKHS and Gram-matrix primitives but no direct kernel PCA, kernel K-means, kernel quadrature, or kernel nearest-centroid declarations. The kernelization arguments and applications require project-local proofs.
