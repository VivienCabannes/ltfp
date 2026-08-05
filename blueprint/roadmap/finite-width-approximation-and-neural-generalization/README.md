---
kind: roadmap
status: mapped
---

# Finite-width approximation and neural generalization

Finite-neuron approximation from bounded variation norm and structure-adaptive risk bounds combining approximation and estimation.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Variation spaces and neural approximation](../variation-spaces-and-neural-approximation/README.md)
- [Shallow ReLU models and norm-controlled estimation](../shallow-relu-models-and-norm-controlled-estimation/README.md)
- [Lipschitz kernel learning and smoothness adaptation](../lipschitz-kernel-learning-and-smoothness-adaptation/README.md)
- [Slow Lasso rates](../slow-lasso-rates/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Proximal, projected, and composite gradient methods](../proximal-projected-and-composite-gradient-methods/README.md)

## Candidate contents

- Hilbert-space Frank-Wolfe algorithm
- Frank-Wolfe one-over-time convergence
- Uniform averaging (Exercise 9.5)
- Frank-Wolfe line search (Exercise 9.6)
- Finite-neuron approximation bound
- Neural-network fitting by Frank-Wolfe
- Arbitrary activations (Exercise 9.7)
- Combined neural estimation-approximation bound
- Finite-width order-n sufficiency
- Lipschitz-target rate
- Latent-subspace rate
- Teacher-network rate
- Additive ridge-function rate (Exercise 9.8)
- Nonlinear variable selection and logarithmic dimension dependence

## Sources

- `sources/ltfp_book.pdf` — Chapter 9, Sections 9.3.6-9.4, printed pages 266-271

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: generic Hilbert-space convexity, smoothness, and finite-sum APIs are available, but they do not instantiate a listed algorithm or approximation theorem. Searches for Frank-Wolfe or conditional-gradient methods, Maurey-type averaging, finite-neuron approximation, teacher networks, and neural generalization rates found no relevant declaration. Materially uncovered members: Hilbert-space Frank-Wolfe algorithm; Frank-Wolfe one-over-time convergence; Uniform averaging (Exercise 9.5); Frank-Wolfe line search (Exercise 9.6); Finite-neuron approximation bound; Neural-network fitting by Frank-Wolfe; Arbitrary activations (Exercise 9.7); Combined neural estimation-approximation bound; Finite-width order-n sufficiency; Lipschitz-target rate; Latent-subspace rate; Teacher-network rate; Additive ridge-function rate (Exercise 9.8); Nonlinear variable selection and logarithmic dimension dependence.
