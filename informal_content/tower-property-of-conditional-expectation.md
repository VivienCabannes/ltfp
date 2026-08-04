# Tower property of conditional expectation

Let `E` be a complete real normed space, let `f` be arbitrary, and let `m1 <= m2 <= m0`. Suppose that the trim of `mu` along `m2 <= m0` is sigma-finite. Conditioning first on `m2` and then on `m1` agrees almost everywhere with conditioning directly on `m1`:

`mu[mu[f | m2] | m1] = mu[f | m1]` almost everywhere with respect to `mu`.

No integrability hypothesis on `f` and no sigma-finiteness assumption for the smaller trim are required; invalid cases are handled by the totalized definition.

## Mathlib

Declarations: `MeasureTheory.condExp_condExp_of_le`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`
