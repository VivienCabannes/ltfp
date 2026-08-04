# Restriction over countable measurable partitions

Let `alpha` be a measurable space, let `mu` be a measure on `alpha`, and let `s : iota -> Set alpha` be a countable family of pairwise disjoint measurable sets. Then

`mu.restrict (union i, s i) = Measure.sum (fun i => mu.restrict (s i))`.

If the family covers the whole space, this specializes to a decomposition of `mu` as the sum of its restrictions to the partition cells. The theorem requires a countable index type, pairwise set-theoretic disjointness, and measurability of every cell. It requires neither finite total mass nor a probability-measure assumption.

Mathlib also provides an almost-everywhere version. There, set-theoretic disjointness is weakened to `AEDisjoint mu` for every pair of distinct cells, meaning their intersection has `mu`-measure zero, and measurability is weakened to `NullMeasurableSet` with respect to `mu`. Neither theorem assumes that the union is the universal set; coverage is an additional hypothesis used only for the whole-measure specialization.

## Mathlib

Declarations: `MeasureTheory.Measure.restrict_iUnion`, `MeasureTheory.Measure.restrict_iUnion_ae`, `MeasureTheory.Measure.restrict_univ`
File: `Mathlib/MeasureTheory/Measure/Restrict.lean`
