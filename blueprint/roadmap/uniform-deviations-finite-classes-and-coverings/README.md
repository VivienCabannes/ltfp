---
kind: roadmap
status: mapped
---

# Uniform deviations, finite classes, and coverings

Reduction of empirical-risk estimation error to uniform deviations controlled by concentration, finite union bounds, and epsilon nets.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Empirical-risk decomposition and approximation](../empirical-risk-decomposition-and-approximation/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Bounded differences and Bernstein concentration](../bounded-differences-and-bernstein-concentration/README.md)
- [Maxima and smooth-sum expectation bounds](../maxima-and-smooth-sum-expectation-bounds/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Matrix and operator concentration](../matrix-and-operator-concentration/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)

## Candidate contents

- Two-sided uniform-deviation bound for estimation error
- Approximate empirical-risk-minimization optimization correction
- McDiarmid reduction to expected deviations
- Quadratic-loss closed-form uniform deviation
- Explicit quadratic uniform-deviation exercise (Exercise 4.6)
- Finite-class Hoeffding bound
- Expected finite-class maximum exercise (Exercise 4.7)
- Covering number
- Arbitrary-norm ball covering-number exercise (Exercise 4.8)
- Epsilon-net uniform-deviation bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Sections 4.4-4.4.4, printed pages 85-91

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Metric.IsCover`
- `Metric.coveringNumber`
- `Metric.minimalCover`
- `Metric.isCover_minimalCover`

Primary file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: Covering number. Assembly ingredients and limits: Metric.IsCover and Metric.minimalCover provide the metric-cover and finite epsilon-net substrate. Scalar concentration exists in prerequisite clusters, but no learning-theory uniform-deviation assembly or finite-dimensional arbitrary-norm ball entropy theorem was found. Materially uncovered members: Two-sided uniform-deviation bound for estimation error; Approximate empirical-risk-minimization optimization correction; McDiarmid reduction to expected deviations; Quadratic-loss closed-form uniform deviation; Explicit quadratic uniform-deviation exercise; Finite-class Hoeffding bound; Expected finite-class maximum exercise; Arbitrary-norm ball covering-number exercise; Epsilon-net uniform-deviation bound.
