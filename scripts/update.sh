#!/usr/bin/env bash

set -euo pipefail

script_path=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/$(basename -- "${BASH_SOURCE[0]}")

run_self_test() {
  local sandbox case_dir fake_bin expected output
  sandbox=$(mktemp -d)
  trap 'rm -rf -- "$sandbox"' RETURN
  fake_bin=$sandbox/bin
  mkdir -p -- "$fake_bin"

  cat >"$fake_bin/curl" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 'leanprover/lean4:v9.9.9'
EOF
  cat >"$fake_bin/lake" <<'EOF'
#!/usr/bin/env bash
set -eu
if [[ ${1-} == update ]]; then
  if [[ ${FAKE_LAKE_MODE-} == fail ]]; then
    printf '%s\n' damaged >lean-toolchain
    printf '%s\n' damaged >lakefile.toml
    printf '%s\n' damaged >lake-manifest.json
    exit 42
  fi
  printf '%s\n' '{"updated":true}' >lake-manifest.json
fi
EOF
  chmod +x "$fake_bin/curl" "$fake_bin/lake"

  make_fixture() {
    case_dir=$1
    mkdir -p -- "$case_dir"
    printf '%s\n' 'leanprover/lean4:v4.1.0' >"$case_dir/lean-toolchain"
    cat >"$case_dir/lakefile.toml" <<'EOF'
name = "Fixture"

[[require]]
  name   =   "mathlib" # preserve this comment
  rev	=	"v4.1.0"   # and this spacing
EOF
    printf '%s\n' '{"original":true}' >"$case_dir/lake-manifest.json"
  }

  case_dir=$sandbox/failure
  make_fixture "$case_dir"
  expected=$sandbox/failure-expected
  cp -a -- "$case_dir" "$expected"
  output=$sandbox/failure.log
  if (cd "$case_dir" && PATH="$fake_bin:$PATH" FAKE_LAKE_MODE=fail \
      bash "$script_path" v9.9.9 >"$output" 2>&1); then
    echo "FAIL  update self-test: fake Lake failure unexpectedly succeeded" >&2
    return 1
  fi
  for file in lean-toolchain lakefile.toml lake-manifest.json; do
    if ! cmp -s -- "$case_dir/$file" "$expected/$file"; then
      echo "FAIL  update self-test: rollback did not restore $file" >&2
      return 1
    fi
  done
  echo "PASS  update self-test: fake Lake failure restored all transaction files"

  case_dir=$sandbox/success
  make_fixture "$case_dir"
  (cd "$case_dir" && PATH="$fake_bin:$PATH" FAKE_LAKE_MODE=success \
    bash "$script_path" v9.9.9 >"$sandbox/success.log" 2>&1)
  cat >"$sandbox/expected-lakefile.toml" <<'EOF'
name = "Fixture"

[[require]]
  name   =   "mathlib" # preserve this comment
  rev	=	"v9.9.9"   # and this spacing
EOF
  if ! cmp -s -- "$case_dir/lakefile.toml" "$sandbox/expected-lakefile.toml"; then
    echo "FAIL  update self-test: Mathlib revision edit changed surrounding bytes" >&2
    return 1
  fi
  if [[ $(<"$case_dir/lean-toolchain") != leanprover/lean4:v9.9.9 ]]; then
    echo "FAIL  update self-test: toolchain was not updated" >&2
    return 1
  fi
  echo "PASS  update self-test: successful edit preserves Mathlib revision whitespace"
}

