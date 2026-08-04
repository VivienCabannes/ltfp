# Countable union bound

Let `mu` be a probability measure, let `I` be a countable index type, and let `A i` be a family of sets. Then

`mu (union i, A i) <= sum' i, mu (A i)`.

No pairwise-disjointness assumption is needed. Mathlib's outer-measure formulation is more general: it proves the inequality for an arbitrary measure and arbitrary sets, so separate measurability hypotheses on the individual sets are unnecessary.

## Mathlib

Declarations: `MeasureTheory.measure_iUnion_le`
File: `Mathlib/MeasureTheory/OuterMeasure/Basic.lean`
