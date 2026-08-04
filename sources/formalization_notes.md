# Source Formalization Notes

These notes record source details that must be resolved explicitly when the
corresponding tier-2 statements are written. Page numbers are printed page
numbers in the May 26, 2025 PDF.

## Global conventions

- Chapter 2 deliberately suppresses measurability conditions. Formal statements
  about learned predictors, conditional laws, Bayes predictors, and argmin rules
  must restore the required measurable-space and measurable-selection hypotheses.
- Proposition 1.7 and Proposition 3.11 are the same matrix Bernstein result in
  different notation. The detailed graph should share one theorem node.

## Visually checked details

- Page 61: the prose after equation (3.7) appears to contain an extra
  `- sigma^2`. The derivation on page 62 uses the excess-risk expression that
  yields the stated lower bound. Treat this as a candidate erratum pending an
  independent faithfulness review.
- Page 65, equation (3.10): the relation is the Loewner lower bound
  `Sigma^(-1/2) * SigmaHat * Sigma^(-1/2) >= (1/4) I`. Text extraction loses the
  positive-semidefinite order symbol.
- Page 117: the book defines its displayed matrix-order symbol semantically by
  positivity of `A - B`. Preserve that semantic definition rather than inferring
  direction from the extracted glyph.
- Page 122: the extracted token `aa` near the smooth strongly convex gradient
  descent proposition is not present in the rendered source.
- Page 141: the blended stochastic-gradient step size is
  `1 / (B^2 * sqrt(t) + mu * t)`.
- Page 172: the Nadaraya-Watson theorem prints `q : R^d -> R`, while its setup and
  proof use a nonnegative kernel or density. The tier-2 statement must resolve
  the missing nonnegativity hypothesis rather than silently strengthening it.
- Exercise 1.24 permits zero weights while its penalty uses
  `Real.log (1 / pi_i)`. Require strictly positive weights, or model the zero
  case with an extended-real infinite penalty; ordinary real logarithms do not
  encode the intended convention.

### Chapters 7-9

- Definition 7.1 uses "positive-definite" for kernels whose finite Gram matrices
  are positive semidefinite. Use the semantic Gram-matrix condition in Lean.
- Page 218 appears to print `d/2 < s <= t`; the surrounding argument instead
  needs `s >= t` and `s <= d/2 + t`. Recheck this against the proof when the
  Sobolev statement is split.
- Lemma 7.2 extends an identity to a closure by an unstated limiting argument.
  The formal proof must supply continuity and density hypotheses explicitly.
- The Bochner theorem discussion is only a partial proof, and Proposition 8.5 is
  stated without proof. These need independent sources or separately reviewed
  proofs.
- Completeness of the neural variation space `F1` is asserted rather than
  proved. Track it as its own obligation, not as a definition-level fact.
- The sharper Sobolev exponent for `gamma2` is cited rather than derived.

### Chapters 10-12

- Section 10.2.1 starts with `s > d`, but the inverse-Wishart expectation and
  denominator `s - d - 1` require `s > d + 1`.
- Page 292 indexes projection replicas by `j in {1,...,n}` although the average
  has `m` replicas; `{1,...,m}` is evidently intended.
- Proposition 11.2's displayed bound omits `B^2`; its prose and proof include
  `B^2 * (1 + log t) / (2 * mu * t)`.
- Proposition 11.3 assumes a conditional squared dual-norm bound by `B` but its
  conclusion and optimization use `B^2`. Resolve the normalization explicitly.
- Proposition 11.4 allows every positive step size, while its proof requires
  `gamma <= 1 / (24 * d * L)`.
- The text says "Thomson sampling" where the standard name is "Thompson
  sampling".
- The adversarial-bandit section mixes reward maximization and a positive-sign
  Hedge update with a minimization-form mirror-descent proposition. State and
  verify the loss/reward sign conversion.
- Exercise 12.2 needs `theta_0 = 0`, or an initialization-dependent correction
  to its iteration bound.
- Exercise 12.5 assumes only `d > n`, but the displayed inverse-Wishart
  expected-risk formula is finite only for `d > n + 1`; treat the boundary
  dimensions separately.
- Pages 361-362 print a positive cross term, while the following
  `Sigma * (I - Pi_S)` identity requires the cross term to be negative.
- Section 12.3.3 is titled "positive-definite matrices", but its domain and
  optimality conditions are positive semidefinite.
- Proposition 12.2 is explicitly informal and conditional on weak convergence;
  it does not establish existence of the limiting flow or a rate.
- Equation (12.26) indexes network arguments by `v_1,...,v_n` although the
  surrounding network has `m` neurons.

### Chapters 13-15

- Page 384 claims a unit Euclidean Lipschitz constant for multiclass softmax;
  the direct bound is generally `sqrt 2` under the stated norm.
- Page 396 prints `arg max` where the loss-decoding rule requires `arg min`.
- Page 397 conditions `E[psi(y) | y]`; the conditioning variable should be `x`.
- Page 414's MMSE criterion omits the expectation over the observation and
  noise. Restore the full probability space in the formal statement.
