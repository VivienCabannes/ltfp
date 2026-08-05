---
kind: roadmap
status: mapped
---

# Maximum-margin implicit bias and perceptron dynamics

On separable data, logistic and exponential-loss dynamics select hard-margin separators, while hinge subgradients yield perceptron-style guarantees.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Minimum-norm interpolation by gradient methods](../minimum-norm-interpolation-by-gradient-methods/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Ordinary differential equations and gradient flows](../ordinary-differential-equations-and-gradient-flows/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)

## Candidate contents

- Maximum-margin classifier
- Hard-margin support-vector-machine dual
- Logistic-loss norm divergence
- Direction convergence to maximum margin
- Exponential-loss gradient flow
- Hinge-loss separator rate
- Stochastic hinge optimization (Exercise 12.1)
- Perceptron mistake bound (Exercise 12.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.1.2, printed pages 346-351

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no perceptron, maximum-margin implicit-bias, logistic or exponential-loss direction-convergence, hinge-separator-rate, or stochastic-hinge dynamics API. Convex, ODE, and subgradient foundations are reusable, but none of the eight classifier-dynamics members is directly covered.
