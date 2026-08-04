#!/usr/bin/env python3
"""Atomically update fine exercise mappings with compare-and-swap checks.

Payload shape:

    {
      "updates": [
        {
          "member": "Exact Phase 1 provisional-member string",
          "expected": {"status": "pending", "tier2_node_ids": []},
          "mapping": {"status": "mapped", "tier2_node_ids": ["Exact tier-2 id"]}
        }
      ]
    }

The immutable owner/exercise identity cannot be changed through this writer.
Every candidate document passes the complete coverage validator before the
atomic replacement. Stable coverage and graph sidecar locks serialize mapping
callers with each other and with Autoform's graph merge writer.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

import check_exercise_coverage as coverage_check

try:
    import fcntl
except ImportError:  # pragma: no cover - this project and CI are POSIX-only
    fcntl = None


PAYLOAD_KEYS = ["updates"]
UPDATE_KEYS = ["member", "expected", "mapping"]
BeforeReplace = Callable[[Path, Path], None]


def decode_json(raw: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw,
            object_pairs_hook=coverage_check.reject_duplicate_keys,
            parse_constant=coverage_check.reject_nonfinite,
        )
    except (json.JSONDecodeError, coverage_check.CoverageError) as error:
        raise coverage_check.CoverageError(f"cannot parse {label}: {error}") from error
    coverage_check.require(type(value) is dict, f"{label} must be a JSON object")
    return value


def load_payload(path: Path | None) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8") if path is not None else sys.stdin.read()
    except (OSError, UnicodeError) as error:
        raise coverage_check.CoverageError(
            f"cannot read mapping payload: {error}"
        ) from error
    coverage_check.require(bool(raw.strip()), "mapping payload must not be empty")
    return decode_json(raw, "mapping payload")


def validate_mapping(mapping: Any, label: str) -> dict[str, Any]:
    coverage_check.exact_keys(mapping, coverage_check.FINE_MAPPING_KEYS, label)
    status = coverage_check.nonempty_string(mapping["status"], f"{label}.status")
    coverage_check.require(
        status in coverage_check.FINE_MAPPING_STATUSES,
        f"{label}.status must be pending or mapped",
    )
    node_ids = coverage_check.unique_string_list(
        mapping["tier2_node_ids"], f"{label}.tier2_node_ids"
    )
    coverage_check.require(
        node_ids == sorted(node_ids),
        f"{label}.tier2_node_ids must be lexicographically ordered",
    )
    if status == "pending":
        coverage_check.require(not node_ids, f"{label}: pending mappings must be empty")
    else:
        coverage_check.require(
            bool(node_ids), f"{label}: mapped mappings must not be empty"
        )
    return mapping


def apply_updates(
    coverage: dict[str, Any], payload: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    coverage_check.exact_keys(payload, PAYLOAD_KEYS, "mapping payload")
    updates = payload["updates"]
    coverage_check.require(
        type(updates) is list and bool(updates), "updates must be a nonempty array"
    )
    coverage_check.require(
        coverage.get("schema_version") == 2,
        "fine mapping updates require coverage schema v2",
    )
    obligations = coverage.get("fine_obligations")
    coverage_check.require(
        type(obligations) is dict, "fine_obligations must be an object"
    )

    candidate = copy.deepcopy(coverage)
    seen_members: set[str] = set()
    changed: list[str] = []
    for index, update in enumerate(updates):
        label = f"updates[{index}]"
        coverage_check.exact_keys(update, UPDATE_KEYS, label)
        member = coverage_check.nonempty_string(update["member"], f"{label}.member")
        coverage_check.require(
            member not in seen_members, f"payload repeats member {member!r}"
        )
        seen_members.add(member)
        coverage_check.require(
            member in obligations, f"unknown fine obligation {member!r}"
        )

        expected = validate_mapping(update["expected"], f"{label}.expected")
        replacement = validate_mapping(update["mapping"], f"{label}.mapping")
        current_record = obligations[member]
        coverage_check.require(
            type(current_record) is dict,
            f"fine obligation {member!r} must be an object",
        )
        current = validate_mapping(
            current_record.get("mapping"), f"current mapping for {member!r}"
        )
        coverage_check.require(
            current == expected,
            f"stale mapping for {member!r}: expected {expected!r}, found {current!r}",
        )
        candidate["fine_obligations"][member]["mapping"] = copy.deepcopy(replacement)
        changed.append(member)
    return candidate, changed


def default_lock_path(coverage_path: Path) -> Path:
    resolved = coverage_path.resolve()
    if resolved.parent.name == "sources":
        return resolved.parent.parent / f"{resolved.name}.lock"
    return Path(f"{resolved}.lock")


def atomic_write(
    path: Path, data: dict[str, Any], *, before_replace: BeforeReplace | None = None
) -> None:
    directory = path.resolve().parent
    destination_mode = (path.stat().st_mode & 0o777) if path.exists() else 0o644
    descriptor, raw_temporary = tempfile.mkstemp(
        dir=directory, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(raw_temporary)
    try:
        os.fchmod(descriptor, destination_mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if before_replace is not None:
            before_replace(temporary, path)
        os.replace(temporary, path)
        directory_descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def update_file(
    coverage_path: Path,
    graph_path: Path,
    phase1_graph_path: Path,
    payload: dict[str, Any],
    *,
    lock_path: Path | None = None,
    before_replace: BeforeReplace | None = None,
    verify_local_sources: bool = True,
) -> tuple[list[str], coverage_check.ValidationResult]:
    coverage_check.require(
        fcntl is not None, "mapping writer requires POSIX fcntl locking"
    )
    repository = Path(__file__).resolve().parents[1]
    lock_path = lock_path or default_lock_path(coverage_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    graph_lock_path = Path(f"{graph_path.resolve()}.lock")
    with lock_path.open("w", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            with graph_lock_path.open("w", encoding="utf-8") as graph_lock:
                fcntl.flock(graph_lock.fileno(), fcntl.LOCK_EX)
                try:
                    current = coverage_check.read_json(coverage_path, "coverage matrix")
                    candidate, changed = apply_updates(current, payload)
                    graph = coverage_check.read_json(graph_path, "live graph")
                    phase1_graph = coverage_check.read_json(
                        phase1_graph_path, "Phase 1 graph"
                    )
                    coverage_check.verify_phase1_artifacts(
                        candidate, 2, phase1_graph_path, repository
                    )
                    result = coverage_check.validate_documents(
                        candidate,
                        graph,
                        phase1_graph,
                        repository,
                        verify_local_sources=verify_local_sources,
                    )
                    atomic_write(
                        coverage_path, candidate, before_replace=before_replace
                    )
                    return changed, result
                finally:
                    fcntl.flock(graph_lock.fileno(), fcntl.LOCK_UN)
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def pending_to_mapped_payload(member: str, node_id: str) -> dict[str, Any]:
    return {
        "updates": [
            {
                "member": member,
                "expected": {"status": "pending", "tier2_node_ids": []},
                "mapping": {"status": "mapped", "tier2_node_ids": [node_id]},
            }
        ]
    }


def run_self_test() -> str:
    repository = Path(__file__).resolve().parents[1]
    current = coverage_check.read_json(
        repository / "sources" / "exercise_coverage.json", "coverage matrix"
    )
    phase1_path = repository / coverage_check.EXPECTED_PHASE1_GRAPH_FILE
    phase1_graph = coverage_check.read_json(phase1_path, "Phase 1 graph")
    v1_fixture = {
        key: copy.deepcopy(current[key]) for key in coverage_check.COVERAGE_V1_KEYS
    }
    v1_fixture["schema_version"] = 1
    base = coverage_check.migrate_v1_document(v1_fixture, phase1_graph)
    graph = copy.deepcopy(phase1_graph)
    members = list(base["fine_obligations"])
    first_member, second_member = members[0], members[1]
    first_node, second_node = "Writer self-test target A", "Writer self-test target B"
    coverage_check.add_test_target(base, graph, first_member, first_node)
    coverage_check.add_test_target(base, graph, second_member, second_node)

    case_count = 0

    def expect_failure(name: str, needle: str, action: Callable[[], Any]) -> None:
        nonlocal case_count
        case_count += 1
        try:
            action()
        except (coverage_check.CoverageError, RuntimeError) as error:
            if needle not in str(error):
                raise AssertionError(
                    f"writer self-test {name!r} expected {needle!r}, got {str(error)!r}"
                ) from error
            return
        raise AssertionError(f"writer self-test {name!r} unexpectedly passed")

    malformed = copy.deepcopy(base)
    malformed["fine_obligations"][first_member] = 0
    expect_failure(
        "scalar obligation record",
        "must be an object",
        lambda: apply_updates(
            malformed, pending_to_mapped_payload(first_member, first_node)
        ),
    )

    with tempfile.TemporaryDirectory(prefix="exercise-mapping-writer-") as raw_tmp:
        temporary = Path(raw_tmp)
        coverage_path = temporary / "exercise_coverage.json"
        graph_path = temporary / "graph.json"
        atomic_write(coverage_path, base)
        atomic_write(graph_path, graph)
        coverage_path.chmod(0o640)

        first_payload = pending_to_mapped_payload(first_member, first_node)
        changed, result = update_file(
            coverage_path,
            graph_path,
            phase1_path,
            first_payload,
            verify_local_sources=False,
        )
        case_count += 1
        if changed != [first_member] or result.mapped_obligations != 1:
            raise AssertionError(
                "writer self-test valid compare-and-swap returned wrong result"
            )
        if coverage_path.stat().st_mode & 0o777 != 0o640:
            raise AssertionError(
                "atomic update did not preserve destination permissions"
            )

        before = coverage_path.read_bytes()
        expect_failure(
            "stale compare-and-swap",
            "stale mapping",
            lambda: update_file(
                coverage_path,
                graph_path,
                phase1_path,
                first_payload,
                verify_local_sources=False,
            ),
        )
        if coverage_path.read_bytes() != before:
            raise AssertionError("stale compare-and-swap changed the coverage file")

        missing_payload = pending_to_mapped_payload(
            second_member, "Absent writer target"
        )
        before = coverage_path.read_bytes()
        expect_failure(
            "candidate validation",
            "names absent tier-2 node",
            lambda: update_file(
                coverage_path,
                graph_path,
                phase1_path,
                missing_payload,
                verify_local_sources=False,
            ),
        )
        if coverage_path.read_bytes() != before:
            raise AssertionError("invalid candidate changed the coverage file")

        second_payload = pending_to_mapped_payload(second_member, second_node)

        def injected_failure(_temporary: Path, _destination: Path) -> None:
            raise RuntimeError("injected pre-replace failure")

        before = coverage_path.read_bytes()
        expect_failure(
            "atomic rollback",
            "injected pre-replace failure",
            lambda: update_file(
                coverage_path,
                graph_path,
                phase1_path,
                second_payload,
                before_replace=injected_failure,
                verify_local_sources=False,
            ),
        )
        if coverage_path.read_bytes() != before:
            raise AssertionError("injected write failure changed the coverage file")
        if list(temporary.glob(".exercise_coverage.json.*.tmp")):
            raise AssertionError("injected write failure left a temporary file")

        graph_lock = Path(f"{graph_path.resolve()}.lock")
        blocked_marker = temporary / "graph-lock-blocked"
        early_marker = temporary / "graph-lock-acquired-too-early"
        acquired_marker = temporary / "graph-lock-acquired"
        lock_probe: subprocess.Popen[str] | None = None

        def probe_graph_lock(_temporary: Path, _destination: Path) -> None:
            nonlocal lock_probe
            probe = """\
