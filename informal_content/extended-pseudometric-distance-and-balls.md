# Extended pseudometric distance and balls

An extended distance on a type `X` takes values in `ENNReal`, so it may equal `infinity`. A `PseudoEMetricSpace X` requires

`edist x x = 0`,

`edist x y = edist y x`,

and

`edist x z <= edist x y + edist y z`.

Distinct points may have extended distance zero. An `EMetricSpace` adds the separation axiom, equivalently `edist x y = 0` if and only if `x = y`.

For `r : ENNReal`, the extended closed ball centered at `x` is

`Metric.closedEBall x r = {y | edist y x <= r}`.

By symmetry, membership is equivalently `edist x y <= r`. Unlike real-valued closed balls, the radius may be `infinity`; the corresponding extended closed ball is then the whole space.

## Mathlib

Declarations: `EDist`, `EDist.edist`, `PseudoEMetricSpace`, `EMetricSpace`, `edist_self`, `edist_comm`, `edist_triangle`, `edist_eq_zero`, `Metric.closedEBall`, `Metric.mem_closedEBall`, `Metric.mem_closedEBall'`, `Metric.closedEBall_top`
File: `Mathlib/Topology/EMetricSpace/Defs.lean`
