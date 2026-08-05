---
kind: node
declaration: definition
statement: formalized
lean: affinePanelInterp, affinePanelInterp_apply, affinePanelInterp_eq_of_ne, affinePanelInterp_left, affinePanelInterp_right, affinePanelInterp_self, affinePanelInterp_self_eq_const, affinePanelInterp_zero_one
---

# Affine panel interpolant

Let `f : Real -> Real` and let `a, b : Real`. Define the total normalized affine panel function by

`A[f; a, b](x) = AffineMap.lineMap (f a) (f b) ((x - a) / (b - a))`.

When `a != b`, this is the affine interpolant of the endpoint data `(a, f a)` and `(b, f b)`. Equivalently,

`A[f; a, b](x) = ((b - x) / (b - a)) * f a + ((x - a) / (b - a)) * f b`.

Consequently `A[f; a, b](a) = f a` and `A[f; a, b](b) = f b`. For `a = 0` and `b = 1`, this reduces to

`A[f; 0, 1](x) = (1 - x) * f 0 + x * f 1`.

When `a = b`, Lean's totalized division makes the scalar parameter zero, and both endpoint values are `f a`; thus `A[f; a, a]` is the constant function with value `f a`.

## Proof

Apply `AffineMap.lineMap_apply_ring` at the scalar parameter `(x - a) / (b - a)`. This gives the first displayed definition as

`(1 - (x - a) / (b - a)) * f a + ((x - a) / (b - a)) * f b`.

If `a != b`, the denominator is nonzero, and elementary field algebra rewrites the first coefficient as `(b - x) / (b - a)`. Substituting `x = a` or `x = b` gives the endpoint identities. The unit-interval formula is the specialization `a = 0`, `b = 1`. If `a = b`, totalized division and the equal endpoint values give the constant-function claim directly.


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 19, Exercise 1.26
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.26, printed page 4

## Planning record

Legacy Mathlib assessment: `partial`.
Primary supporting file: `Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean`.

Verified in the pinned checkout. AffineMap.lineMap is the parameter-zero-to-one affine map through two values and the listed application lemmas are exact. Evaluating it at (x - a) / (b - a) defines a total normalized panel function. Rewriting the first coefficient as (b - x) / (b - a) requires a != b. Both endpoint identities hold in that case; when a = b, totalized division and equal endpoint values make the function constantly f a, so the coincident endpoint identity also holds. No named declaration bundles that normalized-coordinate assembly.

## Depends on

- [Affine line maps](affine-line-maps.md)
