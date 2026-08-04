# Formalization Roadmap

## Objective

Formalize the mathematical content of *Learning Theory from First Principles*
as a reusable Lean/Mathlib development. Coverage includes all fifteen chapters,
every embedded exercise that states a mathematical obligation, the separate
exercise collection, and externally cited results needed to close proof gaps.

This is a large formalization. A realistic full-coverage schedule is measured in
person-years rather than weeks; the graph and milestone gates are designed so
useful, reviewable libraries land well before the final theorem is complete.

## Quality Contract

A milestone is complete only when:

- every declaration compiles on the pinned stable Lean and Mathlib versions;
- no completed file contains `sorry`, `admit`, or an unreviewed project axiom;
- definitions and theorem statements use Mathlib conventions and reusable
  generality rather than mirroring textbook notation mechanically;
- measurability, integrability, finite-moment, compactness, and selection
  hypotheses suppressed by the book are explicit;
- source divergences and corrected typographical errors are documented;
- public declarations have focused tests or downstream uses;
- independent faithfulness, proof-integrity, and code-quality reviews pass.

## Phase 0: Source and Toolchain Lock

Status: complete.

- Pin the official May 2025 book and December 2025 exercise collection by hash.
- Record publication and licensing metadata without committing the PDFs.
- Pin Lean 4.32.2 and Mathlib 4.32.2.
- Establish a clean `lake build` baseline and an Autoform dashboard.

## Phase 1: Coarse Dependency Map

Status: complete and user-approved on August 4, 2026. The approval is bound to
the attested Phase 1 graph in `sources/phase2_approval.json`.

1. Extract tier-1 clusters from chapters 1-15 and both exercise sources.
2. Record source ambiguities and results that the book cites without proof.
3. Audit every cluster against the pinned Mathlib checkout.
4. Ground every missing cluster through explicit dependencies to verified
   Mathlib roots.
5. Run dependency-correcting graph reviews to convergence.
6. Run at least three independent whole-graph reviews.
7. Export the tier-1 blueprint for scope approval.

The converged map has 116 clusters and 461 dependency edges. It is a single
connected acyclic graph, every node reaches a verified Mathlib root, all 209
book exercises have an owner, and two independent waves of three holistic
reviews found no remaining Phase-1 blocker. The tracked exercise matrix checks
all 209 exercises through 225 explicitly tagged owner/member links. The project
blueprint driver binds the interactive map to the full graph and content hashes,
then validates every node, edge, runtime asset, and local reference. The final
graph hash and review waves are recorded in
`sources/phase1_review_attestation.json`.

## Phase 2: Statement-Level Blueprint

Status: in progress; initial dependency-free frontier launched August 4, 2026.

Phase 2 was authorized on August 4, 2026 after approval of the coarse map and
the pinned-primary-source policy for the obligations listed in
`sources/external_sources_needed.md`.
The verified initial frontier, declaration-ownership rules, and first acceptance
checkpoint are recorded in `sources/phase2_launch_packet.md`.

Split each tier-1 cluster into one tier-2 node per definition, lemma, theorem,
algorithmic invariant, quantitative bound, or exercise obligation. Work in
topological order so each statement has stable prerequisites.

Each tier-2 node receives:

- a universal, Mathlib-aligned mathematical statement;
- a complete informal proof when Mathlib does not already provide one;
- exact source provenance and any deliberate divergence;
- verified Mathlib declarations or a precise missing-API assessment;
- explicit dependencies on other tier-2 statements.

Re-project the coarse graph from the detailed graph, review both structure and
content to convergence, then export the complete blueprint.

## Phase 3: Shared Lean Foundations

Build and upstream reusable plumbing before book-specific APIs:

1. finite-dimensional matrix, spectral, Gaussian, and covariance interfaces;
2. conditional probability, concentration, and information-theory lemmas;
3. convex analysis, smoothness, subgradients, mirror maps, and gradient flows;
4. statistical decision theory, risks, estimators, and measurable learning
   rules;
5. Hilbert-space covariance, RKHS, signed-measure, Fourier/Sobolev,
   weak-convergence, and Wasserstein interfaces.

Candidate results that belong in Mathlib are developed in isolated upstreamable
modules. Project-specific composition stays under the main namespace.

## Phase 4: Core Book

Formalize chapters 1-9 in dependency order:

1. mathematical preliminaries and concentration;
2. supervised-learning and decision-theory semantics;
3. ordinary and ridge least squares;
4. empirical-risk and Rademacher generalization bounds;
5. deterministic and stochastic optimization;
6. local averaging and universal consistency;
7. kernels and kernel ridge regression;
8. sparse estimation and Lasso rates;
9. shallow neural networks and variation spaces.

The chapter order is only a presentation order. Implementation follows the
dependency graph and may advance independent branches in parallel.

## Phase 5: Special Topics

Formalize chapters 10-15:

1. bagging, randomized compression, and boosting;
2. online optimization and stochastic/adversarial bandits;
3. implicit bias, double descent, mean-field limits, and neural tangent kernels;
4. multicategory and structured prediction;
5. likelihood, Bayesian inference, and PAC-Bayes;
6. statistical and optimization lower bounds.

Informal or conditional source claims, especially mean-field convergence, are
split into precise hypotheses and conclusions rather than strengthened silently.

## Phase 6: Exercise Closure

Treat the separate exercise collection as a coverage matrix against the theorem
graph. Every exercise is either:

- discharged by an existing theorem;
- promoted to its own statement and proof;
- recorded as computation or exposition with no formal proposition; or
- blocked on an explicitly named external result.

## Phase 7: Final Integration

- Remove obsolete compatibility layers and consolidate public APIs.
- Re-run source-faithfulness, proof-integrity, code-quality, and holistic review.
- Verify zero `sorry`, zero accidental axioms, and a clean full build.
- Generate the final blueprint, API documentation, and coverage report.
- Prepare suitable reusable components for upstream Mathlib review.

## Milestone Policy

Each milestone should be small enough to review and merge independently. The
durable graph, not a calendar estimate, determines readiness: a node is worked
only after its prerequisites are compiled or verified in Mathlib. Source scope
changes require an explicit graph revision and review rather than an informal
promise.
