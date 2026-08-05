---
kind: roadmap
status: detailed
---

# Metric and measure-theoretic geometry

Mathlib foundations for metric spaces, balls, covering and packing numbers, Euclidean volume, and measurable geometric sets.

## Planning status

This milestone is decomposed into 21 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Metric balls and distances
- Covering numbers
- Packing numbers
- Euclidean volume
- Measurable partitions and restrictions

## Detailed nodes

- [Pseudometric distance](definitions/pseudometric-distance.md)
- [Metric open balls](definitions/metric-open-balls.md)
- [Metric closed balls](definitions/metric-closed-balls.md)
- [Extended-metric epsilon-covers](definitions/extended-metric-epsilon-covers.md)
- [Extended-metric separated sets](definitions/extended-metric-separated-sets.md)
- [External covering numbers](definitions/external-covering-numbers.md)
- [Internal covering numbers](definitions/internal-covering-numbers.md)
- [Packing numbers](definitions/packing-numbers.md)
- [External covering number bounded by internal covering number](theorems/external-covering-number-bounded-by-internal-covering-number.md)
- [Packing numbers bounded by external covering numbers](theorems/packing-numbers-bounded-by-external-covering-numbers.md)
- [Covering numbers bounded by packing numbers](theorems/covering-numbers-bounded-by-packing-numbers.md)
- [Doubled-radius covering number bound](theorems/doubled-radius-covering-number-bound.md)
- [Volume of Euclidean open balls](theorems/volume-of-euclidean-open-balls.md)
- [Volume of Euclidean closed balls](theorems/volume-of-euclidean-closed-balls.md)
- [Measurable spaces and sets](definitions/measurable-spaces-and-sets.md)
- [Canonical finite measurable partitions](definitions/canonical-finite-measurable-partitions.md)
- [Measure restriction](definitions/measure-restriction.md)
- [Restriction over countable measurable partitions](theorems/restriction-over-countable-measurable-partitions.md)
- [Extended pseudometric distance and balls](definitions/extended-pseudometric-distance-and-balls.md)
- [Open-measurable and Borel spaces](definitions/open-measurable-and-borel-spaces.md)
- [Countably generated measurable spaces](definitions/countably-generated-measurable-spaces.md)

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `in-mathlib`.

Relevant declarations:

- `Metric.coveringNumber`
- `Metric.packingNumber`
- `Metric.closedBall`
- `MeasureTheory.Measure.restrict`
- `MeasureTheory.volume_sum_rpow_le`

Primary file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Pinned Mathlib defines Metric.coveringNumber and Metric.packingNumber in Mathlib/Topology/MetricSpace/CoveringNumbers.lean, Metric.closedBall in the metric-space core, Measure.restrict in Mathlib/MeasureTheory/Measure/Restrict.lean, and finite-dimensional volume-of-ball results such as MeasureTheory.volume_sum_rpow_le in Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean. Measurable-partition constructions are assembled from the general measurable-set and restriction APIs.
