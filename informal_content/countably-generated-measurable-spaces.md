# Countably generated measurable spaces

A measurable space on `alpha` is countably generated when some countable family of subsets generates its entire sigma-algebra through `MeasurableSpace.generateFrom`.

Mathlib chooses a countable generating family `MeasurableSpace.countableGeneratingSet alpha`, inserting the empty set to keep the family nonempty. It also chooses an enumeration

`MeasurableSpace.natGeneratingSequence alpha : Nat -> Set alpha`.

Generating from either the chosen family or the range of this sequence recovers the original measurable-space structure. These objects are definite choices exposed by Mathlib, not intrinsic choice-independent generators.

No measure, probability, topology, or nonempty-type assumption is involved.

## Mathlib

Declarations: `MeasurableSpace.generateFrom`, `MeasurableSpace.CountablyGenerated`, `MeasurableSpace.countableGeneratingSet`, `MeasurableSpace.countable_countableGeneratingSet`, `MeasurableSpace.generateFrom_countableGeneratingSet`, `MeasurableSpace.natGeneratingSequence`, `MeasurableSpace.generateFrom_natGeneratingSequence`
File: `Mathlib/MeasureTheory/MeasurableSpace/CountablyGenerated.lean`
