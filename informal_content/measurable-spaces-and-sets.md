# Measurable spaces and sets

A measurable space on a type `alpha` specifies a predicate `MeasurableSet` on subsets of `alpha`. The empty set is measurable, the complement of a measurable set is measurable, and the union of a sequence of measurable sets is measurable.

Consequently the universal set and finite intersections and unions are measurable. More generally, if `iota` is any countable index type and every `s i` is measurable, then `union i, s i` is measurable. These statements require only a measurable-space structure; they do not require a measure or a probability measure.

## Mathlib

Declarations: `MeasurableSpace`, `MeasurableSet`, `MeasurableSet.empty`, `MeasurableSet.univ`, `MeasurableSet.compl`, `MeasurableSet.inter`, `MeasurableSet.union`, `MeasurableSet.iUnion`
File: `Mathlib/MeasureTheory/MeasurableSpace/Defs.lean`
