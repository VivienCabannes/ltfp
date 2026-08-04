#!/usr/bin/env python3
"""Mechanically validate tier-2 Autoform informal-content files.

This checker deliberately does not assess mathematical correctness, proof
soundness, faithfulness to a source, or whether a split omitted a result.  It
checks only deterministic acceptance properties: scoped completeness, a
canonical Markdown envelope, graph/pointer agreement, provenance hygiene, and
one-to-one safe content paths.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable


MATHLIB_STATUSES = {"in-mathlib", "partial", "missing"}
SCOPE_FIELDS = {"version", "tier", "content_complete_parents"}
SCOPE_ENTRY_FIELDS = {"parent", "fingerprint_sha256"}
SCOPE_FINGERPRINT_DOMAIN = "ltfp-phase2-content-scope-v3"
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
PLACEHOLDER_RE = re.compile(
    r"(?i)(?:\b(?:TODO|TBD|TBA)\b|statement\s+pending|proof\s+pending|coming\s+soon)"
)
ATX_HEADING_RE = re.compile(r"^[ \t]{0,3}(#{1,6})(?:[ \t]+(.*)|[ \t]*)$")
FENCE_OPEN_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")
THEMATIC_BREAK_RE = re.compile(r"^[ \t]{0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")
BOLD_PROOF_RE = re.compile(
    r"^[ \t]*(?:\*\*Proof[.:]?\*\*|\*Proof[.:]?\*)[ \t]*$", re.IGNORECASE
)
PLAIN_PROOF_RE = re.compile(r"^[ \t]{0,3}Proof[.:]?[ \t]*$", re.IGNORECASE)
MATHLIB_FILE_RE = re.compile(r"Mathlib/.+\.lean\Z")

BIDI_CONTROLS = {
    "\u061c",  # ARABIC LETTER MARK
    "\u200e",  # LEFT-TO-RIGHT MARK
    "\u200f",  # RIGHT-TO-LEFT MARK
    "\u202a",  # LEFT-TO-RIGHT EMBEDDING
    "\u202b",  # RIGHT-TO-LEFT EMBEDDING
    "\u202c",  # POP DIRECTIONAL FORMATTING
    "\u202d",  # LEFT-TO-RIGHT OVERRIDE
    "\u202e",  # RIGHT-TO-LEFT OVERRIDE
    "\u2066",  # LEFT-TO-RIGHT ISOLATE
    "\u2067",  # RIGHT-TO-LEFT ISOLATE
    "\u2068",  # FIRST STRONG ISOLATE
    "\u2069",  # POP DIRECTIONAL ISOLATE
}

CITATION_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "external URL",
        re.compile(r"(?i)(?:https?://|ftp://|www\.)[^\s)>]+"),
        "external URL",
    ),
    (
        "DOI",
        re.compile(r"(?i)(?:\bdoi\s*:\s*)?\b10\.\d{4,9}/[-._;()/:A-Z0-9]+"),
        "DOI",
    ),
    (
        "arXiv identifier",
        re.compile(r"(?i)\barxiv\s*:\s*(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})\b"),
        "arXiv identifier",
    ),
    (
        "LaTeX citation command",
        re.compile(
            r"\\(?:cite|citep|citet|autocite|parencite|textcite|footcite)\*?"
            r"(?:\[[^\]]*\])*\{",
            re.IGNORECASE,
        ),
        "LaTeX citation command",
    ),
    (
        "Markdown footnote",
        re.compile(r"\[\^[^\]\r\n]+\]"),
        "Markdown footnote",
    ),
    (
        "Pandoc citation",
        re.compile(r"\[@[^\]\r\n]+\]"),
        "Pandoc citation",
    ),
    (
        "reference section",
        re.compile(r"(?i)^[ \t]{0,3}#{1,6}[ \t]+(?:references|bibliography)[ \t]*#*[ \t]*$"),
        "reference or bibliography heading",
    ),
    (
        "numbered source label",
        re.compile(
            r"(?i)\b(?:chapters?|sections?|theorem|proposition|lemma|corollary|"
            r"definition|exercise|equation)s?[ \t]+\d+(?:\.\d+)*"
        ),
        "numbered source label",
    ),
    (
        "section-number citation",
        re.compile(r"§[ \t]*\d+(?:\.\d+)*"),
        "section-number citation",
    ),
    (
        "page citation",
        re.compile(r"(?i)\b(?:p{1,2}\.|pages?)[ \t]+\d+(?:[ \t]*[-–][ \t]*\d+)?"),
        "page citation",
    ),
)


class InputError(ValueError):
    """An input document or invocation cannot be interpreted safely."""


class DuplicateKeyError(ValueError):
    """JSON repeated a key and would otherwise be silently lossy."""


def _diagnostic_text(value: str) -> str:
    """Escape terminal controls and invisible Unicode in untrusted labels."""
    return value.encode("unicode_escape", errors="backslashreplace").decode("ascii")


def _physical_lines(value: str) -> list[str]:
    """Split only on CR, LF, or CRLF, as CommonMark physical lines require."""
    return re.split(r"\r\n|\r|\n", value)


def _forbidden_content_control(character: str) -> bool:
    codepoint = ord(character)
    return (
        (codepoint < 32 and character != "\t")
        or 127 <= codepoint <= 159
        or character in {"\u2028", "\u2029"}
        or character in BIDI_CONTROLS
    )


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    node: str = ""
    path: str = ""
    line: int = 0

    def sort_key(self) -> tuple[str, int, str, str, str]:
        return (self.path, self.line, self.code, self.node, self.message)

    def render(self) -> str:
        location = _diagnostic_text(self.path)
        if self.line:
            location = f"{location}:{self.line}" if location else f"line {self.line}"
        node = f" [{_diagnostic_text(self.node)}]" if self.node else ""
        prefix = f" {location}" if location else ""
        return f"FAIL {self.code}{prefix}{node}: {self.message}"


@dataclass(frozen=True)
class LineInfo:
    number: int
    raw: str
    visible: str
    structural: bool
    fence_delimiter: bool


@dataclass
class GraphIndex:
    nodes: dict[str, dict[str, Any]]
    tier1: set[str]
    tier2: set[str]
    children: dict[str, list[str]]
    source_tokens_by_node: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class ScopeEntry:
    parent: str
    fingerprint_sha256: str


@dataclass(frozen=True)
class ContentDocument:
    path: str
    text: str
    exact_bytes: bytes


@dataclass(frozen=True)
class GateOptions:
    mode: str
    scope_path: Path | None = None
    parents: tuple[str, ...] = ()
    all_split_parents: bool = False
    lint_only: bool = False


@dataclass
class GateResult:
    findings: list[Finding]
    tier2_count: int
    document_count: int
    selected_parents: tuple[str, ...]
    pending_parents: tuple[str, ...]
    selection_label: str
    parent_fingerprints: tuple[tuple[str, str], ...]


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value!r} is not permitted")


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as stream:
            document = json.load(
                stream,
                object_pairs_hook=_object_without_duplicates,
                parse_constant=_reject_nonfinite,
            )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise InputError(f"cannot read {label} {path}: {error}") from error
    if not isinstance(document, dict):
        raise InputError(f"{label} {path} must contain a JSON object")
    return document


def _trimmed_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def _unique_trimmed_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and all(_trimmed_string(item) for item in value)
        and len(value) == len(set(value))
    )


def _add_source_token(tokens: set[str], value: Any) -> None:
    if not _trimmed_string(value):
        return
    tokens.add(value)
    if "/" in value or "\\" in value:
        name = PurePosixPath(value.replace("\\", "/")).name
        if len(name) >= 4:
            tokens.add(name)


def _index_graph(graph: dict[str, Any]) -> tuple[GraphIndex, list[Finding]]:
    findings: list[Finding] = []
    version = graph.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 2:
        findings.append(Finding("E_GRAPH_VERSION", "expected integer graph schema version 2"))

    raw_nodes = graph.get("nodes")
    if not isinstance(raw_nodes, dict) or not raw_nodes:
        findings.append(Finding("E_GRAPH_NODES", "expected a nonempty nodes object"))
        raw_nodes = {}

    nodes: dict[str, dict[str, Any]] = {}
    metadata_sources: dict[str, dict[str, Any]] = {}
    metadata = graph.get("metadata")
    if isinstance(metadata, dict):
        sources = metadata.get("sources")
        if isinstance(sources, list):
            for source in sources:
                if isinstance(source, dict):
                    source_file = source.get("file")
                    if isinstance(source_file, str):
                        metadata_sources[source_file] = source

    source_tokens_by_node: dict[str, tuple[str, ...]] = {}
    for node_id, raw_node in raw_nodes.items():
        if not isinstance(node_id, str) or not isinstance(raw_node, dict):
            findings.append(Finding("E_GRAPH_NODE", "every node must have a string key and object value"))
            continue
        nodes[node_id] = raw_node
        path = "graph.json"
        if not _trimmed_string(node_id) or any(ord(char) < 32 for char in node_id):
            findings.append(
                Finding("E_GRAPH_NODE_ID", "node id must be a trimmed, nonempty string without control characters", node_id, path)
            )
        if raw_node.get("id") != node_id:
            findings.append(Finding("E_GRAPH_NODE_ID", "node record id must equal its map key", node_id, path))
        tier = raw_node.get("tier")
        if not isinstance(tier, int) or isinstance(tier, bool) or tier < 1:
            findings.append(Finding("E_GRAPH_TIER", "tier must be a positive integer", node_id, path))
        parent = raw_node.get("parent")
        if parent is not None and not _trimmed_string(parent):
            findings.append(Finding("E_GRAPH_PARENT", "parent must be null or a trimmed node id", node_id, path))
        status_value = raw_node.get("mathlib_status")
        if status_value not in MATHLIB_STATUSES:
            findings.append(
                Finding("E_GRAPH_STATUS", f"mathlib_status must be one of {sorted(MATHLIB_STATUSES)}", node_id, path)
            )
        declarations = raw_node.get("mathlib_declarations")
        if not _unique_trimmed_strings(declarations):
            findings.append(
                Finding("E_GRAPH_DECLARATIONS", "mathlib_declarations must be an array of unique trimmed strings", node_id, path)
            )
        if status_value == "in-mathlib":
            if not isinstance(declarations, list) or not declarations:
                findings.append(
                    Finding("E_GRAPH_DECLARATIONS", "in-mathlib nodes must name at least one declaration", node_id, path)
                )
            mathlib_file = raw_node.get("mathlib_file")
            if not _trimmed_string(mathlib_file) or MATHLIB_FILE_RE.fullmatch(mathlib_file) is None:
                findings.append(
                    Finding("E_GRAPH_MATHLIB_FILE", "in-mathlib nodes must name a Mathlib/**/*.lean file", node_id, path)
                )
        content = raw_node.get("content")
        if content is not None and not _trimmed_string(content):
            findings.append(Finding("E_GRAPH_CONTENT", "content must be null or a trimmed path", node_id, path))
        refs = raw_node.get("source_refs")
        node_tokens: set[str] = set()
        if isinstance(refs, list):
            for ref in refs:
                if isinstance(ref, dict):
                    source_file = ref.get("file")
                    _add_source_token(node_tokens, source_file)
                    _add_source_token(node_tokens, ref.get("location"))
                    matching_source = metadata_sources.get(source_file)
                    if matching_source is not None:
                        _add_source_token(node_tokens, matching_source.get("file"))
                        _add_source_token(node_tokens, matching_source.get("title"))
        source_tokens_by_node[node_id] = tuple(
            sorted(
                {token for token in node_tokens if len(token) >= 4},
                key=lambda token: (-len(token), token.casefold(), token),
            )
        )

    tier1 = {
        node_id
        for node_id, node in nodes.items()
        if isinstance(node.get("tier"), int)
        and not isinstance(node.get("tier"), bool)
        and node.get("tier") == 1
    }
    tier2 = {
        node_id
        for node_id, node in nodes.items()
        if isinstance(node.get("tier"), int)
        and not isinstance(node.get("tier"), bool)
        and node.get("tier") == 2
    }
    children: dict[str, list[str]] = {}
    for node_id in sorted(tier2):
        parent = nodes[node_id].get("parent")
        if isinstance(parent, str):
            children.setdefault(parent, []).append(node_id)

    return GraphIndex(
        nodes, tier1, tier2, children, source_tokens_by_node
    ), findings


def _load_scope(path: Path) -> tuple[ScopeEntry, ...]:
    scope = _load_json_object(path, "content scope")
    actual = set(scope)
    if actual != SCOPE_FIELDS:
        missing = sorted(SCOPE_FIELDS - actual)
        unknown = sorted(actual - SCOPE_FIELDS)
        details: list[str] = []
        if missing:
            details.append(f"missing fields {missing}")
        if unknown:
            details.append(f"unknown fields {unknown}")
        raise InputError(f"content scope must have exactly {sorted(SCOPE_FIELDS)}: {'; '.join(details)}")
    if not isinstance(scope["version"], int) or isinstance(scope["version"], bool) or scope["version"] != 3:
        raise InputError("content scope version must be integer 3")
    if not isinstance(scope["tier"], int) or isinstance(scope["tier"], bool) or scope["tier"] != 2:
        raise InputError("content scope tier must be integer 2")
    raw_entries = scope["content_complete_parents"]
    if not isinstance(raw_entries, list):
        raise InputError("content_complete_parents must be an array")
    entries: list[ScopeEntry] = []
    for index, raw_entry in enumerate(raw_entries):
        where = f"content_complete_parents[{index}]"
        if not isinstance(raw_entry, dict) or set(raw_entry) != SCOPE_ENTRY_FIELDS:
            raise InputError(
                f"{where} must have exactly {sorted(SCOPE_ENTRY_FIELDS)}"
            )
        parent = raw_entry.get("parent")
        fingerprint = raw_entry.get("fingerprint_sha256")
        if not _trimmed_string(parent):
            raise InputError(f"{where}.parent must be a nonempty trimmed string")
        if not isinstance(fingerprint, str) or SHA256_RE.fullmatch(fingerprint) is None:
            raise InputError(
                f"{where}.fingerprint_sha256 must be 64 lowercase hexadecimal characters"
            )
        entries.append(ScopeEntry(parent, fingerprint))
    parents = [entry.parent for entry in entries]
    if len(parents) != len(set(parents)):
        raise InputError("content scope parent entries must be unique")
    if parents != sorted(parents):
        raise InputError("content scope entries must be sorted lexicographically by parent")
    return tuple(entries)


def _select_parents(
    index: GraphIndex, options: GateOptions, project_root: Path
) -> tuple[tuple[str, ...], dict[str, str], str, list[Finding]]:
    findings: list[Finding] = []
    if options.mode == "final":
        if options.scope_path is None:
            raise InputError("final mode requires --scope with the durable parent registry")
        if options.parents or options.all_split_parents or options.lint_only:
            raise InputError("final mode accepts only the durable --scope selector")
    else:
        selectors = sum(
            (
                options.scope_path is not None,
                bool(options.parents),
                options.all_split_parents,
                options.lint_only,
            )
        )
        if selectors != 1:
            raise InputError("incremental mode requires exactly one scope, --parent, --all-split-parents, or --lint-only selector")

    if options.scope_path is not None:
        scope_path = options.scope_path
        if not scope_path.is_absolute():
            scope_path = project_root / scope_path
        entries = _load_scope(scope_path)
        selected = tuple(entry.parent for entry in entries)
        expected_fingerprints = {
            entry.parent: entry.fingerprint_sha256 for entry in entries
        }
        label = f"scope {scope_path.relative_to(project_root) if scope_path.is_relative_to(project_root) else scope_path}"
        if options.mode == "final":
            for missing_parent in sorted(index.tier1 - set(selected)):
                findings.append(
                    Finding(
                        "E_FINAL_SCOPE_MISSING",
                        "final scope registry has no reviewed fingerprint for this tier-1 parent",
                        missing_parent,
                        "graph.json",
                    )
                )
    elif options.parents:
        if not _unique_trimmed_strings(list(options.parents)):
            raise InputError("--parent values must be unique, nonempty, and trimmed")
        selected = tuple(sorted(options.parents))
        expected_fingerprints = {}
        label = "explicit parents"
    elif options.all_split_parents:
        selected = tuple(sorted(parent for parent in index.children if parent in index.tier1))
        expected_fingerprints = {}
        label = "all represented tier-1 parents"
        if not selected:
            findings.append(
                Finding("E_SCOPE_VACUOUS", "--all-split-parents selected no represented tier-1 parent")
            )
    else:
        selected = ()
        expected_fingerprints = {}
        label = "lint-only"
    return selected, expected_fingerprints, label, findings


def _unsafe_path_text(value: str) -> bool:
    return "\\" in value or any(
        ord(character) < 32
        or 127 <= ord(character) <= 159
        or character in {"\u2028", "\u2029"}
        or character in BIDI_CONTROLS
        for character in value
    )


def _canonical_content_path(value: str) -> bool:
    if _unsafe_path_text(value):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and len(path.parts) >= 2
        and path.parts[0] == "informal_content"
        and all(part not in {"", ".", ".."} for part in path.parts)
        and path.suffix == ".md"
        and str(path) == value
    )


def _canonical_source_path(value: str) -> bool:
    if _unsafe_path_text(value):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and len(path.parts) >= 2
        and path.parts[0] == "sources"
        and all(part not in {"", ".", ".."} for part in path.parts)
        and str(path) == value
    )


def _path_has_symlink(project_root: Path, relative: PurePosixPath) -> bool:
    current = project_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _read_documents(
    index: GraphIndex, project_root: Path
) -> tuple[dict[str, ContentDocument], set[str], list[Finding]]:
    findings: list[Finding] = []
    documents: dict[str, ContentDocument] = {}
    unsafe_nodes: set[str] = set()
    referenced: dict[str, str] = {}
    referenced_tier2: set[str] = set()
    inodes: dict[tuple[int, int], tuple[str, str]] = {}

    for node_id in sorted(index.nodes):
        node = index.nodes[node_id]
        content = node.get("content")
        if content is None or not isinstance(content, str):
            continue
        tier = node.get("tier")
        if tier != 2:
            unsafe_nodes.add(node_id)
            findings.append(
                Finding("E_NON_TIER2_CONTENT", "only tier-2 nodes may own informal content in this gate", node_id, content)
            )
        if not _canonical_content_path(content):
            unsafe_nodes.add(node_id)
            findings.append(
                Finding("E_CONTENT_PATH", "expected a canonical informal_content/**/*.md path", node_id, content)
            )
            continue
        prior = referenced.get(content)
        if prior is not None:
            unsafe_nodes.update((prior, node_id))
            findings.append(
                Finding("E_CONTENT_PATH_DUPLICATE", f"path is already owned by node {prior!r}", node_id, content)
            )
        else:
            referenced[content] = node_id
        if tier == 2:
            referenced_tier2.add(content)

        pure = PurePosixPath(content)
        candidate = project_root.joinpath(*pure.parts)
        if _path_has_symlink(project_root, pure):
            unsafe_nodes.add(node_id)
            findings.append(
                Finding("E_CONTENT_SYMLINK", "content paths and their ancestors must not be symlinks", node_id, content)
            )
            continue
        try:
            resolved = candidate.resolve(strict=False)
            resolved.relative_to((project_root / "informal_content").resolve())
        except (OSError, ValueError):
            unsafe_nodes.add(node_id)
            findings.append(
                Finding("E_CONTENT_ESCAPE", "content path escapes the project informal_content directory", node_id, content)
            )
            continue
        try:
            file_stat = candidate.stat()
        except OSError:
            unsafe_nodes.add(node_id)
            findings.append(
                Finding("E_CONTENT_MISSING", "referenced content file does not exist or cannot be inspected", node_id, content)
            )
            continue
        if not stat.S_ISREG(file_stat.st_mode):
            unsafe_nodes.add(node_id)
            findings.append(Finding("E_CONTENT_NONREGULAR", "content path must be a regular file", node_id, content))
            continue
        if file_stat.st_nlink != 1:
            unsafe_nodes.add(node_id)
            findings.append(
                Finding(
                    "E_CONTENT_HARDLINK",
                    f"content file has link count {file_stat.st_nlink}; hard-linked content is forbidden",
                    node_id,
                    content,
                )
            )
        inode = (file_stat.st_dev, file_stat.st_ino)
        prior_inode = inodes.get(inode)
        if prior_inode is not None and prior_inode[0] != content:
            unsafe_nodes.update((prior_inode[1], node_id))
            findings.append(
                Finding("E_CONTENT_HARDLINK", f"content file aliases {prior_inode[0]!r} through a hard link", node_id, content)
            )
        else:
            inodes[inode] = (content, node_id)
        try:
            exact_bytes = candidate.read_bytes()
            raw = exact_bytes.decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            unsafe_nodes.add(node_id)
            findings.append(Finding("E_CONTENT_UTF8", f"content must be strict UTF-8: {error}", node_id, content))
            continue
        documents[node_id] = ContentDocument(content, raw, exact_bytes)

    content_root = project_root / "informal_content"
    if content_root.is_symlink():
        findings.append(Finding("E_CONTENT_ROOT_SYMLINK", "informal_content must not be a symlink", path="informal_content"))
    elif content_root.exists() and not content_root.is_dir():
        findings.append(Finding("E_CONTENT_ROOT_TYPE", "informal_content must be a directory", path="informal_content"))
    elif content_root.is_dir():
        for directory, dirnames, filenames in os.walk(content_root, followlinks=False):
            directory_path = Path(directory)
            for dirname in sorted(list(dirnames)):
                child = directory_path / dirname
                if child.is_symlink():
                    rel = child.relative_to(project_root).as_posix()
                    findings.append(Finding("E_CONTENT_SYMLINK", "directory symlinks are forbidden", path=rel))
                    dirnames.remove(dirname)
            for filename in sorted(filenames):
                child = directory_path / filename
                rel = child.relative_to(project_root).as_posix()
                if child.is_symlink():
                    findings.append(Finding("E_CONTENT_SYMLINK", "file symlinks are forbidden", path=rel))
                elif not child.is_file():
                    findings.append(Finding("E_CONTENT_NONREGULAR", "nonregular files are forbidden", path=rel))
                if rel not in referenced_tier2:
                    findings.append(Finding("E_CONTENT_ORPHAN", "path is not owned by a tier-2 graph node", path=rel))
    return documents, unsafe_nodes, findings


def _strip_html_comments(lines: list[str]) -> tuple[list[str], bool]:
    visible: list[str] = []
    in_comment = False
    for line in lines:
        cursor = 0
        pieces: list[str] = []
        while cursor < len(line):
            if in_comment:
                end = line.find("-->", cursor)
                if end < 0:
                    cursor = len(line)
                else:
                    in_comment = False
                    cursor = end + 3
            else:
                start = line.find("<!--", cursor)
                if start < 0:
                    pieces.append(line[cursor:])
                    cursor = len(line)
                else:
                    pieces.append(line[cursor:start])
                    in_comment = True
                    cursor = start + 4
        visible.append("".join(pieces))
    return visible, in_comment


def _opening_fence(value: str) -> tuple[str, int] | None:
    match = FENCE_OPEN_RE.fullmatch(value)
    if match is None:
        return None
    marker, info = match.groups()
    if marker[0] == "`" and "`" in info:
        return None
    return marker[0], len(marker)


def _line_infos(raw: str) -> tuple[list[LineInfo], bool, bool]:
    raw_lines = _physical_lines(raw)
    visible_lines, unclosed_comment = _strip_html_comments(raw_lines)
    infos: list[LineInfo] = []
    fence: tuple[str, int] | None = None
    for number, (raw_line, visible) in enumerate(zip(raw_lines, visible_lines), start=1):
        if fence is not None:
            char, length = fence
            close = re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(char)}{{{length},}}[ \t]*", visible
            )
            infos.append(LineInfo(number, raw_line, visible, False, close is not None))
            if close is not None:
                fence = None
            continue
        opening = _opening_fence(visible)
        if opening is not None:
            fence = opening
            infos.append(LineInfo(number, raw_line, visible, False, True))
        else:
            infos.append(LineInfo(number, raw_line, visible, True, False))
    return infos, unclosed_comment, fence is not None


def _heading(info: LineInfo) -> tuple[int, str] | None:
    if not info.structural:
        return None
    match = ATX_HEADING_RE.fullmatch(info.visible)
    if match is None:
        return None
    label = (match.group(2) or "").strip()
    label = re.sub(r"[ \t]+#+[ \t]*$", "", label).strip()
    return len(match.group(1)), label


def _normalized_section(label: str) -> str:
    return label.strip().rstrip(".:").strip().casefold()


def _has_payload(infos: Iterable[LineInfo]) -> bool:
    for info in infos:
        value = info.visible.strip()
        if not value or info.fence_delimiter:
            continue
        if info.structural and (_heading(info) is not None or THEMATIC_BREAK_RE.fullmatch(info.visible)):
            continue
        if re.search(r"[\w\d]|[=<>≤≥∈∉∑∫∞]", value, re.UNICODE):
            return True
    return False


def _line_finding(code: str, message: str, node: str, path: str, info: LineInfo) -> Finding:
    return Finding(code, message, node, path, info.number)


def _check_leaks(
    node_id: str, path: str, raw_lines: list[str], source_tokens: tuple[str, ...]
) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(raw_lines[1:], start=2):
        folded = line.casefold()
        if re.search(r"(?i)\bsource[_ -]?refs?\b", line):
            findings.append(
                Finding("E_PROVENANCE_LEAK", "literal source_refs bookkeeping leaked into prose", node_id, path, line_number)
            )
        else:
            for token in source_tokens:
                if token.casefold() in folded:
                    findings.append(
                        Finding("E_PROVENANCE_LEAK", f"source provenance token {token!r} leaked into prose", node_id, path, line_number)
                    )
                    break
        for _, pattern, description in CITATION_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding("E_CITATION_LEAK", f"uncited universal prose must not contain a {description}", node_id, path, line_number)
                )
                break
    return findings


def _validate_document(
    node_id: str, node: dict[str, Any], path: str, raw: str, source_tokens: tuple[str, ...]
) -> list[Finding]:
    findings: list[Finding] = []
    raw_lines = _physical_lines(raw)
    if raw.startswith("\ufeff"):
        findings.append(Finding("E_CONTENT_BOM", "UTF-8 BOM is forbidden", node_id, path, 1))
    for line_number, line in enumerate(raw_lines, start=1):
        if any(_forbidden_content_control(character) for character in line):
            findings.append(
                Finding(
                    "E_CONTENT_CONTROL",
                    "content contains a non-CommonMark line separator or control character",
                    node_id,
                    path,
                    line_number,
                )
            )
    expected_h1 = f"# {node_id}"
    if not raw_lines or raw_lines[0] != expected_h1:
        actual = raw_lines[0] if raw_lines else "<empty file>"
        findings.append(
            Finding("E_H1_IDENTITY", f"first physical line must be exactly {expected_h1!r}, got {actual!r}", node_id, path, 1)
        )

    infos, unclosed_comment, unclosed_fence = _line_infos(raw)
    if unclosed_comment:
        findings.append(Finding("E_MARKDOWN_COMMENT", "unclosed HTML comment", node_id, path))
    if unclosed_fence:
        findings.append(Finding("E_MARKDOWN_FENCE", "unclosed fenced block", node_id, path))

    headings: list[tuple[int, int, str, LineInfo]] = []
    proof_markers: list[tuple[int, bool, LineInfo]] = []
    mathlib_markers: list[tuple[int, bool, LineInfo]] = []
    for index, info in enumerate(infos):
        parsed = _heading(info)
        if parsed is not None:
            level, label = parsed
            headings.append((index, level, label, info))
            normalized = _normalized_section(label)
            if index > 0 and level == 1:
                findings.append(_line_finding("E_H1_EXTRA", "additional H1 headings are forbidden", node_id, path, info))
            if normalized == "proof":
                proof_markers.append((index, info.raw == "## Proof", info))
            if normalized == "mathlib":
                mathlib_markers.append((index, info.raw == "## Mathlib", info))
        elif info.structural and (
            BOLD_PROOF_RE.fullmatch(info.visible)
            or PLAIN_PROOF_RE.fullmatch(info.visible)
        ):
            proof_markers.append((index, False, info))

    recognized_h2_lines = {
        info.number for _, _, info in proof_markers + mathlib_markers
    }
    for _, level, _, info in headings:
        if level == 2 and info.number not in recognized_h2_lines:
            findings.append(_line_finding("E_SECTION_UNKNOWN", "only ## Proof or ## Mathlib is a permitted H2 section", node_id, path, info))

    boundaries = [index for index, level, _, _ in headings if level == 2]
    boundaries.extend(index for index, _, _ in proof_markers)
    statement_end = min((index for index in boundaries if index > 0), default=len(infos))
    if not _has_payload(infos[1:statement_end]):
        findings.append(Finding("E_STATEMENT_EMPTY", "statement body has no visible substantive content", node_id, path))

    for info in infos[1:]:
        if PLACEHOLDER_RE.search(info.raw):
            findings.append(_line_finding("E_CONTENT_PLACEHOLDER", "placeholder text is forbidden", node_id, path, info))

    status_value = node.get("mathlib_status")
    exact_proofs = [(index, info) for index, exact, info in proof_markers if exact]
    exact_mathlib = [(index, info) for index, exact, info in mathlib_markers if exact]

    if status_value in {"partial", "missing"}:
        for _, exact, info in proof_markers:
            if not exact:
                findings.append(_line_finding("E_PROOF_NONCANONICAL", "proof marker must be exactly ## Proof", node_id, path, info))
        if not exact_proofs:
            findings.append(Finding("E_PROOF_MISSING", f"{status_value} nodes require an exact ## Proof section", node_id, path))
        elif len(exact_proofs) > 1:
            for _, info in exact_proofs[1:]:
                findings.append(_line_finding("E_PROOF_DUPLICATE", "only one ## Proof section is permitted", node_id, path, info))
        if exact_proofs and not _has_payload(infos[exact_proofs[0][0] + 1 :]):
            findings.append(Finding("E_PROOF_EMPTY", "proof section has no visible substantive content", node_id, path))
        for _, _, info in mathlib_markers:
            findings.append(_line_finding("E_MATHLIB_SECTION_FORBIDDEN", "partial and missing nodes use graph metadata, not a ## Mathlib prose section", node_id, path, info))

    elif status_value == "in-mathlib":
        for _, _, info in proof_markers:
            findings.append(_line_finding("E_PROOF_FORBIDDEN", "in-mathlib nodes must not contain a proof section", node_id, path, info))
        for _, exact, info in mathlib_markers:
            if not exact:
                findings.append(_line_finding("E_MATHLIB_NONCANONICAL", "Mathlib marker must be exactly ## Mathlib", node_id, path, info))
        if not exact_mathlib:
            findings.append(Finding("E_MATHLIB_POINTER_MISSING", "in-mathlib nodes require an exact ## Mathlib section", node_id, path))
        elif len(exact_mathlib) > 1:
            for _, info in exact_mathlib[1:]:
                findings.append(_line_finding("E_MATHLIB_POINTER_DUPLICATE", "only one ## Mathlib section is permitted", node_id, path, info))
        if exact_mathlib:
            pointer_lines = [
                info.visible
                for info in infos[exact_mathlib[0][0] + 1 :]
                if info.visible.strip()
            ]
            declarations = node.get("mathlib_declarations")
            mathlib_file = node.get("mathlib_file")
            if isinstance(declarations, list) and all(isinstance(item, str) for item in declarations) and isinstance(mathlib_file, str):
                # Pointer declaration order is exactly the authoritative graph-list
                # order.  The graph validator already requires list uniqueness.
                expected_pointer = [
                    "Declarations: " + ", ".join(f"`{declaration}`" for declaration in declarations),
                    f"File: `{mathlib_file}`",
                ]
                if pointer_lines != expected_pointer:
                    findings.append(
                        Finding(
                            "E_MATHLIB_POINTER_MISMATCH",
                            "Mathlib section must contain exactly " + repr(expected_pointer),
                            node_id,
                            path,
                            exact_mathlib[0][1].number,
                        )
                    )

    findings.extend(_check_leaks(node_id, path, raw_lines, source_tokens))
    return findings


def _source_identity(
    source_path: str,
    project_root: Path,
    declared_sha256: str | None,
    *,
    allow_absent_with_declared_identity: bool,
    cache: dict[str, str],
) -> tuple[str | None, list[Finding]]:
    if source_path in cache:
        return cache[source_path], []
    findings: list[Finding] = []
    if not _canonical_source_path(source_path):
        findings.append(
            Finding(
                "E_SOURCE_PATH",
                "expected a canonical sources/** path",
                path=source_path,
            )
        )
        return None, findings

    pure = PurePosixPath(source_path)
    candidate = project_root.joinpath(*pure.parts)
    if _path_has_symlink(project_root, pure):
        findings.append(
            Finding(
                "E_SOURCE_SYMLINK",
                "source paths and their ancestors must not be symlinks",
                path=source_path,
            )
        )
        return None, findings
    try:
        candidate.resolve(strict=False).relative_to(
            (project_root / "sources").resolve()
        )
    except (OSError, ValueError):
        findings.append(
            Finding(
                "E_SOURCE_ESCAPE",
                "source path escapes the project sources directory",
                path=source_path,
            )
        )
        return None, findings

    if not candidate.exists():
        if allow_absent_with_declared_identity and declared_sha256 is not None:
            cache[source_path] = declared_sha256
            return declared_sha256, findings
        findings.append(
            Finding(
                "E_SOURCE_MISSING",
                "referenced local source is absent and has no canonical declared identity",
                path=source_path,
            )
        )
        return None, findings
    try:
        file_stat = candidate.stat()
        if not stat.S_ISREG(file_stat.st_mode):
            raise OSError("not a regular file")
        digest = hashlib.sha256()
        with candidate.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        observed = digest.hexdigest()
    except OSError:
        findings.append(
            Finding(
                "E_SOURCE_READ",
                "source must be a readable regular file",
                path=source_path,
            )
        )
        return None, findings
    if declared_sha256 is not None and observed != declared_sha256:
        findings.append(
            Finding(
                "E_SOURCE_HASH_MISMATCH",
                f"observed SHA-256 is {observed}, expected {declared_sha256}",
                path=source_path,
            )
        )
        return None, findings
    cache[source_path] = observed
    return observed, findings


def _base_review_context(
    graph: dict[str, Any],
    project_root: Path,
    source_cache: dict[str, str],
) -> tuple[
    dict[str, Any] | None,
    dict[str, dict[str, Any]],
    dict[str, str],
    list[Finding],
]:
    findings: list[Finding] = []
    metadata = graph.get("metadata")
    if not isinstance(metadata, dict):
        return None, {}, {}, [Finding("E_REVIEW_CONTEXT", "graph metadata must be an object")]
    lean_toolchain = metadata.get("lean_toolchain")
    mathlib_revision = metadata.get("mathlib_revision")
    if not _trimmed_string(lean_toolchain):
        findings.append(
            Finding("E_REVIEW_CONTEXT", "metadata.lean_toolchain is required")
        )
    if not _trimmed_string(mathlib_revision):
        findings.append(
            Finding("E_REVIEW_CONTEXT", "metadata.mathlib_revision is required")
        )
    raw_sources = metadata.get("sources")
    if not isinstance(raw_sources, list) or not raw_sources:
        findings.append(
            Finding("E_REVIEW_CONTEXT", "metadata.sources must be a nonempty array")
        )
        return None, {}, {}, findings

    records: list[dict[str, Any]] = []
    canonical_identities: dict[str, str] = {}
    seen_files: set[str] = set()
    for index, record in enumerate(raw_sources):
        if not isinstance(record, dict):
            findings.append(
                Finding(
                    "E_REVIEW_CONTEXT",
                    f"metadata.sources[{index}] must be an object",
                )
            )
            continue
        source_path = record.get("file")
        declared = record.get("sha256")
        if not _trimmed_string(source_path) or not _canonical_source_path(source_path):
            findings.append(
                Finding(
                    "E_SOURCE_PATH",
                    f"metadata.sources[{index}].file must be a canonical sources/** path",
                    path=source_path if isinstance(source_path, str) else "",
                )
            )
            continue
        if source_path in seen_files:
            findings.append(
                Finding(
                    "E_REVIEW_CONTEXT",
                    f"duplicate canonical source record for {source_path!r}",
                )
            )
            continue
        seen_files.add(source_path)
        if not isinstance(declared, str) or SHA256_RE.fullmatch(declared) is None:
            findings.append(
                Finding(
                    "E_SOURCE_IDENTITY",
                    "canonical metadata source requires a lowercase SHA-256 identity",
                    path=source_path,
                )
            )
            continue
        observed, source_findings = _source_identity(
            source_path,
            project_root,
            declared,
            allow_absent_with_declared_identity=True,
            cache=source_cache,
        )
        findings.extend(source_findings)
        if observed is not None:
            canonical_identities[source_path] = observed
        records.append(record)

    record_map = {record["file"]: record for record in records}
    if findings:
        return None, record_map, canonical_identities, findings
    records.sort(key=lambda record: record["file"])
    base = {
        "graph_version": graph.get("version"),
        "lean_toolchain": lean_toolchain,
        "mathlib_revision": mathlib_revision,
    }
    return base, record_map, canonical_identities, findings


def _parent_review_context(
    parent: str,
    index: GraphIndex,
    base: dict[str, Any],
    canonical_records: dict[str, dict[str, Any]],
    canonical_identities: dict[str, str],
    project_root: Path,
    source_cache: dict[str, str],
) -> tuple[dict[str, Any] | None, list[Finding]]:
    findings: list[Finding] = []
    identities: dict[str, str] = {}
    metadata_sources: dict[str, dict[str, Any]] = {}
    for child in sorted(index.children[parent]):
        refs = index.nodes[child].get("source_refs")
        if not isinstance(refs, list):
            findings.append(
                Finding(
                    "E_SOURCE_REFS",
                    "source_refs must be an array before review fingerprinting",
                    child,
                    "graph.json",
                )
            )
            continue
        for ref in refs:
            source_path = ref.get("file") if isinstance(ref, dict) else None
            if not _trimmed_string(source_path):
                findings.append(
                    Finding(
                        "E_SOURCE_REFS",
                        "every source reference must name a local source file",
                        child,
                        "graph.json",
                    )
                )
                continue
            if source_path in canonical_records:
                identities[source_path] = canonical_identities[source_path]
                metadata_sources[source_path] = canonical_records[source_path]
                continue
            if source_path in identities:
                continue
            observed, source_findings = _source_identity(
                source_path,
                project_root,
                None,
                allow_absent_with_declared_identity=False,
                cache=source_cache,
            )
            findings.extend(source_findings)
            if observed is not None:
                identities[source_path] = observed
    if findings:
        return None, findings
    context = dict(base)
    context["metadata_sources"] = [
        metadata_sources[source_path]
        for source_path in sorted(metadata_sources)
    ]
    context["source_identities"] = [
        {"file": source_path, "sha256": identities[source_path]}
        for source_path in sorted(identities)
    ]
    return context, findings


def _scope_fingerprint_digest(
    parent: str,
    children: list[dict[str, Any]],
    review_context: dict[str, Any],
) -> str:
    payload = {
        "domain": SCOPE_FINGERPRINT_DOMAIN,
        "parent": parent,
        "review_context": review_context,
        "children": children,
    }
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _scope_entry_output(parent: str, fingerprint: str) -> str:
    return "SCOPE_ENTRY " + json.dumps(
        {"parent": parent, "fingerprint_sha256": fingerprint},
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _parent_fingerprint(
    parent: str,
    index: GraphIndex,
    documents: dict[str, ContentDocument],
    review_context: dict[str, Any],
) -> str:
    children: list[dict[str, Any]] = [
        {
            "id": child,
            "node": index.nodes[child],
            "content_base64": base64.b64encode(
                documents[child].exact_bytes
            ).decode("ascii"),
        }
        for child in sorted(index.children[parent])
    ]
    return _scope_fingerprint_digest(parent, children, review_context)


def validate_gate(
    graph_path: Path, project_root: Path, options: GateOptions
) -> GateResult:
    graph = _load_json_object(graph_path, "graph")
    index, findings = _index_graph(graph)
    selected, expected_fingerprints, selection_label, selection_findings = (
        _select_parents(index, options, project_root)
    )
    findings.extend(selection_findings)

    documents, unsafe_nodes, path_findings = _read_documents(index, project_root)
    findings.extend(path_findings)
    for node_id in sorted(documents):
        document = documents[node_id]
        findings.extend(
            _validate_document(
                node_id,
                index.nodes[node_id],
                document.path,
                document.text,
                index.source_tokens_by_node.get(node_id, ()),
            )
        )

    if options.mode == "final" and not index.tier2:
        findings.append(Finding("E_FINAL_NO_TIER2", "final mode requires at least one tier-2 node"))

    source_cache: dict[str, str] = {}
    review_base: dict[str, Any] | None = None
    canonical_records: dict[str, dict[str, Any]] = {}
    canonical_identities: dict[str, str] = {}
    if selected:
        (
            review_base,
            canonical_records,
            canonical_identities,
            context_findings,
        ) = (
            _base_review_context(graph, project_root, source_cache)
        )
        findings.extend(context_findings)

    parent_fingerprints: list[tuple[str, str]] = []
    for parent in selected:
        node = index.nodes.get(parent)
        if node is None:
            findings.append(Finding("E_SCOPE_PARENT_UNKNOWN", "selected parent does not exist", parent, "graph.json"))
            continue
        if parent not in index.tier1:
            findings.append(Finding("E_SCOPE_PARENT_TIER", "selected parent is not tier 1", parent, "graph.json"))
            continue
        children = index.children.get(parent, [])
        if not children:
            findings.append(Finding("E_PARENT_UNSPLIT", "selected parent has no tier-2 child", parent, "graph.json"))
            continue
        complete_safe_read = True
        for child in children:
            if not isinstance(index.nodes[child].get("content"), str):
                complete_safe_read = False
                findings.append(
                    Finding(
                        "E_CONTENT_REQUIRED",
                        "tier-2 content must be non-null in the selected or final scope",
                        child,
                        "graph.json",
                    )
                )
            if child not in documents or child in unsafe_nodes:
                complete_safe_read = False
        if complete_safe_read and review_base is not None:
            review_context, source_findings = _parent_review_context(
                parent,
                index,
                review_base,
                canonical_records,
                canonical_identities,
                project_root,
                source_cache,
            )
            findings.extend(source_findings)
            if review_context is None:
                continue
            fingerprint = _parent_fingerprint(
                parent, index, documents, review_context
            )
            parent_fingerprints.append((parent, fingerprint))
            expected = expected_fingerprints.get(parent)
            if expected is not None and fingerprint != expected:
                findings.append(
                    Finding(
                        "E_SCOPE_FINGERPRINT",
                        f"content-complete parent fingerprint is {fingerprint}, expected {expected}",
                        parent,
                        "graph.json",
                    )
                )

    if options.mode == "final":
        for parent in sorted(index.tier1):
            if not index.children.get(parent):
                findings.append(
                    Finding(
                        "E_PARENT_UNSPLIT",
                        "final mode requires every tier-1 parent to have a tier-2 child",
                        parent,
                        "graph.json",
                    )
                )
        for child in sorted(index.tier2):
            parent = index.nodes[child].get("parent")
            if not isinstance(parent, str) or parent not in index.tier1:
                findings.append(
                    Finding("E_TIER2_PARENT", "final mode requires every tier-2 node to have an existing tier-1 parent", child, "graph.json")
                )
            if not isinstance(index.nodes[child].get("content"), str):
                findings.append(
                    Finding(
                        "E_CONTENT_REQUIRED",
                        "tier-2 content must be non-null in the selected or final scope",
                        child,
                        "graph.json",
                    )
                )

    selected_set = set(selected)
    pending = tuple(sorted(index.tier1 - selected_set))
    return GateResult(
        findings=sorted(set(findings), key=Finding.sort_key),
        tier2_count=len(index.tier2),
        document_count=len(documents),
        selected_parents=selected,
        pending_parents=pending,
        selection_label=selection_label,
        parent_fingerprints=tuple(parent_fingerprints),
    )


def _minimal_node(
    node_id: str,
    tier: int,
    parent: str | None,
    status_value: str,
    content: str | None,
    declarations: list[str] | None = None,
    mathlib_file: str | None = None,
) -> dict[str, Any]:
    node: dict[str, Any] = {
        "id": node_id,
        "tier": tier,
        "parent": parent,
        "mathlib_status": status_value,
        "mathlib_declarations": declarations or [],
        "source_refs": [{"file": "sources/test.pdf", "location": "Chapter 1, Theorem 1.2"}],
        "content": content,
    }
    if mathlib_file is not None:
        node["mathlib_file"] = mathlib_file
    return node


def _fixture_fingerprint(
    graph: dict[str, Any], files: dict[str, str | bytes], parent: str
) -> str:
    index, findings = _index_graph(graph)
    if findings:
        raise AssertionError(f"invalid self-test graph: {findings}")
    documents: dict[str, ContentDocument] = {}
    for child in index.children.get(parent, []):
        path = index.nodes[child].get("content")
        if not isinstance(path, str) or path not in files:
            raise AssertionError(f"self-test child {child!r} has no fixture content")
        body = files[path]
        exact_bytes = body if isinstance(body, bytes) else body.encode("utf-8")
        documents[child] = ContentDocument(
            path,
            exact_bytes.decode("utf-8"),
            exact_bytes,
        )
    metadata = graph["metadata"]
    identities: dict[str, str] = {}
    source_paths: set[str] = set()
    for child in index.children.get(parent, []):
        source_paths.update(
            ref["file"] for ref in index.nodes[child]["source_refs"]
        )
    for source_path in source_paths:
        body = files[source_path]
        exact_bytes = body if isinstance(body, bytes) else body.encode("utf-8")
        identities[source_path] = hashlib.sha256(exact_bytes).hexdigest()
    review_context = {
        "graph_version": graph["version"],
        "lean_toolchain": metadata["lean_toolchain"],
        "mathlib_revision": metadata["mathlib_revision"],
        "metadata_sources": sorted(
            (
                record
                for record in metadata["sources"]
                if record["file"] in source_paths
            ),
            key=lambda record: record["file"],
        ),
        "source_identities": [
            {"file": source_path, "sha256": identities[source_path]}
            for source_path in sorted(identities)
        ],
    }
    return _parent_fingerprint(parent, index, documents, review_context)


def _fixture() -> tuple[dict[str, Any], dict[str, str | bytes], dict[str, Any]]:
    canonical_source = b"canonical fixture source\n"
    second_source = b"second canonical fixture source\n"
    graph = {
        "version": 2,
        "metadata": {
            "created_at": "2026-01-01T00:00:00Z",
            "last_updated": "2026-01-01T00:00:01Z",
            "lean_root": "/volatile/test/root",
            "lean_toolchain": "leanprover/lean4:v4.32.2",
            "mathlib_revision": "a" * 40,
            "sources": [
                {
                    "file": "sources/test.pdf",
                    "title": "Test Source",
                    "format": "pdf",
                    "sha256": hashlib.sha256(canonical_source).hexdigest(),
                },
                {
                    "file": "sources/second.pdf",
                    "title": "Independent Corpus",
                    "format": "pdf",
                    "sha256": hashlib.sha256(second_source).hexdigest(),
                }
            ],
        },
        "nodes": {
            "Cluster A": _minimal_node("Cluster A", 1, None, "partial", None, ["Nat.zero"], "Mathlib/Data/Nat/Basic.lean"),
            "Cluster B": _minimal_node("Cluster B", 1, None, "partial", None, ["Nat.zero"], "Mathlib/Data/Nat/Basic.lean"),
            "Library result": _minimal_node(
                "Library result",
                2,
                "Cluster A",
                "in-mathlib",
                "informal_content/library-result.md",
                ["Nat.zero", "Nat.succ"],
                "Mathlib/Data/Nat/Basic.lean",
            ),
            "Partial result": _minimal_node(
                "Partial result",
                2,
                "Cluster A",
                "partial",
                "informal_content/partial-result.md",
                ["Nat.add"],
                "Mathlib/Data/Nat/Basic.lean",
            ),
            "Missing result": _minimal_node(
                "Missing result", 2, "Cluster A", "missing", "informal_content/missing-result.md"
            ),
            "Other result": _minimal_node("Other result", 2, "Cluster B", "missing", None),
        },
    }
    graph["nodes"]["Missing result"]["source_refs"] = [
        {"file": "sources/notes.md", "location": "A tracked note"}
    ]
    files: dict[str, str | bytes] = {
        "sources/test.pdf": canonical_source,
        "sources/second.pdf": second_source,
        "sources/notes.md": "tracked fixture notes\n",
        "informal_content/library-result.md": (
            "# Library result\n\nFor every natural number, zero is no greater than its successor.\n\n"
            "## Mathlib\n\nDeclarations: `Nat.zero`, `Nat.succ`\n"
            "File: `Mathlib/Data/Nat/Basic.lean`\n"
        ),
        "informal_content/partial-result.md": (
            "# Partial result\n\nFor natural numbers, addition preserves equality.\n\n"
            "## Proof\n\nSubstitution in both summands gives the claimed equality.\n"
        ),
        "informal_content/missing-result.md": (
            "# Missing result\n\nEvery element in the finite family has the stated property.\n\n"
            "## Proof\n\nApply the property to each indexed element.\n"
        ),
    }
    scope = {
        "version": 3,
        "tier": 2,
        "content_complete_parents": [
            {
                "parent": "Cluster A",
                "fingerprint_sha256": _fixture_fingerprint(
                    graph, files, "Cluster A"
                ),
            }
        ],
    }
    return graph, files, scope


def _write_fixture(
    root: Path,
    graph: dict[str, Any],
    files: dict[str, str | bytes],
    scope: dict[str, Any],
) -> None:
    (root / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    (root / "sources").mkdir(parents=True, exist_ok=True)
    (root / "sources" / "phase2_content_scope.json").write_text(json.dumps(scope), encoding="utf-8")
    for relative, body in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(body, bytes):
            path.write_bytes(body)
        else:
            path.write_text(body, encoding="utf-8")


def run_self_tests() -> int:
    passed = True

    def case(
        label: str,
        *,
        expected: set[str] | None = None,
        forbidden: set[str] | None = None,
        mode: str = "incremental",
        selector: str | tuple[str, ...] = "scope",
        mutate: Callable[[dict[str, Any], dict[str, str | bytes], dict[str, Any]], None] | None = None,
        post: Callable[[Path], None] | None = None,
    ) -> None:
        nonlocal passed
        with tempfile.TemporaryDirectory(prefix="check-informal-content-") as directory:
            root = Path(directory)
            graph, files, scope = _fixture()
            if mutate is not None:
                mutate(graph, files, scope)
            _write_fixture(root, graph, files, scope)
            if post is not None:
                post(root)
            if mode == "final":
                options = GateOptions(
                    mode="final",
                    scope_path=Path("sources/phase2_content_scope.json"),
                )
            elif selector == "scope":
                options = GateOptions(mode="incremental", scope_path=Path("sources/phase2_content_scope.json"))
            elif selector == "all":
                options = GateOptions(mode="incremental", all_split_parents=True)
            elif selector == "lint":
                options = GateOptions(mode="incremental", lint_only=True)
            elif isinstance(selector, tuple):
                options = GateOptions(mode="incremental", parents=selector)
            else:
                options = GateOptions(mode="incremental", parents=(selector,))
            try:
                result = validate_gate(root / "graph.json", root, options)
                codes = {finding.code for finding in result.findings}
                error = None
            except InputError as caught:
                codes = {"INPUT_ERROR"}
                error = str(caught)
            wanted = expected or set()
            disallowed = forbidden or set()
            ok = (
                (not codes)
                if expected is None
                else wanted.issubset(codes) and codes.isdisjoint(disallowed)
            )
            if ok:
                print(f"PASS self-test {label}")
            else:
                passed = False
                print(
                    f"FAIL self-test {label}: expected {sorted(wanted)}, "
                    f"forbidden {sorted(disallowed)}, got {sorted(codes)}"
                )
                if error:
                    print(error)

    vector_index = GraphIndex(
        nodes={"C": {"id": "C", "list": [2, 1]}},
        tier1=set(),
        tier2={"C"},
        children={"P": ["C"]},
        source_tokens_by_node={"C": ()},
    )
    vector_documents = {
        "C": ContentDocument("informal_content/c.md", "", b"\xfb\xff")
    }
    vector_context = {
        "graph_version": 2,
        "lean_toolchain": "leanprover/lean4:v4.32.2",
        "mathlib_revision": "a" * 40,
        "metadata_sources": [],
        "source_identities": [],
    }
    vector_fingerprint = _parent_fingerprint(
        "P", vector_index, vector_documents, vector_context
    )
    if vector_fingerprint == "e90efcec668e61866bd1f344e8686c2f735b2a82fb4a2ed692aff8eaa7d5beb3":
        print("PASS self-test canonical fingerprint and standard Base64 test vector")
    else:
        passed = False
        print(
            "FAIL self-test canonical fingerprint and standard Base64 test vector: "
            + vector_fingerprint
        )

    rendered_control_path = Finding(
        "E_TEST", "safe rendering", path="informal_content/x\x1b\u202e.md"
    ).render()
    if (
        "\x1b" not in rendered_control_path
        and "\u202e" not in rendered_control_path
        and "\\x1b" in rendered_control_path
        and "\\u202e" in rendered_control_path
    ):
        print("PASS self-test diagnostic paths escape controls and bidi markers")
    else:
        passed = False
        print(
            "FAIL self-test diagnostic paths escape controls and bidi markers: "
            + repr(rendered_control_path)
        )

    case("accepts a complete selected parent")
    case("accepts an explicit completed parent", selector="Cluster A")

    with tempfile.TemporaryDirectory(prefix="check-informal-content-output-") as directory:
        root = Path(directory)
        graph, files, scope = _fixture()
        _write_fixture(root, graph, files, scope)
        result = validate_gate(
            root / "graph.json",
            root,
            GateOptions(mode="incremental", parents=("Cluster A",)),
        )
        expected_fingerprint = scope["content_complete_parents"][0][
            "fingerprint_sha256"
        ]
        expected_line = _scope_entry_output("Cluster A", expected_fingerprint)
        if (
            not result.findings
            and result.parent_fingerprints
            == (("Cluster A", expected_fingerprint),)
            and json.loads(expected_line.removeprefix("SCOPE_ENTRY "))
            == scope["content_complete_parents"][0]
        ):
            print("PASS self-test explicit parents expose copyable scope entries")
        else:
            passed = False
            print("FAIL self-test explicit parents expose copyable scope entries")

    def phase1(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"] = {key: value for key, value in graph["nodes"].items() if value["tier"] == 1}
        files.clear()
        scope["content_complete_parents"] = []

    case("accepts Phase 1 with an empty incremental scope", mutate=phase1)
    case(
        "rejects vacuous all-split selection",
        expected={"E_SCOPE_VACUOUS"},
        mutate=phase1,
        selector="all",
    )
    case(
        "rejects Phase 1 in final mode",
        expected={"E_FINAL_NO_TIER2", "E_PARENT_UNSPLIT"},
        mutate=phase1,
        mode="final",
    )

    def finish(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Other result"]["content"] = "informal_content/other-result.md"
        files["informal_content/other-result.md"] = (
            "# Other result\n\nThe secondary cluster has a complete statement.\n\n"
            "## Proof\n\nThe assertion follows directly from its hypothesis.\n"
        )
        scope["content_complete_parents"] = [
            scope["content_complete_parents"][0],
            {
                "parent": "Cluster B",
                "fingerprint_sha256": _fixture_fingerprint(
                    graph, files, "Cluster B"
                ),
            },
        ]

    case("accepts a complete final graph", mutate=finish, mode="final")
    case(
        "accepts repeatable explicit completed parents",
        mutate=finish,
        selector=("Cluster A", "Cluster B"),
    )
    case(
        "final mode rejects null content and an incomplete registry",
        expected={"E_CONTENT_REQUIRED", "E_FINAL_SCOPE_MISSING"},
        mode="final",
    )

    def finish_without_full_registry(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        finish(graph, files, scope)
        scope["content_complete_parents"] = scope["content_complete_parents"][:1]

    case(
        "final mode requires every tier-1 parent in the registry",
        expected={"E_FINAL_SCOPE_MISSING"},
        mutate=finish_without_full_registry,
        mode="final",
    )

    def finish_with_stale_registry(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        finish(graph, files, scope)
        scope["content_complete_parents"][0]["fingerprint_sha256"] = "0" * 64

    case(
        "final mode verifies every registry fingerprint",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=finish_with_stale_registry,
        mode="final",
    )
    case("all-split mode catches an incomplete represented parent", expected={"E_CONTENT_REQUIRED"}, selector="all")

    def unsplit_scope(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Cluster C"] = _minimal_node(
            "Cluster C", 1, None, "partial", None, ["Nat.zero"], "Mathlib/Data/Nat/Basic.lean"
        )
        scope["content_complete_parents"] = [
            {"parent": "Cluster C", "fingerprint_sha256": "0" * 64}
        ]

    case("selected parents cannot pass without children", expected={"E_PARENT_UNSPLIT"}, mutate=unsplit_scope)
    case(
        "rejects an unknown explicit parent",
        expected={"E_SCOPE_PARENT_UNKNOWN"},
        selector="Absent cluster",
    )

    def bad_scope_fields(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["unexpected"] = True

    case("rejects unknown scope fields", expected={"INPUT_ERROR"}, mutate=bad_scope_fields)

    def old_scope_version(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["version"] = 2

    case("rejects obsolete v2 scopes", expected={"INPUT_ERROR"}, mutate=old_scope_version)

    def bad_scope_entry_fields(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["content_complete_parents"][0]["extra"] = True

    case(
        "requires exact scope-entry fields",
        expected={"INPUT_ERROR"},
        mutate=bad_scope_entry_fields,
    )

    def duplicate_scope_parent(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["content_complete_parents"].append(
            dict(scope["content_complete_parents"][0])
        )

    case(
        "requires unique scope parents",
        expected={"INPUT_ERROR"},
        mutate=duplicate_scope_parent,
    )

    def unsorted_scope(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["content_complete_parents"] = [
            {"parent": "Cluster B", "fingerprint_sha256": "0" * 64},
            {"parent": "Cluster A", "fingerprint_sha256": "1" * 64},
        ]

    case("rejects a noncanonical unsorted scope", expected={"INPUT_ERROR"}, mutate=unsorted_scope)

    def uppercase_fingerprint(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        scope["content_complete_parents"][0]["fingerprint_sha256"] = "A" * 64

    case(
        "requires lowercase scope fingerprints",
        expected={"INPUT_ERROR"},
        mutate=uppercase_fingerprint,
    )

    def add_child(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Added result"] = _minimal_node(
            "Added result",
            2,
            "Cluster A",
            "missing",
            "informal_content/added-result.md",
        )
        files["informal_content/added-result.md"] = (
            "# Added result\n\nThe added statement is complete.\n\n"
            "## Proof\n\nThe assertion follows directly.\n"
        )

    case(
        "fingerprint detects an added child",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=add_child,
    )

    def remove_child(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        removed = graph["nodes"].pop("Missing result")
        files.pop(removed["content"])

    case(
        "fingerprint detects a removed child",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=remove_child,
    )

    def rename_child(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        node = graph["nodes"].pop("Missing result")
        old_path = node["content"]
        node["id"] = "Renamed result"
        node["content"] = "informal_content/renamed-result.md"
        graph["nodes"]["Renamed result"] = node
        files[node["content"]] = str(files.pop(old_path)).replace(
            "# Missing result", "# Renamed result", 1
        )

    case(
        "fingerprint detects a renamed child",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=rename_child,
    )

    def rename_parent(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        node = graph["nodes"].pop("Cluster A")
        node["id"] = "Renamed cluster"
        graph["nodes"]["Renamed cluster"] = node
        for child in graph["nodes"].values():
            if child.get("parent") == "Cluster A":
                child["parent"] = "Renamed cluster"

    case(
        "scope detects a renamed parent",
        expected={"E_SCOPE_PARENT_UNKNOWN"},
        mutate=rename_parent,
    )

    def reparent_child(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["parent"] = "Cluster B"

    case(
        "fingerprint detects a reparented child",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=reparent_child,
    )

    def mutate_field(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["description"] = "A changed full node record."

    case(
        "fingerprint covers every child record field",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_field,
    )

    def mutate_list_order(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Library result"]["mathlib_declarations"] = [
            "Nat.succ",
            "Nat.zero",
        ]
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ).replace(
            "Declarations: `Nat.zero`, `Nat.succ`",
            "Declarations: `Nat.succ`, `Nat.zero`",
        )

    case(
        "fingerprint preserves graph-list order",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_list_order,
    )

    def stale_pointer_order(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Library result"]["mathlib_declarations"] = [
            "Nat.succ",
            "Nat.zero",
        ]

    case(
        "Mathlib pointers follow exact graph declaration order",
        expected={"E_MATHLIB_POINTER_MISMATCH"},
        mutate=stale_pointer_order,
        selector="Cluster A",
    )

    def mutate_content_byte(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(
            files["informal_content/partial-result.md"]
        ).replace("claimed equality", "required equality")

    case(
        "fingerprint covers exact content bytes",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_content_byte,
    )

    def reorder_objects(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        library = graph["nodes"]["Library result"]
        graph["nodes"]["Library result"] = dict(reversed(list(library.items())))
        graph["nodes"] = dict(reversed(list(graph["nodes"].items())))

    case(
        "fingerprint ignores JSON object and graph-map insertion order",
        mutate=reorder_objects,
    )

    def swap_scope_fingerprints(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        finish(graph, files, scope)
        fingerprint_a = _fixture_fingerprint(graph, files, "Cluster A")
        fingerprint_b = _fixture_fingerprint(graph, files, "Cluster B")
        scope["content_complete_parents"] = [
            {"parent": "Cluster A", "fingerprint_sha256": fingerprint_b},
            {"parent": "Cluster B", "fingerprint_sha256": fingerprint_a},
        ]

    case(
        "parent-bound fingerprint domain rejects swapped fingerprints",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=swap_scope_fingerprints,
    )

    def mutate_lean_toolchain(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["lean_toolchain"] = "leanprover/lean4:v4.33.0"

    case(
        "fingerprint binds the Lean toolchain",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_lean_toolchain,
    )

    def mutate_mathlib_revision(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["mathlib_revision"] = "b" * 40

    case(
        "fingerprint binds the Mathlib revision",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_mathlib_revision,
    )

    def mutate_relevant_source_record(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["sources"][0]["title"] = "Retitled Relevant Source"

    case(
        "fingerprint binds relevant canonical source metadata",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_relevant_source_record,
    )

    def mutate_volatile_metadata(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["created_at"] = "2030-01-01T00:00:00Z"
        graph["metadata"]["last_updated"] = "2030-01-02T00:00:00Z"
        graph["metadata"]["lean_root"] = "/another/checkout"

    case(
        "fingerprint excludes volatile timestamps and checkout roots",
        mutate=mutate_volatile_metadata,
    )

    def reorder_source_manifest(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["sources"].reverse()

    case(
        "fingerprint canonicalizes metadata source order",
        mutate=reorder_source_manifest,
    )

    def add_unrelated_source(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["metadata"]["sources"].append(
            {
                "file": "sources/later.pdf",
                "title": "Later Unrelated Source",
                "format": "pdf",
                "sha256": "c" * 64,
            }
        )

    case(
        "unrelated later sources do not invalidate completed parents",
        mutate=add_unrelated_source,
    )

    def update_canonical_source(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        replacement = b"updated canonical fixture source\n"
        files["sources/test.pdf"] = replacement
        graph["metadata"]["sources"][0]["sha256"] = hashlib.sha256(
            replacement
        ).hexdigest()

    case(
        "fingerprint binds canonical source identities",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=update_canonical_source,
    )

    def corrupt_canonical_source(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["sources/test.pdf"] = b"corrupted canonical source\n"

    case(
        "local canonical source mismatches fail before fingerprinting",
        expected={"E_SOURCE_HASH_MISMATCH"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=corrupt_canonical_source,
    )

    def remove_gitignored_canonical_sources(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files.pop("sources/test.pdf")
        files.pop("sources/second.pdf")

    case(
        "declared identities allow absent gitignored canonical sources",
        mutate=remove_gitignored_canonical_sources,
    )

    def mutate_referenced_local_source(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["sources/notes.md"] = "changed tracked fixture notes\n"

    case(
        "fingerprint binds exact referenced local source bytes",
        expected={"E_SCOPE_FINGERPRINT"},
        mutate=mutate_referenced_local_source,
    )

    def remove_referenced_local_source(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files.pop("sources/notes.md")

    case(
        "missing referenced local sources fail before fingerprinting",
        expected={"E_SOURCE_MISSING"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=remove_referenced_local_source,
    )

    def wrong_h1(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(files["informal_content/partial-result.md"]).replace(
            "# Partial result", "# partial result", 1
        )

    case("requires exact H1 identity", expected={"E_H1_IDENTITY"}, mutate=wrong_h1)

    def exercise_number_h1(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        node = graph["nodes"].pop("Missing result")
        old_path = node["content"]
        node["id"] = "Exercise 1.1"
        node["content"] = "informal_content/exercise-1-1.md"
        graph["nodes"]["Exercise 1.1"] = node
        files[node["content"]] = str(files.pop(old_path)).replace(
            "# Missing result", "# Exercise 1.1", 1
        )

    case(
        "mandatory Exercise 1.1 H1 is not citation-scanned",
        mutate=exercise_number_h1,
        selector="Cluster A",
    )

    def bom_h1(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = "\ufeff" + str(files["informal_content/partial-result.md"])

    case("rejects a BOM before the H1", expected={"E_CONTENT_BOM", "E_H1_IDENTITY"}, mutate=bom_h1)

    def use_cr_lines(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(
            files["informal_content/partial-result.md"]
        ).replace("\n", "\r")

    case(
        "accepts CR physical lines",
        mutate=use_cr_lines,
        selector="Cluster A",
    )

    def use_crlf_lines(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(
            files["informal_content/partial-result.md"]
        ).replace("\n", "\r\n")

    case(
        "accepts CRLF physical lines",
        mutate=use_crlf_lines,
        selector="Cluster A",
    )

    def inject_body_control(
        files: dict[str, str | bytes], character: str
    ) -> None:
        files["informal_content/partial-result.md"] = str(
            files["informal_content/partial-result.md"]
        ).replace("\n\n## Proof", character + "## Proof")

    def body_line_separator(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        inject_body_control(files, "\u2028")

    case(
        "rejects U+2028 as a Markdown line separator",
        expected={"E_CONTENT_CONTROL", "E_PROOF_MISSING"},
        mutate=body_line_separator,
    )

    def body_paragraph_separator(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        inject_body_control(files, "\u2029")

    case(
        "rejects U+2029 as a Markdown line separator",
        expected={"E_CONTENT_CONTROL", "E_PROOF_MISSING"},
        mutate=body_paragraph_separator,
    )

    def body_vertical_tab(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        inject_body_control(files, "\v")

    case(
        "rejects vertical-tab line confusion",
        expected={"E_CONTENT_CONTROL", "E_PROOF_MISSING"},
        mutate=body_vertical_tab,
    )

    def body_form_feed(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        inject_body_control(files, "\f")

    case(
        "rejects form-feed line confusion",
        expected={"E_CONTENT_CONTROL", "E_PROOF_MISSING"},
        mutate=body_form_feed,
    )

    def body_next_line(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        inject_body_control(files, "\u0085")

    case(
        "rejects NEL line confusion",
        expected={"E_CONTENT_CONTROL", "E_PROOF_MISSING"},
        mutate=body_next_line,
    )

    def body_bidi_control(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(
            files["informal_content/partial-result.md"]
        ).replace("addition preserves", "addition \u202epreserves")

    case(
        "rejects bidi controls in Markdown prose",
        expected={"E_CONTENT_CONTROL"},
        mutate=body_bidi_control,
    )

    def duplicate_h1(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = str(files["informal_content/partial-result.md"]) + "\n# Extra\n"

    case("rejects a second H1", expected={"E_H1_EXTRA"}, mutate=duplicate_h1)

    def empty_statement(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = "# Partial result\n\n<!-- hidden -->\n\n## Proof\n\nA real proof body.\n"

    case("rejects comment-only statements", expected={"E_STATEMENT_EMPTY"}, mutate=empty_statement)

    def placeholder(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = "# Missing result\n\nTODO\n\n## Proof\n\nProof pending.\n"

    case("rejects explicit placeholders", expected={"E_CONTENT_PLACEHOLDER"}, mutate=placeholder)

    def missing_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = "# Missing result\n\nA complete-looking statement without its required proof.\n"

    case("requires proofs for missing nodes", expected={"E_PROOF_MISSING"}, mutate=missing_proof)

    def empty_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = "# Partial result\n\nA statement.\n\n## Proof\n\n<!-- absent -->\n"

    case("rejects empty proofs", expected={"E_PROOF_EMPTY"}, mutate=empty_proof)

    def noncanonical_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = "# Partial result\n\nA statement.\n\n### Proof\n\nAn argument.\n"

    case(
        "rejects noncanonical proof markers",
        expected={"E_PROOF_NONCANONICAL", "E_PROOF_MISSING"},
        mutate=noncanonical_proof,
    )

    def plain_proof_required(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = (
            "# Partial result\n\nA statement.\n\nProof:\n\nAn argument.\n"
        )

    case(
        "treats plain Proof paragraphs as noncanonical",
        expected={"E_PROOF_NONCANONICAL", "E_PROOF_MISSING"},
        mutate=plain_proof_required,
    )

    def bare_proof_required(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = (
            "# Partial result\n\nA statement.\n\nProof\n\nAn argument.\n"
        )

    case(
        "treats standalone bare Proof as noncanonical",
        expected={"E_PROOF_NONCANONICAL", "E_PROOF_MISSING"},
        mutate=bare_proof_required,
    )

    def hidden_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = (
            "# Partial result\n\nA statement.\n\n```markdown\n## Proof\nNot a rendered proof section.\n```\n"
        )

    case("does not count fenced proof markers", expected={"E_PROOF_MISSING"}, mutate=hidden_proof)

    def tilde_fence_with_backticks(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = (
            "# Partial result\n\nA statement followed by a literal example.\n\n"
            "~~~ markdown `literal`\n## Proof\nThis heading is literal.\n~~~\n\n"
            "## Proof\n\nThe actual proof is complete.\n"
        )

    case(
        "accepts tilde-fence info strings containing backticks",
        mutate=tilde_fence_with_backticks,
        selector="Cluster A",
    )

    def tilde_hidden_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/partial-result.md"] = (
            "# Partial result\n\nA statement.\n\n"
            "~~~ markdown `literal`\n## Proof\nNot a structural proof.\n~~~\n"
        )

    case(
        "does not count proof headings inside tilde fences with backticks",
        expected={"E_PROOF_MISSING"},
        forbidden={"E_MARKDOWN_FENCE", "E_PROOF_NONCANONICAL"},
        mutate=tilde_hidden_proof,
    )

    def forbidden_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(files["informal_content/library-result.md"]) + "\n**Proof.**\nAn argument.\n"

    case("forbids proofs for in-mathlib nodes", expected={"E_PROOF_FORBIDDEN"}, mutate=forbidden_proof)

    def forbidden_plain_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ) + "\nProof.\nAn argument.\n"

    case(
        "forbids plain Proof paragraphs for in-mathlib nodes",
        expected={"E_PROOF_FORBIDDEN"},
        mutate=forbidden_plain_proof,
    )

    def forbidden_bare_proof(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ) + "\nProof\nAn argument.\n"

    case(
        "forbids standalone bare Proof for in-mathlib nodes",
        expected={"E_PROOF_FORBIDDEN"},
        mutate=forbidden_bare_proof,
    )

    def noncanonical_mathlib(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(files["informal_content/library-result.md"]).replace(
            "## Mathlib", "### Mathlib"
        )

    case(
        "rejects noncanonical Mathlib sections",
        expected={"E_MATHLIB_NONCANONICAL", "E_MATHLIB_POINTER_MISSING"},
        mutate=noncanonical_mathlib,
    )

    def pointer_subset(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(files["informal_content/library-result.md"]).replace(
            "Declarations: `Nat.zero`, `Nat.succ`", "Declarations: `Nat.zero`"
        )

    case("requires every exact Mathlib declaration", expected={"E_MATHLIB_POINTER_MISMATCH"}, mutate=pointer_subset)

    def pointer_substring(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(files["informal_content/library-result.md"]).replace(
            "`Nat.succ`", "`Nat.succ.rec`"
        )

    case("does not accept declaration substrings", expected={"E_MATHLIB_POINTER_MISMATCH"}, mutate=pointer_substring)

    def pointer_comment(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = (
            "# Library result\n\nA complete statement.\n\n## Mathlib\n\n"
            "<!-- Declarations: `Nat.zero`, `Nat.succ`\nFile: `Mathlib/Data/Nat/Basic.lean` -->\n"
        )

    case("does not accept hidden Mathlib pointers", expected={"E_MATHLIB_POINTER_MISMATCH"}, mutate=pointer_comment)

    def source_leak(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = str(
            files["informal_content/missing-result.md"]
        ) + "\n<!-- sources/notes.md -->\n"

    case(
        "rejects the node's own source provenance inside comments",
        expected={"E_PROVENANCE_LEAK"},
        mutate=source_leak,
    )

    def own_location_leak(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = str(
            files["informal_content/missing-result.md"]
        ).replace("Apply the property", "A tracked note says to apply the property")

    case(
        "rejects the node's own exact source location",
        expected={"E_PROVENANCE_LEAK"},
        mutate=own_location_leak,
    )

    def own_metadata_title_leak(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ).replace(
            "For every natural number",
            "Test Source states that for every natural number",
        )

    case(
        "rejects matching canonical source titles",
        expected={"E_PROVENANCE_LEAK"},
        mutate=own_metadata_title_leak,
    )

    def unrelated_provenance_words(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ).replace(
            "For every natural number",
            "Independent Corpus and A tracked note are labels; for every natural number",
        )

    case(
        "unrelated metadata titles and node locations do not taint prose",
        mutate=unrelated_provenance_words,
        selector="Cluster A",
    )

    def unrelated_metadata_stability(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ).replace(
            "For every natural number",
            "Foreign Reference Corpus is a label; for every natural number",
        )
        graph["metadata"]["sources"].append(
            {
                "file": "sources/foreign.pdf",
                "title": "Foreign Reference Corpus",
                "format": "pdf",
                "sha256": "d" * 64,
            }
        )
        scope["content_complete_parents"][0]["fingerprint_sha256"] = (
            _fixture_fingerprint(graph, files, "Cluster A")
        )

    case(
        "adding unrelated metadata does not invalidate scoped prose",
        mutate=unrelated_metadata_stability,
    )

    def unrelated_node_ref_stability(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(
            files["informal_content/library-result.md"]
        ).replace(
            "For every natural number",
            "Other Node Unique Location is a label; for every natural number",
        )
        graph["nodes"]["Other result"]["source_refs"] = [
            {
                "file": "sources/test.pdf",
                "location": "Other Node Unique Location",
            }
        ]
        scope["content_complete_parents"][0]["fingerprint_sha256"] = (
            _fixture_fingerprint(graph, files, "Cluster A")
        )

    case(
        "adding an unrelated node reference does not invalidate scoped prose",
        mutate=unrelated_node_ref_stability,
    )

    def comment_leak(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = str(files["informal_content/missing-result.md"]) + "\n<!-- source_refs: Chapter 1 -->\n"

    case("detects provenance hidden in comments", expected={"E_PROVENANCE_LEAK"}, mutate=comment_leak)

    def citation_leaks(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = str(files["informal_content/missing-result.md"]) + "\nSee https://example.test and \\cite{source}.\n"

    case("rejects high-confidence citation syntax", expected={"E_CITATION_LEAK"}, mutate=citation_leaks)

    def false_positive_guard(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/library-result.md"] = str(files["informal_content/library-result.md"]).replace(
            "For every natural number, zero is no greater than its successor.",
            "For x in [0,1], P[X] is defined; the word proof is ordinary prose here.",
        )

    case(
        "accepts non-citation brackets and ordinary proof wording",
        mutate=false_positive_guard,
        selector="Cluster A",
    )

    def orphan_md(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/nested/orphan.md"] = "# Orphan\n"

    case("rejects nested orphan Markdown", expected={"E_CONTENT_ORPHAN"}, mutate=orphan_md)

    def orphan_nonmd(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/notes.txt"] = "orphan"

    case("rejects orphan non-Markdown files", expected={"E_CONTENT_ORPHAN"}, mutate=orphan_nonmd)

    def duplicate_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Partial result"]["content"] = "informal_content/library-result.md"

    case(
        "rejects duplicate graph ownership before fingerprinting",
        expected={"E_CONTENT_PATH_DUPLICATE"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=duplicate_path,
    )

    def traversal(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/../escape.md"

    case("rejects traversal content paths", expected={"E_CONTENT_PATH"}, mutate=traversal)

    def backslash_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content\\missing-result.md"

    case("rejects backslash content paths", expected={"E_CONTENT_PATH"}, mutate=backslash_path)

    def newline_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/missing\nresult.md"

    case("rejects control characters in content paths", expected={"E_CONTENT_PATH"}, mutate=newline_path)

    def del_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/missing\x7fresult.md"

    case("rejects DEL in content paths", expected={"E_CONTENT_PATH"}, mutate=del_path)

    def real_nel_content_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        old_path = graph["nodes"]["Missing result"]["content"]
        bad_path = "informal_content/missing\u0085result.md"
        graph["nodes"]["Missing result"]["content"] = bad_path
        files[bad_path] = files.pop(old_path)

    case(
        "rejects a real NEL content filename",
        expected={"E_CONTENT_PATH", "E_CONTENT_ORPHAN"},
        mutate=real_nel_content_path,
    )

    def real_c1_source_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        bad_path = "sources/notes\u0081.md"
        graph["nodes"]["Missing result"]["source_refs"][0]["file"] = bad_path
        files[bad_path] = files.pop("sources/notes.md")

    case(
        "rejects a real C1 source filename",
        expected={"E_SOURCE_PATH"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=real_c1_source_path,
    )

    def line_separator_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/missing\u2028result.md"

    case(
        "rejects Unicode line separators in content paths",
        expected={"E_CONTENT_PATH"},
        mutate=line_separator_path,
    )

    def paragraph_separator_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/missing\u2029result.md"

    case(
        "rejects Unicode paragraph separators in content paths",
        expected={"E_CONTENT_PATH"},
        mutate=paragraph_separator_path,
    )

    def bidi_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "informal_content/missing\u202eresult.md"

    case("rejects bidi controls in content paths", expected={"E_CONTENT_PATH"}, mutate=bidi_path)

    def absolute_path(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Missing result"]["content"] = "/tmp/missing-result.md"

    case("rejects absolute content paths", expected={"E_CONTENT_PATH"}, mutate=absolute_path)

    def invalid_utf8(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files["informal_content/missing-result.md"] = b"\xff\xfe"

    case(
        "rejects invalid UTF-8 before fingerprinting",
        expected={"E_CONTENT_UTF8"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=invalid_utf8,
    )

    def missing_file(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files.pop("informal_content/missing-result.md")

    case(
        "does not fingerprint after an incomplete read",
        expected={"E_CONTENT_MISSING"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=missing_file,
    )

    def symlink_mutation(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        files.pop("informal_content/missing-result.md")

    def make_symlink(root: Path) -> None:
        target = root / "outside.md"
        target.write_text("# Missing result\n", encoding="utf-8")
        os.symlink(target, root / "informal_content" / "missing-result.md")

    case(
        "rejects symlinked content",
        expected={"E_CONTENT_SYMLINK"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        mutate=symlink_mutation,
        post=make_symlink,
    )

    def make_hardlink(root: Path) -> None:
        alias = root / "informal_content" / "partial-result.md"
        alias.unlink()
        os.link(root / "informal_content" / "library-result.md", alias)

    case(
        "rejects hard-linked content aliases before fingerprinting",
        expected={"E_CONTENT_HARDLINK"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        post=make_hardlink,
    )

    def make_external_hardlink(root: Path) -> None:
        os.link(
            root / "informal_content" / "library-result.md",
            root / "outside-content-alias.md",
        )

    case(
        "rejects hard-linked aliases outside the content inventory",
        expected={"E_CONTENT_HARDLINK"},
        forbidden={"E_SCOPE_FINGERPRINT"},
        post=make_external_hardlink,
    )

    def tier1_content(graph: dict[str, Any], files: dict[str, str | bytes], scope: dict[str, Any]) -> None:
        graph["nodes"]["Cluster A"]["content"] = "informal_content/cluster-a.md"
        files["informal_content/cluster-a.md"] = "# Cluster A\n"

    case("rejects content owned by tier 1", expected={"E_NON_TIER2_CONTENT", "E_CONTENT_ORPHAN"}, mutate=tier1_content)

    with tempfile.TemporaryDirectory(prefix="check-informal-content-final-scope-") as directory:
        root = Path(directory)
        graph, files, scope = _fixture()
        _write_fixture(root, graph, files, scope)
        try:
            validate_gate(root / "graph.json", root, GateOptions(mode="final"))
        except InputError:
            print("PASS self-test final mode refuses to bypass the durable scope")
        else:
            passed = False
            print("FAIL self-test final mode refuses to bypass the durable scope")

    with tempfile.TemporaryDirectory(prefix="check-informal-content-json-") as directory:
        root = Path(directory)
        (root / "graph.json").write_text('{"version": 2, "version": 2}', encoding="utf-8")
        try:
            validate_gate(root / "graph.json", root, GateOptions(mode="incremental", lint_only=True))
        except InputError:
            print("PASS self-test rejects duplicate graph JSON keys")
        else:
            passed = False
            print("FAIL self-test rejects duplicate graph JSON keys")

    with tempfile.TemporaryDirectory(prefix="check-informal-content-scope-") as directory:
        root = Path(directory)
        graph, files, scope = _fixture()
        _write_fixture(root, graph, files, scope)
        (root / "sources" / "phase2_content_scope.json").write_text(
            '{"version":3,"tier":2,"content_complete_parents":[],"tier":2}',
            encoding="utf-8",
        )
        try:
            validate_gate(
                root / "graph.json",
                root,
                GateOptions(mode="incremental", scope_path=Path("sources/phase2_content_scope.json")),
            )
        except InputError:
            print("PASS self-test rejects duplicate scope JSON keys")
        else:
            passed = False
            print("FAIL self-test rejects duplicate scope JSON keys")

    with tempfile.TemporaryDirectory(prefix="check-informal-content-order-") as directory:
        root = Path(directory)
        graph, files, scope = _fixture()
        files["informal_content/orphan.txt"] = "orphan"
        files["informal_content/partial-result.md"] = "# wrong\n\nTODO\n"
        _write_fixture(root, graph, files, scope)
        options = GateOptions(mode="incremental", scope_path=Path("sources/phase2_content_scope.json"))
        first = [finding.render() for finding in validate_gate(root / "graph.json", root, options).findings]
        graph["nodes"] = dict(reversed(list(graph["nodes"].items())))
        (root / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
        second = [finding.render() for finding in validate_gate(root / "graph.json", root, options).findings]
        if first == second:
            print("PASS self-test diagnostics are insertion-order deterministic")
        else:
            passed = False
            print("FAIL self-test diagnostics are insertion-order deterministic")

    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", nargs="?", type=Path, default=Path("graph.json"))
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--mode", choices=("incremental", "final"), default="incremental")
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--scope", type=Path)
    selector.add_argument("--parent", action="append", default=[])
    selector.add_argument("--all-split-parents", action="store_true")
    selector.add_argument("--lint-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_tests()

    graph_path = args.graph.resolve()
    project_root = args.project_root.resolve() if args.project_root else graph_path.parent
    scope_path = args.scope
    if args.mode == "incremental" and not (
        scope_path is not None or args.parent or args.all_split_parents or args.lint_only
    ):
        scope_path = Path("sources/phase2_content_scope.json")
    options = GateOptions(
        mode=args.mode,
        scope_path=scope_path,
        parents=tuple(args.parent),
        all_split_parents=args.all_split_parents,
        lint_only=args.lint_only,
    )
    try:
        result = validate_gate(graph_path, project_root, options)
    except InputError as error:
        print(f"ERROR input: {error}", file=sys.stderr)
        return 2

    for finding in result.findings:
        print(finding.render())
    if result.findings:
        print(
            f"Content summary: {len(result.findings)} error(s); "
            f"{result.document_count}/{result.tier2_count} tier-2 document(s) readable"
        )
        return 1

    if args.parent:
        for parent, fingerprint in result.parent_fingerprints:
            print(_scope_entry_output(parent, fingerprint))

    print(
        "PASS informal content gate: "
        f"mode={options.mode}; selector={_diagnostic_text(result.selection_label)}; "
        f"tier2={result.tier2_count}; documents={result.document_count}; "
        f"content-complete parents asserted={len(result.selected_parents)}; "
        f"parents outside scope={len(result.pending_parents)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
