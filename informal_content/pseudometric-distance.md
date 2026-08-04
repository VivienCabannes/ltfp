# Pseudometric distance

Let `X` be a pseudometric space. Its distance is a function

`dist : X -> X -> Real`

such that `dist x x = 0`, `dist x y = dist y x`, and

`dist x z <= dist x y + dist y z`.

These axioms imply `0 <= dist x y`. They do not imply that points at distance zero are equal; that additional separation axiom defines a metric space. Every pseudometric space also has an extended distance satisfying

`edist x y = ENNReal.ofReal (dist x y)`.

Thus a real-valued pseudometric is a special case of a pseudoemetric. A general pseudoemetric may take the value `infinity` and need not arise from a real-valued distance.

The metric separation class is defined in `Mathlib/Topology/MetricSpace/Defs.lean`; the primary file below contains the distance structure and pseudometric theory.

## Mathlib

Declarations: `Dist`, `Dist.dist`, `PseudoMetricSpace`, `PseudoMetricSpace.toPseudoEMetricSpace`, `MetricSpace`, `dist_self`, `dist_comm`, `dist_triangle`, `dist_nonneg`, `edist_dist`
File: `Mathlib/Topology/MetricSpace/Pseudo/Defs.lean`
