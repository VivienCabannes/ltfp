#!/usr/bin/env python3
"""Validate coarse exercise ownership and incremental tier-2 mappings.

Schema v1 is the immutable Phase 1 owner/member matrix. Schema v2 retains that
matrix verbatim, anchors it to the attested Phase 1 graph, and adds one explicit
pending-or-mapped record for every normalized coarse member obligation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_SOURCES = {
    "book": {
        "id": "ltfp-book-2025-05-26",
        "title": "Learning Theory from First Principles",
        "date": "2025-05-26",
        "local_file": "sources/ltfp_book.pdf",
        "format": "pdf",
        "sha256": "5e7840c545d24aaf21a1ea5fbddd76e78153de0a9a952f56810a8618a9fc9e06",
    },
    "supplement": {
        "id": "ltfp-exercises-2025-12-01",
        "title": "Learning Theory from First Principles - Exercises",
        "date": "2025-12-01",
        "local_file": "sources/ltfp_exercises.pdf",
        "format": "pdf",
        "sha256": "b68b440586765f123ae02cc9d8ac17b057cb01266db5358d92786ba0a1b3ab3d",
    },
}

EXPECTED_CREATED_AT = "2026-08-03T14:32:13Z"
EXPECTED_PHASE1_GRAPH_FILE = "sources/phase1_graph.json"
EXPECTED_PHASE1_GRAPH_SHA256 = (
    "cbf4e871f971fd9c590219073389a41e9977dcbe11ebf2111fca1fd6eadd2758"
)
EXPECTED_PHASE1_ATTESTATION_FILE = "sources/phase1_review_attestation.json"
COVERAGE_V1_KEYS = ["schema_version", "sources", "chapters", "exercises"]
COVERAGE_V2_KEYS = COVERAGE_V1_KEYS + ["phase1_graph", "fine_obligations"]
SOURCE_KEYS = ["id", "title", "date", "local_file", "format", "sha256"]
CHAPTER_KEYS = [
    "exercise_range",
    "count",
    "book_printed_pages",
    "supplement_printed_pages",
]
EXERCISE_KEYS = ["owner", "members", "present_in"]
PRESENCE_KEYS = ["book", "supplement"]
GRAPH_SOURCE_KEYS = ["file", "title", "format", "date", "sha256"]
PHASE1_GRAPH_KEYS = ["file", "sha256"]
FINE_OBLIGATION_KEYS = ["owner", "exercise_ids", "mapping"]
FINE_MAPPING_KEYS = ["status", "tier2_node_ids"]
FINE_MAPPING_STATUSES = {"pending", "mapped"}
GRAPH_SOURCE_FORMATS = {"latex", "markdown", "pdf"}
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
SHA256_RE = re.compile(r"[0-9a-f]{64}")

EXPECTED_CHAPTERS = {
    "1": {
        "exercise_range": ["1.1", "1.29"],
        "count": 29,
        "book_printed_pages": [6, 20],
        "supplement_printed_pages": [1, 4],
    },
    "2": {
        "exercise_range": ["2.1", "2.8"],
        "count": 8,
        "book_printed_pages": [30, 32],
        "supplement_printed_pages": [5, 8],
    },
    "3": {
        "exercise_range": ["3.1", "3.10"],
        "count": 10,
        "book_printed_pages": [51, 67],
        "supplement_printed_pages": [9, 12],
    },
    "4": {
        "exercise_range": ["4.1", "4.16"],
        "count": 16,
        "book_printed_pages": [81, 102],
        "supplement_printed_pages": [13, 17],
    },
    "5": {
        "exercise_range": ["5.1", "5.36"],
        "count": 36,
        "book_printed_pages": [115, 152],
        "supplement_printed_pages": [19, 25],
    },
    "6": {
        "exercise_range": ["6.1", "6.6"],
        "count": 6,
        "book_printed_pages": [161, 178],
        "supplement_printed_pages": [27, 28],
    },
    "7": {
        "exercise_range": ["7.1", "7.23"],
        "count": 23,
        "book_printed_pages": [185, 209],
        "supplement_printed_pages": [29, 35],
    },
    "8": {
        "exercise_range": ["8.1", "8.17"],
        "count": 17,
        "book_printed_pages": [225, 245],
        "supplement_printed_pages": [37, 39],
    },
    "9": {
        "exercise_range": ["9.1", "9.10"],
        "count": 10,
        "book_printed_pages": [255, 275],
        "supplement_printed_pages": [41, 42],
    },
    "10": {
        "exercise_range": ["10.1", "10.9"],
        "count": 9,
        "book_printed_pages": [286, 308],
        "supplement_printed_pages": None,
    },
    "11": {
        "exercise_range": ["11.1", "11.8"],
        "count": 8,
        "book_printed_pages": [318, 334],
        "supplement_printed_pages": None,
    },
    "12": {
        "exercise_range": ["12.1", "12.9"],
        "count": 9,
        "book_printed_pages": [351, 375],
        "supplement_printed_pages": None,
    },
    "13": {
        "exercise_range": ["13.1", "13.10"],
        "count": 10,
        "book_printed_pages": [382, 403],
        "supplement_printed_pages": None,
    },
    "14": {
        "exercise_range": ["14.1", "14.13"],
        "count": 13,
        "book_printed_pages": [411, 418],
        "supplement_printed_pages": None,
    },
    "15": {
        "exercise_range": ["15.1", "15.5"],
        "count": 5,
        "book_printed_pages": [437, 449],
        "supplement_printed_pages": None,
    },
}

EXERCISE_MARKER_RE = re.compile(r" \((Exercise|Exercises) ([^()]*)\)$")
EXERCISE_ID_RE = re.compile(r"(?<![\d.])(\d+\.\d+)(?![\d.])")
SOURCE_EXERCISE_ID_PATTERN = r"\d+\.\d+(?![\d.])"
SOURCE_EXERCISE_SEPARATOR_PATTERN = (
    r"(?:\s*[-\u2013\u2014]\s*|\s*,\s*(?:and\s+)?|\s+and\s+)"
)
SOURCE_EXERCISE_CITATION_RE = re.compile(
    rf"\bExercises?\s+({SOURCE_EXERCISE_ID_PATTERN}"
    rf"(?:{SOURCE_EXERCISE_SEPARATOR_PATTERN}{SOURCE_EXERCISE_ID_PATTERN})*)"
)
SOURCE_EXERCISE_RANGE_RE = re.compile(r"(\d+)\.(\d+)\s*[-\u2013\u2014]\s*(\d+)\.(\d+)")


class CoverageError(ValueError):
    """Raised when the coverage contract is inconsistent."""


@dataclass(frozen=True)
class ExerciseInventory:
    expected_ids: list[str]
    obligations: dict[str, dict[str, Any]]
    multipart_count: int
    explicit_link_count: int
    explicit_id_count: int
    shared_member_count: int


@dataclass(frozen=True)
class ValidationResult:
    schema_version: int
    obligation_count: int
    mapped_obligations: int
    pending_obligations: int
    complete_exercises: int
    pending_exercises: int
    summary: str


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CoverageError(message)


def exact_keys(value: Any, keys: list[str], label: str) -> None:
    require(type(value) is dict, f"{label} must be a JSON object")
    require(
        list(value) == keys,
        f"{label} keys must be exactly {keys!r}, found {list(value)!r}",
    )


def nonempty_string(value: Any, label: str) -> str:
    require(
        type(value) is str and bool(value) and value == value.strip(),
        f"{label} must be a non-empty, trimmed string",
    )
    return value


def integer(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} must be an integer (not a boolean)")
    return value


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CoverageError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise CoverageError(f"non-finite JSON number {value!r}")


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, CoverageError) as error:
        raise CoverageError(f"cannot read {label} {path}: {error}") from error
    require(type(value) is dict, f"{label} must be a JSON object")
    return value


def unique_string_list(
    value: Any, label: str, *, allow_empty: bool = True
) -> list[str]:
    require(type(value) is list, f"{label} must be an array")
    if not allow_empty:
        require(bool(value), f"{label} must not be empty")
    for index, item in enumerate(value):
        nonempty_string(item, f"{label}[{index}]")
    require(len(value) == len(set(value)), f"{label} must not contain duplicates")
    return value


def expected_exercise_ids() -> list[str]:
    return [
        f"{chapter}.{number}"
        for chapter, metadata in EXPECTED_CHAPTERS.items()
        for number in range(1, metadata["count"] + 1)
    ]


def exercise_sort_key(identifier: str) -> tuple[int, int]:
    return tuple(map(int, identifier.split(".")))  # type: ignore[return-value]


def canonical_marker(identifiers: list[str]) -> str:
    if len(identifiers) == 1:
        return f"Exercise {identifiers[0]}"
    if len(identifiers) == 2:
        return f"Exercises {identifiers[0]} and {identifiers[1]}"
    return f"Exercises {', '.join(identifiers[:-1])}, and {identifiers[-1]}"


def explicit_exercise_ids(member: str) -> set[str]:
    marker = EXERCISE_MARKER_RE.search(member)
    if marker is None:
        require(
            "(Exercise " not in member and "(Exercises " not in member,
            f"malformed exercise marker in member {member!r}",
        )
        return set()

    require(marker.start() > 0, f"exercise marker has no member name in {member!r}")
    require(
        "(Exercise " not in member[: marker.start()]
        and "(Exercises " not in member[: marker.start()],
        f"multiple exercise markers in member {member!r}",
    )
    kind, clause = marker.groups()
    identifiers = EXERCISE_ID_RE.findall(clause)
    require(identifiers, f"malformed exercise marker in member {member!r}")
    require(
        len(identifiers) == len(set(identifiers)),
        f"duplicate explicit exercise identifier in member {member!r}",
    )
    require(
        identifiers == sorted(identifiers, key=exercise_sort_key),
        f"exercise identifiers are not in numeric order in member {member!r}",
    )
    require(
        f"{kind} {clause}" == canonical_marker(identifiers),
        f"non-canonical exercise marker in member {member!r}",
    )
    return set(identifiers)


def source_exercise_ids(location: str) -> set[str]:
    """Extract IDs only from citations syntactically attached to Exercise(s)."""
    identifiers: set[str] = set()
    known_identifiers = set(expected_exercise_ids())
    for citation in SOURCE_EXERCISE_CITATION_RE.findall(location):
        cited_identifiers = set(EXERCISE_ID_RE.findall(citation))
        unknown_identifiers = sorted(cited_identifiers - known_identifiers)
        require(
            not unknown_identifiers,
            f"exercise citation names unknown ID(s) {unknown_identifiers!r}",
        )
        identifiers.update(cited_identifiers)
        for match in SOURCE_EXERCISE_RANGE_RE.finditer(citation):
            start_chapter_text, start_number_text, end_chapter_text, end_number_text = (
                match.groups()
            )
            start_identifier = f"{start_chapter_text}.{start_number_text}"
            end_identifier = f"{end_chapter_text}.{end_number_text}"
            require(
                start_identifier in known_identifiers
                and end_identifier in known_identifiers,
                f"exercise range {match.group(0)!r} has an out-of-inventory endpoint",
            )
            start_chapter = int(start_chapter_text)
            start_number = int(start_number_text)
            end_chapter = int(end_chapter_text)
            end_number = int(end_number_text)
            require(
                start_chapter == end_chapter,
                f"exercise range {match.group(0)!r} must stay within one chapter",
            )
            require(
                start_number <= end_number,
                f"exercise range {match.group(0)!r} must be increasing",
            )
            identifiers.update(
                f"{start_chapter}.{number}"
                for number in range(start_number, end_number + 1)
            )
    return identifiers


def validate_iso8601(value: Any, label: str) -> None:
    timestamp = nonempty_string(value, label)
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as error:
        raise CoverageError(f"{label} is not an ISO 8601 timestamp") from error
    require(parsed.tzinfo is not None, f"{label} must include a timezone")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise CoverageError(f"cannot hash local source {path}: {error}") from error
    return digest.hexdigest()


def expected_graph_sources() -> list[dict[str, str]]:
    return [
        {
            "file": source["local_file"],
            "title": source["title"],
            "format": source["format"],
            "date": source["date"],
            "sha256": source["sha256"],
        }
        for source in EXPECTED_SOURCES.values()
    ]


def validate_graph_source_record(source: Any, label: str) -> dict[str, Any]:
    exact_keys(source, GRAPH_SOURCE_KEYS, label)
    for field in GRAPH_SOURCE_KEYS:
        nonempty_string(source[field], f"{label}.{field}")
    source_path = PurePosixPath(source["file"])
    require(
        not source_path.is_absolute()
        and len(source_path.parts) >= 2
        and source_path.parts[0] == "sources"
        and all(part not in {"", ".", ".."} for part in source_path.parts)
        and "\\" not in source["file"]
        and str(source_path) == source["file"],
        f"{label}.file must be a canonical relative path below sources/",
    )
    require(
        source["format"] in GRAPH_SOURCE_FORMATS,
        f"{label}.format must be one of {sorted(GRAPH_SOURCE_FORMATS)!r}",
    )
    require(
        DATE_RE.fullmatch(source["date"]) is not None,
        f"{label}.date must use YYYY-MM-DD",
    )
    try:
        parsed_date = datetime.strptime(source["date"], "%Y-%m-%d").date()
    except ValueError as error:
        raise CoverageError(f"{label}.date is not a valid calendar date") from error
    require(parsed_date.isoformat() == source["date"], f"{label}.date is not canonical")
    require(
        SHA256_RE.fullmatch(source["sha256"]) is not None,
        f"{label}.sha256 must be a lowercase SHA-256 digest",
    )
    return source


def validate_graph_envelope(
    graph: dict[str, Any], label: str, *, allow_extra_sources: bool
) -> None:
    exact_keys(graph, ["version", "metadata", "nodes"], label)
    integer(graph.get("version"), f"{label}.version")
    require(graph["version"] == 2, f"{label}.version must be 2")
    metadata = graph.get("metadata")
    require(type(metadata) is dict, f"{label}.metadata must be an object")
    require("created_at" in metadata, f"{label}.metadata.created_at is required")
    require("last_updated" in metadata, f"{label}.metadata.last_updated is required")
    validate_iso8601(metadata["created_at"], f"{label}.metadata.created_at")
    validate_iso8601(metadata["last_updated"], f"{label}.metadata.last_updated")
    require(
        metadata["created_at"] == EXPECTED_CREATED_AT,
        f"{label}.metadata.created_at must be {EXPECTED_CREATED_AT}",
    )
    nodes = graph.get("nodes")
    require(type(nodes) is dict, f"{label}.nodes must be an object")

    graph_sources = metadata.get("sources")
    require(type(graph_sources) is list, f"{label}.metadata.sources must be an array")
    canonical_sources = expected_graph_sources()
    if not allow_extra_sources:
        require(
            len(graph_sources) == len(canonical_sources),
            f"{label} must name exactly the two canonical exercise sources",
        )
        for index, source in enumerate(graph_sources):
            validate_graph_source_record(source, f"{label} source {index}")
        require(
            graph_sources == canonical_sources,
            f"{label} source metadata is not canonical",
        )
        return

    by_file: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(graph_sources):
        source = validate_graph_source_record(source, f"{label} source {index}")
        source_file = source["file"]
        require(
            source_file not in by_file, f"{label} repeats source file {source_file!r}"
        )
        by_file[source_file] = source
    for expected in canonical_sources:
        source_file = expected["file"]
        require(
            source_file in by_file, f"{label} omits canonical source {source_file!r}"
        )
        actual = by_file[source_file]
        require(
            actual == expected,
            f"{label} canonical source {source_file!r} has changed metadata",
        )


def validate_phase1_anchor_block(coverage: dict[str, Any]) -> None:
    anchor = coverage.get("phase1_graph")
    exact_keys(anchor, PHASE1_GRAPH_KEYS, "phase1_graph")
    nonempty_string(anchor["file"], "phase1_graph.file")
    nonempty_string(anchor["sha256"], "phase1_graph.sha256")
    require(
        anchor["file"] == EXPECTED_PHASE1_GRAPH_FILE,
        f"phase1_graph.file must be {EXPECTED_PHASE1_GRAPH_FILE!r}",
    )
    require(
        anchor["sha256"] == EXPECTED_PHASE1_GRAPH_SHA256,
        "phase1_graph.sha256 does not match the frozen Phase 1 graph",
    )


def verify_phase1_artifacts(
    coverage: dict[str, Any],
    schema_version: int,
    phase1_graph_path: Path,
    repository: Path,
) -> None:
    expected_path = (repository / EXPECTED_PHASE1_GRAPH_FILE).resolve()
    require(
        phase1_graph_path.resolve() == expected_path,
        f"Phase 1 graph path must resolve to {expected_path}",
    )
    actual_hash = sha256_file(phase1_graph_path)
    require(
        actual_hash == EXPECTED_PHASE1_GRAPH_SHA256,
        f"Phase 1 graph has SHA-256 {actual_hash}, expected {EXPECTED_PHASE1_GRAPH_SHA256}",
    )
    if schema_version == 2:
        validate_phase1_anchor_block(coverage)

    attestation = read_json(
        repository / EXPECTED_PHASE1_ATTESTATION_FILE, "Phase 1 review attestation"
    )
    artifact = attestation.get("artifact")
    require(type(artifact) is dict, "Phase 1 attestation.artifact must be an object")
    require(
        artifact.get("path") == EXPECTED_PHASE1_GRAPH_FILE,
        "Phase 1 attestation names a different graph artifact",
    )
    require(
        artifact.get("sha256") == EXPECTED_PHASE1_GRAPH_SHA256,
        "Phase 1 attestation has a different graph digest",
    )


def validate_sources(
    coverage: dict[str, Any],
    graph: dict[str, Any],
    phase1_graph: dict[str, Any],
    repository: Path,
    *,
    verify_local_sources: bool,
) -> None:
    sources = coverage.get("sources")
    exact_keys(sources, list(EXPECTED_SOURCES), "coverage sources")
    for source_name, expected in EXPECTED_SOURCES.items():
        source = sources[source_name]
        exact_keys(source, SOURCE_KEYS, f"coverage source {source_name}")
        for field in SOURCE_KEYS:
            nonempty_string(source[field], f"coverage source {source_name}.{field}")
        require(source == expected, f"coverage source {source_name} is not canonical")

    manifest = read_json(repository / "sources" / "manifest.json", "source manifest")
    manifest_sources = manifest.get("sources")
    require(type(manifest_sources) is list, "source manifest.sources must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(manifest_sources):
        require(
            type(source) is dict, f"source manifest entry {index} must be an object"
        )
        source_id = nonempty_string(
            source.get("id"), f"source manifest entry {index}.id"
        )
        require(source_id not in by_id, f"duplicate source manifest id {source_id!r}")
        by_id[source_id] = source

    for source_name, expected in EXPECTED_SOURCES.items():
        source_id = expected["id"]
        require(source_id in by_id, f"source manifest omits {source_id!r}")
        manifest_source = by_id[source_id]
        required_manifest_fields = {
            "title": expected["title"],
            "title_page_date": expected["date"],
            "local_file": expected["local_file"],
            "format": expected["format"],
            "sha256": expected["sha256"],
        }
        for field, expected_value in required_manifest_fields.items():
            actual = nonempty_string(
                manifest_source.get(field), f"source manifest {source_id}.{field}"
            )
            require(
                actual == expected_value,
                f"source manifest {source_id}.{field} differs from the coverage source",
            )

        local_path = (repository / expected["local_file"]).resolve()
        try:
            local_path.relative_to(repository.resolve())
        except ValueError as error:
            raise CoverageError(
                f"source {source_name} local_file escapes the repository"
            ) from error
        if verify_local_sources and local_path.exists():
            require(local_path.is_file(), f"local source {local_path} is not a file")
            require(
                local_path.suffix.lower() == ".pdf",
                f"local source {local_path} is not a PDF",
            )
            require(
                sha256_file(local_path) == expected["sha256"],
                f"local source {local_path} has the wrong SHA-256 digest",
            )

    validate_graph_envelope(graph, "live graph", allow_extra_sources=True)
    validate_graph_envelope(phase1_graph, "Phase 1 graph", allow_extra_sources=False)


def validate_page_range(value: Any, label: str, *, optional: bool = False) -> None:
    if value is None:
        require(optional, f"{label} may not be null")
        return
    require(
        type(value) is list and len(value) == 2, f"{label} must be a two-page array"
    )
    start = integer(value[0], f"{label}[0]")
    end = integer(value[1], f"{label}[1]")
    require(start <= end, f"{label} must be an increasing page range")


def validate_chapters(coverage: dict[str, Any]) -> None:
    chapters = coverage.get("chapters")
    require(type(chapters) is dict, "chapters must be an object")
    require(
        list(chapters) == list(EXPECTED_CHAPTERS),
        "chapter keys must be the ordered strings 1 through 15",
    )
    for chapter, metadata in chapters.items():
        exact_keys(metadata, CHAPTER_KEYS, f"chapter {chapter}")
        exercise_range = metadata["exercise_range"]
        require(
            type(exercise_range) is list and len(exercise_range) == 2,
            f"chapter {chapter}.exercise_range must be a two-ID array",
        )
        for index, identifier in enumerate(exercise_range):
            nonempty_string(identifier, f"chapter {chapter}.exercise_range[{index}]")
        integer(metadata["count"], f"chapter {chapter}.count")
        validate_page_range(
            metadata["book_printed_pages"], f"chapter {chapter}.book_printed_pages"
        )
        validate_page_range(
            metadata["supplement_printed_pages"],
            f"chapter {chapter}.supplement_printed_pages",
            optional=int(chapter) >= 10,
        )
    require(
        chapters == EXPECTED_CHAPTERS,
        "chapter counts or page metadata differ from the audit",
    )


def build_exercise_inventory(
    coverage: dict[str, Any], coarse_graph: dict[str, Any], graph_label: str
) -> ExerciseInventory:
    expected_ids = expected_exercise_ids()
    expected_id_set = set(expected_ids)
    require(len(expected_ids) == 209, "internal expected exercise count is not 209")
    require(
        sum(EXPECTED_CHAPTERS[str(chapter)]["count"] for chapter in range(1, 10))
        == 155,
        "internal supplement exercise count is not 155",
    )

    exercises = coverage.get("exercises")
    require(type(exercises) is dict, "exercises must be an object keyed by exercise ID")
    require(
        len(exercises) == 209, f"expected 209 exercise entries, found {len(exercises)}"
    )
    require(
        set(exercises) == expected_id_set,
        "exercise ID set does not match the 209 book IDs",
    )
    require(
        list(exercises) == expected_ids,
        "exercise entries are not in deterministic numeric order",
    )

    nodes = coarse_graph.get("nodes")
    require(type(nodes) is dict, f"{graph_label}.nodes must be an object")
    member_locations: dict[str, list[str]] = defaultdict(list)
    for owner, node in nodes.items():
        nonempty_string(owner, f"{graph_label} node key")
        require(type(node) is dict, f"{graph_label} node {owner!r} must be an object")
        require(
            node.get("id") == owner,
            f"{graph_label} node key {owner!r} differs from its id",
        )
        tier = integer(node.get("tier"), f"{graph_label} node {owner!r} tier")
        if tier != 1:
            continue
        members = node.get("provisional_members")
        require(
            type(members) is list, f"{graph_label} node {owner!r} has no member list"
        )
        for member in members:
            nonempty_string(member, f"{graph_label} node {owner!r} provisional member")
            member_locations[member].append(owner)
        require(
            len(members) == len(set(members)),
            f"{graph_label} node {owner!r} repeats a provisional member",
        )
    for member, owners in member_locations.items():
        require(
            len(owners) == 1,
            f"{graph_label} provisional member {member!r} is reused under owners {owners!r}",
        )

    mapped_by_location: dict[tuple[str, str], set[str]] = defaultdict(set)
    obligations: dict[str, dict[str, Any]] = {}
    book_count = 0
    supplement_count = 0
    multipart_count = 0

    for exercise_id in expected_ids:
        record = exercises[exercise_id]
        exact_keys(record, EXERCISE_KEYS, f"exercise {exercise_id}")

        owner = record["owner"]
        members = record["members"]
        present_in = record["present_in"]
        nonempty_string(owner, f"exercise {exercise_id}.owner")
        require(
            owner in nodes,
            f"exercise {exercise_id} owner {owner!r} is absent from the graph",
        )
        owner_node = nodes[owner]
        tier = integer(owner_node.get("tier"), f"exercise {exercise_id} owner tier")
        require(tier == 1, f"exercise {exercise_id} owner {owner!r} is not tier 1")
        require(
            owner_node.get("parent") is None,
            f"exercise {exercise_id} tier-1 owner {owner!r} must have null parent",
        )
        require(
            type(members) is list and members,
            f"exercise {exercise_id} must have at least one representing member",
        )
        for index, member in enumerate(members):
            nonempty_string(member, f"exercise {exercise_id}.members[{index}]")
        require(
            len(members) == len(set(members)),
            f"exercise {exercise_id} repeats a representing member",
        )
        expected_members = [
            member
            for member in owner_node["provisional_members"]
            if exercise_id in explicit_exercise_ids(member)
        ]
        require(
            members == expected_members,
            f"exercise {exercise_id}.members must equal its ordered Phase 1 members "
            f"{expected_members!r}",
        )

        chapter = int(exercise_id.split(".", maxsplit=1)[0])
        expected_presence = {"book": True, "supplement": chapter <= 9}
        exact_keys(present_in, PRESENCE_KEYS, f"exercise {exercise_id}.present_in")
        for source_name in PRESENCE_KEYS:
            require(
                type(present_in[source_name]) is bool,
                f"exercise {exercise_id}.present_in.{source_name} must be a boolean",
            )
        require(
            present_in == expected_presence,
            f"exercise {exercise_id} has incorrect source presence {present_in!r}",
        )
        book_count += int(present_in["book"])
        supplement_count += int(present_in["supplement"])

        if len(members) > 1:
            multipart_count += 1
        for member in members:
            locations = member_locations.get(member, [])
            require(
                locations,
                f"exercise {exercise_id} member {member!r} is absent from the graph",
            )
            require(
                locations == [owner],
                f"exercise {exercise_id} member {member!r} occurs under {locations!r}, not only {owner!r}",
            )
            mapped_by_location[(owner, member)].add(exercise_id)
            if member not in obligations:
                obligations[member] = {"owner": owner, "exercise_ids": [exercise_id]}
            else:
                require(
                    obligations[member]["owner"] == owner,
                    f"member {member!r} is shared across exercise owners",
                )
                obligations[member]["exercise_ids"].append(exercise_id)

    require(book_count == 209, f"expected 209 book obligations, found {book_count}")
    require(
        supplement_count == 155,
        f"expected 155 supplement obligations, found {supplement_count}",
    )

    explicit_id_count = 0
    explicit_link_count = 0
    shared_explicit_members = 0
    for member, owners in member_locations.items():
        explicit_ids = explicit_exercise_ids(member)
        if not explicit_ids:
            continue
        require(
            explicit_ids <= expected_id_set,
            f"member {member!r} names an unknown exercise ID",
        )
        explicit_link_count += 1
        for owner in owners:
            mapped_ids = mapped_by_location.get((owner, member), set())
            require(
                mapped_ids == explicit_ids,
                f"explicit IDs {sorted(explicit_ids)!r} in {owner!r}: {member!r} "
                f"do not match matrix IDs {sorted(mapped_ids)!r}",
            )
        explicit_id_count += len(explicit_ids)
        shared_explicit_members += int(len(explicit_ids) > 1)

    for (owner, member), exercise_ids in mapped_by_location.items():
        explicit_ids = explicit_exercise_ids(member)
        require(
            explicit_ids,
            f"mapped graph link {owner!r}: {member!r} has no explicit exercise marker",
        )
        require(
            explicit_ids == exercise_ids,
            f"mapped graph link {owner!r}: {member!r} names IDs "
            f"{sorted(explicit_ids, key=exercise_sort_key)!r}, expected "
            f"{sorted(exercise_ids, key=exercise_sort_key)!r}",
        )
        require(
            all(
                exercises[exercise_id]["owner"] == owner for exercise_id in exercise_ids
            ),
            f"member {member!r} is shared across exercise owners",
        )

    require(
        multipart_count == 13,
        f"expected 13 multipart exercises, found {multipart_count}",
    )
    require(
        len(obligations) == 225,
        f"expected 225 normalized obligations, found {len(obligations)}",
    )
    require(
        explicit_link_count == 225,
        f"expected 225 explicit links, found {explicit_link_count}",
    )
    require(
        explicit_id_count == 226,
        f"expected 226 explicit ID-links, found {explicit_id_count}",
    )
    require(
        shared_explicit_members == 1,
        f"expected one shared member, found {shared_explicit_members}",
    )
    return ExerciseInventory(
        expected_ids=expected_ids,
        obligations=obligations,
        multipart_count=multipart_count,
        explicit_link_count=explicit_link_count,
        explicit_id_count=explicit_id_count,
        shared_member_count=shared_explicit_members,
    )


def validate_v1_live_scaffold(
    coverage: dict[str, Any], graph: dict[str, Any], expected: ExerciseInventory
) -> None:
    nodes = graph["nodes"]
    for node_id, node in nodes.items():
        require(type(node) is dict, f"live graph node {node_id!r} must be an object")
        tier = integer(node.get("tier"), f"live graph node {node_id!r} tier")
        require(
            tier == 1,
            "schema v1 cannot accompany tier-2 or finer nodes; migrate coverage to schema v2 first",
        )
    live = build_exercise_inventory(coverage, graph, "live graph")
    require(
        live.obligations == expected.obligations,
        "live Phase 1 exercise ownership differs from the immutable snapshot",
    )


def exercise_source_files(
    exercise_id: str, exercises: dict[str, dict[str, Any]]
) -> list[str]:
    present = exercises[exercise_id]["present_in"]
    files = [EXPECTED_SOURCES["book"]["local_file"]]
    if present["supplement"]:
        files.append(EXPECTED_SOURCES["supplement"]["local_file"])
    return files


def validate_mapping_traceability(
    member: str,
    exercise_ids: list[str],
    target_nodes: list[tuple[str, dict[str, Any]]],
    exercises: dict[str, dict[str, Any]],
) -> None:
    required_pairs = {
        (exercise_id, source_file)
        for exercise_id in exercise_ids
        for source_file in exercise_source_files(exercise_id, exercises)
    }
    canonical_source_files = {
        source["local_file"] for source in EXPECTED_SOURCES.values()
    }
    allowed_exercise_ids = set(exercise_ids)
    found_pairs: set[tuple[str, str]] = set()
    for node_id, node in target_nodes:
        refs = node.get("source_refs")
        require(
            type(refs) is list,
            f"mapped tier-2 node {node_id!r} must have a source_refs array",
        )
        target_traced = False
        for index, ref in enumerate(refs):
            require(
                type(ref) is dict,
                f"mapped tier-2 node {node_id!r} source_refs[{index}] must be an object",
            )
            source_file = ref.get("file")
            location = ref.get("location")
            if type(source_file) is not str or type(location) is not str:
                continue
            if source_file not in canonical_source_files:
                continue
            named_ids = source_exercise_ids(location)
            extra_ids = sorted(named_ids - allowed_exercise_ids, key=exercise_sort_key)
            require(
                not extra_ids,
                f"mapped tier-2 node {node_id!r} canonical source reference names "
                f"exercise IDs outside obligation {member!r}: {extra_ids!r}",
            )
            for named_id in sorted(named_ids, key=exercise_sort_key):
                require(
                    source_file in exercise_source_files(named_id, exercises),
                    f"mapped tier-2 node {node_id!r} cites Exercise {named_id} in "
                    f"source {source_file!r}, where that exercise is not present",
                )
            for exercise_id, expected_file in required_pairs:
                if source_file == expected_file and exercise_id in named_ids:
                    found_pairs.add((exercise_id, expected_file))
                    target_traced = True
        require(
            target_traced,
            f"mapped tier-2 node {node_id!r} has no exact source reference for obligation {member!r}",
        )
    missing_pairs = sorted(required_pairs - found_pairs)
    require(
        not missing_pairs,
        f"fine obligation {member!r} lacks exact exercise provenance {missing_pairs!r}",
    )


def validate_fine_obligations(
    coverage: dict[str, Any],
    graph: dict[str, Any],
    inventory: ExerciseInventory,
    *,
    require_owner_complete: list[str],
    require_fine_complete: bool,
) -> ValidationResult:
    fine_obligations = coverage.get("fine_obligations")
    exact_keys(
        fine_obligations,
        list(inventory.obligations),
        "fine_obligations",
    )
    nodes = graph["nodes"]
    exercises = coverage["exercises"]
    target_owner: dict[str, str] = {}
    pending_members: list[str] = []
    mapped_count = 0

    for member, expected in inventory.obligations.items():
        record = fine_obligations[member]
        exact_keys(record, FINE_OBLIGATION_KEYS, f"fine obligation {member!r}")
        owner = nonempty_string(record["owner"], f"fine obligation {member!r}.owner")
        require(
            owner == expected["owner"],
            f"fine obligation {member!r} owner must remain {expected['owner']!r}",
        )
        exercise_ids = unique_string_list(
            record["exercise_ids"],
            f"fine obligation {member!r}.exercise_ids",
            allow_empty=False,
        )
        require(
            exercise_ids == expected["exercise_ids"],
            f"fine obligation {member!r} exercise_ids must be {expected['exercise_ids']!r}",
        )

        require(owner in nodes, f"fine obligation {member!r} owner {owner!r} is absent")
        owner_node = nodes[owner]
        require(
            type(owner_node) is dict,
            f"fine obligation owner {owner!r} is not an object",
        )
        require(
            integer(owner_node.get("tier"), f"fine obligation owner {owner!r} tier")
            == 1,
            f"fine obligation owner {owner!r} is not tier 1",
        )
        require(
            owner_node.get("parent") is None,
            f"fine obligation owner {owner!r} must have null parent",
        )

        mapping = record["mapping"]
        exact_keys(mapping, FINE_MAPPING_KEYS, f"fine obligation {member!r}.mapping")
        status = nonempty_string(
            mapping["status"], f"fine obligation {member!r}.status"
        )
        require(
            status in FINE_MAPPING_STATUSES,
            f"fine obligation {member!r} status must be pending or mapped",
        )
        target_ids = unique_string_list(
            mapping["tier2_node_ids"], f"fine obligation {member!r}.tier2_node_ids"
        )
        require(
            target_ids == sorted(target_ids),
            f"fine obligation {member!r} tier2_node_ids must be lexicographically ordered",
        )
        if status == "pending":
            require(
                not target_ids,
                f"pending fine obligation {member!r} must have no tier-2 node IDs",
            )
            pending_members.append(member)
            continue

        require(
            target_ids, f"mapped fine obligation {member!r} must name a tier-2 node"
        )
        target_nodes: list[tuple[str, dict[str, Any]]] = []
        for node_id in target_ids:
            require(
                node_id not in target_owner,
                f"tier-2 node {node_id!r} is reused by obligations "
                f"{target_owner.get(node_id)!r} and {member!r}",
            )
            require(
                node_id in nodes,
                f"fine obligation {member!r} names absent tier-2 node {node_id!r}",
            )
            node = nodes[node_id]
            require(
                type(node) is dict, f"mapped tier-2 node {node_id!r} must be an object"
            )
            require(
                node.get("id") == node_id,
                f"mapped node key {node_id!r} differs from its id",
            )
            require(
                integer(node.get("tier"), f"mapped node {node_id!r} tier") == 2,
                f"mapped node {node_id!r} must be tier 2",
            )
            require(
                node.get("parent") == owner,
                f"mapped node {node_id!r} has parent {node.get('parent')!r}, expected {owner!r}",
            )
            target_owner[node_id] = member
            target_nodes.append((node_id, node))
        validate_mapping_traceability(member, exercise_ids, target_nodes, exercises)
        mapped_count += 1

    requested_owners = unique_string_list(
        require_owner_complete, "--require-owner-complete values"
    )
    known_owners = {record["owner"] for record in inventory.obligations.values()}
    for owner in requested_owners:
        require(
            owner in known_owners,
            f"--require-owner-complete names non-exercise owner {owner!r}",
        )
        owner_pending = [
            member
            for member in pending_members
            if inventory.obligations[member]["owner"] == owner
        ]
        require(
            not owner_pending,
            f"owner {owner!r} has {len(owner_pending)} pending fine obligation(s): "
            f"{owner_pending[:5]!r}",
        )

    if require_fine_complete:
        require(
            not pending_members,
            f"final fine coverage has {len(pending_members)} pending obligation(s): "
            f"{pending_members[:5]!r}",
        )

    complete_exercises = sum(
        all(
            fine_obligations[member]["mapping"]["status"] == "mapped"
            for member in record["members"]
        )
        for record in exercises.values()
    )
    pending_exercises = len(exercises) - complete_exercises
    if require_fine_complete:
        require(
            complete_exercises == 209,
            f"final fine coverage completes only {complete_exercises}/209 exercises",
        )
    pending_count = len(pending_members)
    return ValidationResult(
        schema_version=2,
        obligation_count=len(inventory.obligations),
        mapped_obligations=mapped_count,
        pending_obligations=pending_count,
        complete_exercises=complete_exercises,
        pending_exercises=pending_exercises,
        summary=(
            "PASS: schema v2; 209 exercises across 15 chapters; "
            f"{mapped_count}/225 fine obligations mapped and {pending_count} pending; "
            f"{complete_exercises}/209 exercises complete and {pending_exercises} pending; "
            f"{inventory.multipart_count} multipart exercises; "
            f"{inventory.shared_member_count} shared obligation"
        ),
    )


def validate_documents(
    coverage: dict[str, Any],
    graph: dict[str, Any],
    phase1_graph: dict[str, Any],
    repository: Path,
    *,
    require_owner_complete: list[str] | None = None,
    require_fine_complete: bool = False,
    verify_local_sources: bool = True,
) -> ValidationResult:
    schema_version = integer(coverage.get("schema_version"), "schema_version")
    require(schema_version in {1, 2}, "schema_version must be 1 or 2")
    exact_keys(
        coverage,
        COVERAGE_V1_KEYS if schema_version == 1 else COVERAGE_V2_KEYS,
        "coverage matrix",
    )
    if schema_version == 2:
        validate_phase1_anchor_block(coverage)

    validate_sources(
        coverage,
        graph,
        phase1_graph,
        repository,
        verify_local_sources=verify_local_sources,
    )
    validate_chapters(coverage)
    inventory = build_exercise_inventory(coverage, phase1_graph, "Phase 1 graph")
    requested_owners = list(require_owner_complete or [])

    if schema_version == 1:
        require(
            not requested_owners,
            "--require-owner-complete requires coverage schema v2",
        )
        require(
            not require_fine_complete,
            "--require-fine-complete requires coverage schema v2",
        )
        validate_v1_live_scaffold(coverage, graph, inventory)
        return ValidationResult(
            schema_version=1,
            obligation_count=len(inventory.obligations),
            mapped_obligations=0,
            pending_obligations=len(inventory.obligations),
            complete_exercises=0,
            pending_exercises=209,
            summary=(
                "PASS: schema v1 Phase 1 scaffold; 209 exercises across 15 chapters; "
                f"{inventory.multipart_count} multipart exercises; "
                f"{inventory.explicit_link_count} explicit coarse links carrying "
                f"{inventory.explicit_id_count} ID-links; "
                f"{inventory.shared_member_count} shared member"
            ),
        )

    return validate_fine_obligations(
        coverage,
        graph,
        inventory,
        require_owner_complete=requested_owners,
        require_fine_complete=require_fine_complete,
    )


def validate(
    coverage_path: Path,
    graph_path: Path,
    phase1_graph_path: Path,
    *,
    require_owner_complete: list[str] | None = None,
    require_fine_complete: bool = False,
) -> ValidationResult:
    repository = Path(__file__).resolve().parents[1]
    coverage = read_json(coverage_path, "coverage matrix")
    graph = read_json(graph_path, "live graph")
    phase1_graph = read_json(phase1_graph_path, "Phase 1 graph")
    schema_version = integer(coverage.get("schema_version"), "schema_version")
    require(schema_version in {1, 2}, "schema_version must be 1 or 2")
    verify_phase1_artifacts(coverage, schema_version, phase1_graph_path, repository)
    return validate_documents(
        coverage,
        graph,
        phase1_graph,
        repository,
        require_owner_complete=require_owner_complete,
        require_fine_complete=require_fine_complete,
    )


def migrate_v1_document(
    coverage: dict[str, Any], phase1_graph: dict[str, Any]
) -> dict[str, Any]:
    """Return the deterministic all-pending schema-v2 form of a v1 matrix."""
    require(coverage.get("schema_version") == 1, "migration input must use schema v1")
    exact_keys(coverage, COVERAGE_V1_KEYS, "migration input")
    inventory = build_exercise_inventory(coverage, phase1_graph, "Phase 1 graph")
    migrated = copy.deepcopy(coverage)
    migrated["schema_version"] = 2
    migrated["phase1_graph"] = {
        "file": EXPECTED_PHASE1_GRAPH_FILE,
        "sha256": EXPECTED_PHASE1_GRAPH_SHA256,
    }
    migrated["fine_obligations"] = {
        member: {
            "owner": record["owner"],
            "exercise_ids": list(record["exercise_ids"]),
            "mapping": {"status": "pending", "tier2_node_ids": []},
        }
        for member, record in inventory.obligations.items()
    }
    return migrated


def add_test_target(
    coverage: dict[str, Any],
    graph: dict[str, Any],
    member: str,
    node_id: str,
    *,
    parent: str | None = None,
    tier: int = 2,
    refs: list[dict[str, str]] | None = None,
) -> None:
    obligation = coverage["fine_obligations"][member]
    owner = obligation["owner"] if parent is None else parent
    require(
        node_id not in graph["nodes"], f"test target {node_id!r} collides with fixture"
    )
    if refs is None:
        refs = [
            {"file": source_file, "location": f"Exercise {exercise_id}"}
            for exercise_id in obligation["exercise_ids"]
            for source_file in exercise_source_files(exercise_id, coverage["exercises"])
        ]
    graph["nodes"][node_id] = {
        "id": node_id,
        "tier": tier,
        "parent": owner,
        "source_refs": refs,
    }


def map_test_obligation(
    coverage: dict[str, Any],
    graph: dict[str, Any],
    member: str,
    node_ids: list[str],
) -> None:
    for node_id in node_ids:
        add_test_target(coverage, graph, member, node_id)
    coverage["fine_obligations"][member]["mapping"] = {
        "status": "mapped",
        "tier2_node_ids": list(node_ids),
    }


def run_self_test() -> str:
    repository = Path(__file__).resolve().parents[1]
    raw_coverage = read_json(
        repository / "sources" / "exercise_coverage.json", "coverage"
    )
    phase1_path = repository / EXPECTED_PHASE1_GRAPH_FILE
    phase1_graph = read_json(phase1_path, "Phase 1 graph")
    raw_schema_version = integer(raw_coverage.get("schema_version"), "schema_version")
    verify_phase1_artifacts(raw_coverage, raw_schema_version, phase1_path, repository)
    v1_fixture = {key: copy.deepcopy(raw_coverage[key]) for key in COVERAGE_V1_KEYS}
    v1_fixture["schema_version"] = 1
    base = migrate_v1_document(v1_fixture, phase1_graph)
    live_graph = copy.deepcopy(phase1_graph)

    case_count = 0

    def check(
        coverage: dict[str, Any],
        graph: dict[str, Any],
        *,
        owners: list[str] | None = None,
        final: bool = False,
    ) -> ValidationResult:
        return validate_documents(
            coverage,
            graph,
            phase1_graph,
            repository,
            require_owner_complete=owners,
            require_fine_complete=final,
            verify_local_sources=False,
        )

    def passes(name: str, action: Any) -> Any:
        nonlocal case_count
        case_count += 1
        try:
            return action()
        except CoverageError as error:
            raise AssertionError(
                f"self-test {name!r} unexpectedly failed: {error}"
            ) from error

    def fails(name: str, needle: str, action: Any) -> None:
        nonlocal case_count
        case_count += 1
        try:
            action()
        except CoverageError as error:
            require(
                needle in str(error),
                f"self-test {name!r} expected {needle!r}, got {str(error)!r}",
            )
            return
        raise AssertionError(f"self-test {name!r} unexpectedly passed")

    def check_source_citation_parser() -> None:
        require(
            source_exercise_ids("Exercises 13.1-13.3") == {"13.1", "13.2", "13.3"},
            "hyphenated exercise range did not expand",
        )
        require(
            source_exercise_ids("Exercises 13.1\u201313.3 and 13.5")
            == {"13.1", "13.2", "13.3", "13.5"},
            "en-dash exercise range/list did not expand",
        )
        require(
            source_exercise_ids("Exercise 1.1.2") == set(),
            "three-component identifier was accepted as Exercise 1.1",
        )
        require(
            source_exercise_ids("Chapter 1, Section 1.2, Exercise 1.9") == {"1.9"},
            "bare section number leaked into the exercise citation",
        )

    passes(
        "source citation lists, ranges, and boundaries", check_source_citation_parser
    )
    fails(
        "cross-chapter exercise range",
        "must stay within one chapter",
        lambda: source_exercise_ids("Exercises 13.1-14.2"),
    )
    fails(
        "out-of-inventory exercise citation",
        "unknown ID",
        lambda: source_exercise_ids("Exercise 1.30"),
    )
    fails(
        "huge exercise range endpoint",
        "unknown ID",
        lambda: source_exercise_ids("Exercises 1.1-1.1000000000"),
    )

    v1 = {key: copy.deepcopy(base[key]) for key in COVERAGE_V1_KEYS}
    v1["schema_version"] = 1
    passes("schema v1 scaffold", lambda: check(v1, copy.deepcopy(live_graph)))
    fails(
        "schema v1 final mode",
        "requires coverage schema v2",
        lambda: check(v1, copy.deepcopy(live_graph), final=True),
    )
    v1_graph = copy.deepcopy(live_graph)
    first_member = next(iter(base["fine_obligations"]))
    add_test_target(base, v1_graph, first_member, "Unexpected tier-2 node")
    fails(
        "schema v1 with tier 2",
        "migrate coverage to schema v2",
        lambda: check(v1, v1_graph),
    )

    pending = passes(
        "schema v2 all pending",
        lambda: check(copy.deepcopy(base), copy.deepcopy(live_graph)),
    )
    require(pending.pending_obligations == 225, "self-test pending count is wrong")
    fails(
        "all pending final mode",
        "225 pending obligation",
        lambda: check(copy.deepcopy(base), copy.deepcopy(live_graph), final=True),
    )

    bad = copy.deepcopy(base)
    bad["phase1_graph"]["sha256"] = "0" * 64
    fails(
        "altered Phase 1 anchor", "frozen Phase 1 graph", lambda: check(bad, live_graph)
    )

    bad = copy.deepcopy(base)
    bad["schema_version"] = True
    fails(
        "boolean schema version", "must be an integer", lambda: check(bad, live_graph)
    )

    bad = copy.deepcopy(base)
    bad["unexpected"] = None
    fails(
        "extra top-level field", "keys must be exactly", lambda: check(bad, live_graph)
    )

    bad = copy.deepcopy(base)
    bad["fine_obligations"].pop(first_member)
    fails("missing obligation", "fine_obligations keys", lambda: check(bad, live_graph))

    bad = copy.deepcopy(base)
    items = list(bad["fine_obligations"].items())
    items[0], items[1] = items[1], items[0]
    bad["fine_obligations"] = dict(items)
    fails(
        "reordered obligations", "fine_obligations keys", lambda: check(bad, live_graph)
    )

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["owner"] = "Wrong owner"
    fails("wrong immutable owner", "owner must remain", lambda: check(bad, live_graph))

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["exercise_ids"] = ["1.2"]
    fails(
        "wrong shared identity", "exercise_ids must be", lambda: check(bad, live_graph)
    )

    bad = copy.deepcopy(base)
    bad["exercises"]["4.9"]["members"][0], bad["exercises"]["4.9"]["members"][1] = (
        bad["exercises"]["4.9"]["members"][1],
        bad["exercises"]["4.9"]["members"][0],
    )
    fails(
        "reordered coarse multipart members",
        "ordered Phase 1 members",
        lambda: check(bad, live_graph),
    )

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["mapping"] = {
        "status": "pending",
        "tier2_node_ids": ["Absent"],
    }
    fails("pending with targets", "must have no tier-2", lambda: check(bad, live_graph))

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["mapping"]["status"] = "mapped"
    fails("mapped without target", "must name a tier-2", lambda: check(bad, live_graph))

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["mapping"]["status"] = "unknown"
    fails("unknown mapping status", "pending or mapped", lambda: check(bad, live_graph))

    bad = copy.deepcopy(base)
    bad["fine_obligations"][first_member]["mapping"] = {
        "status": "mapped",
        "tier2_node_ids": ["Absent"],
    }
    fails("absent mapped node", "names absent tier-2", lambda: check(bad, live_graph))

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Wrong-tier target"])
    graph["nodes"]["Wrong-tier target"]["tier"] = 1
    fails("wrong target tier", "must be tier 2", lambda: check(bad, graph))

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Wrong-parent target"])
    wrong_parent = next(
        node_id
        for node_id, node in graph["nodes"].items()
        if node["tier"] == 1
        and node_id != bad["fine_obligations"][first_member]["owner"]
    )
    graph["nodes"]["Wrong-parent target"]["parent"] = wrong_parent
    fails("wrong target parent", "expected", lambda: check(bad, graph))

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    add_test_target(bad, graph, first_member, "Duplicate target")
    bad["fine_obligations"][first_member]["mapping"] = {
        "status": "mapped",
        "tier2_node_ids": ["Duplicate target", "Duplicate target"],
    }
    fails(
        "duplicate target in mapping",
        "must not contain duplicates",
        lambda: check(bad, graph),
    )

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    add_test_target(bad, graph, first_member, "A target")
    add_test_target(bad, graph, first_member, "Z target")
    bad["fine_obligations"][first_member]["mapping"] = {
        "status": "mapped",
        "tier2_node_ids": ["Z target", "A target"],
    }
    fails("unsorted target IDs", "lexicographically ordered", lambda: check(bad, graph))

    first_owner = base["fine_obligations"][first_member]["owner"]
    same_owner_members = [
        member
        for member, record in base["fine_obligations"].items()
        if record["owner"] == first_owner
    ]
    require(len(same_owner_members) >= 2, "self-test needs two same-owner obligations")
    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, same_owner_members[0], ["Reused target"])
    bad["fine_obligations"][same_owner_members[1]]["mapping"] = {
        "status": "mapped",
        "tier2_node_ids": ["Reused target"],
    }
    fails(
        "cross-obligation reuse", "is reused by obligations", lambda: check(bad, graph)
    )

    good, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(good, graph, first_member, ["Fine target A", "Fine target B"])
    passes("multi-node obligation", lambda: check(good, graph))

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Untraced target"])
    graph["nodes"]["Untraced target"]["source_refs"] = [
        {"file": EXPECTED_SOURCES["book"]["local_file"], "location": "Exercise 1.2"}
    ]
    fails(
        "wrong-exercise mapped target",
        "exercise IDs outside obligation",
        lambda: check(bad, graph),
    )

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Number-only target"])
    graph["nodes"]["Number-only target"]["source_refs"] = [
        {
            "file": EXPECTED_SOURCES["book"]["local_file"],
            "location": "Section 1.1",
        },
        {
            "file": EXPECTED_SOURCES["supplement"]["local_file"],
            "location": "Page 1.1",
        },
    ]
    fails(
        "source number without exercise marker",
        "no exact source reference",
        lambda: check(bad, graph),
    )

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Detached-marker target"])
    graph["nodes"]["Detached-marker target"]["source_refs"] = [
        {
            "file": EXPECTED_SOURCES["book"]["local_file"],
            "location": "Exercise discussion; Section 1.1",
        },
        {
            "file": EXPECTED_SOURCES["supplement"]["local_file"],
            "location": "Exercise appendix; page 1.1",
        },
    ]
    fails(
        "detached exercise marker",
        "no exact source reference",
        lambda: check(bad, graph),
    )

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Book-only target"])
    graph["nodes"]["Book-only target"]["source_refs"] = [
        {"file": EXPECTED_SOURCES["book"]["local_file"], "location": "Exercise 1.1"}
    ]
    fails(
        "missing supplement trace",
        "lacks exact exercise provenance",
        lambda: check(bad, graph),
    )

    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, first_member, ["Cross-obligation citation target"])
    graph["nodes"]["Cross-obligation citation target"]["source_refs"] = [
        {
            "file": source_file,
            "location": "Exercises 1.1 and 1.2",
        }
        for source_file in (
            EXPECTED_SOURCES["book"]["local_file"],
            EXPECTED_SOURCES["supplement"]["local_file"],
        )
    ]
    fails(
        "canonical cross-obligation citation",
        "exercise IDs outside obligation",
        lambda: check(bad, graph),
    )

    book_only_member = base["exercises"]["10.1"]["members"][0]
    bad, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(bad, graph, book_only_member, ["Wrong-source-presence target"])
    graph["nodes"]["Wrong-source-presence target"]["source_refs"].append(
        {
            "file": EXPECTED_SOURCES["supplement"]["local_file"],
            "location": "Exercise 10.1",
        }
    )
    fails(
        "exercise cited in absent canonical source",
        "where that exercise is not present",
        lambda: check(bad, graph),
    )

    good, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(good, graph, first_member, ["External citation target"])
    graph["metadata"]["sources"].append(
        {
            "file": "sources/external-reference.pdf",
            "title": "External Reference",
            "format": "pdf",
            "date": "2026-01-01",
            "sha256": "0" * 64,
        }
    )
    graph["nodes"]["External citation target"]["source_refs"].append(
        {
            "file": "sources/external-reference.pdf",
            "location": "Exercise 20.1",
        }
    )
    passes("external exercise citation ignored", lambda: check(good, graph))

    graph = copy.deepcopy(live_graph)
    graph["metadata"]["sources"].append(
        {
            "file": "sources/external-reference.pdf",
            "title": "External Reference",
            "format": "pdf",
            "date": "2026-01-01",
            "sha256": "0" * 64,
        }
    )
    passes("additional Phase 2 source", lambda: check(copy.deepcopy(base), graph))

    bad_graph = copy.deepcopy(live_graph)
    bad_graph["metadata"]["sources"].append({"file": "../not-a-source", "junk": True})
    fails(
        "malformed additional source",
        "keys must be exactly",
        lambda: check(copy.deepcopy(base), bad_graph),
    )

    bad_graph = copy.deepcopy(live_graph)
    bad_graph["metadata"]["sources"][0]["sha256"] = "0" * 64
    fails(
        "mutated canonical source",
        "has changed metadata",
        lambda: check(base, bad_graph),
    )

    fails(
        "owner checkpoint pending",
        "pending fine obligation",
        lambda: check(
            copy.deepcopy(base), copy.deepcopy(live_graph), owners=[first_owner]
        ),
    )
    owner_complete, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    for index, member in enumerate(same_owner_members):
        map_test_obligation(
            owner_complete, graph, member, [f"Owner target {index:03d}"]
        )
    passes(
        "owner checkpoint complete",
        lambda: check(owner_complete, graph, owners=[first_owner]),
    )
    fails(
        "unknown owner checkpoint",
        "non-exercise owner",
        lambda: check(
            copy.deepcopy(base), copy.deepcopy(live_graph), owners=["No such owner"]
        ),
    )

    shared_member = "Marginal-density calculations (Exercises 14.9 and 14.11)"
    shared, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(
        shared, graph, shared_member, ["Shared marginal-density target"]
    )
    graph["nodes"]["Shared marginal-density target"]["source_refs"] = [
        {
            "file": EXPECTED_SOURCES["book"]["local_file"],
            "location": "Exercises 14.9 and 14.11",
        }
    ]
    shared_result = passes("shared obligation", lambda: check(shared, graph))
    require(
        shared_result.complete_exercises == 1,
        "shared obligation must complete 14.11 but not multipart Exercise 14.9",
    )

    multipart_members = base["exercises"]["4.9"]["members"]
    require(len(multipart_members) == 5, "self-test expected five Exercise 4.9 parts")
    multipart, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(
        multipart, graph, multipart_members[0], ["One multipart target"]
    )
    multipart_result = passes(
        "partial multipart mapping", lambda: check(multipart, graph)
    )
    require(
        multipart_result.complete_exercises == 0,
        "one mapped part must not complete a multipart exercise",
    )

    complete, complete_graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    for index, member in enumerate(complete["fine_obligations"]):
        map_test_obligation(
            complete,
            complete_graph,
            member,
            [f"Fine exercise target {index:03d}"],
        )
    complete_result = passes(
        "all obligations complete", lambda: check(complete, complete_graph, final=True)
    )
    require(
        complete_result.complete_exercises == 209,
        "complete fixture must cover all 209 exercises",
    )

    almost = copy.deepcopy(complete)
    last_member = next(reversed(almost["fine_obligations"]))
    almost["fine_obligations"][last_member]["mapping"] = {
        "status": "pending",
        "tier2_node_ids": [],
    }
    fails(
        "224 of 225 final mapping",
        "1 pending obligation",
        lambda: check(almost, complete_graph, final=True),
    )

    deleted, graph = copy.deepcopy(base), copy.deepcopy(live_graph)
    map_test_obligation(deleted, graph, first_member, ["Deleted target"])
    del graph["nodes"]["Deleted target"]
    fails("deleted mapped target", "names absent tier-2", lambda: check(deleted, graph))

    with tempfile.TemporaryDirectory(prefix="exercise-coverage-self-test-") as raw_tmp:
        duplicate_path = Path(raw_tmp) / "duplicate.json"
        duplicate_path.write_text('{"schema_version": 2, "schema_version": 2}\n')
        fails(
            "duplicate JSON key",
            "duplicate JSON key",
            lambda: read_json(duplicate_path, "duplicate fixture"),
        )
        nonfinite_path = Path(raw_tmp) / "nonfinite.json"
        nonfinite_path.write_text('{"value": NaN}\n')
        fails(
            "non-finite JSON value",
            "non-finite JSON number",
            lambda: read_json(nonfinite_path, "non-finite fixture"),
        )

    return f"PASS: exercise coverage self-test ({case_count} adversarial cases)"


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage",
        type=Path,
        default=repository / "sources" / "exercise_coverage.json",
        help="coverage matrix to validate",
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=repository / "graph.json",
        help="live Autoform graph to validate against",
    )
    parser.add_argument(
        "--phase1-graph",
        type=Path,
        default=repository / EXPECTED_PHASE1_GRAPH_FILE,
        help="immutable, hash-attested Phase 1 graph",
    )
    parser.add_argument(
        "--require-owner-complete",
        action="append",
        default=[],
        metavar="OWNER",
        help="require every fine obligation owned by OWNER to be mapped; repeatable",
    )
    parser.add_argument(
        "--require-fine-complete",
        action="store_true",
        help="require all 225 fine obligations and all 209 exercises to be mapped",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run adversarial schema and mapping tests",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        if arguments.self_test:
            summary = run_self_test()
        else:
            result = validate(
                arguments.coverage,
                arguments.graph,
                arguments.phase1_graph,
                require_owner_complete=arguments.require_owner_complete,
                require_fine_complete=arguments.require_fine_complete,
            )
            summary = result.summary
    except (CoverageError, AssertionError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
