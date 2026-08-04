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
