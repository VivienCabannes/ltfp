---
kind: node
declaration: definition
mathlib: true
---

# Extended-metric separated sets

Let `X` be a pseudoemetric space, let `epsilon : ENNReal`, and let `s` be a subset of `X`. The set `s` is `epsilon`-separated when every two distinct points of `s` satisfy

`epsilon < edist x y`.

This is a strict separation condition. Unlike an `epsilon`-cover, its radius is allowed to be any extended nonnegative real, including `infinity`. Since no extended distance is strictly greater than `infinity`, an infinity-separated set is necessarily a subsingleton. In an emetric space every set is zero-separated, but this need not hold in a pseudoemetric space because distinct points may have extended distance zero.

## Mathlib

Declarations: `Metric.IsSeparated`, `Metric.isSeparated_iff_setRelIsSeparated`, `Metric.isSeparated_zero`
File: `Mathlib/Topology/MetricSpace/MetricSeparated.lean`


## Roadmap and coverage

- [Metric and measure-theoretic geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/MetricSpace/MetricSeparated.lean`.

Verified in the pinned checkout. Under PseudoEMetricSpace, IsSeparated has ENNReal radius and is Set.Pairwise (epsilon < edist x y). At radius top only subsingletons qualify. isSeparated_zero requires EMetricSpace separation and fails in general for distinct points at zero edistance.

## Depends on

- [Extended pseudometric distance and balls](extended-pseudometric-distance-and-balls.md)
