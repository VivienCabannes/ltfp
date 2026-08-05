---
kind: node
declaration: definition
mathlib: true
---

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


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/EMetricSpace/Defs.lean`.

Independently verified in the pinned checkout. PseudoEMetricSpace has ENNReal-valued edist with zero self-distance, symmetry, and triangle inequality, allowing top and zero distance between distinct points. EMetricSpace adds separation and edist_eq_zero. closedEBall takes arbitrary ENNReal radius; closedEBall_top proves the top-radius ball is univ.

## Depends on

This node has no prerequisites.
