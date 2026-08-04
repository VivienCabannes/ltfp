# Exercise Collection Audit

The December 1, 2025 exercise collection was checked visually against the
May 26, 2025 book. For Chapters 1-9, both sources contain the same 155 exercise
identifiers and the supplement has no additional exercise ID. The main book
contains another 54 embedded exercises in Chapters 10-15; the supplement ends
with Chapter 9 and contains none of those identifiers or solutions. Thus the
main book has 209 exercise identifiers in total, while the supplement has 155.

| Chapter | Exercise IDs | Count | Supplement pages | Main-book pages |
| --- | --- | ---: | ---: | ---: |
| 1 | 1.1-1.29 | 29 | 1-4 | 6-20 |
| 2 | 2.1-2.8 | 8 | 5-8 | 30-32 |
| 3 | 3.1-3.10 | 10 | 9-12 | 51-67 |
| 4 | 4.1-4.16 | 16 | 13-17 | 81-102 |
| 5 | 5.1-5.36 | 36 | 19-25 | 115-152 |
| 6 | 6.1-6.6 | 6 | 27-28 | 161-178 |
| 7 | 7.1-7.23 | 23 | 29-35 | 185-209 |
| 8 | 8.1-8.17 | 17 | 37-39 | 225-245 |
| 9 | 9.1-9.10 | 10 | 41-42 | 255-275 |

All Chapter 1-9 obligations are semantically represented in the tier-1 graph's
`provisional_members`, and all 170 representing links carry their exact exercise
identifiers. The 58 exercises in Chapters 4-6 map to 73 descriptive member links
because eleven multipart exercises are deliberately decomposed. The exact
mapping for all chapters is tracked in `sources/exercise_coverage.json` and
checked against `graph.json` by `scripts/check_exercise_coverage.py`.

## Embedded Exercises in Chapters 10-15

The main-book inventory below was checked against the exercise headings in the
book text and the rendered PDF. The supplement's final page is Chapter 9,
printed page 42 (PDF page 44), so every identifier in this section is book-only.
There is no supplement wording or answer with which these statements could
conflict.

| Chapter | Exercise IDs | Count | Main-book printed pages | Supplement presence |
| --- | --- | ---: | ---: | --- |
| 10 | 10.1-10.9 | 9 | 286-308 | Absent |
| 11 | 11.1-11.8 | 8 | 318-334 | Absent |
| 12 | 12.1-12.9 | 9 | 351-375 | Absent |
| 13 | 13.1-13.10 | 10 | 382-403 | Absent |
| 14 | 14.1-14.13 | 13 | 411-418 | Absent |
| 15 | 15.1-15.5 | 5 | 437-449 | Absent |
| **Total** | **10.1-15.5** | **54** | | **All absent** |

### One-to-One Tier-1 Reconciliation

`Book only` means that the statement occurs in the main book and has no entry
in the exercise supplement. Member names are copied from the current tier-1
graph. Where an exercise has several parts, multiple members in the same owner
cluster are listed together.