if [[ ${1-} == --self-test ]]; then
  if [[ $# -ne 1 ]]; then
    echo "usage: $0 --self-test" >&2
    exit 2
  fi
  run_self_test
  exit
fi

if [[ $# -ne 1 || ! $1 =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "usage: $0 <stable-mathlib-tag> (for example: v4.32.2)" >&2
  exit 2
fi

for required_file in lean-toolchain lakefile.toml lake-manifest.json; do
  if [[ ! -f $required_file ]]; then
    echo "error: required transaction file $required_file does not exist" >&2
    exit 1
  fi
done

tag=$1
toolchain_url="https://raw.githubusercontent.com/leanprover-community/mathlib4/${tag}/lean-toolchain"
new_toolchain=$(curl --fail --location --silent --show-error "$toolchain_url")

if [[ ! $new_toolchain =~ ^leanprover/lean4:v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: ${tag} does not expose a stable Lean toolchain" >&2
  exit 1
fi

transaction_files=(lean-toolchain lakefile.toml lake-manifest.json)
backup_dir=$(mktemp -d)
for file in "${transaction_files[@]}"; do
  cp -p -- "$file" "$backup_dir/$file"
done
committed=0

finish_transaction() {
  local status=$?
  trap - EXIT HUP INT TERM
  set +e
  if [[ $committed -eq 0 ]]; then
    for file in "${transaction_files[@]}"; do
      cp -p -- "$backup_dir/$file" "$file" || status=1
    done
    if [[ $status -ne 0 ]]; then
      echo "error: update failed; transaction files were rolled back" >&2
    fi
  fi
  rm -rf -- "$backup_dir"
  exit "$status"
}
trap finish_transaction EXIT
trap 'exit 130' HUP INT TERM

python3 - "$tag" <<'PY'
from pathlib import Path
import re
import sys
import tomllib

tag = sys.argv[1]
path = Path("lakefile.toml")
with path.open("r", encoding="utf-8", newline="") as stream:
    text = stream.read()

try:
    document = tomllib.loads(text)
except tomllib.TOMLDecodeError as error:
    raise SystemExit(f"error: cannot parse {path}: {error}") from error
requirements = document.get("require")
if not isinstance(requirements, list):
    raise SystemExit(f"error: {path} has no [[require]] tables")
if sum(isinstance(item, dict) and item.get("name") == "mathlib" for item in requirements) != 1:
    raise SystemExit(f"error: expected exactly one Mathlib requirement in {path}")

lines = text.splitlines(keepends=True)
header_re = re.compile(r"^[ \t]*\[\[require\]\][ \t]*(?:#[^\r\n]*)?(?:\r?\n)?$")
table_re = re.compile(r"^[ \t]*\[")
assignment = lambda field: re.compile(
    rf'^(?P<prefix>[ \t]*{field}[ \t]*=[ \t]*")'
    rf'(?P<value>[^"\r\n]+)(?P<suffix>"[^\r\n]*(?:\r?\n)?)$'
)
name_re = assignment("name")
rev_re = assignment("rev")
blocks: list[tuple[int, int]] = []
index = 0
while index < len(lines):
    if header_re.fullmatch(lines[index]):
        stop = index + 1
        while stop < len(lines) and not table_re.match(lines[stop]):
            stop += 1
        blocks.append((index, stop))
        index = stop
    else:
        index += 1

mathlib_blocks: list[tuple[int, int]] = []
for start, stop in blocks:
    names = [match.group("value") for line in lines[start:stop] if (match := name_re.fullmatch(line))]
    if names == ["mathlib"]:
        mathlib_blocks.append((start, stop))
if len(mathlib_blocks) != 1:
    raise SystemExit(
        f"error: expected one textual [[require]] block for Mathlib in {path}, "
        f"found {len(mathlib_blocks)}"
    )

start, stop = mathlib_blocks[0]
revision_lines = [
    (line_index, match)
    for line_index in range(start, stop)
    if (match := rev_re.fullmatch(lines[line_index]))
]
if len(revision_lines) != 1:
    raise SystemExit(
        f"error: expected one quoted Mathlib rev assignment in {path}, found {len(revision_lines)}"
    )
line_index, match = revision_lines[0]
line = lines[line_index]
lines[line_index] = line[: match.start("value")] + tag + line[match.end("value") :]
with path.open("w", encoding="utf-8", newline="") as stream:
    stream.write("".join(lines))
PY

printf '%s\n' "$new_toolchain" >lean-toolchain

lake update mathlib
lake exe cache get
lake build

committed=1
