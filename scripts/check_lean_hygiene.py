#!/usr/bin/env python3
"""Reject Lean trust shortcuts lexically and through the compiled environment."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


PROOF_HOLE = re.compile(r"(?<![\w'])(sorry|admit)(?![\w'])")
DECLARATION_COMMAND = re.compile(
    r"(?m)^[ \t]*(?:(?:@\[[^\]\r\n]*\]|private|protected|noncomputable|unsafe|local|scoped)"
    r"[ \t]+)*(axiom|axioms|constant|constants)(?![\w'])"
)
INTERPOLATED_PREFIXES = ("s!\"", "m!\"")
EXCLUDED_SOURCE_DIRS = {
    ".autoform",
    ".codex",
    ".git",
    ".lake",
    "blueprint",
    "blueprint_export",
    "node_modules",
    "__pycache__",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    column: int
    token: str


def _blank(output: list[str], text: str, start: int, stop: int) -> None:
    for index in range(start, min(stop, len(text))):
        if text[index] not in "\r\n":
            output[index] = " "


def mask_non_code(text: str) -> str:
    """Mask comments, literal text, and quoted identifiers while retaining code.

    Lean block comments nest. Interpolated string text is masked, but expressions
    inside its braces are recursively scanned as code.
    """

    output = list(text)
    length = len(text)

    def scan_block_comment(start: int) -> int:
        index = start + 2
        depth = 1
        while index < length and depth:
            if text.startswith("/-", index):
                depth += 1
                index += 2
            elif text.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        _blank(output, text, start, index)
        return index

    def scan_line_comment(start: int) -> int:
        newline = text.find("\n", start + 2)
        stop = length if newline < 0 else newline
        _blank(output, text, start, stop)
        return stop

    def scan_quoted_identifier(start: int) -> int:
        stop = text.find("»", start + 1)
        stop = length if stop < 0 else stop + 1
        _blank(output, text, start, stop)
        return stop

    def scan_string(start: int) -> int:
        index = start + 1
        while index < length:
            if text[index] == "\\":
                index = min(index + 2, length)
            elif text[index] == '"':
                index += 1
                break
            else:
                index += 1
        _blank(output, text, start, index)
        return index

    def scan_raw_string(start: int, hashes: int) -> int:
        opening_length = hashes + 2
        closing = '"' + ("#" * hashes)
        stop = text.find(closing, start + opening_length)
        stop = length if stop < 0 else stop + len(closing)
        _blank(output, text, start, stop)
        return stop

    def scan_interpolated(start: int, prefix_length: int) -> int:
        _blank(output, text, start, start + prefix_length)
        index = start + prefix_length
        segment_start = index
        while index < length:
            if text[index] == "\\":
                index = min(index + 2, length)
                continue
            if text[index] == '"':
                _blank(output, text, segment_start, index + 1)
                return index + 1
            if text.startswith("{{", index) or text.startswith("}}", index):
                index += 2
                continue
            if text[index] == "{":
                _blank(output, text, segment_start, index + 1)
                index = scan_code(index + 1, stop_at_brace=True)
                segment_start = index
                continue
            index += 1
        _blank(output, text, segment_start, length)
        return length

    def scan_code(start: int, *, stop_at_brace: bool) -> int:
        index = start
        while index < length:
            if stop_at_brace and text[index] == "}":
                _blank(output, text, index, index + 1)
                return index + 1
            if text.startswith("--", index):
                index = scan_line_comment(index)
                continue
            if text.startswith("/-", index):
                index = scan_block_comment(index)
                continue
            if text[index] == "«":
                index = scan_quoted_identifier(index)
                continue
            interpolated = next(
                (prefix for prefix in INTERPOLATED_PREFIXES if text.startswith(prefix, index)),
                None,
            )
            if interpolated is not None:
                index = scan_interpolated(index, len(interpolated))
                continue
            raw_match = re.match(r"r(#+)\"", text[index:])
            if raw_match is not None:
                index = scan_raw_string(index, len(raw_match.group(1)))
                continue
            if text[index] == '"':
                index = scan_string(index)
                continue
            if text[index] == "{":
                index = scan_code(index + 1, stop_at_brace=True)
                continue
            index += 1
        return length

    scan_code(0, stop_at_brace=False)
    return "".join(output)


def scan_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    masked = mask_non_code(text)
    findings: list[Finding] = []
    matches = sorted(
        [*PROOF_HOLE.finditer(masked), *DECLARATION_COMMAND.finditer(masked)],
        key=lambda match: match.start(),
    )
    for match in matches:
        line = masked.count("\n", 0, match.start()) + 1
        previous_newline = masked.rfind("\n", 0, match.start())
        column = match.start() - previous_newline
        findings.append(Finding(path, line, column, match.group(1)))
    return findings


def project_sources(project_root: Path) -> list[Path]:
    sources: list[Path] = []
    for path in project_root.rglob("*.lean"):
        relative = path.relative_to(project_root)
        if any(part in EXCLUDED_SOURCE_DIRS for part in relative.parts[:-1]):
            continue
        if path.is_file():
            sources.append(path)
    return sorted(set(sources))


def lexical_audit(paths: list[Path]) -> int:
    findings: list[Finding] = []
    for path in paths:
        try:
            findings.extend(scan_file(path))
        except ValueError as error:
            print(f"FAIL  Lean source audit: {error}", file=sys.stderr)
            return 2
    if findings:
        for finding in findings:
            print(
                f"FAIL  {finding.path}:{finding.line}:{finding.column}: "
                f"forbidden Lean token {finding.token!r}"
            )
        return 1
    print(f"PASS  lexical Lean trust audit ({len(paths)} files)")
    return 0


def _module_name(path: Path, project_root: Path) -> str:
    relative = path.relative_to(project_root).with_suffix("")
    return ".".join(relative.parts)


def _audit_query(module_names: list[str]) -> str:
    imports = "\n".join(f"import {name}" for name in module_names)
    encoded_names = ", ".join(json.dumps(name) for name in module_names)
    return f"""\
{imports}
import Lean.Util.CollectAxioms
import Lean.Elab.Command

