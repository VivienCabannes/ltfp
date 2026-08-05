---
kind: node
declaration: definition
mathlib: true
---

# Random variable

Let `Omega` and `E` be types with measurable-space structures. A function `X : Omega -> E` is measurable when the inverse image under `X` of every measurable subset of `E` is measurable in `Omega`. This predicate requires no measure or probability-measure assumption. Measurable functions are closed under composition and are almost everywhere measurable with respect to any chosen measure.

Mathlib has no separate `RandomVariable` alias; the canonical predicate for this concept is `Measurable`. Its measure-dependent relaxation `AEMeasurable` is distinct from strong measurability, which also requires topological structure.

## Mathlib

Declarations: `Measurable`, `Measurable.comp`, `AEMeasurable`, `Measurable.aemeasurable`
File: `Mathlib/MeasureTheory/MeasurableSpace/Defs.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.1, printed pages 22-24

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/MeasurableSpace/Defs.lean`.

Verified in the pinned checkout. Mathlib has no RandomVariable alias: the canonical predicate is Measurable X, defined by measurable preimages and requiring only measurable-space structures. Measurable.comp supplies closure under composition. The measure-dependent relaxation AEMeasurable X P is used downstream, and every measurable function is almost everywhere measurable for any measure via Measurable.aemeasurable. Strong measurability is a separate topological notion and is not part of this node.

## Depends on

This node has no prerequisites.
