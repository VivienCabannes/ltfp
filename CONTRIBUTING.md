# Contributing

Contributions to the formalization of *Learning Theory from First Principles*
are welcome. Coordinate substantial work against the Markdown roadmap under
`blueprint/` so that parallel contributions use the same definitions and
dependency order. The attested `graph.json` and its existing audit files remain
part of the Phase 1/2 verification boundary until those checks are migrated.

## Development Requirements

- Use the Lean and Mathlib versions pinned by `lean-toolchain` and
  `lake-manifest.json`.
- Follow Mathlib naming, namespace, statement-generalization, and style
  conventions.
- Do not introduce `sorry`, `admit`, or project axioms in completed work.
- State analytic, measurability, moment, compactness, and selection hypotheses
  explicitly when the source suppresses them.
- Record source corrections or deliberate divergences in `sources/`.
- Do not commit the copyrighted source PDFs or extracted text.

## Before Submitting

Run:

```bash
python3 scripts/check_plan.py --require-grounding --projection incremental
python3 scripts/check_phase2_approval.py
python3 scripts/check_exercise_coverage.py
python3 scripts/check_informal_content.py --mode incremental \
  --scope sources/phase2_content_scope.json
python3 scripts/check_lean_hygiene.py
uv run --project "$AUTOFORM_PLUGIN_ROOT" autoform check blueprint --lean-root .
lake exe mk_all --check
lake build
```

Do not edit fine exercise mappings in place. Apply compare-and-swap updates
through `scripts/update_exercise_mapping.py`, after the referenced tier-2 graph
nodes have been merged. A cluster is content-complete only after its parent is
added to `sources/phase2_content_scope.json` and the scoped content gate passes.
Final Phase 2 acceptance uses the strict commands in
`sources/phase2_acceptance_contract.md`.

New reusable mathematics should include focused tests or downstream uses and
should be placed in an upstreamable module when it belongs in Mathlib. A change
is complete only after its source-faithfulness, proof-integrity, and code-quality
reviews pass.