open Lean Elab Command

private def auditedModules : Array String := #[{encoded_names}]

private def namesText (names : Array Name) : String :=
  String.intercalate ", " (names.toList.map Name.toString)

elab "#run_project_declaration_audit" : command => do
  let env <- getEnv
  let mut declarations : Array Name := #[]
  for index in [:env.header.moduleNames.size] do
    if auditedModules.contains env.header.moduleNames[index]!.toString then
      declarations := declarations.append env.header.moduleData[index]!.constNames

  let direct := declarations.filter fun name =>
    match env.find? name with
    | some info => info.isAxiom
    | none => false
  let directSet : NameSet := direct.foldl (init := {{}}) fun names name => names.insert name
  let mut contaminated : Array (Prod Name (Array Name)) := #[]
  for declaration in declarations do
    let dependencies <- liftCoreM <| Lean.collectAxioms declaration
    let forbidden := dependencies.filter fun name =>
      name == ``sorryAx || directSet.contains name
    unless forbidden.isEmpty do
      contaminated := contaminated.push (declaration, forbidden)

  unless direct.isEmpty && contaminated.isEmpty do
    let directText := if direct.isEmpty then "none" else namesText direct
    let uses := contaminated.toList.map fun (declaration, dependencies) =>
      s!"{{declaration}}: {{namesText dependencies}}"
    throwError "project declaration trust audit failed\n\
      direct project declarations without values: {{directText}}\n\
      declarations with forbidden dependencies: {{String.intercalate "; " uses}}"
  logInfo m!"Audited {{declarations.size}} project declarations: no forbidden dependencies."

#run_project_declaration_audit
"""


def _run(command: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def compiled_audit(project_root: Path, sources: list[Path]) -> int:
    relative_sources = [path.relative_to(project_root).as_posix() for path in sources]
    module_names = sorted({_module_name(path, project_root) for path in sources})
    build = subprocess.run(
        ["lake", "build", *relative_sources],
        cwd=project_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if build.returncode != 0:
        print("FAIL  compiled Lean trust audit: project build failed")
        print(build.stdout, end="")
        return 1

    with tempfile.TemporaryDirectory(prefix="lean-declaration-audit-") as directory:
        helper = Path(directory) / "Audit.lean"
        helper.write_text(_audit_query(module_names), encoding="utf-8")
        query = _run(["lake", "env", "lean", str(helper)], project_root)
    if query.returncode != 0:
        print("FAIL  compiled Lean declaration trust audit")
        print(query.stdout, end="")
        return 1
    print("PASS  compiled Lean declaration trust audit")
    if query.stdout.strip():
        print(query.stdout, end="" if query.stdout.endswith("\n") else "\n")
    return 0


def _lake_environment(project_root: Path) -> dict[str, str] | None:
    result = subprocess.run(
        ["lake", "env", "env", "-0"],
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    environment: dict[str, str] = {}
    for entry in result.stdout.split(b"\0"):
        if b"=" not in entry:
            continue
        key, value = entry.split(b"=", 1)
        environment[key.decode()] = value.decode()
    return environment


def _compiled_negative_self_test(project_root: Path) -> bool:
    environment = _lake_environment(project_root)
    if environment is None:
        print("FAIL  self-test could not obtain the Lake environment")
        return False
    lean = shutil.which("lean", path=environment.get("PATH"))
    if lean is None:
        print("FAIL  self-test could not locate Lean in the Lake environment")
        return False

    with tempfile.TemporaryDirectory(prefix="lean-compiled-negative-") as directory:
        root = Path(directory)
        fixture = root / "HygieneAuditNegative.lean"
        fixture.write_text(
            """\
