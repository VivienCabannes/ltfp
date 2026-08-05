# Learning Theory from First Principles in Lean

This project formalizes the mathematical content of Francis Bach's
*Learning Theory from First Principles* in Lean 4, including all fifteen
chapters, the embedded exercises, and the separate exercise collection.

**Blueprint:** [Browse the formalization blueprint](blueprint/README.md).

The target is Mathlib-quality code: reusable definitions, theorem statements at
the right level of generality, explicit analytic and measurability hypotheses,
no project axioms, and no `sorry` in completed milestones.

## Status

The first Lean modules landed on August 5, 2026. Seven files under
`LearningTheoryFromFirstPrinciples/Mathlib/` formalize the fourteen reviewed
tier-2 statements of the content-complete clusters that the pinned Mathlib
checkout does not already provide: the affine panel interpolant, its panel and
piecewise-affine integral identities, the exact trapezoidal error
decomposition, Exercises 1.26, 1.27 and 1.28 including an Euler-Maclaurin style
Bernoulli-kernel identity for the trapezoidal error, the variance, mean-square
error, deviation bound and convergence in probability of an iid sample mean,
and the two elementary tail bounds behind Markov's inequality and the supremum
union bound. The library builds clean with no `sorry`, no project axiom, and no
declaration depending on anything beyond `propext`, `Classical.choice` and
`Quot.sound`. The other 97 tier-2 statements of those clusters are already in
Mathlib and need no project declaration.
`sources/lean_correspondence.md` maps each formalized node to its declarations.

Autoform Phase 1 is complete and approved. Phase 2 statement-level planning
started on August 4, 2026 under the pinned-primary-source policy recorded in
`sources/phase2_approval.json`. The attested legacy graph has 227 nodes and 661
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

The accepted plan is now presented in the Markdown vault under `blueprint/`:
116 coarse milestone pages and a 111-node, 200-edge fine DAG. The attested
legacy planning graph remains in `graph.json` for the existing Phase 1 and
Phase 2 audit scripts. Source ambiguities that affect formal statements are
recorded in `sources/formalization_notes.md`; proof obligations that require an
external source decision are listed in `sources/external_sources_needed.md`.

The pinned environment is:

- Lean `v4.32.2`
- Mathlib `v4.32.2` at commit
  `905b95818eb32af7874a58b427f50c1711a5e96c`
- Autoform `0.5.0` for the Markdown blueprint, derived statuses, and rendering
- Pages: uv `0.12.1`, MkDocs `1.6.1`, and pymdown-extensions `10.21.3`
- Legacy exporter: Python `3.12.13`, uv `0.11.15`, and Graphviz `2.44.0` on Linux

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
Autoform Markdown vault is the human-editable roadmap; its rendered MkDocs site
adds a book overview, aggregate progress, leanblueprint-style statement
environments, source-code permalinks, and project-, chapter-, local-, and
full-DAG dependency maps.

With `AUTOFORM_PLUGIN_ROOT` set to the installed Autoform plugin checkout,
validate and build the presentation with:

```bash
uv run --project "$AUTOFORM_PLUGIN_ROOT" autoform check blueprint --lean-root .
uv run --project "$AUTOFORM_PLUGIN_ROOT" autoform-visualize blueprint
uv run --project "$AUTOFORM_PLUGIN_ROOT" autoform render blueprint \
  --output site-src --lean-root . --require-declarations
uv run --with mkdocs==1.6.1 --with pymdown-extensions==10.21.3 \
  mkdocs build --strict
```

`autoform render` writes the ignored `site-src/` tree and leaves the vault
untouched. GitHub Pages repeats the same validation and build from an immutable
Autoform commit.

## Repository Layout

- `LearningTheoryFromFirstPrinciples/`: Lean source files
- `LearningTheoryFromFirstPrinciples/Mathlib/`: upstreamable modules for results
  missing from the pinned Mathlib checkout
- `blueprint/`: Obsidian-compatible roadmap, coverage, source map, and fine DAG
- `mkdocs.yml`: configuration for the derived blueprint site
- `graph.json`: attested legacy planning graph used by the existing audit scripts
- `sources/lean_correspondence.md`: tier-2 node to Lean declaration mapping
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
- `scripts/blueprint.py`: retained Autoform 0.4.4 exporter for the legacy graph view
- `formalization.yaml`: project scope, provenance, and review metadata
- `website/`: retained source for the former upstreaming-dashboard site

## License

Original project material is licensed under Apache-2.0. See `LICENSE`.
