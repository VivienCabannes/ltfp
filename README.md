# Learning Theory from First Principles in Lean

This project formalizes the mathematical content of Francis Bach's
*Learning Theory from First Principles* in Lean 4, including all fifteen
chapters, the embedded exercises, and the separate exercise collection.

The target is Mathlib-quality code: reusable definitions, theorem statements at
the right level of generality, explicit analytic and measurability hypotheses,
no project axioms, and no `sorry` in completed milestones.

## Status

Autoform Phase 1 is complete and approved. Phase 2 statement-level planning
started on August 4, 2026 under the pinned-primary-source policy recorded in
`sources/phase2_approval.json`. The live graph currently has 227 nodes and 661
edges. Seven dependency-ready clusters have passed Mathlib, graph, and content
review and are pinned in the content-complete scope: five
finite-dimensional linear-algebra statements, 12 calculus statements, 23
probability and conditional-expectation statements, and 22 convex-analysis and
normed-geometry statements, 21 metric and measure-geometry statements, 16
elementary probability and convexity statements, and 12 deterministic
quadrature statements. The fine graph is acyclic. Reclassifying integral Jensen
as a probability/expectation bridge also makes the represented tier-1 quotient
acyclic without deleting any fine dependency.

The converged tier-1 map has 116 clusters and 461 dependency edges in one
connected acyclic graph. Every cluster reaches a verified Mathlib root, all 209
book exercises have an owner, and all 225 representing links carry
machine-checked exercise identifiers. The Phase 2 registry tracks those 225
fine obligations explicitly. Six obligations covering Exercises 1.9-1.11 and
1.26-1.28 are mapped to reviewed tier-2 nodes; 219 remain pending. Two
independent holistic-review waves found no remaining coarse-map blocker; the
final graph and review record are pinned in `sources/phase1_review_attestation.json`.

The live graph is stored in `graph.json`. Source ambiguities that affect formal
statements are recorded in `sources/formalization_notes.md`; proof obligations
that require an external source decision are listed in
`sources/external_sources_needed.md`.

The pinned environment is:

- Lean `v4.32.2`
- Mathlib `v4.32.2` at commit
  `905b95818eb32af7874a58b427f50c1711a5e96c`
- Autoform `0.4.4` for planning and blueprint generation
- Blueprint Python `3.12.13`, uv `0.11.15`, and Graphviz `2.44.0` on Linux

Run the current checks with:

```bash
python3 scripts/check_plan.py --require-grounding --projection incremental
python3 scripts/check_phase2_approval.py
python3 scripts/check_exercise_coverage.py
python3 scripts/check_informal_content.py --mode incremental \
  --scope sources/phase2_content_scope.json
python3 scripts/check_lean_hygiene.py
lake exe mk_all --check
lake build
```

## Sources

- [Official book PDF](https://www.di.ens.fr/~fbach/ltfp_book.pdf), dated
  May 26, 2025
- [Official exercise collection](https://www.di.ens.fr/~fbach/ltfp_exercises.pdf),
  dated December 1, 2025
- [MIT Press edition](https://mitpress.mit.edu/9780262049443/learning-theory-from-first-principles/)

Exact checksums and retrieval metadata are in `sources/manifest.json`. The PDFs
are copyrighted and are intentionally ignored by Git; this repository licenses
only its original Lean and project material under Apache-2.0.

The official book has no appendix section in its table of contents. Its
preface, conclusions, embedded exercises, references needed by proofs, and the
separate exercise collection are nevertheless within the source audit.

## Planning

See `ROADMAP.md` for the staged formalization strategy and quality gates. The
Autoform review dashboard and generated blueprint provide the navigable view of
the dependency graph.

To regenerate the blueprint on Linux, first create its hash-locked local
toolchain, then export and build from `graph.json`:

```bash
python3 scripts/blueprint.py setup
python3 scripts/blueprint.py export
python3 scripts/blueprint.py build
python3 scripts/blueprint.py serve --port 8005
```

The server binds only to `127.0.0.1`. `refresh` runs setup, export, and build in
one command. `check` verifies full graph and content provenance, all nodes and
edges, the runtime-asset hashes, and the complete local-reference closure
without rebuilding. Tree promotion requires Linux `renameat2` exchange support
so a failed refresh cannot destroy the last validated generation.

## Repository Layout

- `LearningTheoryFromFirstPrinciples/`: Lean source files
- `graph.json`: durable Autoform dependency graph
- `sources/manifest.json`: authoritative source metadata
- `sources/formalization_notes.md`: source ambiguities and external proof gaps
- `sources/exercise_audit.md`: source reconciliation of all 209 exercises
- `sources/exercise_coverage.json`: machine-checked exercise-to-graph matrix
- `sources/phase1_graph.json`: immutable, hash-attested Phase 1 graph snapshot
- `sources/phase2_launch_packet.md`: gated first frontier and review checkpoint
- `sources/phase2_approval.json`: roadmap and external-source authorization
- `sources/phase2_acceptance_contract.md`: strict fine-graph acceptance rules
- `sources/phase2_content_scope.json`: reviewed content-complete parent registry
- `sources/external_sources_needed.md`: Phase-2 proof-source authorization gate
- `sources/phase1_review_attestation.json`: final graph hash and review record
- `scripts/check_plan.py`: graph, grounding, and tier-projection checker
- `scripts/check_phase2_approval.py`: Phase 1 hash and launch-policy gate
- `scripts/check_exercise_coverage.py`: coarse and fine exercise traceability
- `scripts/update_exercise_mapping.py`: locked fine-obligation mapping writer
- `scripts/check_informal_content.py`: scoped tier-2 prose contract checker
- `scripts/check_lean_hygiene.py`: lexical and compiled Lean trust audit
- `scripts/blueprint.py`: pinned, clean blueprint export/build/serve driver
- `formalization.yaml`: project scope, provenance, and review metadata
- `website/`: project site configuration

## License

Original project material is licensed under Apache-2.0. See `LICENSE`.
