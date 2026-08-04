#!/usr/bin/env python3
"""Reproducibly export, build, check, and serve this project's blueprint.

The Autoform exporter is deliberately treated as an external, versioned input.
This driver is Linux-only: safe replacement of an existing tree requires
``renameat2(RENAME_EXCHANGE)`` on the destination filesystem.
Run ``python3 scripts/blueprint.py --help`` for the supported workflow.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import html.parser
import http.server
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import dataclass, replace
from functools import partial
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


AUTOFORM_VERSION = "0.4.4"
PYTHON_VERSION = "3.12.13"
UV_VERSION = "0.11.15"
GRAPHVIZ_VERSION = "2.44.0"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIRECT_REQUIREMENTS = Path(__file__).with_name("blueprint-requirements.txt")
REQUIREMENTS_LOCK = Path(__file__).with_name("blueprint-requirements.lock")
OWNER_SENTINEL = ".autoform-blueprint-owner.json"
SOURCE_PROVENANCE = ".blueprint-provenance.json"
RUNTIME_MANIFEST = ".blueprint-runtime-assets.json"
TOOLCHAIN_PROVENANCE = ".blueprint-toolchain-provenance.json"

# These are the complete Autoform files that influence export, plus the plugin
# manifest and governing visualization runbook. A same-version modified plugin
# is not accepted silently.
AUTOFORM_FILE_HASHES = {
    ".codex-plugin/plugin.json": "835165f60f9692c7ab6268f5572bb0b85464fb72ba025120ae5cfed92e9f6f02",
    "scripts/export_blueprint.py": "5ec040db8f3568887568d83375070f3845025978f79a72a1a153a5accd415352",
    "templates/dep_graph.html": "e0ed22463c04c70e17e14c5a1cb70901556bd8309a39f9b2512133126b56f044",
    "assets/review/dep_graph_core.js": "e9c60d1c4cbc4368dad9b76b7ced351543b6b8fe9d450e65f0bdfd9f732d1758",
    "internal/runbooks/visualization.md": "4ad89193ecc7f394bec19a3e3c77947ddc2f7b755b2c8c0f620296e84553e0b4",
}

CORE_GRAPHVIZ_LIBRARIES = (
    "libcdt",
    "libcgraph",
    "libgvc",
    "libpathplan",
    "libxdot",
)

# pygraphviz loads libgvc in the platform Python process. These are the full
# non-libc library families observed in that loader closure on supported hosts.
GRAPHVIZ_LOADER_LIBRARIES = CORE_GRAPHVIZ_LIBRARIES + (
    "libexpat",
    "libltdl",
    "libz",
    "libgobject-2.0",
    "libglib-2.0",
    "libffi",
    "libpcre",
    "libXrender",
    "libX11",
    "libXext",
    "libxcb",
    "libXau",
)

REQUIRED_WEB_FILES = (
    "dep_graph_document.html",
    "index.html",
    "symbol-defs.svg",
    "styles/dep_graph.css",
    "styles/extra_styles.css",
    "js/d3-graphviz.js",
    "js/d3.min.js",
    "js/dep_graph_core.js",
    "js/hpcc.min.js",
    "js/jquery.min.js",
    "js/plastex.js",
    "js/tier_dots.js",
    "js/expatlib.wasm",
    "js/graphvizlib.wasm",
)

RUNTIME_SUFFIXES = {".css", ".js", ".wasm"}

PACKAGE_IMPORTS = {
    "fastmcp": "fastmcp",
    "leanblueprint": "leanblueprint",
    "plasTeX": "plasTeX",
    "plastexdepgraph": "plastexdepgraph",
    "plastexshowmore": "plastexshowmore",
    "pygraphviz": "pygraphviz",
}


class BlueprintError(RuntimeError):
    """A user-facing blueprint workflow failure."""


@dataclass(frozen=True)
class Paths:
    project: Path
    graph: Path
    output: Path
    tool_state: Path
    venv: Path
    gvlibs: Path
    plugin: Path

    @property
    def source(self) -> Path:
        return self.output / "blueprint" / "src"

    @property
    def web(self) -> Path:
        return self.output / "blueprint" / "web"

    @property
    def python(self) -> Path:
        return self.venv / "bin" / "python"

    @property
    def plastex(self) -> Path:
        return self.venv / "bin" / "plastex"

    @property
    def toolchain_provenance(self) -> Path:
        return self.tool_state / TOOLCHAIN_PROVENANCE

    def at_tool_state(self, tool_state: Path) -> "Paths":
        return replace(
            self,
            tool_state=tool_state,
            venv=tool_state / ".venv",
            gvlibs=tool_state / "gvlibs",
        )


@dataclass(frozen=True)
class GraphInfo:
    raw: dict[str, object]
    nodes: dict[str, dict[str, object]]
    tiers: tuple[int, ...]
    nodes_by_tier: dict[int, tuple[str, ...]]
    edges: tuple[tuple[str, str], ...]
    slugs: dict[str, str]

    @property
    def edge_count(self) -> int:
        return len(self.edges)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
    except FileNotFoundError as exc:
        raise BlueprintError(f"missing file: {path}") from exc
    return digest.hexdigest()


def _canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def _write_json(path: Path, value: object) -> None:
    path.write_text(_canonical_json(value), encoding="utf-8")


def _relative_display(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BlueprintError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BlueprintError(f"invalid JSON in {path}: {exc}") from exc


def _plugin_error(root: Path, detail: str) -> BlueprintError:
    return BlueprintError(f"invalid Autoform plugin root {root}: {detail}")


def _verify_plugin(root: Path) -> Path:
    root = root.expanduser().resolve()
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise _plugin_error(root, "plugin.json is not an object")
    if manifest.get("name") != "autoform":
        raise _plugin_error(root, "plugin name is not 'autoform'")
    if manifest.get("version") != AUTOFORM_VERSION:
        raise _plugin_error(
            root,
            f"need version {AUTOFORM_VERSION}, found {manifest.get('version')!r}",
        )

    missing = [relative for relative in AUTOFORM_FILE_HASHES if not (root / relative).is_file()]
    if missing:
        raise _plugin_error(root, "missing " + ", ".join(missing))
    mismatches = {
        relative: {"expected": expected, "actual": _sha256(root / relative)}
        for relative, expected in AUTOFORM_FILE_HASHES.items()
        if _sha256(root / relative) != expected
    }
    if mismatches:
        raise _plugin_error(root, f"file digest mismatch: {mismatches}")
    return root


def _installed_plugin_candidates() -> Iterable[Path]:
    homes: list[Path] = []
    if os.environ.get("CODEX_HOME"):
        homes.append(Path(os.environ["CODEX_HOME"]).expanduser())
    homes.append(Path.home() / ".codex")

    seen: set[Path] = set()
    for home in homes:
        patterns = (
            f"plugins/cache/*/autoform/{AUTOFORM_VERSION}",
            f"plugins/cache/autoform/*/{AUTOFORM_VERSION}",
            f"plugins/autoform/{AUTOFORM_VERSION}",
        )
        for pattern in patterns:
            for candidate in sorted(home.glob(pattern)):
                resolved = candidate.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    yield resolved


def resolve_plugin(explicit: str | None) -> Path:
    if explicit:
        return _verify_plugin(Path(explicit))

    configured = os.environ.get("AUTOFORM_PLUGIN_ROOT")
    if configured:
        return _verify_plugin(Path(configured))

    failures: list[str] = []
    for candidate in _installed_plugin_candidates():
        try:
            return _verify_plugin(candidate)
        except BlueprintError as exc:
            failures.append(str(exc))

    suffix = ""
    if failures:
        suffix = "\n" + "\n".join(f"  {item}" for item in failures)
    raise BlueprintError(
        f"Autoform {AUTOFORM_VERSION} is not installed; set AUTOFORM_PLUGIN_ROOT "
        f"to its exact plugin root{suffix}"
    )


def _resolve_under(base: Path, value: str | None, default: str) -> Path:
    path = Path(value) if value else Path(default)
    if not path.is_absolute():
        path = base / path
    return path.expanduser().resolve()


def _require_linux() -> None:
    if not sys.platform.startswith("linux"):
        raise BlueprintError(
            "the blueprint driver is Linux-only because it requires atomic "
            "renameat2(RENAME_EXCHANGE) tree promotion"
        )


def _reject_symlink_components(path: Path) -> None:
    absolute = path.expanduser().absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        if current.is_symlink():
            raise BlueprintError(f"refusing path with symlink component: {current}")
        if not current.exists():
            break


def _project_id(project: Path) -> str:
    value = "autoform-blueprint-owner-v1\0" + str(project.resolve())
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _owner_payload(project: Path) -> dict[str, object]:
    return {
        "schema_version": 1,
        "project": str(project.resolve()),
        "project_id": _project_id(project),
    }


def _is_default_output(paths: Paths) -> bool:
    return paths.output == (paths.project / "blueprint_export").resolve()


def _protected_roots(project: Path) -> tuple[Path, ...]:
    roots = [
        project / ".autoform",
        project / ".git",
        project / ".lake",
        project / "scripts",
        project / "sources",
        project / "informal_content",
    ]
    for lean_entry in project.glob("*.lean"):
        module_tree = project / lean_entry.stem
        if module_tree.is_dir():
            roots.append(module_tree)
    return tuple(root.resolve() for root in roots if root.exists())


def _assert_output_safe(paths: Paths) -> None:
    _require_linux()
    _reject_symlink_components(paths.output)
    output = paths.output.resolve()
    project = paths.project.resolve()
    if output == project or output in project.parents:
        raise BlueprintError(f"refusing output that contains the project: {output}")
    for protected in _protected_roots(project):
        if output == protected or protected in output.parents:
            raise BlueprintError(f"refusing output inside protected project tree: {protected}")
    if output.exists() and not output.is_dir():
        raise BlueprintError(f"output exists and is not a directory: {output}")

    sentinel = output / OWNER_SENTINEL
    if sentinel.exists() or sentinel.is_symlink():
        if sentinel.is_symlink() or not sentinel.is_file():
            raise BlueprintError(f"invalid blueprint ownership sentinel: {sentinel}")
        if _read_json(sentinel) != _owner_payload(project):
            raise BlueprintError(f"blueprint ownership sentinel does not match project: {sentinel}")
    elif output.exists() and not _is_default_output(paths):
        raise BlueprintError(
            f"existing non-default output lacks a matching {OWNER_SENTINEL}: {output}"
        )


def _write_owner_sentinel(paths: Paths, output: Path | None = None) -> None:
    destination = output or paths.output
    _write_json(destination / OWNER_SENTINEL, _owner_payload(paths.project))


def make_paths(args: argparse.Namespace) -> Paths:
    _require_linux()
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        raise BlueprintError(f"project directory does not exist: {project}")
    graph = _resolve_under(project, args.graph, "graph.json")
    raw_output = Path(args.output) if args.output else Path("blueprint_export")
    if not raw_output.is_absolute():
        raw_output = project / raw_output
    raw_output = raw_output.expanduser().absolute()
    _reject_symlink_components(raw_output)
    output = raw_output.resolve()

    plugin = resolve_plugin(args.plugin_root)
    tool_state = project / ".autoform" / "blueprint-toolchain"
    paths = Paths(
        project=project,
        graph=graph,
        output=output,
        tool_state=tool_state,
        venv=tool_state / ".venv",
        gvlibs=tool_state / "gvlibs",
        plugin=plugin,
    )
    _assert_output_safe(paths)
    return paths


def _run(command: Sequence[os.PathLike[str] | str], **kwargs: object) -> None:
    printable = " ".join(str(part) for part in command)
    print(f"+ {printable}", flush=True)
    try:
        subprocess.run([str(part) for part in command], check=True, **kwargs)
    except FileNotFoundError as exc:
        raise BlueprintError(f"command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise BlueprintError(f"command failed with exit code {exc.returncode}: {printable}") from exc


_SLUG_KEEP = re.compile(r"[^A-Za-z0-9_:.]+")


def _make_slug(name: str) -> str:
    slug = _SLUG_KEEP.sub("_", name).strip("_") or "node"
    if slug[0].isdigit():
        slug = "n_" + slug
    return slug


def _slug_map(ids: Iterable[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    used: set[str] = set()
    for node_id in sorted(ids):
        base = _make_slug(node_id)
        slug = base
        suffix = 2
        while slug in used:
            slug = f"{base}_{suffix}"
            suffix += 1
        used.add(slug)
        result[node_id] = slug
    return result


def _load_graph(graph_path: Path) -> GraphInfo:
    raw_value = _read_json(graph_path)
    if not isinstance(raw_value, dict):
        raise BlueprintError(f"graph root is not an object: {graph_path}")
    raw_nodes = raw_value.get("nodes", raw_value.get("concepts"))
    nodes: dict[str, dict[str, object]] = {}
    if isinstance(raw_nodes, dict):
        for key, value in raw_nodes.items():
            if not isinstance(key, str) or not isinstance(value, dict):
                raise BlueprintError("graph nodes map must have string keys and object values")
            node = dict(value)
            node.setdefault("id", key)
            if node.get("id") != key:
                raise BlueprintError(f"node key {key!r} disagrees with its id field")
            nodes[key] = node
    elif isinstance(raw_nodes, list):
        for index, value in enumerate(raw_nodes):
            if not isinstance(value, dict) or not isinstance(value.get("id"), str):
                raise BlueprintError(f"graph node {index} has no string id")
            node_id = value["id"]
            if node_id in nodes:
                raise BlueprintError(f"graph has duplicate node id: {node_id}")
            nodes[node_id] = dict(value)
    else:
        raise BlueprintError("graph has no nodes object or list")
    if not nodes:
        raise BlueprintError("graph has no nodes")

    by_tier: dict[int, list[str]] = {}
    edges: list[tuple[str, str]] = []
    for node_id, node in nodes.items():
        tier_value = node.get("tier", 2)
        if isinstance(tier_value, bool):
            raise BlueprintError(f"node {node_id!r} has invalid tier {tier_value!r}")
        try:
            tier = int(tier_value)
        except (TypeError, ValueError) as exc:
            raise BlueprintError(f"node {node_id!r} has invalid tier {tier_value!r}") from exc
        if tier < 1 or tier_value != tier:
            raise BlueprintError(f"node {node_id!r} has invalid tier {tier_value!r}")
        by_tier.setdefault(tier, []).append(node_id)

        dependencies = node.get("depends_on", []) or []
        if not isinstance(dependencies, list) or not all(
            isinstance(dependency, str) for dependency in dependencies
        ):
            raise BlueprintError(f"node {node_id!r} has non-string dependencies")
        if len(dependencies) != len(set(dependencies)):
            raise BlueprintError(f"node {node_id!r} has duplicate dependencies")
        for dependency in dependencies:
            if dependency not in nodes:
                raise BlueprintError(f"dangling graph edge: {dependency!r} -> {node_id!r}")
            if dependency == node_id:
                raise BlueprintError(f"self graph edge: {node_id!r}")
            edges.append((dependency, node_id))

    return GraphInfo(
        raw=raw_value,
        nodes=nodes,
        tiers=tuple(sorted(by_tier)),
        nodes_by_tier={tier: tuple(sorted(ids)) for tier, ids in by_tier.items()},
        edges=tuple(sorted(edges)),
        slugs=_slug_map(nodes),
    )


def _graph_node_ids(graph_path: Path) -> list[str]:
    return list(_load_graph(graph_path).nodes)


def _replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise BlueprintError(f"expected exactly one {old!r} in {path}, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def _repair_extra_js(config: Path) -> None:
    lines = config.read_text(encoding="utf-8").splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip().startswith("extra-js=")]
    if len(matches) != 1:
        raise BlueprintError(f"expected one extra-js entry in {config}, found {len(matches)}")
    index = matches[0]
    _, value = lines[index].split("=", 1)
    assets = [item for item in re.split(r"[\s,]+", value.strip()) if item]
    expected = ["tier_dots.js", "dep_graph_core.js"]
    if sorted(assets) != sorted(expected):
        raise BlueprintError(f"unexpected extra-js assets in {config}: {assets}")
    lines[index] = "extra-js=" + " ".join(expected)
    config.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _promote_macros(source: Path) -> None:
    macro_names = {
        "common": "autoform_common_macros.tex",
        "web": "autoform_web_macros.tex",
        "print": "autoform_print_macros.tex",
    }
    macros = source / "macros"
    for old_name, new_name in macro_names.items():
        old_path = macros / f"{old_name}.tex"
        if not old_path.is_file():
            raise BlueprintError(f"exporter did not create {old_path}")
        os.replace(old_path, source / new_name)
    try:
        macros.rmdir()
    except OSError as exc:
        raise BlueprintError(f"unexpected files remain in {macros}") from exc

    _replace_once(
        source / "web.tex",
        "\\input{macros/common}\n",
        "\\input{autoform_common_macros.tex}\n",
    )
    _replace_once(
        source / "web.tex",
        "\\input{macros/web}\n",
        "\\input{autoform_web_macros.tex}\n",
    )
    _replace_once(
        source / "print.tex",
        "\\input{macros/common}\n",
        "\\input{autoform_common_macros.tex}\n",
    )
    _replace_once(
        source / "print.tex",
        "\\input{macros/print}\n",
        "\\input{autoform_print_macros.tex}\n",
    )
    for tex_name in ("web.tex", "print.tex"):
        _replace_once(source / tex_name, "\\input{content}\n", "\\input{content.tex}\n")


def _js_json_constant(text: str, name: str, path: Path) -> object:
    match = re.search(rf"^const {re.escape(name)} = (.+);$", text, flags=re.MULTILINE)
    if not match:
        raise BlueprintError(f"cannot find {name} in {path}")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise BlueprintError(f"invalid {name} JSON in {path}: {exc}") from exc


def _tier_edges(graph: GraphInfo) -> dict[int, set[tuple[str, str]]]:
    result: dict[int, set[tuple[str, str]]] = {tier: set() for tier in graph.tiers}
    node_tiers = {
        node_id: int(node.get("tier", 2)) for node_id, node in graph.nodes.items()
    }
    tier1 = set(graph.nodes_by_tier.get(1, ()))
    tier2 = set(graph.nodes_by_tier.get(2, ()))
    if tier1 and tier2:
        parents = {
            node_id: node.get("parent")
            for node_id, node in graph.nodes.items()
            if node_id in tier2 and node.get("parent") in tier1
        }
        for dependency, dependent in graph.edges:
            if dependency not in tier2 or dependent not in tier2:
                continue
            source_parent = parents.get(dependency)
            target_parent = parents.get(dependent)
            if source_parent and target_parent and source_parent != target_parent:
                result[1].add((graph.slugs[source_parent], graph.slugs[target_parent]))
    else:
        for dependency, dependent in graph.edges:
            if node_tiers[dependency] == node_tiers[dependent] == 1:
                result[1].add((graph.slugs[dependency], graph.slugs[dependent]))

    for tier in graph.tiers:
        if tier == 1:
            continue
        for dependency, dependent in graph.edges:
            if node_tiers[dependency] == node_tiers[dependent] == tier:
                result[tier].add((graph.slugs[dependency], graph.slugs[dependent]))
    return result


def _dot_structure(dot: str, path: Path, tier: int) -> tuple[set[str], set[tuple[str, str]]]:
    if not dot.strip():
        raise BlueprintError(f"DOT_TIER{tier} is empty in {path}")
    nodes = set(re.findall(r'^\s*"([A-Za-z0-9_:.]+)"\s+\[', dot, flags=re.MULTILINE))
    edges = set(
        re.findall(
            r'^\s*"([A-Za-z0-9_:.]+)"\s*->\s*"([A-Za-z0-9_:.]+)"',
            dot,
            flags=re.MULTILINE,
        )
    )
    if not nodes:
        raise BlueprintError(f"DOT_TIER{tier} has no nodes in {path}")
    return nodes, edges


def _check_graph_javascript(graph: GraphInfo, javascript: Path) -> int:
    text = javascript.read_text(encoding="utf-8")
    tiers_value = _js_json_constant(text, "TIERS_PRESENT", javascript)
    if tiers_value != list(graph.tiers):
        raise BlueprintError(
            f"TIERS_PRESENT mismatch in {javascript}: expected {list(graph.tiers)}, "
            f"found {tiers_value!r}"
        )

    names = _js_json_constant(text, "TIER_NODE_NAMES", javascript)
    expected_names = {graph.slugs[node_id]: node_id for node_id in graph.nodes}
    if names != expected_names:
        raise BlueprintError(f"TIER_NODE_NAMES does not exactly match graph nodes: {javascript}")

    expected_edges = _tier_edges(graph)
    edges_value = _js_json_constant(text, "TIER_EDGES", javascript)
    if not isinstance(edges_value, dict) or set(edges_value) != {str(t) for t in graph.tiers}:
        raise BlueprintError(f"TIER_EDGES tier keys do not match graph tiers: {javascript}")
    for tier in graph.tiers:
        value = edges_value[str(tier)]
        if not isinstance(value, list) or not all(
            isinstance(edge, list)
            and len(edge) == 2
            and all(isinstance(endpoint, str) for endpoint in edge)
            for edge in value
        ):
            raise BlueprintError(f"TIER_EDGES[{tier}] is malformed in {javascript}")
        actual = {tuple(edge) for edge in value}
        if len(actual) != len(value) or actual != expected_edges[tier]:
            raise BlueprintError(
                f"TIER_EDGES[{tier}] mismatch: expected {len(expected_edges[tier])}, "
                f"found {len(actual)}"
            )

    dot_tiers = {
        int(match.group(1))
        for match in re.finditer(r"^const DOT_TIER([0-9]+) =", text, flags=re.MULTILINE)
    }
    if dot_tiers != set(graph.tiers):
        raise BlueprintError(f"DOT tier constants do not match graph tiers: {javascript}")
    for tier in graph.tiers:
        dot_value = _js_json_constant(text, f"DOT_TIER{tier}", javascript)
        if not isinstance(dot_value, str):
            raise BlueprintError(f"DOT_TIER{tier} is not a string in {javascript}")
        dot_nodes, dot_edges = _dot_structure(dot_value, javascript, tier)
        expected_nodes = {graph.slugs[node_id] for node_id in graph.nodes_by_tier[tier]}
        if dot_nodes != expected_nodes:
            raise BlueprintError(
                f"DOT_TIER{tier} node mismatch: missing={sorted(expected_nodes - dot_nodes)}, "
                f"extra={sorted(dot_nodes - expected_nodes)}"
            )
        if dot_edges != expected_edges[tier]:
            raise BlueprintError(
                f"DOT_TIER{tier} edge mismatch: missing={sorted(expected_edges[tier] - dot_edges)}, "
                f"extra={sorted(dot_edges - expected_edges[tier])}"
            )
    return len(graph.nodes)


def _content_file(paths: Paths, graph: GraphInfo, node_id: str) -> Path | None:
    node = graph.nodes[node_id]
    content_dir = paths.project / "informal_content"
    candidates: list[Path] = []
    declared = node.get("content")
    if declared is not None and not isinstance(declared, str):
        raise BlueprintError(f"node {node_id!r} has a non-string content reference")
    if declared:
        candidate = Path(declared)
        if candidate.is_absolute():
            candidates.append(candidate)
        else:
            candidates.extend((paths.project / candidate, content_dir / candidate))
    candidates.extend(
        (content_dir / f"{node_id}.md", content_dir / f"{graph.slugs[node_id]}.md")
    )
    for candidate in candidates:
        if candidate.is_file():
            resolved = candidate.resolve()
            try:
                resolved.relative_to(paths.project)
            except ValueError as exc:
                raise BlueprintError(f"content reference escapes project: {resolved}") from exc
            return resolved
    if declared:
        raise BlueprintError(f"declared content file for {node_id!r} does not exist: {declared}")
    return None


def _input_provenance(paths: Paths, title: str | None) -> dict[str, object]:
    _verify_plugin(paths.plugin)
    graph = _load_graph(paths.graph)
    contents = []
    for node_id in sorted(graph.nodes):
        content = _content_file(paths, graph, node_id)
        if content is not None:
            contents.append(
                {
                    "node": node_id,
                    "path": _relative_display(content, paths.project),
                    "sha256": _sha256(content),
                }
            )

    sources = []
    metadata = graph.raw.get("metadata", {})
    if isinstance(metadata, dict):
        source_entries = metadata.get("sources", []) or []
        if not isinstance(source_entries, list):
            raise BlueprintError("graph metadata.sources is not a list")
        for index, entry in enumerate(source_entries):
            if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
                raise BlueprintError(f"graph source {index} has no string file")
            source = (paths.project / entry["file"]).resolve()
            try:
                source.relative_to(paths.project)
            except ValueError as exc:
                raise BlueprintError(f"graph source escapes project: {source}") from exc
            actual_hash = _sha256(source)
            declared_hash = entry.get("sha256")
            if declared_hash is not None and declared_hash != actual_hash:
                raise BlueprintError(
                    f"graph source digest mismatch for {entry['file']}: "
                    f"declared {declared_hash}, actual {actual_hash}"
                )
            sources.append(
                {
                    "path": _relative_display(source, paths.project),
                    "sha256": actual_hash,
                }
            )

    driver_files = {
        _relative_display(path, paths.project): _sha256(path)
        for path in (Path(__file__).resolve(), DIRECT_REQUIREMENTS, REQUIREMENTS_LOCK)
    }
    return {
        "schema_version": 1,
        "project_id": _project_id(paths.project),
        "graph": {
            "path": _relative_display(paths.graph, paths.project),
            "sha256": _sha256(paths.graph),
            "tier_count": len(graph.tiers),
            "tiers": list(graph.tiers),
            "tier_node_counts": {
                str(tier): len(graph.nodes_by_tier[tier]) for tier in graph.tiers
            },
            "node_count": len(graph.nodes),
            "edge_count": graph.edge_count,
        },
        "content_files": contents,
        "source_files": sources,
        "autoform": {
            "version": AUTOFORM_VERSION,
            "files": {
                relative: _sha256(paths.plugin / relative)
                for relative in sorted(AUTOFORM_FILE_HASHES)
            },
        },
        "driver_files": driver_files,
        "export_options": {"title": title},
    }


def _export_asset_hashes(output: Path) -> dict[str, str]:
    source = output / "blueprint" / "src"
    files = [path for path in source.rglob("*") if path.is_file()]
    return {
        path.relative_to(output).as_posix(): _sha256(path)
        for path in sorted(files)
        if path.name != SOURCE_PROVENANCE
    }


def _write_source_provenance(paths: Paths, output: Path, title: str | None) -> None:
    provenance = {
        "inputs": _input_provenance(paths, title),
        "export_assets": _export_asset_hashes(output),
    }
    _write_json(output / "blueprint" / "src" / SOURCE_PROVENANCE, provenance)


def _check_source_provenance(paths: Paths, output: Path) -> dict[str, object]:
    provenance_path = output / "blueprint" / "src" / SOURCE_PROVENANCE
    value = _read_json(provenance_path)
    if not isinstance(value, dict) or not isinstance(value.get("inputs"), dict):
        raise BlueprintError(f"invalid source provenance: {provenance_path}")
    options = value["inputs"].get("export_options")
    if not isinstance(options, dict) or options.get("title") is not None and not isinstance(
        options.get("title"), str
    ):
        raise BlueprintError(f"invalid export options in {provenance_path}")
    expected_inputs = _input_provenance(paths, options.get("title"))
    if value["inputs"] != expected_inputs:
        raise BlueprintError(f"source provenance is stale for current inputs: {provenance_path}")
    actual_assets = _export_asset_hashes(output)
    if value.get("export_assets") != actual_assets:
        raise BlueprintError(f"export asset digest mismatch: {provenance_path}")
    return value


def check_export(paths: Paths, output: Path | None = None) -> int:
    output = output or paths.output
    source = output / "blueprint" / "src"
    required = (
        "web.tex",
        "print.tex",
        "content.tex",
        "plastex.cfg",
        "tier_dots.js",
        "dep_graph_core.js",
        "autoform_common_macros.tex",
        "autoform_web_macros.tex",
        "autoform_print_macros.tex",
    )
    for relative in required:
        file = source / relative
        if not file.is_file() or file.stat().st_size == 0:
            raise BlueprintError(f"missing or empty export asset: {file}")

    config = (source / "plastex.cfg").read_text(encoding="utf-8")
    if "extra-js=tier_dots.js dep_graph_core.js" not in config:
        raise BlueprintError("plastex.cfg does not list JavaScript assets separately")
    if "extra-js=tier_dots.js,dep_graph_core.js" in config:
        raise BlueprintError("plastex.cfg still contains the exporter comma bug")

    for tex_name in ("web.tex", "print.tex"):
        text = (source / tex_name).read_text(encoding="utf-8")
        if "\\input{macros/" in text:
            raise BlueprintError(f"unresolved nested macro input remains in {tex_name}")
        if "\\input{content.tex}" not in text:
            raise BlueprintError(f"explicit content.tex input missing from {tex_name}")
    provenance = _check_source_provenance(paths, output)
    graph = _load_graph(paths.graph)
    count = _check_graph_javascript(graph, source / "tier_dots.js")
    graph_record = provenance["inputs"]["graph"]
    if graph_record["node_count"] != count or graph_record["edge_count"] != graph.edge_count:
        raise BlueprintError("provenance graph counts do not match checked export")
    return count


def _rename_exchange(source: Path, destination: Path) -> bool:
    if not sys.platform.startswith("linux"):
        return False
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is None:
        return False
    renameat2.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    renameat2.restype = ctypes.c_int
    at_fdcwd = -100
    rename_exchange = 2
    result = renameat2(
        at_fdcwd,
        os.fsencode(source),
        at_fdcwd,
        os.fsencode(destination),
        rename_exchange,
    )
    if result == 0:
        return True
    error = ctypes.get_errno()
    if error in {errno.ENOSYS, errno.EINVAL, errno.ENOTSUP, errno.EXDEV}:
        return False
    raise OSError(error, os.strerror(error), str(destination))


_EXCHANGE_PROBED: set[Path] = set()


def _require_atomic_exchange(parent: Path) -> None:
    _require_linux()
    parent.mkdir(parents=True, exist_ok=True)
    resolved = parent.resolve()
    if resolved in _EXCHANGE_PROBED:
        return
    with tempfile.TemporaryDirectory(prefix=".blueprint-exchange-a-", dir=parent) as first:
        with tempfile.TemporaryDirectory(prefix=".blueprint-exchange-b-", dir=parent) as second:
            if not _rename_exchange(Path(first), Path(second)):
                raise BlueprintError(
                    f"filesystem does not support atomic renameat2(RENAME_EXCHANGE): {parent}"
                )
    _EXCHANGE_PROBED.add(resolved)


def _promote_tree(
    staged: Path,
    destination: Path,
    validate: Callable[[], object],
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    _require_atomic_exchange(destination.parent)
    existed = destination.exists()
    if existed:
        if not destination.is_dir() or destination.is_symlink():
            raise BlueprintError(f"tree destination is not a real directory: {destination}")
        if not _rename_exchange(staged, destination):
            raise BlueprintError(f"atomic tree exchange unexpectedly unavailable: {destination}")
    else:
        os.replace(staged, destination)
    try:
        validate()
    except BaseException as exc:
        try:
            if existed:
                if not _rename_exchange(staged, destination):
                    raise BlueprintError(f"could not roll back tree exchange: {destination}")
            else:
                os.replace(destination, staged)
        except BaseException as rollback_exc:
            raise BlueprintError(
                f"validation failed after promotion and rollback failed: {rollback_exc}"
            ) from exc
        raise


def _replace_file_atomically(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{destination.name}.staging-", dir=destination.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        with source.open("rb") as input_stream:
            shutil.copyfileobj(input_stream, stream)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def export_blueprint(paths: Paths, title: str | None = None) -> None:
    _load_graph(paths.graph)
    _assert_output_safe(paths)
    paths.output.mkdir(parents=True, exist_ok=True)
    _write_owner_sentinel(paths)
    (paths.output / "blueprint").mkdir(parents=True, exist_ok=True)
    _require_atomic_exchange(paths.source.parent)
    exporter = paths.plugin / "scripts" / "export_blueprint.py"
    content = paths.project / "informal_content"

    with tempfile.TemporaryDirectory(
        prefix=f".{paths.output.name}.staging-", dir=paths.output.parent
    ) as temporary:
        staged = Path(temporary) / "payload"
        command: list[os.PathLike[str] | str] = [
            sys.executable,
            exporter,
            paths.graph,
            "--out",
            staged,
        ]
        if content.is_dir():
            command.extend(("--content", content))
        if title:
            command.extend(("--title", title))
        _run(command, cwd=paths.project)

        source = staged / "blueprint" / "src"
        _repair_extra_js(source / "plastex.cfg")
        _promote_macros(source)
        _write_source_provenance(paths, staged, title)
        count = check_export(paths, staged)
        expected = _read_json(source / SOURCE_PROVENANCE)
        _assert_output_safe(paths)
        if _read_json(source / SOURCE_PROVENANCE) != expected:
            raise BlueprintError("staged source provenance changed before promotion")
        if expected["inputs"] != _input_provenance(paths, title):
            raise BlueprintError("blueprint inputs changed during export")
        _promote_tree(source, paths.source, lambda: check_export(paths))
        _replace_file_atomically(staged / "Makefile", paths.output / "Makefile")

    print(f"Exported {count} graph nodes with Autoform {AUTOFORM_VERSION}: {paths.output}")


def _library_search_roots(dot: Path) -> list[Path]:
    candidates = [
        dot.resolve().parent.parent / "lib",
        dot.resolve().parent.parent / "lib64",
        Path("/lib64"),
        Path("/usr/lib64"),
        Path("/lib"),
        Path("/usr/lib"),
        Path("/usr/local/lib"),
        Path("/opt/homebrew/lib"),
    ]
    candidates.extend(sorted(Path("/lib").glob("*-linux-gnu")))
    candidates.extend(sorted(Path("/usr/lib").glob("*-linux-gnu")))
    if shutil.which("brew"):
        result = subprocess.run(
            ["brew", "--prefix", "graphviz"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            candidates.insert(0, Path(result.stdout.strip()) / "lib")

    roots: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_dir() and resolved not in seen:
            roots.append(resolved)
            seen.add(resolved)
    return roots


def _family_matches(root: Path, family: str) -> list[Path]:
    patterns = (
        f"{family}.so*",
        f"{family}.dylib",
        f"{family}.*.dylib",
    )
    matches: list[Path] = []
    for directory in (root, root / "graphviz"):
        if directory.is_dir():
            for pattern in patterns:
                matches.extend(sorted(directory.glob(pattern)))
    return matches


def _copy_library_set(matches: Sequence[Path], destination: Path) -> dict[str, Path]:
    # Copy regular targets before symlinks so relative soname links are valid.
    origins: dict[str, Path] = {}
    for source in sorted(matches, key=lambda path: path.is_symlink()):
        target = destination / source.name
        if target.exists() or target.is_symlink():
            continue
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        elif source.is_file():
            shutil.copy2(source, target)
        else:
            continue
        origins[target.name] = source.absolute()
    return origins


def curate_graphviz_libraries(paths: Paths) -> dict[str, Path]:
    dot_name = shutil.which("dot")
    if not dot_name:
        raise BlueprintError("graphviz 'dot' is required; install graphviz first")
    dot = Path(dot_name)
    roots = _library_search_roots(dot)
    if not roots:
        raise BlueprintError("could not find Graphviz library search roots")

    if paths.gvlibs.exists():
        shutil.rmtree(paths.gvlibs)
    paths.gvlibs.mkdir(parents=True)
    copied: dict[str, list[str]] = {}
    origins: dict[str, Path] = {}
    for family in GRAPHVIZ_LOADER_LIBRARIES:
        matches: list[Path] = []
        for root in roots:
            matches = _family_matches(root, family)
            if matches:
                break
        if matches:
            origins.update(_copy_library_set(matches, paths.gvlibs))
            copied[family] = [match.name for match in matches]

    missing_core = [family for family in CORE_GRAPHVIZ_LIBRARIES if family not in copied]
    if missing_core:
        raise BlueprintError("missing Graphviz runtime libraries: " + ", ".join(missing_core))
    print(
        "Curated Graphviz loader families: "
        + ", ".join(family for family in GRAPHVIZ_LOADER_LIBRARIES if family in copied)
    )
    return origins


def _normalize_package(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _direct_requirements() -> dict[str, str]:
    if not DIRECT_REQUIREMENTS.is_file():
        raise BlueprintError(f"missing direct requirements: {DIRECT_REQUIREMENTS}")
    locked: dict[str, str] = {}
    for line in DIRECT_REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.count("==") != 1:
            raise BlueprintError(f"direct requirement is not exactly pinned: {line}")
        name, version = line.split("==")
        if not name or not version:
            raise BlueprintError(f"invalid pinned requirement: {line}")
        normalized = _normalize_package(name)
        if normalized in locked:
            raise BlueprintError(f"duplicate direct requirement: {name}")
        locked[normalized] = version
    expected = {_normalize_package(name) for name in PACKAGE_IMPORTS}
    if set(locked) != expected:
        raise BlueprintError(
            f"dependency lock packages {sorted(locked)} do not match required "
            f"packages {sorted(expected)}"
        )
    return locked


def _lock_requirements() -> dict[str, tuple[str, tuple[str, ...]]]:
    if not REQUIREMENTS_LOCK.is_file():
        raise BlueprintError(f"missing universal hash lock: {REQUIREMENTS_LOCK}")
    text = REQUIREMENTS_LOCK.read_text(encoding="utf-8")
    header_fragments = (
        "uv pip compile",
        "--universal",
        "--generate-hashes",
        f"--python-version {PYTHON_VERSION}",
    )
    missing_header = [fragment for fragment in header_fragments if fragment not in text]
    if missing_header:
        raise BlueprintError(f"universal lock header is missing {missing_header}")

    starts = [
        index
        for index, line in enumerate(text.splitlines())
        if line and not line[0].isspace() and not line.startswith("#")
    ]
    lines = text.splitlines()
    records: dict[str, tuple[str, tuple[str, ...]]] = {}
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        stanza = "\n".join(lines[start:end])
        first = lines[start].rstrip().removesuffix("\\").strip()
        match = re.match(r"^([A-Za-z0-9_.-]+)==([^ ;\\]+)(?:\s*;.*)?$", first)
        if not match:
            raise BlueprintError(f"invalid locked requirement line: {lines[start]}")
        name = _normalize_package(match.group(1))
        hashes = tuple(sorted(set(re.findall(r"--hash=sha256:([0-9a-f]{64})", stanza))))
        if not hashes:
            raise BlueprintError(f"locked requirement has no SHA256 hashes: {name}")
        if name in records:
            raise BlueprintError(f"duplicate locked requirement: {name}")
        records[name] = (match.group(2), hashes)

    direct = _direct_requirements()
    mismatches = {
        name: (version, records.get(name, (None, ()))[0])
        for name, version in direct.items()
        if records.get(name, (None, ()))[0] != version
    }
    if mismatches:
        raise BlueprintError(f"direct/universal lock mismatch: {mismatches}")
    return records


def _command_version(command: Sequence[str]) -> str:
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise BlueprintError(f"cannot query tool version: {' '.join(command)}") from exc
    return (result.stdout + result.stderr).strip()


def _host_tools() -> dict[str, object]:
    uv_name = shutil.which("uv")
    dot_name = shutil.which("dot")
    if not uv_name:
        raise BlueprintError("uv is required so its host proxy configuration is honored")
    if not dot_name:
        raise BlueprintError("graphviz 'dot' is not on PATH")
    uv_output = _command_version([uv_name, "--version"])
    dot_output = _command_version([dot_name, "-V"])
    uv_match = re.search(r"\buv\s+([^\s]+)", uv_output)
    dot_match = re.search(r"graphviz version\s+([^\s]+)", dot_output)
    if not uv_match or uv_match.group(1) != UV_VERSION:
        raise BlueprintError(f"need uv {UV_VERSION}, found {uv_output!r}")
    if not dot_match or dot_match.group(1) != GRAPHVIZ_VERSION:
        raise BlueprintError(f"need Graphviz {GRAPHVIZ_VERSION}, found {dot_output!r}")
    uv_path = Path(uv_name).resolve()
    dot_path = Path(dot_name).resolve()
    return {
        "uv": {"version": UV_VERSION, "path": str(uv_path), "sha256": _sha256(uv_path)},
        "graphviz": {
            "version": GRAPHVIZ_VERSION,
            "path": str(dot_path),
            "sha256": _sha256(dot_path),
        },
    }


_DISTRIBUTION_PROBE = r'''
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import sys
from pathlib import Path
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

lock = Path(sys.argv[1])
venv = Path(sys.argv[2]).resolve()
expected = {}
for line in lock.read_text(encoding="utf-8").splitlines():
    if not line or line[0].isspace() or line.startswith("#"):
        continue
    requirement = Requirement(line.rstrip().removesuffix("\\").strip())
    if requirement.marker is not None and not requirement.marker.evaluate():
        continue
    versions = [item.version for item in requirement.specifier if item.operator == "=="]
    if len(versions) != 1:
        raise RuntimeError(f"non-exact applicable requirement: {requirement}")
    expected[canonicalize_name(requirement.name)] = versions[0]

installed = {}
for distribution in importlib.metadata.distributions():
    name = canonicalize_name(distribution.metadata["Name"])
    entries = []
    for relative in sorted(distribution.files or [], key=str):
        relative_text = str(relative).replace(os.sep, "/")
        if relative_text.endswith(".pyc") or "/__pycache__/" in f"/{relative_text}":
            continue
        path = Path(distribution.locate_file(relative)).resolve()
        try:
            path.relative_to(venv)
        except ValueError:
            raise RuntimeError(f"distribution file escapes venv: {name}: {path}")
        if path.is_file():
            entries.append((relative_text, hashlib.sha256(path.read_bytes()).hexdigest()))
    digest = hashlib.sha256()
    for relative_text, file_hash in entries:
        digest.update(relative_text.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    installed[name] = {
        "version": distribution.version,
        "file_count": len(entries),
        "tree_sha256": digest.hexdigest(),
    }

print(json.dumps({
    "python": ".".join(str(item) for item in sys.version_info[:3]),
    "expected": expected,
    "installed": installed,
}, sort_keys=True))
'''


def _distribution_record(paths: Paths) -> dict[str, object]:
    try:
        result = subprocess.run(
            [
                str(paths.python),
                "-c",
                _DISTRIBUTION_PROBE,
                str(REQUIREMENTS_LOCK),
                str(paths.venv),
            ],
            check=True,
            capture_output=True,
            text=True,
            env=_tool_env(paths),
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "unknown distribution probe error").strip()
        raise BlueprintError(f"cannot verify locked distributions: {detail}") from exc
    try:
        record = json.loads(result.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        raise BlueprintError("distribution probe returned invalid JSON") from exc
    if record.get("python") != PYTHON_VERSION:
        raise BlueprintError(f"need Python {PYTHON_VERSION}, found {record.get('python')!r}")
    expected = record.get("expected")
    installed = record.get("installed")
    if not isinstance(expected, dict) or not isinstance(installed, dict):
        raise BlueprintError("distribution probe omitted expected or installed packages")
    versions = {name: value.get("version") for name, value in installed.items()}
    if versions != expected:
        missing = sorted(set(expected) - set(versions))
        extra = sorted(set(versions) - set(expected))
        mismatched = {
            name: (expected[name], versions.get(name))
            for name in expected.keys() & versions.keys()
            if expected[name] != versions[name]
        }
        raise BlueprintError(
            f"installed distributions do not exactly match applicable universal lock: "
            f"missing={missing}, extra={extra}, versions={mismatched}"
        )
    empty = sorted(
        name for name, value in installed.items() if not value.get("file_count")
    )
    if empty:
        raise BlueprintError(f"installed distributions have no verifiable files: {empty}")
    return {"python": PYTHON_VERSION, "distributions": installed}


def _library_record(
    paths: Paths,
    origins: Mapping[str, Path] | None = None,
    stored: Mapping[str, object] | None = None,
) -> dict[str, object]:
    if not paths.gvlibs.is_dir():
        raise BlueprintError(f"missing curated native library directory: {paths.gvlibs}")
    entries = sorted(paths.gvlibs.iterdir(), key=lambda path: path.name)
    if not entries:
        raise BlueprintError(f"curated native library directory is empty: {paths.gvlibs}")
    result: dict[str, object] = {}
    for path in entries:
        if not path.is_file():
            raise BlueprintError(f"invalid curated native library entry: {path}")
        if origins is not None:
            origin = origins.get(path.name)
            if origin is None:
                raise BlueprintError(f"native library origin was not recorded: {path.name}")
        else:
            if stored is None or not isinstance(stored.get(path.name), dict):
                raise BlueprintError(f"native library is absent from provenance: {path.name}")
            origin_value = stored[path.name].get("origin")
            if not isinstance(origin_value, str):
                raise BlueprintError(f"native library has invalid origin provenance: {path.name}")
            origin = Path(origin_value)
        if not origin.exists():
            raise BlueprintError(f"native library origin disappeared: {origin}")
        result[path.name] = {
            "sha256": _sha256(path),
            "symlink_target": os.readlink(path) if path.is_symlink() else None,
            "origin": str(origin.absolute()),
            "origin_sha256": _sha256(origin),
        }
    return result


def _toolchain_record(
    paths: Paths,
    origins: Mapping[str, Path] | None = None,
    stored_libraries: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "host_tools": _host_tools(),
        "requirements": {
            "direct_sha256": _sha256(DIRECT_REQUIREMENTS),
            "lock_sha256": _sha256(REQUIREMENTS_LOCK),
            "driver_sha256": _sha256(Path(__file__).resolve()),
        },
        "python": {
            "version": PYTHON_VERSION,
            "executable_sha256": _sha256(paths.python.resolve()),
        },
        "packages": _distribution_record(paths),
        "native_libraries": _library_record(paths, origins, stored_libraries),
    }


def _tool_env(paths: Paths) -> dict[str, str]:
    environment = os.environ.copy()
    executable_dir = paths.python.parent
    environment["PATH"] = os.pathsep.join(
        (str(executable_dir), str(paths.gvlibs), environment.get("PATH", ""))
    )
    for variable in ("LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH"):
        current = environment.get(variable)
        environment[variable] = str(paths.gvlibs) + (os.pathsep + current if current else "")
    environment.setdefault("LC_ALL", "C.UTF-8")
    environment.setdefault("LANG", "C.UTF-8")
    return environment


def _pygraphviz_build_env(paths: Paths) -> dict[str, str]:
    environment = _tool_env(paths)
    include_candidates = [Path("/usr/include/graphviz"), Path("/usr/local/include/graphviz")]
    library_candidates = _library_search_roots(Path(shutil.which("dot") or "dot"))
    includes = [path for path in include_candidates if path.is_dir()]
    if shutil.which("brew"):
        result = subprocess.run(
            ["brew", "--prefix", "graphviz"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            prefix = Path(result.stdout.strip())
            includes.insert(0, prefix / "include")
            library_candidates.insert(0, prefix / "lib")
    if includes:
        flags = " ".join(f"-I{path}" for path in includes)
        environment["CFLAGS"] = f"{environment.get('CFLAGS', '')} {flags}".strip()
    if library_candidates:
        flags = " ".join(f"-L{path}" for path in library_candidates)
        environment["LDFLAGS"] = f"{environment.get('LDFLAGS', '')} {flags}".strip()
    return environment


def _apply_depgraph_hashfix(paths: Paths) -> None:
    candidates = list(paths.venv.glob("lib/python*/site-packages/plastexdepgraph/Packages/depgraph.py"))
    if len(candidates) != 1:
        raise BlueprintError(f"expected one plastexdepgraph depgraph.py, found {len(candidates)}")
    path = candidates[0]
    text = path.read_text(encoding="utf-8")
    marker = "autoform-hashfix"
    if marker in text:
        return
    needle = "graph.nodes = set(nodes)"
    if text.count(needle) != 1:
        raise BlueprintError(f"cannot apply plastexdepgraph hashability fix to {path}")
    replacement = (
        "for _n in nodes:\n"
        "            if type(_n).__hash__ is None:\n"
        "                type(_n).__hash__ = lambda self: id(self)  # autoform-hashfix\n"
        "        graph.nodes = set(nodes)"
    )
    path.write_text(text.replace(needle, replacement), encoding="utf-8")


def _rewrite_venv_shebangs(staged: Paths, final: Paths) -> None:
    staged_prefix = str(staged.venv).encode("utf-8")
    final_prefix = str(final.venv).encode("utf-8")
    for path in staged.venv.joinpath("bin").iterdir():
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        if staged_prefix in data:
            path.write_bytes(data.replace(staged_prefix, final_prefix))


def check_toolchain(paths: Paths) -> None:
    _lock_requirements()
    _host_tools()
    if not paths.python.is_file() or not paths.plastex.is_file():
        raise BlueprintError("blueprint toolchain is not set up; run the setup command")

    probe = (
        "import importlib.metadata, json; "
        f"names={json.dumps(PACKAGE_IMPORTS)}; "
        "[__import__(module) for module in names.values()]; "
        "print(json.dumps({name: importlib.metadata.version(name) for name in names}))"
    )
    try:
        result = subprocess.run(
            [str(paths.python), "-c", probe],
            check=True,
            capture_output=True,
            text=True,
            env=_tool_env(paths),
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "unknown import error").strip()
        raise BlueprintError(f"blueprint package import failed: {detail}") from exc
    installed = json.loads(result.stdout.strip().splitlines()[-1])
    direct = _direct_requirements()
    mismatches = {
        name: (version, installed.get(original))
        for original, module in PACKAGE_IMPORTS.items()
        for name, version in ((_normalize_package(original), direct[_normalize_package(original)]),)
        if installed.get(original) != version
    }
    if mismatches:
        raise BlueprintError(f"blueprint dependency version mismatch: {mismatches}")

    depgraph = list(
        paths.venv.glob("lib/python*/site-packages/plastexdepgraph/Packages/depgraph.py")
    )
    if len(depgraph) != 1 or "autoform-hashfix" not in depgraph[0].read_text(encoding="utf-8"):
        raise BlueprintError("plastexdepgraph hashability fix is missing")
    provenance = _read_json(paths.toolchain_provenance)
    if not isinstance(provenance, dict) or not isinstance(
        provenance.get("native_libraries"), dict
    ):
        raise BlueprintError(f"invalid toolchain provenance: {paths.toolchain_provenance}")
    current = _toolchain_record(
        paths, stored_libraries=provenance["native_libraries"]
    )
    if provenance != current:
        raise BlueprintError(f"toolchain provenance mismatch: {paths.toolchain_provenance}")
    print(
        f"Toolchain OK: uv={UV_VERSION}, graphviz={GRAPHVIZ_VERSION}, "
        f"python={PYTHON_VERSION}, distributions={len(current['packages']['distributions'])}"
    )


def setup_toolchain(paths: Paths) -> None:
    _lock_requirements()
    tools = _host_tools()
    uv = str(tools["uv"]["path"])
    paths.tool_state.parent.mkdir(parents=True, exist_ok=True)
    _require_atomic_exchange(paths.tool_state.parent)

    with tempfile.TemporaryDirectory(
        prefix=".blueprint-toolchain.staging-", dir=paths.tool_state.parent
    ) as temporary:
        staged_state = Path(temporary) / "payload"
        staged = paths.at_tool_state(staged_state)
        staged_state.mkdir()
        origins = curate_graphviz_libraries(staged)
        _run(
            [
                uv,
                "venv",
                "--clear",
                "--relocatable",
                "--no-project",
                "--python",
                PYTHON_VERSION,
                staged.venv,
            ],
            cwd=paths.project,
        )
        _run(
            [
                uv,
                "pip",
                "install",
                "--strict",
                "--require-hashes",
                "--python",
                staged.python,
                "--requirement",
                REQUIREMENTS_LOCK,
            ],
            cwd=paths.project,
            env=_pygraphviz_build_env(staged),
        )
        _apply_depgraph_hashfix(staged)
        _rewrite_venv_shebangs(staged, paths)
        record = _toolchain_record(staged, origins=origins)
        _write_json(staged.toolchain_provenance, record)
        check_toolchain(staged)
        _promote_tree(staged_state, paths.tool_state, lambda: check_toolchain(paths))


class _ReferenceParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.inline_css: list[str] = []
        self.anchors: set[str] = set()
        self._style_depth = 0

    def _attributes(self, attributes: list[tuple[str, str | None]]) -> None:
        for name, value in attributes:
            if value is None:
                continue
            lowered = name.lower()
            if lowered in {"id", "name"}:
                self.anchors.add(value)
            elif lowered in {"href", "src", "poster", "data"}:
                self.references.append(value)
            elif lowered == "srcset":
                self.references.extend(
                    candidate.strip().split()[0]
                    for candidate in value.split(",")
                    if candidate.strip()
                )
            elif lowered == "style":
                self.inline_css.append(value)

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._attributes(attrs)
        if tag.lower() == "style":
            self._style_depth += 1

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._attributes(attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style" and self._style_depth:
            self._style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self.inline_css.append(data)


_CSS_REFERENCE = re.compile(
    r"url\(\s*(['\"]?)(.*?)\1\s*\)|@import\s+(['\"])(.*?)\3",
    flags=re.IGNORECASE | re.DOTALL,
)


def _css_references(text: str) -> list[str]:
    return [match.group(2) or match.group(4) for match in _CSS_REFERENCE.finditer(text)]


def _resolve_local_reference(web: Path, source: Path, reference: str) -> Path | None:
    value = reference.strip()
    if not value or value.startswith("#") or value.startswith("//"):
        return None
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme:
        return None
    path_text = urllib.parse.unquote(parsed.path)
    if not path_text:
        return None
    candidate = web / path_text.lstrip("/") if path_text.startswith("/") else source.parent / path_text
    resolved = candidate.resolve()
    try:
        resolved.relative_to(web.resolve())
    except ValueError as exc:
        raise BlueprintError(f"local reference escapes web root in {source}: {reference}") from exc
    if resolved.is_dir():
        resolved /= "index.html"
    if not resolved.is_file():
        raise BlueprintError(f"broken local reference in {source}: {reference}")
    return resolved


def _check_reference_closure(web: Path) -> int:
    checked = 0
    for path in sorted(web.rglob("*")):
        if path.is_symlink():
            raise BlueprintError(f"web output contains a symlink: {path}")
        if not path.is_file() or path.suffix.lower() not in {".html", ".css"}:
            continue
        text = path.read_text(encoding="utf-8")
        references: list[str]
        if path.suffix.lower() == ".html":
            parser = _ReferenceParser()
            try:
                parser.feed(text)
                parser.close()
            except (UnicodeError, ValueError) as exc:
                raise BlueprintError(f"invalid HTML in {path}: {exc}") from exc
            references = parser.references
            for css in parser.inline_css:
                references.extend(_css_references(css))
        else:
            references = _css_references(text)
        for reference in references:
            _resolve_local_reference(web, path, reference)
            checked += 1
    return checked


def _runtime_asset_hashes(web: Path) -> dict[str, str]:
    assets: dict[str, str] = {}
    for path in sorted(web.rglob("*")):
        if path.is_file() and path.suffix.lower() in RUNTIME_SUFFIXES:
            if path.stat().st_size == 0:
                raise BlueprintError(f"empty runtime asset: {path}")
            assets[path.relative_to(web).as_posix()] = _sha256(path)
    if "js/hpcc.min.js" not in assets:
        raise BlueprintError("Graphviz runtime asset js/hpcc.min.js is missing")
    return assets


def _write_runtime_manifest(paths: Paths, web: Path) -> None:
    value = {
        "schema_version": 1,
        "source_provenance_sha256": _sha256(paths.source / SOURCE_PROVENANCE),
        "toolchain_provenance_sha256": _sha256(paths.toolchain_provenance),
        "assets": _runtime_asset_hashes(web),
    }
    _write_json(web / RUNTIME_MANIFEST, value)


def _check_runtime_manifest(paths: Paths, web: Path) -> int:
    manifest_path = web / RUNTIME_MANIFEST
    value = _read_json(manifest_path)
    expected = {
        "schema_version": 1,
        "source_provenance_sha256": _sha256(paths.source / SOURCE_PROVENANCE),
        "toolchain_provenance_sha256": _sha256(paths.toolchain_provenance),
        "assets": _runtime_asset_hashes(web),
    }
    if value != expected:
        raise BlueprintError(f"runtime asset digest mismatch: {manifest_path}")
    return len(expected["assets"])


def check_build(paths: Paths, web: Path | None = None) -> int:
    web = web or paths.web
    source_count = check_export(paths)
    for relative in REQUIRED_WEB_FILES:
        asset = web / relative
        if not asset.is_file() or asset.stat().st_size == 0:
            raise BlueprintError(f"missing or empty web asset: {asset}")
    graph = _load_graph(paths.graph)
    built_count = _check_graph_javascript(graph, web / "js" / "tier_dots.js")
    if built_count != source_count:
        raise BlueprintError(
            f"source/build node counts differ: source={source_count}, build={built_count}"
        )

    source_provenance = paths.source / SOURCE_PROVENANCE
    built_provenance = web / SOURCE_PROVENANCE
    if not built_provenance.is_file() or built_provenance.read_bytes() != source_provenance.read_bytes():
        raise BlueprintError("built provenance does not exactly match source provenance")
    page_anchors: dict[Path, set[str]] = {}
    for node_id in graph.nodes_by_tier.get(1, ()):
        page = web / f"{graph.slugs[node_id]}.html"
        if not page.is_file() or page.stat().st_size == 0:
            raise BlueprintError(f"missing tier-1 HTML page for {node_id!r}: {page}")

    for node_id in graph.nodes_by_tier.get(2, ()):
        parent = graph.nodes[node_id].get("parent")
        if isinstance(parent, str) and parent in graph.nodes_by_tier.get(1, ()):
            page_slug = graph.slugs[parent]
        else:
            page_slug = _make_slug("Additional statements")
        page = web / f"{page_slug}.html"
        if not page.is_file() or page.stat().st_size == 0:
            raise BlueprintError(
                f"missing tier-2 parent HTML page for {node_id!r}: {page}"
            )
        if page not in page_anchors:
            parser = _ReferenceParser()
            parser.feed(page.read_text(encoding="utf-8"))
            parser.close()
            page_anchors[page] = parser.anchors
        anchor = graph.slugs[node_id]
        if anchor not in page_anchors[page]:
            raise BlueprintError(
                f"missing tier-2 HTML anchor for {node_id!r}: {page}#{anchor}"
            )

    html = (web / "dep_graph_document.html").read_text(encoding="utf-8")
    for reference in ("js/tier_dots.js", "js/dep_graph_core.js", "js/d3-graphviz.js"):
        if f'src="{reference}"' not in html:
            raise BlueprintError(f"dependency graph HTML does not load {reference}")
    if "tier_dots.js,dep_graph_core.js" in html:
        raise BlueprintError("dependency graph HTML contains the comma-separated JavaScript bug")
    reference_count = _check_reference_closure(web)
    asset_count = _check_runtime_manifest(paths, web)
    print(
        f"Blueprint check passed: {built_count} nodes, {graph.edge_count} graph edges, "
        f"{asset_count} hashed runtime assets, {reference_count} local references"
    )
    return built_count


def build_blueprint(paths: Paths) -> None:
    check_export(paths)
    check_toolchain(paths)
    _assert_output_safe(paths)
    paths.web.parent.mkdir(parents=True, exist_ok=True)
    _require_atomic_exchange(paths.web.parent)
    with tempfile.TemporaryDirectory(
        prefix=".blueprint-web.staging-", dir=paths.web.parent
    ) as temporary:
        root = Path(temporary) / "payload"
        staged_source = root / "src"
        staged_web = root / "web"
        shutil.copytree(paths.source, staged_source)
        _run(
            [paths.plastex, "-c", "plastex.cfg", "web.tex"],
            cwd=staged_source,
            env=_tool_env(paths),
        )
        shutil.copy2(paths.source / SOURCE_PROVENANCE, staged_web / SOURCE_PROVENANCE)
        _write_runtime_manifest(paths, staged_web)
        check_build(paths, staged_web)
        check_toolchain(paths)
        _assert_output_safe(paths)
        check_export(paths)
        _promote_tree(staged_web, paths.web, lambda: check_build(paths))


class _LoopbackServer(http.server.ThreadingHTTPServer):
    daemon_threads = True


def serve_blueprint(paths: Paths, port: int) -> None:
    check_toolchain(paths)
    check_build(paths)
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(paths.web))
    try:
        server = _LoopbackServer(("127.0.0.1", port), handler)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            raise BlueprintError(
                f"127.0.0.1:{port} is already in use; choose another --port"
            ) from exc
        raise
    actual_port = server.server_address[1]
    print(
        f"Serving {paths.web}\n"
        f"http://127.0.0.1:{actual_port}/dep_graph_document.html\n"
        "Press Ctrl-C to stop.",
        flush=True,
    )
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer") from exc
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reproducible Autoform 0.4.4 blueprint workflow for this project.",
        epilog=(
            "Linux only (renameat2 tree exchange). Typical refresh stages setup, "
            "export, and build in that order: python3 scripts/blueprint.py refresh; "
            "then serve with python3 scripts/blueprint.py serve --port 8005"
        ),
    )
    parser.add_argument(
        "--project",
        default=str(PROJECT_ROOT),
        help="project root (default: the parent of scripts/)",
    )
    parser.add_argument("--graph", help="graph JSON, relative to project (default: graph.json)")
    parser.add_argument(
        "--output",
        help="export directory, relative to project (default: blueprint_export)",
    )
    parser.add_argument(
        "--plugin-root",
        help="exact Autoform 0.4.4 root (otherwise AUTOFORM_PLUGIN_ROOT or installed cache)",
    )

    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export", help="atomically regenerate the blueprint sources")
    export.add_argument("--title", help="override the exported document title")
    commands.add_parser("setup", help="create the pinned uv toolchain and curate Graphviz libs")
    commands.add_parser("build", help="stage, validate, and atomically promote web output")
    commands.add_parser("check", help="check plugin, toolchain, export, assets, and node counts")
    commands.add_parser("refresh", help="run setup, export, then build with staged promotion")
    serve = commands.add_parser("serve", help="serve the checked web output on loopback only")
    serve.add_argument(
        "--port",
        type=_port,
        default=_port(os.environ.get("BLUEPRINT_PORT", "8005")),
        help="loopback port, or 0 for an ephemeral port (default: 8005)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        paths = make_paths(args)
        print(f"Project: {paths.project}")
        print(f"Autoform: {paths.plugin} (version {AUTOFORM_VERSION})")
        print(f"Output: {paths.output}")

        if args.command == "export":
            export_blueprint(paths, args.title)
        elif args.command == "setup":
            setup_toolchain(paths)
        elif args.command == "build":
            build_blueprint(paths)
        elif args.command == "check":
            check_toolchain(paths)
            check_build(paths)
        elif args.command == "refresh":
            setup_toolchain(paths)
            export_blueprint(paths)
            build_blueprint(paths)
        elif args.command == "serve":
            serve_blueprint(paths, args.port)
        else:  # argparse makes this unreachable.
            raise BlueprintError(f"unsupported command: {args.command}")
        return 0
    except BlueprintError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopped.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