| Exercise | Main-book obligation | Tier-1 owner and representing member(s) | Sources |
| --- | --- | --- | --- |
| 10.1 | Distributed multicategory nearest-neighbor risk and optimal replication count | `Averaging and bagging of predictors`: `Distributed nearest-neighbor rate (Exercise 10.1)` | Book only |
| 10.2 | Computation for ridge regression split across `m` chunks | `Averaging and bagging of predictors`: `Replicated ridge-regression rate (Exercise 10.2)` | Book only |
| 10.3 | Exponential majority-vote error bound for independent classifiers | `Averaging and bagging of predictors`: `Independent majority-vote error bound (Exercise 10.3)` | Book only |
| 10.4 | Expected distinct fraction in a bootstrap sample | `Averaging and bagging of predictors`: `Bootstrap and subsampling bagging (Exercise 10.4)` | Book only |
| 10.5 | Moments and risk bound for coordinate-sampling sketches | `Randomized least-squares compression and embeddings`: `Coordinate-sampling sketch moments (Exercise 10.5)` | Book only |
| 10.6 | Efficient weak-learner optimization for coordinatewise linear stumps | `Atomic geometry and classical boosting`: `Weak-learner oracle (Exercise 10.6)` | Book only |
| 10.7 | Orthogonal matching-pursuit approximation rate | `Atomic geometry and classical boosting`: `Orthogonal matching-pursuit approximation rate (Exercise 10.7)` | Book only |
| 10.8 | Improved quadratic-objective gradient-boosting rate | `Gradient boosting convergence and early stopping`: `Gradient-boosting convergence theorem (Exercise 10.8)` | Book only |
| 10.9 | Rademacher bound for metric-distance features | `Gradient boosting convergence and early stopping`: `Rademacher complexity of variation balls (Exercise 10.9)` | Book only |
| 11.1 | Regret for unconstrained online gradient descent on smooth convex losses | `Online convex regret with projected gradients`: `Convex online-regret theorem (Exercise 11.1)` | Book only |
| 11.2 | Stochastic mirror descent with an `l1` comparison norm | `Mirror descent geometry`: `Stochastic mirror descent for l1 regularization (Exercise 11.2)` | Book only |
| 11.3 | Upper and lower weighted-regret bounds | `Online minimax regret lower bounds`: `Weighted-regret upper and lower bounds (Exercise 11.3)` | Book only |
| 11.4 | Sixth Gaussian norm moment and weighted covariance moment | `Gaussian zeroth-order optimization and smoothing`: `Gaussian moment bounds (Exercise 11.4)` | Book only |
| 11.5 | Poincare improvement of the Gaussian gradient-estimator variance | `Gaussian zeroth-order optimization and smoothing`: `Gradient-estimator second moment (Exercise 11.5)` | Book only |
| 11.6 | Optimal smoothing and step sizes with two function evaluations | `Gaussian zeroth-order optimization and smoothing`: `Smooth zeroth-order convergence (Exercise 11.6)` | Book only |
| 11.7 | Linear-regret lower bound for pure exploitation | `Stochastic multiarmed bandits`: `Pure-exploitation linear-regret lower bound (Exercise 11.7)` | Book only |
| 11.8 | Gap-free explore-then-commit tuning with `m = t^(2/3)` | `Stochastic multiarmed bandits`: `Gap-free explore-then-commit bound (Exercise 11.8)` | Book only |
| 12.1 | Single-pass stochastic hinge optimization for separable data | `Maximum-margin implicit bias and perceptron dynamics`: `Stochastic hinge optimization (Exercise 12.1)` | Book only |
| 12.2 | Perceptron mistake bound | `Maximum-margin implicit bias and perceptron dynamics`: `Perceptron mistake bound (Exercise 12.2)` | Book only |
| 12.3 | Bregman Pythagorean identity and interpolation bias | `Bregman and multiplicative implicit bias`: `Bregman Pythagorean identity (Exercise 12.3)` | Book only |
| 12.4 | Discrete mirror-descent interpolation bias | `Bregman and multiplicative implicit bias`: `Discrete mirror-descent implicit bias (Exercise 12.4)` | Book only |
| 12.5 | U-shaped overparameterized Gaussian risk and its minimizer | `Gaussian linear double descent`: `Overparameterized risk minimizer (Exercise 12.5)` | Book only |
| 12.6 | Almost-sure weak convergence of empirical measures | `Weak convergence and Wasserstein gradient flows`: `Empirical-measure convergence (Exercise 12.6)` | Book only |
| 12.7 | Rank preservation along a factorized PSD flow | `Positive-semidefinite factor flows and matrix sensing`: `Rank preservation (Exercise 12.7)` | Book only |
| 12.8 | Local minima of the factorized objective are global | `Positive-semidefinite factor flows and matrix sensing`: `Local minima are global (Exercise 12.8)` | Book only |
| 12.9 | Commuting matrix-sensing mirror flow and small-initialization nuclear-norm bias | `Positive-semidefinite factor flows and matrix sensing`: `Matrix-sensing mirror flow (Exercise 12.9)`; `Nuclear-norm implicit bias (Exercise 12.9)` | Book only |
| 13.1 | Majority-class condition for multicategory hinge consistency | `Multicategory convex surrogates`: `Majority-class Fisher consistency of the multicategory hinge (Exercise 13.1)` | Book only |
| 13.2 | One-versus-all surrogate ordering | `Multicategory convex surrogates`: `One-versus-all surrogate analysis (Exercise 13.2)` | Book only |
| 13.3 | Pairwise surrogate ordering | `Multicategory convex surrogates`: `Pairwise surrogate analysis (Exercise 13.3)` | Book only |
| 13.4 | Trace-norm mirror map and stochastic mirror-descent rate | `Vector-valued learning bounds`: `Mirror descent with trace-norm penalty (Exercise 13.4)` | Book only |
| 13.5 | Rademacher bound for multicategory neural networks | `Vector-valued learning bounds`: `Neural multicategory bound (Exercise 13.5)` | Book only |
| 13.6 | Softmax calibration function | `Smooth structured surrogates`: `Softmax calibration function (Exercise 13.6)` | Book only |
| 13.7 | Componentwise binary-logistic calibration reduction | `Smooth structured surrogates`: `Reduction to binary calibration problems (Exercise 13.7)` | Book only |
| 13.8 | Binary max-min calibration | `Nonsmooth structured surrogates`: `Binary max-min specialization (Exercise 13.8)` | Book only |
| 13.9 | Closed multicategory max-min surrogate | `Nonsmooth structured surrogates`: `Multicategory max-min formulation (Exercise 13.9)` | Book only |
| 13.10 | Generalization bound for an alternative smooth surrogate | `Structured surrogate generalization`: `Alternative smooth surrogate bound (Exercise 13.10)` | Book only |
| 14.1 | Convex reparameterization of the Gaussian negative log-density | `Likelihood-loss and MAP-regularization correspondences`: `Gaussian negative log-density (Exercise 14.1)` | Book only |
| 14.2 | Variance of a Laplace random variable | `Likelihood-loss and MAP-regularization correspondences`: `Laplace variance (Exercise 14.2)` | Book only |
| 14.3 | Gaussian-inverse-Gamma mixture and Student marginal | `Likelihood-loss and MAP-regularization correspondences`: `Gaussian-inverse-Gamma mixture gives a Student prior (Exercise 14.3)` | Book only |
| 14.4 | Gaussian scale mixtures are super-Gaussian | `Hierarchical sparse priors`: `Scale mixtures are super-Gaussian (Exercise 14.4)` | Book only |
| 14.5 | Posterior covariance differential identity | `Posterior mean and posterior mode`: `Posterior covariance differential identity (Exercise 14.5)` | Book only |
| 14.6 | Poisson and geometric posterior-mean identities | `Posterior mean and posterior mode`: `Poisson and geometric posterior-mean identities (Exercise 14.6)` | Book only |
| 14.7 | MMSE estimator represented as MAP under a transformed prior | `Posterior mean and posterior mode`: `MMSE as MAP for a transformed prior (Exercise 14.7)` | Book only |
| 14.8 | Spike-and-slab marginal, MMSE, and MAP estimators | `Posterior mean and posterior mode`: `Spike-and-slab posterior estimator (Exercise 14.8)` | Book only |
| 14.9 | Laplace-prior marginal, MMSE, and MAP estimators | `Posterior mean and posterior mode`: `Laplace-prior posterior estimator (Exercise 14.9)`; `Marginal-density calculations (Exercises 14.9 and 14.11)` | Book only |
| 14.10 | Gaussian-prior covariance-form MMSE and MAP | `Posterior mean and posterior mode`: `Gaussian covariance MMSE and MAP (Exercise 14.10)` | Book only |
| 14.11 | Student-prior marginal density | `Posterior mean and posterior mode`: `Marginal-density calculations (Exercises 14.9 and 14.11)` | Book only |
| 14.12 | Maximum-likelihood LDA parameters | `Generative classification models`: `Maximum-likelihood LDA parameters (Exercise 14.12)` | Book only |
| 14.13 | Quadratic discriminant analysis as quadratic softmax scores | `Generative classification models`: `Quadratic discriminant analysis (Exercise 14.13)` | Book only |
| 15.1 | Euclidean-ball packing lower bound for fixed-design regression | `Regression minimax lower bounds`: `Euclidean-ball packing lower bound (Exercise 15.1)` | Book only |
| 15.2 | First-order-oracle lower bound for differentiable Lipschitz objectives | `Derivative-free nonconvex lower bounds`: `First-order-oracle extension for differentiable Lipschitz objectives (Exercise 15.2)` | Book only |
| 15.3 | Random-query covering lower bound | `Derivative-free nonconvex lower bounds`: `Random-query covering lower bound (Exercise 15.3)` | Book only |
| 15.4 | Zeroth-order lower bound for gradient-Lipschitz objectives | `Derivative-free nonconvex lower bounds`: `Gradient-Lipschitz zeroth-order lower bound (Exercise 15.4)` | Book only |
| 15.5 | Quadratic stochastic-gradient generalization lower bound | `Stochastic first-order lower bounds`: `Quadratic stochastic-gradient lower bound (Exercise 15.5)` | Book only |

