# Metric closed balls

Let `X` be a pseudometric space, let `x : X`, and let `r : Real`. The closed ball of radius `r` centered at `x` is

`Metric.closedBall x r = {y | dist y x <= r}`.

By symmetry of the distance, membership is equivalently `dist x y <= r`. The radius is an arbitrary real number. The closed ball is closed without any point-separation assumption.

For a negative radius the closed ball is empty. At radius zero it is the closure of the center's singleton in a pseudometric space, so it need not be a singleton when distance does not separate points. It becomes exactly `{x}` under the stronger `MetricSpace` assumption. More generally, for a nonpositive radius the closed ball agrees with the corresponding sphere.

If `X` also has a measurable space in which every open set is measurable, then every metric closed ball is measurable. This uses `OpensMeasurableSpace X`; no measure or probability-measure assumption is required.

The definition and elementary radius lemmas are in the primary file below. `Metric.closedBall_zero'` and `Metric.isClosed_closedBall` are in `Mathlib/Topology/MetricSpace/Pseudo/Lemmas.lean`; `measurableSet_closedBall` is in `Mathlib/MeasureTheory/Constructions/BorelSpace/Metric.lean`.

## Mathlib

Declarations: `Metric.closedBall`, `Metric.mem_closedBall`, `Metric.mem_closedBall'`, `Metric.closedBall_eq_empty`, `Metric.closedBall_eq_sphere_of_nonpos`, `Metric.closedBall_zero'`, `Metric.isClosed_closedBall`, `measurableSet_closedBall`
File: `Mathlib/Topology/MetricSpace/Pseudo/Defs.lean`
