#!/usr/bin/env python3
"""Validate the durable authorization for starting Autoform Phase 2."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import socket
import tempfile
import urllib.parse
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


APPROVAL_FIELDS = {
    "schema_version",
    "approved_at",
    "phase1_graph",
    "decisions",
    "external_source_requirements",
    "user_response",
}
GRAPH_FIELDS = {"path", "sha256"}
DECISION_FIELDS = {
    "phase1_roadmap_approved",
    "external_proof_source_policy",
}
REQUIREMENT_FIELDS = {
    "pin_before_graph_use",
    "required_metadata",
    "axioms_permitted",
    "exact_hypotheses_required",
}
REQUIRED_SOURCE_METADATA = [
    "edition_or_commit",
    "url",
    "retrieval_date",
    "sha256",
]
CANONICAL_USER_RESPONSE = "1. Yes; 2. Yes"
INTERNAL_SOURCE_REFS = {"sources/formalization_notes.md"}
MANIFEST_PIN_FIELDS = {
    "edition_or_commit",
    "url",
    "retrieval_date",
    "sha256",
}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
UTC_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


class DuplicateKeyError(ValueError):
    """JSON repeated a key that the standard decoder would discard."""


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value!r} is forbidden")


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as stream:
            value = json.load(
                stream,
                object_pairs_hook=_object_without_duplicates,
                parse_constant=_reject_nonfinite,
            )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"cannot read {label} {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} {path} must contain a JSON object")
    return value


def _exact_fields(value: Any, expected: set[str], where: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{where}: expected an object"]
    actual = set(value)
    if actual == expected:
        return []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    return [f"{where}: missing fields {missing}; unknown fields {extra}"]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _trimmed_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def _canonical_source_path(value: Any) -> bool:
    if (
        not _trimmed_string(value)
        or "\\" in value
        or "//" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and path.as_posix() == value
        and len(path.parts) >= 2
        and path.parts[0] == "sources"
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _calendar_date(value: Any) -> bool:
    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _primary_url(value: Any) -> bool:
    if not _trimmed_string(value) or any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        return False
    try:
        parsed = urllib.parse.urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or hostname is None:
        return False
    lowered = hostname.rstrip(".").lower()
    if not lowered or lowered == "localhost" or lowered.endswith(
        (
            ".localhost",
            ".invalid",
            ".test",
            ".example",
            ".local",
            ".internal",
            ".onion",
        )
    ):
        return False
    address: ipaddress.IPv4Address | ipaddress.IPv6Address | None = None
    try:
        address = ipaddress.ip_address(lowered)
    except ValueError:
        try:
            address = ipaddress.IPv4Address(socket.inet_aton(lowered))
        except OSError:
            labels = lowered.split(".")
            if len(labels) < 2 or any(
                not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
                for label in labels
            ):
                return False
    else:
        pass
    if address is not None and (not address.is_global or address.is_multicast):
        return False
    return (
        bool(parsed.netloc)
        and parsed.username is None
        and parsed.password is None
    )


def _validate_source_policy(
    live: dict[str, Any], project_root: Path
) -> list[str]:
    errors: list[str] = []
    manifest_path = project_root / "sources" / "manifest.json"
    try:
        manifest = _load_object(manifest_path, "source manifest")
    except ValueError as error:
        return [str(error)]

    manifest_sources = manifest.get("sources")
    if not isinstance(manifest_sources, list) or not manifest_sources:
        return ["source manifest.sources: expected a nonempty array"]

    by_file: dict[str, dict[str, Any]] = {}
    seen_ids: set[str] = set()
    for index, source in enumerate(manifest_sources):
        where = f"source manifest.sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: expected an object")
            continue
        source_id = source.get("id")
        if not _trimmed_string(source_id):
            errors.append(f"{where}.id: expected a nonempty, trimmed string")
        elif source_id in seen_ids:
            errors.append(f"{where}.id: duplicate source id {source_id!r}")
        else:
            seen_ids.add(source_id)

        source_file = source.get("local_file")
        if not _canonical_source_path(source_file):
            errors.append(
                f"{where}.local_file: expected a canonical relative path below sources/"
            )
        elif source_file in by_file:
            errors.append(f"{where}.local_file: duplicate source path {source_file!r}")
        else:
            by_file[source_file] = source

        missing_pins = sorted(MANIFEST_PIN_FIELDS - set(source))
        if missing_pins:
            errors.append(f"{where}: missing pin metadata {missing_pins}")
        if not _trimmed_string(source.get("edition_or_commit")):
            errors.append(f"{where}.edition_or_commit: expected a nonempty string")
        if not _primary_url(source.get("url")):
            errors.append(f"{where}.url: expected an HTTP(S) primary-source URL")
        if not _calendar_date(source.get("retrieval_date")):
            errors.append(f"{where}.retrieval_date: expected a valid YYYY-MM-DD date")
        elif date.fromisoformat(source["retrieval_date"]) > datetime.now(
            timezone.utc
        ).date():
            errors.append(f"{where}.retrieval_date: may not be in the future")
        declared_hash = source.get("sha256")
        if not isinstance(declared_hash, str) or SHA256_RE.fullmatch(declared_hash) is None:
            errors.append(f"{where}.sha256: expected lowercase SHA-256")

        aliases = (
            ("canonical_url", "url"),
            ("retrieved_at", "retrieval_date"),
            ("title_page_date", "edition_or_commit"),
        )
        for alias, canonical in aliases:
            if alias in source and source.get(alias) != source.get(canonical):
                errors.append(
                    f"{where}.{alias}: contradicts policy field {canonical!r}"
                )

        if _canonical_source_path(source_file) and isinstance(declared_hash, str):
            local_path = (project_root / source_file).resolve()
            try:
                local_path.relative_to(project_root.resolve())
            except ValueError:
                errors.append(f"{where}.local_file: resolves outside the project root")
            else:
                if local_path.exists():
                    if not local_path.is_file():
                        errors.append(f"{where}.local_file: expected a regular file")
                    elif SHA256_RE.fullmatch(declared_hash) is not None:
                        try:
                            observed_hash = _sha256(local_path)
                        except OSError as error:
                            errors.append(f"{where}.local_file: cannot hash file: {error}")
                        else:
                            if observed_hash != declared_hash:
                                errors.append(
                                    f"{where}.sha256: declared {declared_hash}, "
                                    f"observed {observed_hash}"
                                )

    metadata = live.get("metadata")
    graph_sources = metadata.get("sources") if isinstance(metadata, dict) else None
    if not isinstance(graph_sources, list) or not graph_sources:
        errors.append("live graph metadata.sources: expected a nonempty array")
        return errors

    registered_files: set[str] = set()
    for index, graph_source in enumerate(graph_sources):
        where = f"live graph metadata.sources[{index}]"
        if not isinstance(graph_source, dict):
            errors.append(f"{where}: expected an object")
            continue
        source_file = graph_source.get("file")
        if not _canonical_source_path(source_file):
            errors.append(
                f"{where}.file: expected a canonical relative path below sources/"
            )
            continue
        if source_file in registered_files:
            errors.append(f"{where}.file: duplicate source path {source_file!r}")
            continue
        registered_files.add(source_file)
        manifest_source = by_file.get(source_file)
        if manifest_source is None:
            errors.append(
                f"{where}.file: source {source_file!r} is not registered in "
                "sources/manifest.json"
            )
            continue
        comparisons = {
            "title": "title",
            "format": "format",
            "sha256": "sha256",
        }
        for graph_field, manifest_field in comparisons.items():
            if graph_source.get(graph_field) != manifest_source.get(manifest_field):
                errors.append(
                    f"{where}.{graph_field}: does not match manifest field "
                    f"{manifest_field!r}"
                )
        graph_date = graph_source.get("date")
        manifest_date = manifest_source.get("title_page_date")
        if manifest_date is not None and graph_date != manifest_date:
            errors.append(f"{where}.date: does not match manifest title_page_date")
        edition = manifest_source.get("edition_or_commit")
        if _calendar_date(edition) and graph_date != edition:
            errors.append(f"{where}.date: does not match manifest edition_or_commit")

    nodes = live.get("nodes")
    if isinstance(nodes, dict):
        for node_id, node in sorted(nodes.items()):
            if not isinstance(node, dict):
                continue
            references = node.get("source_refs")
            if not isinstance(references, list):
                errors.append(
                    f"live graph node {node_id!r}.source_refs: expected an array"
                )
                continue
            for index, reference in enumerate(references):
                if not isinstance(reference, dict):
                    errors.append(
                        f"live graph node {node_id!r}.source_refs[{index}]: "
                        "expected an object"
                    )
                    continue
                if set(reference) != {"file", "location"}:
                    errors.append(
                        f"live graph node {node_id!r}.source_refs[{index}]: "
                        "expected exactly 'file' and 'location' fields"
                    )
                source_file = reference.get("file")
                if not _trimmed_string(reference.get("location")):
                    errors.append(
                        f"live graph node {node_id!r}.source_refs[{index}].location: "
                        "expected a nonempty, trimmed string"
                    )
                if not _canonical_source_path(source_file):
                    errors.append(
                        f"live graph node {node_id!r}.source_refs[{index}].file: "
                        "expected a canonical relative path below sources/"
                    )
                    continue
                if (
                    source_file not in INTERNAL_SOURCE_REFS
                    and source_file not in registered_files
                ):
                    errors.append(
                        f"live graph node {node_id!r}.source_refs[{index}]: "
                        f"external source {source_file!r} is not registered in "
                        "metadata.sources and sources/manifest.json"
                    )
    return errors


def validate(
    approval_path: Path,
    snapshot_path: Path,
    live_graph_path: Path,
    project_root: Path,
) -> list[str]:
    errors: list[str] = []
    try:
        approval = _load_object(approval_path, "approval record")
    except ValueError as error:
        return [str(error)]

    errors.extend(_exact_fields(approval, APPROVAL_FIELDS, "approval"))
    if errors:
        return errors

    version = approval["schema_version"]
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        errors.append("approval.schema_version: expected integer 1")

    approved_datetime: datetime | None = None
    approved_at = approval["approved_at"]
    if not isinstance(approved_at, str) or UTC_RE.fullmatch(approved_at) is None:
        errors.append("approval.approved_at: expected a UTC timestamp ending in Z")
    else:
        try:
            approved_datetime = datetime.fromisoformat(
                approved_at.removesuffix("Z") + "+00:00"
            )
        except ValueError:
            errors.append("approval.approved_at: invalid calendar timestamp")
        else:
            if approved_datetime > datetime.now(timezone.utc):
                errors.append("approval.approved_at: may not be in the future")

    graph_record = approval["phase1_graph"]
    errors.extend(_exact_fields(graph_record, GRAPH_FIELDS, "approval.phase1_graph"))
    if isinstance(graph_record, dict) and set(graph_record) == GRAPH_FIELDS:
        recorded_path = graph_record["path"]
        recorded_hash = graph_record["sha256"]
        canonical_snapshot_path = (
            project_root / "sources" / "phase1_graph.json"
        ).resolve()
        try:
            supplied_snapshot_path = snapshot_path.resolve()
        except OSError as error:
            errors.append(f"phase1 snapshot: cannot resolve {snapshot_path}: {error}")
        else:
            if supplied_snapshot_path != canonical_snapshot_path:
                errors.append(
                    "phase1 snapshot: supplied path does not match "
                    "approval.phase1_graph.path"
                )
        snapshot_path = canonical_snapshot_path
        if recorded_path != "sources/phase1_graph.json":
            errors.append(
                "approval.phase1_graph.path: expected 'sources/phase1_graph.json'"
            )
        if not isinstance(recorded_hash, str) or SHA256_RE.fullmatch(recorded_hash) is None:
            errors.append("approval.phase1_graph.sha256: expected lowercase SHA-256")
        else:
            try:
                actual_hash = _sha256(snapshot_path)
            except OSError as error:
                errors.append(f"phase1 snapshot: cannot hash {snapshot_path}: {error}")
            else:
                if actual_hash != recorded_hash:
                    errors.append(
                        "approval.phase1_graph.sha256: "
                        f"recorded {recorded_hash}, observed {actual_hash}"
                    )

    decisions = approval["decisions"]
    errors.extend(_exact_fields(decisions, DECISION_FIELDS, "approval.decisions"))
    if isinstance(decisions, dict) and set(decisions) == DECISION_FIELDS:
        if decisions["phase1_roadmap_approved"] is not True:
            errors.append("approval.decisions.phase1_roadmap_approved: must be true")
        if decisions["external_proof_source_policy"] != "pinned-primary-sources":
            errors.append(
                "approval.decisions.external_proof_source_policy: "
                "expected 'pinned-primary-sources'"
            )

    requirements = approval["external_source_requirements"]
    errors.extend(
        _exact_fields(
            requirements,
            REQUIREMENT_FIELDS,
            "approval.external_source_requirements",
        )
    )
    if isinstance(requirements, dict) and set(requirements) == REQUIREMENT_FIELDS:
        if requirements["pin_before_graph_use"] is not True:
            errors.append(
                "approval.external_source_requirements.pin_before_graph_use: must be true"
            )
        if requirements["required_metadata"] != REQUIRED_SOURCE_METADATA:
            errors.append(
                "approval.external_source_requirements.required_metadata: expected "
                f"{REQUIRED_SOURCE_METADATA} in canonical order"
            )
        if requirements["axioms_permitted"] is not False:
            errors.append(
                "approval.external_source_requirements.axioms_permitted: must be false"
            )
        if requirements["exact_hypotheses_required"] is not True:
            errors.append(
                "approval.external_source_requirements.exact_hypotheses_required: must be true"
            )

    response = approval["user_response"]
    if response != CANONICAL_USER_RESPONSE:
        errors.append(
            "approval.user_response: expected the canonical affirmative response "
            f"{CANONICAL_USER_RESPONSE!r}"
        )

    try:
        snapshot = _load_object(snapshot_path, "Phase 1 snapshot")
    except ValueError as error:
        errors.append(str(error))
    else:
        metadata = snapshot.get("metadata")
        finalized_at = metadata.get("last_updated") if isinstance(metadata, dict) else None
        if not isinstance(finalized_at, str) or UTC_RE.fullmatch(finalized_at) is None:
            errors.append(
                "Phase 1 snapshot metadata.last_updated: expected a UTC timestamp ending in Z"
            )
        else:
            try:
                finalized_datetime = datetime.fromisoformat(
                    finalized_at.removesuffix("Z") + "+00:00"
                )
            except ValueError:
                errors.append(
                    "Phase 1 snapshot metadata.last_updated: invalid calendar timestamp"
                )
            else:
                if (
                    approved_datetime is not None
                    and approved_datetime < finalized_datetime
                ):
                    errors.append(
                        "approval.approved_at: predates Phase 1 snapshot finalization"
                    )
        nodes = snapshot.get("nodes")
        if not isinstance(nodes, dict) or not nodes:
            errors.append("Phase 1 snapshot: expected a nonempty nodes object")
        else:
            for node_id, node in sorted(nodes.items()):
                if not isinstance(node, dict):
                    errors.append(f"Phase 1 snapshot node {node_id!r}: expected object")
                    continue
                tier = node.get("tier")
                if (
                    not isinstance(tier, int)
                    or isinstance(tier, bool)
                    or tier != 1
                    or node.get("parent") is not None
                ):
                    errors.append(
                        f"Phase 1 snapshot node {node_id!r}: expected a tier-1 root record"
                    )
                if node.get("content") is not None:
                    errors.append(
                        f"Phase 1 snapshot node {node_id!r}: content must remain null"
                    )

    try:
        live = _load_object(live_graph_path, "live graph")
    except ValueError as error:
        errors.append(str(error))
    else:
        errors.extend(_validate_source_policy(live, project_root))
        live_nodes = live.get("nodes")
        if not isinstance(live_nodes, dict) or not live_nodes:
            errors.append("live graph: expected a nonempty nodes object")
        elif any(
            isinstance(node, dict)
            and isinstance(node.get("tier"), int)
            and not isinstance(node.get("tier"), bool)
            and node["tier"] >= 2
            for node in live_nodes.values()
        ) and errors:
            errors.append(
                "live graph contains Phase 2 nodes but its launch authorization is invalid"
            )

    try:
        approval_path.resolve().relative_to(project_root.resolve())
        snapshot_path.resolve().relative_to(project_root.resolve())
        live_graph_path.resolve().relative_to(project_root.resolve())
    except (OSError, ValueError):
        errors.append("approval inputs must resolve inside the project root")

    return sorted(set(errors))


def _fixture(root: Path) -> tuple[Path, Path, Path]:
    sources = root / "sources"
    sources.mkdir()
    primary_path = sources / "primary.pdf"
    primary_path.write_bytes(b"pinned primary source\n")
    primary_hash = _sha256(primary_path)
    graph_source = {
        "file": "sources/primary.pdf",
        "title": "Primary source",
        "format": "pdf",
        "date": "2026-08-03",
        "sha256": primary_hash,
    }
    snapshot = {
        "version": 2,
        "metadata": {
            "created_at": "2026-08-03T08:00:00Z",
            "last_updated": "2026-08-04T08:00:00Z",
            "sources": [graph_source],
        },
        "nodes": {
            "Root": {
                "id": "Root",
                "tier": 1,
                "parent": None,
                "content": None,
                "source_refs": [
                    {"file": "sources/primary.pdf", "location": "Theorem 1"}
                ],
            }
        },
    }
    manifest = {
        "sources": [
            {
                "id": "primary-2026-08-03",
                "title": "Primary source",
                "local_file": "sources/primary.pdf",
                "format": "pdf",
                "title_page_date": "2026-08-03",
                "edition_or_commit": "2026-08-03",
                "canonical_url": "https://example.org/primary.pdf",
                "url": "https://example.org/primary.pdf",
                "retrieved_at": "2026-08-04",
                "retrieval_date": "2026-08-04",
                "sha256": primary_hash,
            }
        ]
    }
    (sources / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    snapshot_path = sources / "phase1_graph.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    live_path = root / "graph.json"
    live_path.write_text(json.dumps(snapshot), encoding="utf-8")
    approval = {
        "schema_version": 1,
        "approved_at": "2026-08-04T08:16:43Z",
        "phase1_graph": {
            "path": "sources/phase1_graph.json",
            "sha256": _sha256(snapshot_path),
        },
        "decisions": {
            "phase1_roadmap_approved": True,
            "external_proof_source_policy": "pinned-primary-sources",
        },
        "external_source_requirements": {
            "pin_before_graph_use": True,
            "required_metadata": list(REQUIRED_SOURCE_METADATA),
            "axioms_permitted": False,
            "exact_hypotheses_required": True,
        },
        "user_response": "1. Yes; 2. Yes",
    }
    approval_path = sources / "phase2_approval.json"
    approval_path.write_text(json.dumps(approval), encoding="utf-8")
    return approval_path, snapshot_path, live_path


def run_self_tests() -> int:
    passed = True

    def case(name: str, mutate: Any = None, expected: str | None = None) -> None:
        nonlocal passed
        with tempfile.TemporaryDirectory(prefix="phase2-approval-") as directory:
            root = Path(directory)
            approval, snapshot, live = _fixture(root)
            if mutate is not None:
                mutate(approval, snapshot, live)
            errors = validate(approval, snapshot, live, root)
            ok = not errors if expected is None else any(expected in error for error in errors)
            if ok:
                print(f"PASS self-test {name}")
            else:
                passed = False
                print(f"FAIL self-test {name}: {errors}")

    case("accepts the canonical approval record")

    def false_roadmap(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["decisions"]["phase1_roadmap_approved"] = False
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects an unapproved roadmap", false_roadmap, "must be true")

    def wrong_policy(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["decisions"]["external_proof_source_policy"] = "unrestricted"
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects the wrong source policy", wrong_policy, "pinned-primary-sources")

    def negative_response(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["user_response"] = "No"
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects a contradictory response", negative_response, "canonical affirmative")

    def premature_approval(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["approved_at"] = "2026-08-04T07:59:59Z"
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects approval before Phase 1 finalization", premature_approval, "predates")

    def future_approval(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["approved_at"] = "2999-01-01T00:00:00Z"
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects a future approval timestamp", future_approval, "future")

    def unregistered_graph_source(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["metadata"]["sources"].append(
            {
                "file": "sources/unregistered.pdf",
                "title": "Unregistered source",
                "format": "pdf",
                "date": "2026-08-03",
                "sha256": "0" * 64,
            }
        )
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects an unregistered graph source",
        unregistered_graph_source,
        "not registered in sources/manifest.json",
    )

    def incomplete_manifest_pin(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        del value["sources"][0]["url"]
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects incomplete manifest pin metadata",
        incomplete_manifest_pin,
        "missing pin metadata",
    )

    def future_retrieval_date(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["retrieval_date"] = "2999-01-01"
        value["sources"][0]["retrieved_at"] = "2999-01-01"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case("rejects a future retrieval date", future_retrieval_date, "future")

    def nonpublic_source_url(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["url"] = "http://127.0.0.1/primary.pdf"
        value["sources"][0]["canonical_url"] = "http://127.0.0.1/primary.pdf"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case("rejects a non-public source URL", nonpublic_source_url, "primary-source URL")

    def legacy_loopback_source_url(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["url"] = "https://127.1/primary.pdf"
        value["sources"][0]["canonical_url"] = "https://127.1/primary.pdf"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a legacy-numeric loopback source URL",
        legacy_loopback_source_url,
        "primary-source URL",
    )

    def malformed_source_url(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["url"] = "https://[bad"
        value["sources"][0]["canonical_url"] = "https://[bad"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case("rejects a malformed source URL", malformed_source_url, "primary-source URL")

    def private_namespace_source_url(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["url"] = "https://source.local/primary.pdf"
        value["sources"][0]["canonical_url"] = "https://source.local/primary.pdf"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a private-namespace source URL",
        private_namespace_source_url,
        "primary-source URL",
    )

    def control_character_source_url(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        value["sources"][0]["url"] = "https://example.org/\nprimary.pdf"
        value["sources"][0]["canonical_url"] = "https://example.org/\nprimary.pdf"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a control character in a source URL",
        control_character_source_url,
        "primary-source URL",
    )

    def edition_date_mismatch_without_alias(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        manifest_path = live.parent / "sources" / "manifest.json"
        value = json.loads(manifest_path.read_text())
        del value["sources"][0]["title_page_date"]
        value["sources"][0]["edition_or_commit"] = "2026-08-02"
        manifest_path.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a graph-edition date mismatch without legacy metadata",
        edition_date_mismatch_without_alias,
        "edition_or_commit",
    )

    def graph_manifest_hash_mismatch(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["metadata"]["sources"][0]["sha256"] = "0" * 64
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a graph-manifest checksum mismatch",
        graph_manifest_hash_mismatch,
        "does not match manifest",
    )

    def unregistered_external_reference(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["nodes"]["Root"]["source_refs"].append(
            {"file": "sources/external.pdf", "location": "Theorem 2"}
        )
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects an unregistered external source reference",
        unregistered_external_reference,
        "external source 'sources/external.pdf' is not registered",
    )

    def malformed_external_reference(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["nodes"]["Root"]["source_refs"].append(
            {"file": "../external.pdf", "location": "Theorem 2"}
        )
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a malformed external source reference",
        malformed_external_reference,
        "expected a canonical relative path",
    )

    def redundant_slash_source_reference(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["nodes"]["Root"]["source_refs"][0]["file"] = "sources//primary.pdf"
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a redundant-slash source reference",
        redundant_slash_source_reference,
        "expected a canonical relative path",
    )

    def normalized_alias_source_reference(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        value["nodes"]["Root"]["source_refs"][0]["file"] = "./sources/primary.pdf"
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a normalized-alias source reference",
        normalized_alias_source_reference,
        "expected a canonical relative path",
    )

    def missing_source_location(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        value = json.loads(live.read_text())
        del value["nodes"]["Root"]["source_refs"][0]["location"]
        live.write_text(json.dumps(value), encoding="utf-8")

    case(
        "rejects a source reference without a location",
        missing_source_location,
        "expected a nonempty, trimmed string",
    )

    def changed_local_source(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        (live.parent / "sources" / "primary.pdf").write_bytes(b"changed\n")

    case(
        "rejects local source hash drift",
        changed_local_source,
        "observed",
    )

    def absent_but_pinned_source(
        _approval: Path, _snapshot: Path, live: Path
    ) -> None:
        (live.parent / "sources" / "primary.pdf").unlink()

    case(
        "accepts a manifest-pinned source absent from a copyright-clean checkout",
        absent_but_pinned_source,
    )

    def changed_snapshot(_approval: Path, snapshot: Path, _live: Path) -> None:
        snapshot.write_text(snapshot.read_text() + "\n", encoding="utf-8")

    case("rejects snapshot hash drift", changed_snapshot, "recorded")

    def permits_axioms(approval: Path, _snapshot: Path, _live: Path) -> None:
        value = json.loads(approval.read_text())
        value["external_source_requirements"]["axioms_permitted"] = True
        approval.write_text(json.dumps(value), encoding="utf-8")

    case("rejects permission for axioms", permits_axioms, "must be false")

    def duplicate_key(approval: Path, _snapshot: Path, _live: Path) -> None:
        approval.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")

    case("rejects duplicate JSON keys", duplicate_key, "duplicate JSON key")

    with tempfile.TemporaryDirectory(prefix="phase2-approval-") as directory:
        root = Path(directory)
        approval, snapshot, live = _fixture(root)
        alternate = snapshot.with_name("alternate_snapshot.json")
        alternate.write_bytes(snapshot.read_bytes())
        errors = validate(approval, alternate, live, root)
        if any("supplied path does not match" in error for error in errors):
            print("PASS self-test rejects a caller-supplied snapshot alias")
        else:
            passed = False
            print(f"FAIL self-test rejects a caller-supplied snapshot alias: {errors}")
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--approval", type=Path, default=Path("sources/phase2_approval.json")
    )
    parser.add_argument(
        "--snapshot", type=Path, default=Path("sources/phase1_graph.json")
    )
    parser.add_argument("--graph", type=Path, default=Path("graph.json"))
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_tests()

    project_root = args.project_root.resolve()
    approval = args.approval if args.approval.is_absolute() else project_root / args.approval
    snapshot = args.snapshot if args.snapshot.is_absolute() else project_root / args.snapshot
    graph = args.graph if args.graph.is_absolute() else project_root / args.graph
    errors = validate(approval, snapshot, graph, project_root)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(
        "PASS Phase 2 approval: roadmap approved; pinned-primary-source policy; "
        f"snapshot {_sha256(snapshot)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