### Reconciliation Result

- No exercise identifier is absent from the graph at the tier-1 cluster level.
- Every exercise has one unambiguous tier-1 owner. Multi-part Exercises 12.9
  and 14.9 intentionally map to two members within one owner cluster.
- The machine-readable matrix contains the exact ordered 209-identifier set,
  records book/supplement presence, and validates all 225 current owner/member
  links. Every mapped member carries its exact exercise identifier(s), including
  every member of a multipart exercise and both links used for Exercise 14.9;
  the checker also rejects graph markers that have no matrix entry.
- Coverage-source identities match `sources/manifest.json`; when the two local
  PDFs are present, the checker verifies their recorded SHA-256 digests.
- Exercise 11.7 received a dedicated pure-exploitation lower-bound member during
  this audit. Exercise 12.6 is owned only by the reusable weak-convergence cluster;
  the duplicate mean-field member was removed.

### Embedded-Source Defects and Clarifications

There are no unresolved `??` references in the Chapter 10-15 exercise statements.
Because the supplement has no corresponding entries, there are no book-supplement
statement or answer conflicts. The following defects are internal to the main book or
to context required by an exercise:

| Exercise or context | Issue | Canonical handling |
| --- | --- | --- |
| 11.6 | The exercise optimizes the parameters in Proposition 11.4, whose statement permits every positive step size although its proof needs `gamma <= 1 / (24 * d * L)`. | Carry the proof-required step-size restriction into the exercise statement. |
| 12.2 | The perceptron iteration starts at arbitrary `theta_0`, but the stated `(rho * R)^2` bound omits initialization dependence. | Require `theta_0 = 0`, or add an initialization-dependent term. |
| 12.5 | The exercise says only `d > n`, while the inverse-Wishart expected-risk formula is finite only beyond the interpolation boundary. | State the finite-moment regime `d > n + 1` and handle boundary dimensions separately. |
| 13.4-13.5 context | The surrounding text uses Euclidean Lipschitz constant `1` for multiclass softmax; the direct constant is generally `sqrt 2`. | Propagate `sqrt 2` into any softmax-specialized exercise rate. |
| 14.1 | The displayed Gaussian negative log-density contains `(x - mu)^2` although its observation variable is `y`. | Replace `x` by `y`; the rendered PDF confirms this is a source typo, not extraction noise. |
| 14.5-14.7 context | The empirical-Bayes paragraph says `y | theta` is Gaussian with mean zero, contradicting the additive model `y = theta + epsilon`. | Use conditional mean `theta` throughout. |
| 15.2-15.4 context | The lower-bound construction says the hidden point is at distance "at most" the covering radius from every query, but the construction needs it at distance at least that radius. | Reverse the inequality in the reused covering argument. |
| 15.3 | Part (c) switches from the domain `Theta` to `diam(X)`. | Read this as `diam(Theta)`. |
| 15.5 context | Section 15.3 introduces `D` as a ball radius and later calls it the diameter when stating the lower bound. | Choose one normalization explicitly; for radius `D`, the diameter is `2 * D`. |

