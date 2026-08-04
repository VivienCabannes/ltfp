# Singular values of finite-dimensional linear maps

Let `T : E -> F` be a linear map between finite-dimensional inner-product spaces over a real or complex scalar field. Its singular values form a decreasing, finitely supported real sequence indexed from zero. For an index below the dimension of `E`, the value is the square root of the corresponding eigenvalue of the domain Gram operator `T.adjoint` composed with `T`, counted with multiplicity. Its support is exactly the initial segment whose length is the dimension of the range of `T`; consequently the value at `i` is zero exactly when that rank is at most `i`.

## Mathlib

Declarations: `LinearMap.singularValues`, `LinearMap.singularValues_fin`, `LinearMap.sq_singularValues_fin`, `LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues`, `LinearMap.singularValues_antitone`, `LinearMap.support_singularValues`, `LinearMap.singularValues_eq_zero_iff_le_finrank_range`
File: `Mathlib/Analysis/InnerProductSpace/SingularValues.lean`