import Lean
open Lean Elab Command
run_cmd
  let declaration := Declaration.axiomDecl {
    name := `HygieneAuditNegative.hidden
    levelParams := []
    type := mkConst ``False
    isUnsafe := false
  }
  liftCoreM <| addDecl declaration
""",
            encoding="utf-8",
        )
        if scan_file(fixture):
            print("FAIL  self-test hidden declaration unexpectedly failed the lexical layer")
            return False
        compile_result = _run(
            [
                lean,
                "-R",
                str(root),
                "-o",
                str(root / "HygieneAuditNegative.olean"),
                str(fixture),
            ],
            root,
            env=environment,
        )
        if compile_result.returncode != 0:
            print("FAIL  self-test could not compile the hidden-declaration fixture")
            print(compile_result.stdout, end="")
            return False
        environment = dict(environment)
        environment["LEAN_PATH"] = os.pathsep.join(
            [str(root), environment.get("LEAN_PATH", "")]
        ).rstrip(os.pathsep)
        audit = root / "Audit.lean"
        audit.write_text(_audit_query(["HygieneAuditNegative"]), encoding="utf-8")
        query = _run([lean, "-R", str(root), str(audit)], root, env=environment)
        if query.returncode == 0:
            print("FAIL  self-test compiled layer accepted a programmatic declaration")
            return False
        print("PASS  self-test compiled layer rejects a programmatic declaration")
        return True


def run_self_tests(project_root: Path) -> int:
    positive = """\
-- sorry, admit, axiom, and constant are prose here.
/- A nested comment: /- axioms and constants -/ still prose. -/
def words := ("sorry", "axiom", r#"admit and constant"#)
def quoted := «sorry»
def interpolation := s!"safe {"sorry in an ordinary string"}"
theorem clean : True := by exact True.intro
"""
    negatives = {
        "sorry term": "theorem bad : True := by sorry\n",
        "admit tactic": "theorem bad : True := by admit\n",
        "direct declaration": "axiom bad : False\n",
        "attributed declaration": "@[implemented_by good] axiom bad : False\n",
        "declaration synonym": "private constant bad : False\n",
        "interpolated expression": 'def bad := s!"{sorry}"\n',
    }
    passed = True
    with tempfile.TemporaryDirectory(prefix="lean-hygiene-") as directory:
        fixture = Path(directory) / "Fixture.lean"
        fixture.write_text(positive, encoding="utf-8")
        if scan_file(fixture):
            print("FAIL  self-test positive lexical fixture")
            passed = False
        else:
            print("PASS  self-test positive lexical fixture")
        for label, source in negatives.items():
            fixture.write_text(source, encoding="utf-8")
            if scan_file(fixture):
                print(f"PASS  self-test rejects {label}")
            else:
                print(f"FAIL  self-test rejects {label}")
                passed = False
    if passed:
        passed = _compiled_negative_self_test(project_root)
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Lean files to scan")
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--skip-compiled-audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else Path(__file__).resolve().parent.parent
    )
    if args.self_test:
        return run_self_tests(project_root)
    paths = [path.resolve() for path in args.paths] if args.paths else project_sources(project_root)
    if not paths:
        print("FAIL  Lean source audit: no Lean source files found", file=sys.stderr)
        return 2
    lexical_result = lexical_audit(paths)
    if lexical_result != 0 or args.skip_compiled_audit:
        return lexical_result
    return compiled_audit(project_root, paths)


if __name__ == "__main__":
    raise SystemExit(main())