### Applied Graph Corrections

1. Added `Pure-exploitation linear-regret lower bound (Exercise 11.7)` to
   `Stochastic multiarmed bandits`.
2. Retained Exercise 12.6 as `Empirical-measure convergence (Exercise 12.6)` in
   `Weak convergence and Wasserstein gradient flows` and removed the duplicate
   mean-field member. The mean-field cluster already depends on that reusable
   support cluster.

## Material Statement Conflicts

| Exercise | Difference | Canonical statement |
| --- | --- | --- |
| 1.12 | The supplement changes the Gaussian lower-tail constant from `1/4` to `1/2`. At `t = 1`, the supplement lower bound is about `0.1839`, above the actual tail probability of about `0.1587`. | Retain the main-book bound `1/4 * exp(-t^2) <= P(X >= t) <= exp(-t^2 / 2)`. |
| 1.17 | The supplement weakens `2 * q! * (2 * tau^2)^q` to `(2q) * q! * (2 * tau^2)^q`. | Retain the sharper main-book bound, which follows directly by tail integration. |
| 4.13 | The supplement extends `p in (1,2]` to every `p > 1`. For `n = d = 1`, its bound is too small when `p > 2`. | Retain `p in (1,2]` and `R * D / (sqrt n * sqrt(p - 1))`. |
| 5.1 | The supplement changes the quadratic-descent exponent from `2t` to `t`, while its solution still derives `2t`. | Retain the main-book and solution exponent `2t`. |
| 5.7 | The supplement drops convexity. The concave quadratic `F(x) = -mu*x^2/2` disproves the resulting statement. | Retain the main book's differentiable-convex hypothesis. |
| 6.4 | The supplement changes `C_h <= 2 * vol(X)` to `C_h <= vol(X)/2`. Approximate-identity convergence gives `C_h -> vol(X)`. | Retain the main-book constant `2 * vol(X)` for sufficiently small explicit `h`. |

