# External Proof Source Gate

The book cites, sketches, or conditionally states several results that are not
proved at the generality required by its later arguments. Pinned Mathlib does
not close these gaps. Phase 2 must not silently treat them as axioms or as
book-proved facts.

The user authorized the pinned-primary-source policy on August 4, 2026; see
`sources/phase2_approval.json`. No external proof source has yet been added to
the authoritative source manifest. Each accepted source must be pinned by
edition or commit, URL, retrieval date, and checksum before its results enter
the statement-level graph.

| Obligation | Book use | Required Phase-2 handling |
| --- | --- | --- |
| Stone's nearest-neighbor lemma | Chapter 6 universal consistency | Add a primary proof source or develop and independently review a complete proof. |
| Arbitrarily slow universal convergence | Proposition 2.3 | Add the cited Devroye et al. theorem at the exact generality used. |
| Multivariate CLT and M-estimation expansion | Asymptotic empirical-risk analysis | Add a proof source and make differentiability, moments, identifiability, and nonsingularity explicit. |
| Density of Lipschitz functions in `L2` | Chapter 6 universal consistency | Add the exact approximation theorem; bounded-continuous density alone is insufficient. |
| Bochner/Mercer and sparse-estimation gaps | Chapters 7-9 | Source the partially proved Bochner result, Proposition 8.5, neural variation-space completeness, and cited Sobolev estimates as separate obligations. |
| Inverse-Wishart expectations | Chapters 10 and 12 | Add a proof source with the correct finite-moment dimension regimes. |
| ODE invariance and Wasserstein flows | Chapters 11-12 | Source the flow, invariance, continuity-equation, and convergence interfaces not supplied by basic Mathlib ODE existence. |
| Maximum-margin implicit bias | Chapter 12 | Add the cited logistic-loss result; the book proves only a modified exponential-loss case. |
| Mean-field and lazy/NTK limits | Chapter 12 | Keep the book's conditional claims conditional and source any stronger convergence or linearization theorem. |
| Donsker-Varadhan and sparse PAC-Bayes | Chapter 14 | Add a proof of the variational formula and the cited sparse-regression specialization. |
| Continuous data processing and Fano | Chapter 15 | Add exact measure-theoretic versions used by the minimax reductions. |
| Deterministic optimization hard chains | Chapter 15 | Add proof-bearing sources for the smooth and strongly-convex lower-bound constructions left to cited texts. |

The posterior-computation, Laplace/BIC, ARD, Gaussian-process, and modern-neural
survey passages will remain definition-level unless the scope is explicitly
expanded to include external convergence or approximation theorems.
