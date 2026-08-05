---
kind: node
declaration: theorem
mathlib: true
---

# Countable union bound

Let `mu` be a probability measure, let `I` be a countable index type, and let `A i` be a family of sets. Then

`mu (union i, A i) <= sum' i, mu (A i)`.

No pairwise-disjointness assumption is needed. Mathlib's outer-measure formulation is more general: it proves the inequality for an arbitrary measure and arbitrary sets, so separate measurability hypotheses on the individual sets are unnecessary.

## Mathlib

Declarations: `MeasureTheory.measure_iUnion_le`
File: `Mathlib/MeasureTheory/OuterMeasure/Basic.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 9, union-bound display

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/OuterMeasure/Basic.lean`.

Verified in the pinned checkout. For any OuterMeasureClass-valued measure-like object mu and any index type with a Countable instance, measure_iUnion_le bounds mu of the indexed union by the ENNReal tsum of the component values. It needs neither set measurability nor pairwise disjointness. The source's probability-measure statement is an immediate specialization.

## Depends on

- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
