---
kind: roadmap
status: detailed
---

# Measure-theoretic probability and conditional expectation

Mathlib foundations for probability measures, laws, independent random variables, integration, conditional expectation, and integral expectation inequalities.

## Planning status

This milestone is decomposed into 23 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

This milestone has no coarse prerequisites.

## Candidate contents

- Probability measures and random variables
- Laws of random variables
- Independent families
- Conditional expectation
- Product measures and independent samples
- Integral Jensen and expectation inequalities

## Detailed nodes

- [Probability measure](definitions/probability-measure.md)
- [Random variable](definitions/random-variable.md)
- [Law of a random variable](definitions/law-of-a-random-variable.md)
- [Identically distributed random variables](definitions/identically-distributed-random-variables.md)
- [Independent family of random variables](definitions/independent-family-of-random-variables.md)
- [Finite product law of independent random variables](theorems/finite-product-law-of-independent-random-variables.md)
- [Independence characterized by a finite product law](theorems/independence-characterized-by-a-finite-product-law.md)
- [Infinite product law of independent random variables](theorems/infinite-product-law-of-independent-random-variables.md)
- [Independence characterized by an infinite product law](theorems/independence-characterized-by-an-infinite-product-law.md)
- [Independent coordinates on an infinite product space](theorems/independent-coordinates-on-an-infinite-product-space.md)
- [Existence of iid random variables](theorems/existence-of-iid-random-variables.md)
- [Radon-Nikodym derivative of measures](definitions/radon-nikodym-derivative-of-measures.md)
- [Measurability of the Radon-Nikodym derivative](theorems/measurability-of-the-radon-nikodym-derivative.md)
- [Radon-Nikodym representation theorem](theorems/radon-nikodym-representation-theorem.md)
- [Almost-everywhere uniqueness of the Radon-Nikodym derivative](theorems/almost-everywhere-uniqueness-of-the-radon-nikodym-derivative.md)
- [Conditional expectation](definitions/conditional-expectation.md)
- [Strong measurability of conditional expectation](theorems/strong-measurability-of-conditional-expectation.md)
- [Integrability of conditional expectation](theorems/integrability-of-conditional-expectation.md)
- [Conditional expectation set-integral identity](theorems/conditional-expectation-set-integral-identity.md)
- [Uniqueness of conditional expectation](theorems/uniqueness-of-conditional-expectation.md)
- [Law of total expectation](theorems/law-of-total-expectation.md)
- [Tower property of conditional expectation](theorems/tower-property-of-conditional-expectation.md)
- [Integral Jensen inequality](theorems/integral-jensen-inequality.md)

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `in-mathlib`.

Relevant declarations:

- `ProbabilityTheory.HasLaw`
- `ProbabilityTheory.iIndepFun`
- `ProbabilityTheory.iIndepFun.hasLaw_pi`
- `ProbabilityTheory.iIndepFun_iff_hasLaw_pi_pi`
- `ProbabilityTheory.iIndepFun_infinitePi`
- `ProbabilityTheory.exists_iid`
- `MeasureTheory.condExp`
- `MeasureTheory.Measure.rnDeriv`
- `MeasureTheory.integral`
- `ConvexOn.map_average_le`
- `ConvexOn.map_integral_le`
- `Convex.integral_mem`
- `MeasureTheory.average_eq_integral`

Primary file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. Laws and finite product laws are in Mathlib/Probability/HasLaw.lean, independence and infinite products under Mathlib/Probability/Independence, and an explicit iid realization in Mathlib/Probability/HasLawExists.lean. Conditional expectation is under MeasureTheory/Function/ConditionalExpectation, the Radon-Nikodym derivative under MeasureTheory/Measure/Decomposition/Lebesgue, and Bochner integration under MeasureTheory/Integral/Bochner. Integral Jensen and its finite-measure average variant are in Mathlib/Analysis/Convex/Integral.lean; the probability-measure theorem retains closed-domain, continuity, almost-everywhere membership, and Bochner integrability hypotheses. Fine statements must retain the integrability and sigma-algebra hypotheses of condExp and the ENNReal-valued almost-everywhere semantics of rnDeriv.
