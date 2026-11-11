#!/usr/bin/env bash
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(dirname "$script_dir")"
venv_bin="$repo_dir/.venv/bin"
tests=false
errors=0

if [[ $# -gt 1 || ( $# -eq 1 && "$1" != '--tests' ) ]]; then
    echo 'Usage: scripts/check.sh [--tests]' >&2
    exit 2
fi
if [[ $# -eq 1 ]]; then
    tests=true
fi
if [[ ! -f "$repo_dir/pyproject.toml" ]]; then
    echo 'Project marker missing' >&2
    exit 1
fi
for tool in python uv ruff mypy; do
    if [[ ! -x "$venv_bin/$tool" ]]; then
        echo "Required tool missing: $tool; run the documented locked setup" >&2
        exit 1
    fi
done
if $tests && [[ ! -x "$venv_bin/pytest" ]]; then
    echo 'Required tool missing: pytest' >&2
    exit 1
fi
cd "$repo_dir" || exit 1

run_check() {
    local label="$1"
    shift
    echo "Checking $label"
    "$@"
    local result=$?
    if [[ $result -ne 0 ]]; then
        echo "$label failed with exit $result" >&2
        errors=$((errors + 1))
    fi
}

# Static checks
run_check format "$venv_bin/ruff" format --check src tests scripts
run_check lint "$venv_bin/ruff" check src tests scripts
run_check types "$venv_bin/mypy"

# Package qualification
run_check build "$venv_bin/uv" build --offline --no-build-isolation

# Explicitly selected test mode
if $tests; then
    run_check tests "$venv_bin/python" -m pytest tests/
    run_check source-tests "$venv_bin/python" scripts/verify_distribution.py \
        --tests
else
    run_check distributions "$venv_bin/python" scripts/verify_distribution.py
    echo 'Tests not selected; static and build checks only'
fi

if [[ $errors -ne 0 ]]; then
    echo "$errors check groups failed" >&2
    exit 1
fi
echo 'All selected check groups passed'
