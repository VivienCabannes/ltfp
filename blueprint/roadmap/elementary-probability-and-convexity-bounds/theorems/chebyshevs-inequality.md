---
kind: node
declaration: theorem
mathlib: true
---

# Chebyshev's inequality

Let `mu` be a probability measure, let `X : Omega -> Real` belong to `L^2(mu)`, and let `epsilon > 0`. Then

`mu.real {omega | epsilon < abs (X omega - integral omega, X omega dmu)}`

`<= Var[X; mu] / epsilon^2`.

The deviation event is strict, as in the source. The `L^2` hypothesis supplies measurability, integrability, and the finite second moment. Mathlib bounds the stronger closed-threshold event by the measure-valued right-hand side `ENNReal.ofReal (Var[X; mu] / epsilon^2)`; event inclusion and finite real values give the displayed probability inequality.

## Mathlib

Declarations: `ProbabilityTheory.meas_ge_le_variance_div_sq`
File: `Mathlib/Probability/Moments/Variance.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, Chebyshev display

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/Moments/Variance.lean`.

Verified in the pinned checkout. Under IsFiniteMeasure mu, MemLp X 2 mu, and 0 < c, meas_ge_le_variance_div_sq bounds the closed-threshold event {c <= abs (X - integral X)} by ENNReal.ofReal (variance X mu / c^2). The source's strict event is a subset. A probability measure supplies the finite-measure instance, and finiteness permits the displayed measureReal specialization. No separate measurability premise is needed beyond MemLp.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/random-variable.md)
- [Markov's inequality](markovs-inequality.md)
