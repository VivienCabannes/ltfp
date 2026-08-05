---
kind: node
declaration: theorem
mathlib: true
---

# Tower property of conditional expectation

Let `E` be a complete real normed space, let `f` be arbitrary, and let `m1 <= m2 <= m0`. Suppose that the trim of `mu` along `m2 <= m0` is sigma-finite. Conditioning first on `m2` and then on `m1` agrees almost everywhere with conditioning directly on `m1`:

`mu[mu[f | m2] | m1] = mu[f | m1]` almost everywhere with respect to `mu`.

No integrability hypothesis on `f` and no sigma-finiteness assumption for the smaller trim are required; invalid cases are handled by the totalized definition.

## Mathlib

Declarations: `MeasureTheory.condExp_condExp_of_le`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 4, Section 4.5.1, printed pages 92-93

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. For m1 <= m2 <= m0, an arbitrary measure mu on m0, arbitrary f : alpha -> E, and a complete real normed-space codomain, condExp_condExp_of_le proves that conditioning first on m2 and then on m1 equals direct conditioning on m1 almost everywhere with respect to mu. It assumes only sigma-finiteness of the trim along m2 <= m0; neither input integrability nor sigma-finiteness of the smaller trim is required because conditional expectation is totalized to zero in invalid cases.

## Depends on

- [Strong measurability of conditional expectation](strong-measurability-of-conditional-expectation.md)
- [Integrability of conditional expectation](integrability-of-conditional-expectation.md)
- [Conditional expectation set-integral identity](conditional-expectation-set-integral-identity.md)