## Statement Splits Exposed by Solutions

- Exercises 2.2-2.4: separate density-free median and quantile
  characterizations from proofs requiring conditional densities and
  differentiation.
- Exercises 3.2-3.3: separate full-column-rank, projector-trace, and
  covariance-to-risk lemmas.
- Exercises 3.5-3.6: separate Woodbury algebra from homoscedastic ridge
  bias-variance analysis.
- Exercises 4.12 and 4.14: expose dual-norm, sub-Gaussian maximum,
  symmetrization, and contraction prerequisites.
- Exercise 6.1: separate row-sparse nonsymmetric nearest-neighbor matrices from
  permutation-block-diagonal partition matrices.
- Exercise 6.3: isolate the reduction from classification consistency to
  squared-integrable regression consistency.
- Exercises 7.2-7.3: separate kernel closure from multinomial feature and
  stars-and-bars dimension results.
- Exercise 7.11: separate dual derivation from the shared-nonzero-spectrum
  condition-number comparison.
- Exercise 7.13: convexity is needed for duality but not for the centered-span
  representer result.
- Exercises 8.2 and 8.6: expose the constrained least-squares basic inequality
  and the Lasso KKT/subgradient criterion.
- Exercise 9.1: expose Holder duality and the maximum-of-sub-Gaussians bound.

## Supplement Defects

The solution to Exercise 2.1 on supplement page 5 attaches `c_-` and `c_+` to
the wrong predicted labels in its displayed conditional risks. Its final
threshold is nevertheless correct.

Forty statements retain unresolved `??` references:

`3.5, 3.7, 3.8; 4.6, 4.7, 4.15, 4.16; 5.2, 5.3, 5.8, 5.12, 5.14,
5.15, 5.17, 5.21, 5.25-5.28, 5.32, 5.34, 5.35; 6.2; 7.12, 7.13,
7.15, 7.23; 8.1-8.3, 8.6, 8.8-8.11; 9.1, 9.5-9.7, 9.10`.

These broken references obscure dependencies but introduce no new mathematical
obligation. Phase-2 splitters must reconstruct each dependency from the proof.
