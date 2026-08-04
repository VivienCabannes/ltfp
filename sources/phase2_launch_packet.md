# Phase 2 Launch Packet

## Gate State

Phase 2 was authorized on August 4, 2026 after both gates passed:

1. the user approved the 116-cluster Phase 1 roadmap; and
2. the user approved the pinned-primary-source policy for cited external
   results.

The durable decision record is `sources/phase2_approval.json`. It binds the
authorization to the attested Phase 1 graph hash below. Phase 2 may split the
initial source-independent frontier immediately. An externally supported result
may enter the graph only after its primary source metadata and checksum are
pinned.

The tracked Phase 1 artifact is `sources/phase1_graph.json`, SHA-256
`cbf4e871f971fd9c590219073389a41e9977dcbe11ebf2111fca1fd6eadd2758`.
It has 116 tier-1 clusters, 461 dependency edges, four dependency-free
Mathlib roots, and complete ownership for all 209 exercises.

At authorization time no tier-2 node, Lean declaration, prover worker, or Lean
proof jury existed.
The local backend resolves to Codex, and `lake env lean` passes from the project
root. These checks establish readiness only; they do not authorize dispatch.

## Initial Frontier

The first four clusters are the exact dependency-free frontier:

1. `Finite-dimensional linear algebra and spectral theory`
2. `Differential and integral calculus`
3. `Measure-theoretic probability and conditional expectation`
4. `Convex analysis and normed-space geometry`

Launch their splitters as the first Phase 2 wave, but apply these ownership
rules before merging any result:

- `Bochner integral` has one tier-2 owner under `Differential and integral
  calculus`. Probability nodes use it through cross-cluster dependencies; they
  do not create a second integral node.
- The generic orthogonal projection onto a closed subspace has one tier-2 owner
  under `Convex analysis and normed-space geometry`. A genuinely
  finite-dimensional specialization may be separate, but it must depend on the
  generic node and must not duplicate it.
- `HasFTaylorSeriesUpTo` is a derivative-jet interface, not a Taylor expansion.
  Taylor nodes use the actual expansion or remainder declarations recorded in
  the graph.
- A Hessian node uses `iteratedFDeriv` at order two or proves an explicit bridge;
  it must not claim that Mathlib has a standalone Hessian API.
- Singular values do not imply that Mathlib supplies a complete SVD or
  singular-vector factorization.
- Conditional expectation, Radon-Nikodym, and integral nodes retain their exact
  measurability, integrability, sigma-algebra, almost-everywhere, and codomain
  hypotheses.

Owner results are merged before dependent results. All graph changes go through
Autoform's `merge_node.py`; unresolved cross-cluster references are never
silently discarded.

## First Acceptance Checkpoint

As soon as the calculus, probability, and convex roots are merged and reviewed,
split `Elementary probability and convexity bounds`. This is the first cluster
with substantive book mathematics. It contains the foundations for later
concentration arguments and Exercises 1.9-1.11.

Likely fine statement families include:

- independent-sum and sample-mean variance;
- mean-square convergence and a finite convergence-in-probability bound;
- the scalar iid central limit theorem;
- the pointwise indicator lemma, Markov inequality, and Chebyshev inequality;
- countable-union and carefully bounded supremum-tail forms;
- Chernoff bounds;
- the nonnegative layer-cake identity; and
- real and integral Jensen inequalities.

The splitter must make positivity of sample size, measurability, `MemLp`, and
integrability assumptions explicit. It must preserve strict versus non-strict
tail events, avoid unrestricted real suprema for empty or unbounded families,
and record both book and supplement provenance for Exercises 1.9-1.11.

The five clusters above form the first acceptance checkpoint. This is a review
checkpoint, not a scheduling barrier: other dependency-ready clusters continue
through the pool when reviewer capacity is available.

## Next Ready Set

After all four roots are split, exactly eleven tier-1 clusters are topologically
ready:

- `Matrix algebra and Gaussian conditioning`
- `Spectral and differential matrix tools`
- `Elementary probability and convexity bounds`
- `Deterministic quadrature error`
- `Supervised learning setup and evaluation`
- `Metric and measure-theoretic geometry`
- `Convex smoothness and duality foundations`
- `Fourier analysis and Sobolev approximation`
- `Hilbert-space covariance operators and probability`
- `Signed measures and variation norms`
- `Ordinary differential equations and gradient flows`

The ODE/gradient-flow cluster is topologically ready but not source-ready. Its
non-Mathlib invariance and flow interfaces remain deferred until the selected
external-source policy has been applied and any accepted source is pinned by
edition or commit, URL, retrieval date, and checksum. Coarse edges are not
copied mechanically to every fine child; each tier-2 edge must be justified by
the child's statement or proof.

## Per-Cluster Gate

Every cluster follows the same durable sequence:

1. A canonical splitter reads the exact source passages and writes one fine node
   per definition or mathematical statement.
2. The orchestrator merges structural records through `merge_node.py` only.
3. A fresh Mathlib checker verifies every fine node against the pinned checkout.
4. Content and graph reviewers run in parallel and iterate to convergence.
5. Structural, acyclicity, grounding, content-path, and exercise checks pass.
6. The blueprint is refreshed and the cluster remains reviewable from its exact
   source and Mathlib provenance.

Checkpoint acceptance additionally requires no null content among its tier-2
children, no orphan prose file, no duplicate concept ownership, and no missing
exercise obligation. When an exercise-bearing cluster is split, the coverage
matrix must gain exact fine-node links while retaining the Phase 1 coarse
mapping as an audit trail.

The deterministic incremental and final commands for exercise traceability,
prose shape, and tier re-projection are specified in
`sources/phase2_acceptance_contract.md`.

## External-Source Policy

The initial five-cluster checkpoint does not need any item in
`sources/external_sources_needed.md`; the scalar central limit theorem it uses
already exists in pinned Mathlib. The global policy is still required before
Phase 2 because later clusters depend on cited results that the book does not
prove at the required generality.

Under the recommended policy, the project may use the book's cited primary
sources. Each source is added to the authoritative manifest before its result is
split, and the fine node records the exact hypotheses and any difference from
the book. No cited result is treated as an axiom.
