---
kind: roadmap
status: mapped
---

# Minimum-norm interpolation by gradient methods

Gradient descent from zero in overparameterized least squares stays in the row span and converges to the Moore-Penrose minimum-norm interpolator.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Overparameterized least-squares model
- Residual recursion
- Row-span invariance
- Algorithmic representer property
- Pseudoinverse interpolator
- Minimum-l2 interpolation duality
- Polyak-Lojasiewicz inequality
- Linear convergence under the PL inequality

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.1.1, printed pages 343-346

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib has orthogonal projections, adjoints, ranges and kernels, but Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean explicitly says pseudoinverses are not considered. Searches found no Moore-Penrose interpolator, overparameterized least-squares gradient recursion, row-span invariance theorem, Polyak-Lojasiewicz inequality, or PL convergence result. All eight cluster members require assembly or new proofs.
