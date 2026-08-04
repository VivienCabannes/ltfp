#!/usr/bin/env python3
"""Validate the complete Autoform v2 plan schema and graph invariants.

Projection checks have two explicit lifecycle modes.  ``incremental`` derives
the live tier-2-to-tier-1 projection but does not reject drift in the authored
Phase 1 scaffold, because Autoform intentionally re-projects it only after the
fine graph is complete.  ``final`` requires the stored tier-1 graph to equal
that projection exactly.

This project validates checkpoint graphs, not merge transactions: even in
incremental projection mode every finer node must already have a non-null,
resolving parent.  Autoform may use null parents transiently while assembling a
merge, but such an orphan must be resolved before running this checker.

``--content-free-snapshot`` is reserved for immutable planning snapshots whose
nodes all have ``content: null``.  It requires that condition and prevents the
snapshot from treating prose owned by the evolving live graph as its own orphan
inventory.  It never weakens the live-graph content checks.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import re
import sys
import tempfile
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


KINDS = {"definition", "theorem", "proposition", "lemma", "corollary", "example"}
MATHLIB_STATUSES = {"in-mathlib", "partial", "missing"}
PROJECTION_MODES = {"incremental", "final"}
SOURCE_FORMATS = {"latex", "markdown", "pdf"}
TOP_LEVEL_FIELDS = {"version", "metadata", "nodes"}
METADATA_FIELDS = {
    "created_at",
    "last_updated",
    "sources",
    "lean_root",
    "lean_toolchain",
    "mathlib_revision",
}
SOURCE_FIELDS = {"file", "title", "format", "date", "sha256"}
NODE_FIELDS = {
    "id",
    "tier",
    "parent",
    "kind",
    "description",
    "provisional_members",
    "depends_on",
    "mathlib_status",
    "mathlib_declarations",
    "mathlib_file",
    "mathlib_notes",
    "source_refs",
    "content",
}
COMMON_NODE_FIELDS = NODE_FIELDS - {"provisional_members", "mathlib_file"}
SOURCE_REF_FIELDS = {"file", "location"}
TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
TOOLCHAIN_RE = re.compile(r"leanprover/lean4:v\d+\.\d+\.\d+")
REVISION_RE = re.compile(r"[0-9a-f]{40}")
UNSAFE_PATH_CODEPOINTS = {
    0x2028,
    0x2029,
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
}


class DuplicateKeyError(ValueError):
    """A JSON object repeated a key and would otherwise be silently lossy."""


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value!r} is not permitted")


def load_graph(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as stream:
            graph = json.load(
                stream,
                object_pairs_hook=_object_without_duplicates,
                parse_constant=_reject_nonfinite,
            )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    if not isinstance(graph, dict):
        raise ValueError("the graph document must be a JSON object")
    return graph


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and value == value.strip() and bool(value)


def _list_of_unique_strings(value: Any, *, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_nonempty_string(item) for item in value)
        and len(value) == len(set(value))
    )


@dataclass(frozen=True)
class TierProjection:
    """Pure tier-2-to-tier-1 projection derived from fine-node records.

    ``depends_on`` is stored in dependent-to-prerequisite orientation.  Thus a
    fine edge ``x -> y`` with parents ``A`` and ``B`` induces ``B`` in the
    stored ``depends_on`` set of ``A``.  Witnesses retain the fine edge that
    induced each quotient edge so a mismatch is actionable.
    """

    coarse_ids: tuple[str, ...]
    fine_ids: tuple[str, ...]
    members: dict[str, tuple[str, ...]]
    quotient: dict[str, frozenset[str]]
    witnesses: dict[tuple[str, str], tuple[tuple[str, str], ...]]
    status_rollup: dict[str, str]
    issues: tuple[str, ...]


def rollup_mathlib_status(statuses: Iterable[str]) -> str:
    """Roll child Mathlib coverage up under the project's explicit policy.

    A cluster is fully in Mathlib only when every child is; it is wholly
    missing only when every child is.  Every heterogeneous set, including any
    set containing a ``partial`` child, rolls up to ``partial``.  The child
    statuses remain curated Mathlib judgments; this function verifies only the
    consistency of the declared coarse rollup.
    """

    values = tuple(statuses)
    if not values:
        raise ValueError("cannot roll up an empty child set")
    if all(status == "in-mathlib" for status in values):
        return "in-mathlib"
    if all(status == "missing" for status in values):
        return "missing"
    return "partial"


def derive_tier2_projection(nodes: dict[str, dict[str, Any]]) -> TierProjection:
    """Derive membership, quotient edges, witnesses, and status rollups.

    The function is deliberately independent of insertion order and has no
    side effects.  Schema validation normally guarantees all references; the
    ``issues`` field makes the derivation total and prevents a future caller
    from silently dropping an orphan or malformed fine edge.
    """

    coarse_ids = tuple(sorted(node_id for node_id, node in nodes.items() if node.get("tier") == 1))
    fine_ids = tuple(sorted(node_id for node_id, node in nodes.items() if node.get("tier") == 2))
    coarse_set = set(coarse_ids)
    fine_set = set(fine_ids)
    member_lists: dict[str, list[str]] = {node_id: [] for node_id in coarse_ids}
    issue_set: set[str] = set()
    parent_of: dict[str, str] = {}

    for node_id in fine_ids:
        parent = nodes[node_id].get("parent")
        if parent is None:
            issue_set.add(
                f"tier-2 node {node_id!r} has a null parent; checkpoint graphs "
                "must resolve transient Autoform orphans"
            )
            continue
        if parent not in coarse_set:
            issue_set.add(
                f"tier-2 node {node_id!r} has non-tier-1 parent {parent!r}"
            )
            continue
        parent_of[node_id] = parent
        member_lists[parent].append(node_id)

    quotient_sets: dict[str, set[str]] = {node_id: set() for node_id in coarse_ids}
    witness_lists: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for node_id in fine_ids:
        source_parent = parent_of.get(node_id)
        if source_parent is None:
            continue
        dependencies = nodes[node_id].get("depends_on")
        if not isinstance(dependencies, list):
            issue_set.add(f"tier-2 node {node_id!r} has a non-array depends_on value")
            continue
        for dependency in sorted(dependencies, key=repr):
            if not isinstance(dependency, str) or dependency not in fine_set:
                issue_set.add(
                    f"tier-2 node {node_id!r} has non-tier-2 dependency {dependency!r}"
                )
                continue
            target_parent = parent_of.get(dependency)
            if target_parent is None:
                issue_set.add(
                    f"tier-2 dependency {node_id!r} -> {dependency!r} has no "
                    "complete parent projection"
                )
                continue
            if source_parent == target_parent:
                continue
            quotient_sets[source_parent].add(target_parent)
            witness_lists.setdefault((source_parent, target_parent), []).append(
                (node_id, dependency)
            )

    members = {
        node_id: tuple(sorted(member_lists[node_id]))
        for node_id in coarse_ids
    }
    quotient = {
        node_id: frozenset(quotient_sets[node_id])
        for node_id in coarse_ids
    }
    witnesses = {
        edge: tuple(sorted(set(edge_witnesses)))
        for edge, edge_witnesses in sorted(witness_lists.items())
    }
    status_rollup = {
        node_id: rollup_mathlib_status(
            nodes[member]["mathlib_status"] for member in members[node_id]
        )
        for node_id in coarse_ids
        if members[node_id]
    }
    return TierProjection(
        coarse_ids=coarse_ids,
        fine_ids=fine_ids,
        members=members,
        quotient=quotient,
        witnesses=witnesses,
        status_rollup=status_rollup,
        issues=tuple(sorted(issue_set)),
    )


def _field_set_errors(actual: set[str], allowed: set[str], required: set[str], where: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(required - actual)
    unknown = sorted(actual - allowed)
    if missing:
        errors.append(f"{where}: missing required fields {missing}")
    if unknown:
        errors.append(f"{where}: unknown fields {unknown}")
    return errors


def _relative_source_path(value: str) -> bool:
    if "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and len(path.parts) >= 2
        and path.parts[0] == "sources"
        and all(part not in {"", ".", ".."} for part in path.parts)
        and str(path) == value
    )


def _parse_timestamp(value: Any, where: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or TIMESTAMP_RE.fullmatch(value) is None:
        errors.append(f"{where}: expected canonical UTC timestamp YYYY-MM-DDTHH:MM:SSZ")
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        errors.append(f"{where}: invalid calendar timestamp {value!r}")
        return None


def validate_metadata(graph: dict[str, Any]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    metadata = graph.get("metadata")
    if not isinstance(metadata, dict):
        return ["metadata: expected an object"], set()

    required = {"created_at", "last_updated", "sources"}
    errors.extend(_field_set_errors(set(metadata), METADATA_FIELDS, required, "metadata"))
    created_at = _parse_timestamp(metadata.get("created_at"), "metadata.created_at", errors)
    last_updated = _parse_timestamp(metadata.get("last_updated"), "metadata.last_updated", errors)
    if created_at is not None and last_updated is not None and created_at > last_updated:
        errors.append("metadata: created_at must not be later than last_updated")

    for field in ("lean_root", "lean_toolchain", "mathlib_revision"):
        if field in metadata and not _nonempty_string(metadata[field]):
            errors.append(f"metadata.{field}: expected a nonempty, trimmed string")
    if "lean_root" in metadata and isinstance(metadata["lean_root"], str):
        if not Path(metadata["lean_root"]).is_absolute():
            errors.append("metadata.lean_root: expected an absolute path")
    if "lean_toolchain" in metadata and isinstance(metadata["lean_toolchain"], str):
        if TOOLCHAIN_RE.fullmatch(metadata["lean_toolchain"]) is None:
            errors.append("metadata.lean_toolchain: expected a stable Lean toolchain identifier")
    if "mathlib_revision" in metadata and isinstance(metadata["mathlib_revision"], str):
        if REVISION_RE.fullmatch(metadata["mathlib_revision"]) is None:
            errors.append("metadata.mathlib_revision: expected a lowercase 40-character Git revision")

    source_files: set[str] = set()
    sources = metadata.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("metadata.sources: expected a nonempty array")
        return errors, source_files

    for index, source in enumerate(sources):
        where = f"metadata.sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: expected an object")
            continue
        errors.extend(
            _field_set_errors(set(source), SOURCE_FIELDS, {"file", "title", "format"}, where)
        )
        source_file = source.get("file")
        if not _nonempty_string(source_file) or not _relative_source_path(source_file):
            errors.append(f"{where}.file: expected a canonical relative path below sources/")
        elif source_file in source_files:
            errors.append(f"{where}.file: duplicate source path {source_file!r}")
        else:
            source_files.add(source_file)
        if not _nonempty_string(source.get("title")):
            errors.append(f"{where}.title: expected a nonempty, trimmed string")
        if source.get("format") not in SOURCE_FORMATS:
            errors.append(f"{where}.format: expected one of {sorted(SOURCE_FORMATS)}")
        if "date" in source:
            source_date = source["date"]
            if not isinstance(source_date, str) or DATE_RE.fullmatch(source_date) is None:
                errors.append(f"{where}.date: expected YYYY-MM-DD")
            else:
                try:
                    if date.fromisoformat(source_date).isoformat() != source_date:
                        raise ValueError
                except ValueError:
                    errors.append(f"{where}.date: invalid calendar date {source_date!r}")
        if "sha256" in source and (
            not isinstance(source["sha256"], str)
            or SHA256_RE.fullmatch(source["sha256"]) is None
        ):
            errors.append(f"{where}.sha256: expected a lowercase SHA-256 digest")
    return errors, source_files


def _validate_content_path(
    value: str,
    node_id: str,
    project_root: Path,
    referenced: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    where = f"{node_id}.content"
    if "\\" in value or any(
        ord(character) < 32
        or ord(character) == 127
        or ord(character) in UNSAFE_PATH_CODEPOINTS
        for character in value
    ):
        return [f"{where}: backslashes and control characters are not permitted in content paths"]
    pure_path = PurePosixPath(value)
    if (
        pure_path.is_absolute()
        or len(pure_path.parts) < 2
        or pure_path.parts[0] != "informal_content"
        or any(part in {"", ".", ".."} for part in pure_path.parts)
        or pure_path.suffix != ".md"
        or str(pure_path) != value
    ):
        return [f"{where}: expected a canonical informal_content/**/*.md path"]

    root = project_root.resolve()
    candidate = root / Path(*pure_path.parts)
    try:
        content_root = (root / "informal_content").resolve()
        resolved = candidate.resolve()
    except (OSError, RuntimeError) as error:
        return [f"{where}: cannot safely resolve content path: {error}"]
    try:
        resolved.relative_to(root)
        resolved.relative_to(content_root)
    except ValueError:
        errors.append(f"{where}: path escapes the project informal_content directory")
        return errors
    if not candidate.is_file():
        errors.append(f"{where}: referenced prose file does not exist")
    prior = referenced.get(value)
    if prior is not None:
        errors.append(f"{where}: path is already referenced by node {prior!r}")
    else:
        referenced[value] = node_id
    return errors


def validate_nodes(
    graph: dict[str, Any],
    project_root: Path,
    source_files: set[str],
    *,
    content_free_snapshot: bool = False,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    raw_nodes = graph.get("nodes")
    if not isinstance(raw_nodes, dict) or not raw_nodes:
        return ["nodes: expected a nonempty object keyed by node id"], {}
    if not all(isinstance(node_id, str) and isinstance(node, dict) for node_id, node in raw_nodes.items()):
        return ["nodes: every entry must have a string key and object value"], {}

    nodes: dict[str, dict[str, Any]] = raw_nodes
    referenced_content: dict[str, str] = {}
    for node_id in sorted(nodes):
        node = nodes[node_id]
        where = f"nodes[{node_id!r}]"
        tier = node.get("tier")
        required = set(COMMON_NODE_FIELDS)
        if tier == 1:
            required.add("provisional_members")
        if node.get("mathlib_status") != "missing":
            required.add("mathlib_file")
        errors.extend(_field_set_errors(set(node), NODE_FIELDS, required, where))

        if not _nonempty_string(node_id):
            errors.append(f"{where}: node key must be a nonempty, trimmed string")
        if node.get("id") != node_id:
            errors.append(f"{where}.id: expected exact node key {node_id!r}")
        if not isinstance(tier, int) or isinstance(tier, bool) or tier < 1:
            errors.append(f"{where}.tier: expected a positive integer")
        parent = node.get("parent")
        if tier == 1 and parent is not None:
            errors.append(f"{where}.parent: tier-1 nodes must have a null parent")
        elif isinstance(tier, int) and not isinstance(tier, bool) and tier > 1:
            if not _nonempty_string(parent):
                errors.append(
                    f"{where}.parent: checkpoint graphs require every finer node to have "
                    "a parent; resolve transient Autoform orphans before validation"
                )
        elif tier != 1 and parent is not None and not _nonempty_string(parent):
            errors.append(f"{where}.parent: expected a node id or null")
        if node.get("kind") not in KINDS:
            errors.append(f"{where}.kind: expected one of {sorted(KINDS)}")
        if not _nonempty_string(node.get("description")):
            errors.append(f"{where}.description: expected a nonempty, trimmed string")

        if tier == 1:
            members = node.get("provisional_members")
            if not _list_of_unique_strings(members, allow_empty=False):
                errors.append(f"{where}.provisional_members: expected a nonempty array of unique strings")
        elif "provisional_members" in node:
            errors.append(f"{where}.provisional_members: field is permitted only on tier-1 nodes")

        dependencies = node.get("depends_on")
        if not _list_of_unique_strings(dependencies):
            errors.append(f"{where}.depends_on: expected an array of unique node ids")

        status = node.get("mathlib_status")
        if status not in MATHLIB_STATUSES:
            errors.append(f"{where}.mathlib_status: expected one of {sorted(MATHLIB_STATUSES)}")
        declarations = node.get("mathlib_declarations")
        if not _list_of_unique_strings(declarations):
            errors.append(f"{where}.mathlib_declarations: expected an array of unique declaration names")
        if not _nonempty_string(node.get("mathlib_notes")):
            errors.append(f"{where}.mathlib_notes: expected a nonempty, trimmed string")
        mathlib_file = node.get("mathlib_file")
        if status == "missing":
            if isinstance(declarations, list) and declarations:
                errors.append(f"{where}: missing nodes must have no Mathlib declarations")
            if "mathlib_file" in node:
                errors.append(f"{where}: missing nodes must omit mathlib_file")
        elif status in {"in-mathlib", "partial"}:
            if isinstance(declarations, list) and not declarations:
                errors.append(f"{where}: {status} nodes must name at least one Mathlib declaration")
            if not _nonempty_string(mathlib_file) or not re.fullmatch(r"Mathlib/.+\.lean", mathlib_file):
                errors.append(f"{where}.mathlib_file: expected a Mathlib/**/*.lean path")

        refs = node.get("source_refs")
        if not isinstance(refs, list):
            errors.append(f"{where}.source_refs: expected an array")
        else:
            seen_refs: set[tuple[str, str]] = set()
            for index, ref in enumerate(refs):
                ref_where = f"{where}.source_refs[{index}]"
                if not isinstance(ref, dict):
                    errors.append(f"{ref_where}: expected an object")
                    continue
                errors.extend(
                    _field_set_errors(set(ref), SOURCE_REF_FIELDS, SOURCE_REF_FIELDS, ref_where)
                )
                ref_file = ref.get("file")
                location = ref.get("location")
                if not _nonempty_string(ref_file) or not _relative_source_path(ref_file):
                    errors.append(f"{ref_where}.file: expected a canonical path below sources/")
                if not _nonempty_string(location):
                    errors.append(f"{ref_where}.location: expected a nonempty, trimmed string")
                if isinstance(ref_file, str) and isinstance(location, str):
                    pair = (ref_file, location)
                    if pair in seen_refs:
                        errors.append(f"{ref_where}: duplicate source reference")
                    seen_refs.add(pair)
                    if ref_file not in source_files and not (project_root / ref_file).is_file():
                        errors.append(
                            f"{ref_where}.file: not a declared source and no project source file exists"
                        )

        content = node.get("content")
        if content_free_snapshot and content is not None:
            errors.append(
                f"{where}.content: content-free snapshots require every content field to be null"
            )
        elif content is not None and not _nonempty_string(content):
            errors.append(f"{where}.content: expected null or a nonempty, trimmed string")
        elif isinstance(content, str):
            errors.extend(_validate_content_path(content, node_id, project_root, referenced_content))

    content_root = project_root / "informal_content"
    if not content_free_snapshot and content_root.exists():
        try:
            prose_files = {
                path.relative_to(project_root).as_posix()
                for path in content_root.rglob("*.md")
                if path.is_file()
            }
        except OSError as error:
            errors.append(f"informal_content: cannot inspect prose files: {error}")
        else:
            for orphan in sorted(prose_files - set(referenced_content)):
                errors.append(f"informal_content: orphan prose file {orphan!r}")
    return errors, nodes


def validate_schema(
    graph: dict[str, Any],
    project_root: Path,
    *,
    content_free_snapshot: bool = False,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors = _field_set_errors(set(graph), TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, "graph")
    version = graph.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 2:
        errors.append(f"version: expected integer schema version 2, got {version!r}")
    metadata_errors, source_files = validate_metadata(graph)
    errors.extend(metadata_errors)
    node_errors, nodes = validate_nodes(
        graph,
        project_root,
        source_files,
        content_free_snapshot=content_free_snapshot,
    )
    errors.extend(node_errors)
    return errors, nodes


def check_references_and_tiers(nodes: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for node_id in sorted(nodes):
        node = nodes[node_id]
        tier = node["tier"]
        parent = node["parent"]
        if parent is not None:
            if parent not in nodes:
                errors.append(f"{node_id}: absent parent {parent!r}")
            elif nodes[parent]["tier"] != tier - 1:
                errors.append(
                    f"{node_id}: parent {parent!r} is tier {nodes[parent]['tier']}, expected {tier - 1}"
                )
        for dependency in sorted(node["depends_on"]):
            if dependency not in nodes:
                errors.append(f"{node_id}: absent dependency {dependency!r}")
            elif nodes[dependency]["tier"] != tier:
                errors.append(
                    f"{node_id}: dependency {dependency!r} crosses from tier {tier} "
                    f"to tier {nodes[dependency]['tier']}"
                )
    return errors


def find_cycle(nodes: dict[str, dict[str, Any]], tier: int) -> list[str] | None:
    members = {node_id for node_id, node in nodes.items() if node["tier"] == tier}
    state = {node_id: 0 for node_id in members}
    for start in sorted(members):
        if state[start] != 0:
            continue
        state[start] = 1
        path = [start]
        stack = [(start, iter(sorted(nodes[start]["depends_on"])))]
        while stack:
            node_id, dependencies = stack[-1]
            for dependency in dependencies:
                if dependency not in members:
                    continue
                if state[dependency] == 1:
                    return path[path.index(dependency) :] + [dependency]
                if state[dependency] == 0:
                    state[dependency] = 1
                    path.append(dependency)
                    stack.append(
                        (dependency, iter(sorted(nodes[dependency]["depends_on"])))
                    )
                    break
            else:
                state[node_id] = 2
                path.pop()
                stack.pop()
    return None


def find_adjacency_cycle(adjacency: dict[str, Iterable[str]]) -> list[str] | None:
    """Return one deterministic directed cycle from an explicit adjacency map."""

    members = set(adjacency)
    state = {node_id: 0 for node_id in members}
    for start in sorted(members):
        if state[start] != 0:
            continue
        state[start] = 1
        path = [start]
        stack = [
            (
                start,
                iter(
                    sorted(
                        dependency
                        for dependency in adjacency[start]
                        if dependency in members
                    )
                ),
            )
        ]
        while stack:
            node_id, dependencies = stack[-1]
            for dependency in dependencies:
                if state[dependency] == 1:
                    return path[path.index(dependency) :] + [dependency]
                if state[dependency] == 0:
                    state[dependency] = 1
                    path.append(dependency)
                    stack.append(
                        (
                            dependency,
                            iter(
                                sorted(
                                    target
                                    for target in adjacency[dependency]
                                    if target in members
                                )
                            ),
                        )
                    )
                    break
            else:
                state[node_id] = 2
                path.pop()
                stack.pop()
    return None


def check_acyclic(nodes: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for tier in sorted({node["tier"] for node in nodes.values()}):
        cycle = find_cycle(nodes, tier)
        if cycle:
            errors.append(f"tier {tier} cycle: {' -> '.join(cycle)}")
    return errors


def check_tier2_projection(
    nodes: dict[str, dict[str, Any]], mode: str
) -> tuple[list[str], list[str]]:
    """Check or report the tier-2-to-tier-1 projection for one lifecycle mode."""

    if mode not in PROJECTION_MODES:
        raise ValueError(f"unknown projection mode {mode!r}")

    projection = derive_tier2_projection(nodes)
    errors = list(projection.issues)
    notes: list[str] = []
    represented = {
        parent for parent, members in projection.members.items() if members
    }
    unrepresented = sorted(set(projection.coarse_ids) - represented)
    expected_edges = {
        (source, target)
        for source, dependencies in projection.quotient.items()
        for target in dependencies
    }
    actual_edges = {
        (source, target)
        for source in projection.coarse_ids
        for target in nodes[source]["depends_on"]
    }
    missing_edges = sorted(expected_edges - actual_edges)
    spurious_edges = sorted(actual_edges - expected_edges)
    status_drift = sorted(
        parent
        for parent, expected in projection.status_rollup.items()
        if nodes[parent]["mathlib_status"] != expected
    )
    quotient_cycle = find_adjacency_cycle(projection.quotient)

    if mode == "incremental":
        if not projection.fine_ids:
            notes.append(
                "incremental projection: no tier-2 nodes; tier-1 remains the Phase 1 scaffold"
            )
        else:
            notes.append(
                "incremental projection: "
                f"{len(projection.fine_ids)} tier-2 nodes represent "
                f"{len(represented)}/{len(projection.coarse_ids)} tier-1 parents and induce "
                f"{len(expected_edges)} quotient edges"
            )
            notes.append(
                "incremental scaffold drift is non-gating until re-projection: "
                f"{len(missing_edges)} derived edge(s) absent, "
                f"{len(spurious_edges)} scaffold edge(s) unsupported, "
                f"{len(status_drift)} represented status rollup(s) stale"
            )
            if quotient_cycle is not None:
                notes.append(
                    "incremental derived quotient currently has a cycle (non-gating until "
                    f"final re-projection): {' -> '.join(quotient_cycle)}"
                )
        return sorted(errors), notes

    if not projection.fine_ids:
        errors.append("final projection is non-vacuous and requires at least one tier-2 node")
    if unrepresented:
        shown = ", ".join(repr(node_id) for node_id in unrepresented[:12])
        remainder = len(unrepresented) - 12
        suffix = f", ... (+{remainder} more)" if remainder > 0 else ""
        errors.append(
            f"{len(unrepresented)} tier-1 parent(s) have no tier-2 member: "
            + shown
            + suffix
        )
    projected_member_count = sum(len(members) for members in projection.members.values())
    if projected_member_count != len(projection.fine_ids):
        errors.append(
            "derived membership covers "
            f"{projected_member_count}/{len(projection.fine_ids)} tier-2 nodes exactly once"
        )

    notes.append(
        "final projection: "
        f"{len(projection.fine_ids)} tier-2 nodes, "
        f"{len(represented)}/{len(projection.coarse_ids)} represented tier-1 parents, "
        f"{len(expected_edges)} quotient edges"
    )
    if (
        not projection.fine_ids
        or unrepresented
        or projected_member_count != len(projection.fine_ids)
        or projection.issues
    ):
        # Exact edge and status comparisons are meaningful only after membership
        # is complete.  Reporting every Phase 1 scaffold edge as unsupported in
        # an empty or partial projection would obscure the actual blocking error.
        return sorted(set(errors)), notes

    for source, target in missing_edges:
        witnesses = projection.witnesses[(source, target)]
        rendered = ", ".join(
            f"{fine_source!r} depends on {fine_target!r}"
            for fine_source, fine_target in witnesses
        )
        errors.append(
            f"tier-1 node {source!r} is missing derived dependency {target!r}; "
            f"tier-2 witness(es): {rendered}"
        )
    for source, target in spurious_edges:
        errors.append(
            f"tier-1 node {source!r} has unsupported dependency {target!r}; "
            "no cross-parent tier-2 edge induces it"
        )
    for parent in status_drift:
        member_statuses = ", ".join(
            f"{member!r}={nodes[member]['mathlib_status']}"
            for member in projection.members[parent]
        )
        errors.append(
            f"tier-1 node {parent!r} has mathlib_status "
            f"{nodes[parent]['mathlib_status']!r}, expected "
            f"{projection.status_rollup[parent]!r} from children: {member_statuses}"
        )
    if quotient_cycle is not None:
        errors.append(
            "derived tier-1 quotient is cyclic despite tier-2 acyclicity: "
            + " -> ".join(quotient_cycle)
        )

    return sorted(set(errors)), notes


def check_grounding(nodes: dict[str, dict[str, Any]]) -> list[str]:
    memo: dict[str, bool] = {}

    def grounded(node_id: str, active: set[str]) -> bool:
        if node_id in memo:
            return memo[node_id]
        if node_id in active:
            return False
        node = nodes[node_id]
        if node["mathlib_status"] == "in-mathlib":
            memo[node_id] = True
            return True
        result = any(
            dependency in nodes and grounded(dependency, active | {node_id})
            for dependency in node["depends_on"]
        )
        memo[node_id] = result
        return result

    errors = [
        f"{node_id}: missing node has no path to an in-mathlib root"
        for node_id, node in nodes.items()
        if node["mathlib_status"] == "missing" and not grounded(node_id, set())
    ]
    errors.extend(
        f"{node_id}: dependency-free root has status {node['mathlib_status']!r}"
        for node_id, node in nodes.items()
        if not node["depends_on"] and node["mathlib_status"] != "in-mathlib"
    )
    return errors


def check_weak_connectedness(
    nodes: dict[str, dict[str, Any]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    skipped: list[str] = []
    for tier in sorted({node["tier"] for node in nodes.values()}):
        members = {node_id for node_id, node in nodes.items() if node["tier"] == tier}
        if tier > 1:
            parents = {
                node_id for node_id, node in nodes.items() if node["tier"] == tier - 1
            }
            represented_parents = {
                nodes[node_id]["parent"] for node_id in members
            }
            absent_parents = sorted(parents - represented_parents)
            if absent_parents:
                skipped.append(
                    f"tier {tier} is still being built; {len(absent_parents)} "
                    f"tier-{tier - 1} parent(s) have no child yet"
                )
                continue
        adjacency = {node_id: set() for node_id in members}
        for node_id in members:
            for dependency in nodes[node_id]["depends_on"]:
                if dependency in members:
                    adjacency[node_id].add(dependency)
                    adjacency[dependency].add(node_id)
        components: list[list[str]] = []
        unseen = set(members)
        while unseen:
            start = min(unseen)
            component: list[str] = []
            queue = deque([start])
            unseen.remove(start)
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in sorted(adjacency[current] & unseen):
                    unseen.remove(neighbor)
                    queue.append(neighbor)
            components.append(sorted(component))
        if len(components) > 1:
            representatives = [component[0] for component in components]
            errors.append(
                f"tier {tier} has {len(components)} weak components; representatives: "
                + ", ".join(repr(item) for item in representatives)
            )
    return errors, skipped


def _print_failures(name: str, errors: Iterable[str]) -> None:
    for error in sorted(errors):
        print(f"FAIL  {name}: {error}")


def validate_path(
    path: Path,
    *,
    require_grounding: bool,
    project_root: Path | None = None,
    projection_mode: str = "incremental",
    content_free_snapshot: bool = False,
) -> int:
    try:
        graph = load_graph(path)
    except ValueError as error:
        print(f"FAIL  graph input: {error}", file=sys.stderr)
        return 2

    resolved_project_root = (
        project_root.resolve() if project_root is not None else path.resolve().parent
    )
    schema_errors, nodes = validate_schema(
        graph,
        resolved_project_root,
        content_free_snapshot=content_free_snapshot,
    )
    if schema_errors:
        _print_failures("v2 schema", schema_errors)
        print(f"Schema summary: {len(schema_errors)} error(s); graph invariants not run")
        return 1
    print("PASS  complete v2 schema")

    connectedness_errors, skipped_connectedness = check_weak_connectedness(nodes)
    projection_errors, projection_notes = check_tier2_projection(nodes, projection_mode)
    checks: list[tuple[str, list[str]]] = [
        ("reference and tier integrity", check_references_and_tiers(nodes)),
        ("per-tier acyclicity", check_acyclic(nodes)),
    ]
    if require_grounding:
        checks.append(("Mathlib root reachability", check_grounding(nodes)))
    checks.extend(
        [
            ("complete-tier weak connectedness", connectedness_errors),
            (f"tier-2-to-tier-1 projection ({projection_mode})", projection_errors),
        ]
    )

    failed = False
    for name, errors in checks:
        if errors:
            failed = True
            _print_failures(name, errors)
        else:
            print(f"PASS  {name}")
    for note in skipped_connectedness:
        print(f"SKIP  incomplete-tier weak connectedness: {note}")
    for note in projection_notes:
        print(f"INFO  {note}")

    edge_count = sum(len(node["depends_on"]) for node in nodes.values())
    tiers = sorted({node["tier"] for node in nodes.values()})
    print(f"Graph summary: {len(nodes)} nodes, {edge_count} edges, tiers {tiers}")
    return 1 if failed else 0


def _self_test_graph() -> dict[str, Any]:
    return {
        "version": 2,
        "metadata": {
            "created_at": "2026-01-01T00:00:00Z",
            "last_updated": "2026-01-01T00:00:01Z",
            "sources": [
                {"file": "sources/test.pdf", "title": "Test", "format": "pdf"}
            ],
        },
        "nodes": {
            "Root": {
                "id": "Root",
                "tier": 1,
                "parent": None,
                "kind": "definition",
                "description": "A trusted root.",
                "provisional_members": ["Root definition"],
                "depends_on": [],
                "mathlib_status": "in-mathlib",
                "mathlib_declarations": ["Nat.zero"],
                "mathlib_file": "Mathlib/Data/Nat/Basic.lean",
                "mathlib_notes": "A fixture declaration.",
                "source_refs": [],
                "content": None,
            },
            "Result": {
                "id": "Result",
                "tier": 1,
                "parent": None,
                "kind": "theorem",
                "description": "A result grounded in the root.",
                "provisional_members": ["Result theorem"],
                "depends_on": ["Root"],
                "mathlib_status": "missing",
                "mathlib_declarations": [],
                "mathlib_notes": "The result is not in Mathlib.",
                "source_refs": [
                    {"file": "sources/test.pdf", "location": "Chapter 1"}
                ],
                "content": None,
            },
        },
    }


def _self_test_fine_node(
    node_id: str,
    parent: str,
    *,
    dependencies: list[str] | None = None,
    status: str = "in-mathlib",
    tier: int = 2,
) -> dict[str, Any]:
    node: dict[str, Any] = {
        "id": node_id,
        "tier": tier,
        "parent": parent,
        "kind": "theorem",
        "description": f"A fixture statement for {node_id}.",
        "depends_on": list(dependencies or []),
        "mathlib_status": status,
        "mathlib_declarations": [] if status == "missing" else ["Nat.zero"],
        "mathlib_notes": (
            "The fixture statement is not in Mathlib."
            if status == "missing"
            else "A fixture declaration."
        ),
        "source_refs": [],
        "content": None,
    }
    if status != "missing":
        node["mathlib_file"] = "Mathlib/Data/Nat/Basic.lean"
    return node


def _self_test_projection_graph() -> dict[str, Any]:
    graph = _self_test_graph()
    graph["nodes"]["Root detail"] = _self_test_fine_node(
        "Root detail", "Root"
    )
    graph["nodes"]["Result detail"] = _self_test_fine_node(
        "Result detail",
        "Result",
        dependencies=["Root detail"],
        status="missing",
    )
    return graph


def _self_test_cyclic_quotient_graph() -> dict[str, Any]:
    graph = _self_test_graph()
    nodes = graph["nodes"]
    nodes["Root"]["depends_on"] = ["Result"]
    nodes["Result"]["mathlib_status"] = "in-mathlib"
    nodes["Result"]["mathlib_declarations"] = ["Nat.zero"]
    nodes["Result"]["mathlib_file"] = "Mathlib/Data/Nat/Basic.lean"
    nodes["Result"]["mathlib_notes"] = "A fixture declaration."
    nodes["Root detail one"] = _self_test_fine_node(
        "Root detail one", "Root", dependencies=["Result detail one"]
    )
    nodes["Root detail two"] = _self_test_fine_node(
        "Root detail two", "Root", dependencies=["Result detail one"]
    )
    nodes["Result detail one"] = _self_test_fine_node(
        "Result detail one", "Result"
    )
    nodes["Result detail two"] = _self_test_fine_node(
        "Result detail two", "Result", dependencies=["Root detail two"]
    )
    return graph


def run_self_tests() -> int:
    with tempfile.TemporaryDirectory(prefix="check-plan-") as directory:
        root = Path(directory)
        graph_path = root / "graph.json"

        def check(
            graph: dict[str, Any],
            expected: int,
            label: str,
            *,
            projection: str = "incremental",
            require_grounding: bool = True,
            content_free_snapshot: bool = False,
            contains: tuple[str, ...] = (),
        ) -> bool:
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                actual = validate_path(
                    graph_path,
                    require_grounding=require_grounding,
                    projection_mode=projection,
                    content_free_snapshot=content_free_snapshot,
                )
            if actual != expected:
                print(f"FAIL  self-test {label}: expected exit {expected}, got {actual}")
                print(output.getvalue())
                return False
            missing_output = [
                fragment for fragment in contains if fragment not in output.getvalue()
            ]
            if missing_output:
                print(
                    f"FAIL  self-test {label}: output omitted expected fragment(s) "
                    f"{missing_output}"
                )
                print(output.getvalue())
                return False
            print(f"PASS  self-test {label}")
            return True

        def pure_check(condition: bool, label: str, detail: str = "") -> bool:
            if not condition:
                suffix = f": {detail}" if detail else ""
                print(f"FAIL  self-test {label}{suffix}")
                return False
            print(f"PASS  self-test {label}")
            return True

        valid = _self_test_graph()
        results = [
            check(
                valid,
                0,
                "accepts a Phase 1 graph in incremental projection mode",
                contains=("no tier-2 nodes; tier-1 remains the Phase 1 scaffold",),
            ),
            check(
                valid,
                1,
                "rejects a vacuous final projection",
                projection="final",
                contains=("final projection is non-vacuous",),
            ),
        ]
        content_root = root / "informal_content"
        content_root.mkdir()
        orphan = content_root / "future-tier2.md"
        orphan.write_text("# Future tier-2 node\n", encoding="utf-8")
        results.append(
            check(
                valid,
                1,
                "live graphs reject prose absent from their content inventory",
                contains=("orphan prose file",),
            )
        )
        results.append(
            check(
                valid,
                0,
                "content-free snapshots ignore the evolving live prose inventory",
                content_free_snapshot=True,
            )
        )
        orphan.unlink()
        content_root.rmdir()

        contentful_snapshot = copy.deepcopy(valid)
        contentful_snapshot["nodes"]["Root"]["content"] = "informal_content/root.md"
        results.append(
            check(
                contentful_snapshot,
                1,
                "content-free snapshot mode rejects non-null content fields",
                content_free_snapshot=True,
                contains=("content-free snapshots require every content field to be null",),
            )
        )
        malformed = copy.deepcopy(valid)
        malformed["nodes"]["Result"]["depends_on"] = [{}]
        results.append(check(malformed, 1, "controls an unhashable dependency value"))
        disconnected = copy.deepcopy(valid)
        disconnected["nodes"]["Other root"] = copy.deepcopy(disconnected["nodes"]["Root"])
        disconnected["nodes"]["Other root"]["id"] = "Other root"
        results.append(check(disconnected, 1, "rejects a disconnected tier"))

        partial_fine_tier = copy.deepcopy(valid)
        partial_fine_tier["nodes"]["Root detail"] = {
            "id": "Root detail",
            "tier": 2,
            "parent": "Root",
            "kind": "definition",
            "description": "A fine-grained root detail.",
            "depends_on": [],
            "mathlib_status": "in-mathlib",
            "mathlib_declarations": ["Nat.zero"],
            "mathlib_file": "Mathlib/Data/Nat/Basic.lean",
            "mathlib_notes": "A fixture declaration.",
            "source_refs": [],
            "content": None,
        }
        results.append(
            check(
                partial_fine_tier,
                0,
                "permits disconnected finer tiers while parent coverage is incomplete",
            )
        )
        results.append(
            check(
                partial_fine_tier,
                1,
                "requires every coarse parent in final projection mode",
                projection="final",
                contains=("tier-1 parent(s) have no tier-2 member",),
            )
        )
        transient_orphan = copy.deepcopy(partial_fine_tier)
        transient_orphan["nodes"]["Root detail"]["parent"] = None
        results.append(
            check(
                transient_orphan,
                1,
                "rejects transient null parents in checkpoint graphs",
                contains=("resolve transient Autoform orphans before validation",),
            )
        )

        disconnected_complete_fine_tier = copy.deepcopy(partial_fine_tier)
        disconnected_complete_fine_tier["nodes"]["Result detail"] = {
            "id": "Result detail",
            "tier": 2,
            "parent": "Result",
            "kind": "theorem",
            "description": "A disconnected fine-grained result.",
            "depends_on": [],
            "mathlib_status": "in-mathlib",
            "mathlib_declarations": ["Nat.zero"],
            "mathlib_file": "Mathlib/Data/Nat/Basic.lean",
            "mathlib_notes": "A fixture declaration.",
            "source_refs": [],
            "content": None,
        }
        results.append(
            check(
                disconnected_complete_fine_tier,
                1,
                "rejects a disconnected finer tier once every parent is represented",
            )
        )

        exact_projection = _self_test_projection_graph()
        results.append(
            check(
                exact_projection,
                0,
                "accepts exact final membership, quotient, and status rollups",
                projection="final",
                contains=("PASS  tier-2-to-tier-1 projection (final)",),
            )
        )

        stale_projection = _self_test_projection_graph()
        stale_nodes = stale_projection["nodes"]
        stale_nodes["Result detail"] = _self_test_fine_node(
            "Result detail", "Result"
        )
        stale_nodes["Root detail"]["depends_on"] = ["Result detail"]
        results.append(
            check(
                stale_projection,
                0,
                "reports fully represented stale scaffold without gating incremental work",
                contains=("incremental scaffold drift is non-gating",),
            )
        )

        missing_projection_edge = _self_test_projection_graph()
        missing_projection_edge["nodes"]["Result"]["depends_on"] = []
        results.append(
            check(
                missing_projection_edge,
                1,
                "rejects a missing coarse quotient edge",
                projection="final",
                require_grounding=False,
                contains=(
                    "tier-1 node 'Result' is missing derived dependency 'Root'",
                    "'Result detail' depends on 'Root detail'",
                ),
            )
        )

        spurious_projection_edge = _self_test_projection_graph()
        spurious_projection_edge["nodes"]["Root"]["depends_on"] = ["Result"]
        results.append(
            check(
                spurious_projection_edge,
                1,
                "rejects a spurious coarse scaffold edge",
                projection="final",
                contains=(
                    "tier-1 node 'Root' has unsupported dependency 'Result'",
                ),
            )
        )

        reversed_projection_edge = _self_test_projection_graph()
        reversed_projection_edge["nodes"]["Root"]["depends_on"] = ["Result"]
        reversed_projection_edge["nodes"]["Result"]["depends_on"] = []
        results.append(
            check(
                reversed_projection_edge,
                1,
                "rejects reversed coarse dependency orientation",
                projection="final",
                require_grounding=False,
                contains=(
                    "tier-1 node 'Result' is missing derived dependency 'Root'",
                    "tier-1 node 'Root' has unsupported dependency 'Result'",
                ),
            )
        )

        coarse_self_edge = _self_test_projection_graph()
        coarse_self_edge["nodes"]["Root"]["depends_on"] = ["Root"]
        results.append(
            check(
                coarse_self_edge,
                1,
                "does not project intra-parent dependencies into coarse self-edges",
                projection="final",
                contains=("tier-1 node 'Root' has unsupported dependency 'Root'",),
            )
        )

        duplicate_witnesses = _self_test_projection_graph()
        duplicate_witnesses["nodes"]["Result detail two"] = _self_test_fine_node(
            "Result detail two",
            "Result",
            dependencies=["Root detail"],
            status="missing",
        )
        duplicate_projection = derive_tier2_projection(duplicate_witnesses["nodes"])
        results.append(
            pure_check(
                duplicate_projection.quotient["Result"] == frozenset({"Root"})
                and duplicate_projection.witnesses[("Result", "Root")]
                == (
                    ("Result detail", "Root detail"),
                    ("Result detail two", "Root detail"),
                ),
                "deduplicates quotient edges and sorts all fine witnesses",
            )
        )
        shuffled_nodes = {
            node_id: copy.deepcopy(node)
            for node_id, node in reversed(list(duplicate_witnesses["nodes"].items()))
        }
        for node in shuffled_nodes.values():
            node["depends_on"] = list(reversed(node["depends_on"]))
        results.append(
            pure_check(
                derive_tier2_projection(shuffled_nodes) == duplicate_projection,
                "keeps projection output deterministic under input reordering",
            )
        )
        results.append(
            check(
                duplicate_witnesses,
                0,
                "accepts multiple fine witnesses for one quotient edge",
                projection="final",
            )
        )

        rollup_cases = {
            ("in-mathlib",): "in-mathlib",
            ("missing",): "missing",
            ("partial",): "partial",
            ("in-mathlib", "in-mathlib"): "in-mathlib",
            ("missing", "missing"): "missing",
            ("in-mathlib", "missing"): "partial",
            ("partial", "missing"): "partial",
            ("in-mathlib", "partial"): "partial",
            ("in-mathlib", "partial", "missing"): "partial",
        }
        results.append(
            pure_check(
                all(
                    rollup_mathlib_status(statuses) == expected
                    for statuses, expected in rollup_cases.items()
                ),
                "implements the complete Mathlib status rollup truth table",
            )
        )
        stale_status = _self_test_projection_graph()
        stale_status["nodes"]["Root"]["mathlib_status"] = "partial"
        results.append(
            check(
                stale_status,
                1,
                "rejects a stale final Mathlib status rollup",
                projection="final",
                require_grounding=False,
                contains=(
                    "tier-1 node 'Root' has mathlib_status 'partial', expected 'in-mathlib'",
                ),
            )
        )

        cyclic_quotient = _self_test_cyclic_quotient_graph()
        cyclic_projection = derive_tier2_projection(cyclic_quotient["nodes"])
        results.append(
            pure_check(
                find_cycle(cyclic_quotient["nodes"], 2) is None
                and find_adjacency_cycle(cyclic_projection.quotient) is not None,
                "constructs an acyclic fine graph with a cyclic quotient",
            )
        )
        results.append(
            check(
                cyclic_quotient,
                1,
                "rejects a cyclic quotient of an acyclic fine graph",
                projection="final",
                contains=("derived tier-1 quotient is cyclic despite tier-2 acyclicity",),
            )
        )

        tier3_graph = _self_test_projection_graph()
        projection_before_tier3 = derive_tier2_projection(tier3_graph["nodes"])
        tier3_graph["nodes"]["Lean root detail"] = _self_test_fine_node(
            "Lean root detail", "Root detail", tier=3
        )
        projection_after_tier3 = derive_tier2_projection(tier3_graph["nodes"])
        results.append(
            pure_check(
                projection_after_tier3 == projection_before_tier3,
                "isolates tier-2-to-tier-1 projection from tier-3 records",
            )
        )
        results.append(
            check(
                tier3_graph,
                0,
                "accepts an exact final projection when tier 3 is partially built",
                projection="final",
            )
        )

        unsafe_path = copy.deepcopy(valid)
        unsafe_path["nodes"]["Root"]["content"] = "informal_content/unsafe\u202e.md"
        results.append(
            check(
                unsafe_path,
                1,
                "rejects Unicode control characters in content paths",
                contains=(
                    "backslashes and control characters are not permitted in content paths",
                ),
            )
        )

        loop_root = root / "symlink-loop"
        loop_root.mkdir()
        loop_graph = copy.deepcopy(valid)
        loop_graph["nodes"]["Root"]["content"] = "informal_content/root.md"
        loop_graph_path = loop_root / "graph.json"
        loop_graph_path.write_text(json.dumps(loop_graph), encoding="utf-8")
        (loop_root / "informal_content").symlink_to(
            "informal_content", target_is_directory=True
        )
        loop_output = io.StringIO()
        with contextlib.redirect_stdout(loop_output), contextlib.redirect_stderr(
            loop_output
        ):
            loop_code = validate_path(
                loop_graph_path,
                require_grounding=True,
                project_root=loop_root,
            )
        results.append(
            pure_check(
                loop_code == 1
                and "cannot safely resolve content path" in loop_output.getvalue(),
                "reports symlink loops without a traceback",
                loop_output.getvalue(),
            )
        )

        deterministic_a = copy.deepcopy(valid)
        deterministic_a["nodes"]["Root"]["kind"] = "invalid-root-kind"
        deterministic_a["nodes"]["Root"]["depends_on"] = ["Missing Z", "Missing A"]
        deterministic_a["nodes"]["Result"]["kind"] = "invalid-result-kind"
        deterministic_b = copy.deepcopy(deterministic_a)
        deterministic_b["nodes"] = dict(
            reversed(list(deterministic_b["nodes"].items()))
        )
        for node in deterministic_b["nodes"].values():
            node["depends_on"] = list(reversed(node["depends_on"]))

        def validation_output(graph: dict[str, Any]) -> tuple[int, str]:
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            rendered = io.StringIO()
            with contextlib.redirect_stdout(rendered), contextlib.redirect_stderr(
                rendered
            ):
                code = validate_path(graph_path, require_grounding=True)
            return code, rendered.getvalue()

        result_a = validation_output(deterministic_a)
        result_b = validation_output(deterministic_b)
        results.append(
            pure_check(
                result_a == result_b and result_a[0] == 1,
                "keeps full diagnostics deterministic under input reordering",
                f"first={result_a!r}; second={result_b!r}",
            )
        )

        graph_path.write_text('{"version": 2, "version": 2}', encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            duplicate_code = validate_path(graph_path, require_grounding=True)
        if duplicate_code != 2:
            print("FAIL  self-test rejects duplicate JSON keys")
            results.append(False)
        else:
            print("PASS  self-test rejects duplicate JSON keys")
            results.append(True)
    return 0 if all(results) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", nargs="?", type=Path, default=Path("graph.json"))
    parser.add_argument(
        "--project-root",
        type=Path,
        help="repository root for resolving graph-relative content and source paths",
    )
    parser.add_argument("--require-grounding", action="store_true")
    parser.add_argument(
        "--projection",
        choices=sorted(PROJECTION_MODES),
        default="incremental",
        help=(
            "incremental reports derived tier-1 drift without gating it; final requires "
            "exact tier-2-to-tier-1 membership, edges, and Mathlib status rollups"
        ),
    )
    parser.add_argument(
        "--content-free-snapshot",
        action="store_true",
        help=(
            "require every content field to be null and do not compare this immutable "
            "snapshot with the live project's informal_content inventory"
        ),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_tests()
    return validate_path(
        args.graph,
        require_grounding=args.require_grounding,
        project_root=args.project_root,
        projection_mode=args.projection,
        content_free_snapshot=args.content_free_snapshot,
    )


if __name__ == "__main__":
    raise SystemExit(main())
