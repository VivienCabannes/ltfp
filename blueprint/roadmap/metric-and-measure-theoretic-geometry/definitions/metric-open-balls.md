---
kind: node
declaration: definition
mathlib: true
---

# Metric open balls

Let `X` be a pseudometric space, let `x : X`, and let `r : Real`. The open ball of radius `r` centered at `x` is

`Metric.ball x r = {y | dist y x < r}`.

By symmetry of the distance, membership is equivalently `dist x y < r`. The radius is an arbitrary real number; in particular, a nonpositive-radius open ball is empty. The ball is open without any point-separation assumption.

If `X` also has a measurable space in which every open set is measurable, then every metric open ball is measurable. This uses `OpensMeasurableSpace X`; no measure or probability-measure assumption is required.

The definition, membership, empty-radius, and openness declarations are in the primary file below. `measurableSet_ball` is in `Mathlib/MeasureTheory/Constructions/BorelSpace/Metric.lean`.

## Mathlib

Declarations: `Metric.ball`, `Metric.mem_ball`, `Metric.mem_ball'`, `Metric.ball_eq_empty`, `Metric.isOpen_ball`, `measurableSet_ball`
File: `Mathlib/Topology/MetricSpace/Pseudo/Defs.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/Pseudo/Defs.lean`.

Verified in the pinned checkout. Definition, membership, and openness require only PseudoMetricSpace; a ball is empty exactly for nonpositive real radius. measurableSet_ball is in Mathlib/MeasureTheory/Constructions/BorelSpace/Metric.lean and additionally requires MeasurableSpace and OpensMeasurableSpace. No measure or separation assumption is needed.

## Depends on

- [Pseudometric distance](pseudometric-distance.md)
- [Open-measurable and Borel spaces](open-measurable-and-borel-spaces.md)