import fcntl
import pathlib
import sys

lock_path, blocked_path, early_path, acquired_path = map(pathlib.Path, sys.argv[1:])
with lock_path.open("w") as lock:
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        blocked_path.write_text("blocked")
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        acquired_path.write_text("acquired")
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    else:
        early_path.write_text("acquired-too-early")
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
"""
            lock_probe = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    probe,
                    str(graph_lock),
                    str(blocked_marker),
                    str(early_marker),
                    str(acquired_marker),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            deadline = time.monotonic() + 5
            while (
                not blocked_marker.exists()
                and not early_marker.exists()
                and lock_probe.poll() is None
                and time.monotonic() < deadline
            ):
                time.sleep(0.01)
            if early_marker.exists():
                raise RuntimeError(
                    "graph-lock probe acquired the lock during replacement"
                )
            if not blocked_marker.exists():
                raise RuntimeError("graph-lock probe did not observe a held lock")

        update_file(
            coverage_path,
            graph_path,
            phase1_path,
            second_payload,
            before_replace=probe_graph_lock,
            verify_local_sources=False,
        )
        case_count += 1
        if lock_probe is None:
            raise AssertionError("graph-lock probe was not launched")
        probe_stdout, probe_stderr = lock_probe.communicate(timeout=10)
        if (
            lock_probe.returncode != 0
            or not blocked_marker.exists()
            or not acquired_marker.exists()
            or early_marker.exists()
        ):
            raise AssertionError(
                f"graph-lock probe did not acquire after release: {probe_stdout}{probe_stderr}"
            )

        atomic_write(coverage_path, base)
        payload_paths: list[Path] = []
        for index, payload in enumerate((first_payload, second_payload)):
            payload_path = temporary / f"payload-{index}.json"
            atomic_write(payload_path, payload)
            payload_paths.append(payload_path)
        processes = [
            subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--coverage",
                    str(coverage_path),
                    "--graph",
                    str(graph_path),
                    "--phase1-graph",
                    str(phase1_path),
                    "--payload",
                    str(payload_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for payload_path in payload_paths
        ]
        outputs = [process.communicate(timeout=30) for process in processes]
        case_count += 1
        for process, (stdout, stderr) in zip(processes, outputs, strict=True):
            if process.returncode != 0:
                raise AssertionError(
                    f"concurrent writer failed ({process.returncode}): {stdout}{stderr}"
                )
        concurrent = coverage_check.read_json(coverage_path, "concurrent result")
        for member in (first_member, second_member):
            if concurrent["fine_obligations"][member]["mapping"]["status"] != "mapped":
                raise AssertionError("concurrent updates lost a mapping")

    return f"PASS: exercise mapping writer self-test ({case_count} cases)"


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage",
        type=Path,
        default=repository / "sources" / "exercise_coverage.json",
    )
    parser.add_argument("--graph", type=Path, default=repository / "graph.json")
    parser.add_argument(
        "--phase1-graph",
        type=Path,
        default=repository / coverage_check.EXPECTED_PHASE1_GRAPH_FILE,
    )
    parser.add_argument("--payload", type=Path, help="payload file; defaults to stdin")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        if arguments.self_test:
            print(run_self_test())
            return 0
        payload = load_payload(arguments.payload)
        changed, result = update_file(
            arguments.coverage,
            arguments.graph,
            arguments.phase1_graph,
            payload,
        )
    except (
        OSError,
        UnicodeError,
        AssertionError,
        RuntimeError,
        subprocess.SubprocessError,
        coverage_check.CoverageError,
    ) as error:
        print(f"mapping update rejected: {error}", file=sys.stderr)
        return 2
    print(
        f"updated {len(changed)} fine obligation(s); "
        f"{result.mapped_obligations}/{result.obligation_count} mapped"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
