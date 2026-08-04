# Phase 2 Acceptance Contract

This project treats Phase 2 as a durable construction process. Incremental
states may be incomplete, but every accepted cluster and the final detailed
blueprint must satisfy explicit, non-vacuous gates.

## Checkpoint Policy

Every Phase 2 checkpoint first validates the roadmap and source-policy decision
against the immutable Phase 1 snapshot:

```bash
python3 scripts/check_phase2_approval.py
```

Autoform permits a finer node with `parent: null` transiently while a splitter
discovers a new cluster. This repository does not persist such an orphan as a
checked milestone. Before the graph is validated or committed, its parent must
exist exactly one tier above it.

All structural graph changes go through Autoform's locked `merge_node.py`.
Content files and exercise mappings are updated immediately after their graph
nodes land, before a cluster is declared complete.

## Exercise Obligations

`sources/exercise_coverage.json` preserves the immutable Phase 1 mapping and
tracks one fine obligation for each distinct Phase 1 owner/member link. The
normalized set has 225 obligations carrying 226 exercise-ID links for all 209
exercises.

During construction, an obligation is either `pending` or `mapped`. A mapped
obligation names one or more unique tier-2 nodes under its exact Phase 1 owner.
The same tier-2 node cannot discharge two distinct normalized obligations.

The incremental check is:

```bash
python3 scripts/check_exercise_coverage.py
```

A cluster checkpoint additionally requires:

```bash
python3 scripts/check_exercise_coverage.py \
  --require-owner-complete "<tier-1 owner>"
```

Final Phase 2 acceptance requires:

```bash
python3 scripts/check_exercise_coverage.py --require-fine-complete
```

## Informal Content

`sources/phase2_content_scope.json` is the version-3 durable registry of tier-1
parents whose tier-2 prose has passed the cluster gate. Each sorted entry
contains the parent and a SHA-256 fingerprint over its complete review context.
Adding, removing, renaming, reparenting, or editing a child invalidates the
reviewed assertion. Merely having one child does not make a parent
content-complete.

The fingerprint is SHA-256 of the UTF-8 bytes of canonical JSON produced with
`sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=True`, and
`allow_nan=False`, without a trailing newline. Its object is:

```text
{
  "domain": "ltfp-phase2-content-scope-v3",
  "parent": <exact tier-1 id>,
  "review_context": {
    "graph_version": <graph schema version>,
    "lean_toolchain": <metadata value>,
    "mathlib_revision": <metadata value>,
    "metadata_sources": <canonical records for sources cited by these children,
                         sorted by file>,
    "source_identities": <{file, sha256} for those cited sources, sorted by file>
  },
  "children": <children sorted by graph-map key, each containing its duplicate
               id, complete node record, and standard RFC 4648 Base64 encoding
               of the exact content-file bytes>
}
```

Canonical source artifacts bind through the lowercase SHA-256 declared in
`metadata.sources`; when such an artifact is locally present, the checker also
verifies its bytes. This permits intentionally gitignored canonical PDFs to be
absent in CI. A cited local file without a canonical metadata record must exist
and is hashed from its exact bytes. Adding an unrelated source record does not
invalidate an already reviewed parent.

The stable global review context includes the graph schema, Lean toolchain, and
Mathlib revision. It intentionally excludes `created_at`, `last_updated`, and
`lean_root`: timestamps change on later merges and checkout roots are
machine-local, so including them would invalidate mathematically unrelated
completed clusters.

After a cluster review passes, obtain its exact scope entry with:

```bash
python3 scripts/check_informal_content.py --mode incremental \
  --parent "<tier-1 parent>"
```

The command prints the canonical `{parent, fingerprint_sha256}` entry that is
then added to the sorted scope registry.

Every tier-2 content file begins on its first physical line with the exact node
identity. Physical lines use only LF, CR, or CRLF semantics; Unicode line and
paragraph separators and non-CommonMark control characters are rejected.

```markdown
# <node id>
```

An `in-mathlib` node has a nonempty statement followed by an exact pointer:

```markdown
## Mathlib

Declarations: `Exact.declaration`, `Another.declaration`
File: `Mathlib/Exact/File.lean`
```

The declaration list, in graph order, and file must equal the node's graph
metadata. It has no explicit proof section or structural `Proof`, `Proof.`, or
`Proof:` paragraph. The mandatory H1 is identity metadata and is not citation
scanned; every body line remains subject to provenance and citation checks.
Exact provenance tokens are node-local: they come from that node's own
`source_refs` and matching canonical source record, so unrelated sources and
other nodes' locations do not retroactively taint accepted prose.

A `partial` or `missing` node has a nonempty statement and:

```markdown
## Proof

<complete informal proof>
```

These mechanical rules do not establish mathematical correctness,
source-faithfulness, originality, or the truth of a Mathlib correspondence.
The Mathlib checker and independent content reviewers establish those semantic
properties.

Incremental CI validates every existing prose file and requires completeness
for every parent listed in the scope file:

```bash
python3 scripts/check_informal_content.py --mode incremental \
  --scope sources/phase2_content_scope.json
```

Final Phase 2 acceptance uses the non-vacuous final mode and the durable
registry. Final mode requires one verified scope entry for every tier-1 parent:

```bash
python3 scripts/check_informal_content.py --mode final \
  --scope sources/phase2_content_scope.json
```

## Tier Projection

During splitting, tier 1 remains the Phase 1 scaffold. New fine dependencies
may reveal missing coarse edges, and old scaffold edges may prove unnecessary,
so incremental projection drift is reported but is not a failure.

At final re-projection, tier 2 is authoritative. The tier-1 node set must equal
the distinct tier-2 parents, and a tier-1 edge `A -> B` must exist exactly when
a tier-2 node under `A` depends on one under `B`. The derived quotient must be
acyclic even though tier 2 itself is already a DAG.

The project status rollup is:

- every child `in-mathlib`: parent `in-mathlib`;
- every child `missing`: parent `missing`;
- every other homogeneous or mixed case: parent `partial`.

Incremental CI uses:

```bash
python3 scripts/check_plan.py --require-grounding \
  --projection incremental
```

Final Phase 2 acceptance permanently switches the live graph to:

```bash
python3 scripts/check_plan.py --require-grounding --projection final
```

The immutable Phase 1 snapshot always remains in incremental projection mode
with `--content-free-snapshot`. That flag requires all snapshot content fields
to remain null and prevents future live prose from being misclassified as prose
owned by the archived graph; it is never used for the live graph.