- Page 415 says `y | theta` has mean zero where the model requires mean `theta`.
- Exercise 14.1 writes `(x - mu)^2` in the Gaussian negative log-density even
  though the observation variable is `y`; replace `x` by `y`.
- Page 421's Laplace covariance is missing the minus sign needed because the
  expansion is around a maximizer of the log density.
- Page 425 alternates between `m` candidate models and `f_1,...,f_n`; use one
  cardinality consistently. Page 434 likewise switches between `m` and `M`.
- Page 439 puts a prior on `{-beta,beta}^n` in a `d`-dimensional construction;
  the support should have dimension `d`.
- Page 445 says a packing distance is "at most" where the argument needs "at
  least". Pages 447-449 also switch between radius and diameter conventions for
  `D`; formal statements must choose one normalization consistently.
- Exercise 15.3 switches from the domain `Theta` to `diam(X)` in part (c); read
  this as `diam(Theta)`.
- The conclusion repeats an estimation comparison in a paragraph contrasting
  estimation and optimization; verify the intended second term before encoding
  it.

## External-source gaps

- The nearest-neighbor universal-consistency argument cites Stone's lemma without
  proving it. A complete formalization needs either a source that proves the
  lemma or a separately reviewed proof development.
- The spectral theorem, singular-value decomposition, central limit theorem,
  inverse-Wishart expectation, and matrix concentration results are invoked as
  background in some chapters. Their exact Mathlib coverage must be checked at
  the pinned revision before treating them as roots.
- Section 14.3.1 surveys MCMC, variational inference, and Laplace approximation
  without developing their convergence or approximation theory. Phase 2 must
  either narrow these to definitions or add proof sources.
- Section 14.3 does not prove the Laplace posterior asymptotics or Bayesian
  information-criterion expansion it discusses.
- The sparse-regression specialization of the PAC-Bayes bound is delegated to
  Alquier-Lounici and Rigollet-Tsybakov; include a primary proof source before
  treating that performance claim as covered.
- The PAC-Bayes derivation also uses the Donsker-Varadhan variational formula
  without proving it. Formalize that formula from an appropriate source first.
- Section 15.2.1 leaves parts of the smooth and strongly-convex hard-chain
  construction to cited optimization texts. A complete lower-bound proof needs
  those sources or a separately reviewed development.
- Section 15.1.3 asserts continuous data-processing and Fano extensions without
  proof. Add an information-theory source for the exact versions used by the
  minimax reductions.
- Proposition 2.3, the arbitrary-slow-convergence no-free-lunch theorem, is
  quoted without proof from Devroye et al. (1996), Theorem 7.2. Include that
  source or supply an independently reviewed proof.
- The asymptotic empirical-risk discussion uses a multivariate central limit
  theorem and M-estimation expansion but gives only a heuristic justification.
  The pinned checkout supplies a scalar CLT, not this full argument.
- The universal-consistency proof needs density of Lipschitz functions in the
  relevant `L^2` space. Mathlib has density of bounded continuous functions,
  which does not by itself discharge the Lipschitz approximation step.
- The ODE existence, invariance, and gradient-flow infrastructure used in
  Chapters 11-12 is not established in the book. Mathlib has basic ODE
  existence and uniqueness, but the remaining interfaces need a proof source.
- Inverse-Wishart expectations used in Sections 10.2.1 and 12.2.3-12.2.4 are
  cited externally and absent from pinned Mathlib.
- The full logistic-loss maximum-margin convergence statement is deferred to
  external work; the book proves only a modified exponential-loss flow case.
- The Chapter 12 mean-field limit and lazy-training linearization rely on cited
  work or informal arguments. Do not promote them to unconditional convergence
  theorems without adding the missing sources and hypotheses.
- The separate exercise supplement ends at Chapter 9. Embedded exercises in
  Chapters 10-15 therefore have no supplied solution source.

## Exercise collection reconciliation

For Chapters 1-9, the supplement contains the same 155 exercise identifiers as
the main book and no supplement-only exercise. The main book has another 54
embedded exercises in Chapters 10-15, for 209 total; none of those later
exercises appears in the supplement. The complete mapping and solution-driven
statement splits are recorded in `sources/exercise_audit.md`.

- Exercise 1.12: retain the main book's Gaussian lower-tail constant `1/4`;
  the supplement's `1/2` is false at `t = 1`.
- Exercise 1.17: retain the main book's sharper moment factor `2 * q!`; the
  supplement introduces an unnecessary factor `q`.
- Exercise 4.13: retain `p in (1, 2]`; the supplement's extension to all
  `p > 1` is false already in one dimension.
- Exercise 5.1: retain exponent `2t`, which the supplement's own solution proves.
- Exercise 5.7: retain the main book's convexity assumption.
- Exercise 6.4: retain `C_h <= 2 * vol(X)`; the supplement's factor `1/2`
  contradicts approximate-identity convergence.
- The Exercise 2.1 supplement solution swaps the costs attached to its two
  displayed predicted-label risks, although its final decision threshold is
  correct.
