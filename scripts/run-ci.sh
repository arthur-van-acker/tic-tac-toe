#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python}"
SKIP_EDITABLE_INSTALL="${SKIP_EDITABLE_INSTALL:-0}"

echo "Running local CI checks with ${PYTHON_BIN}" >&2

if [[ "${SKIP_EDITABLE_INSTALL}" != "1" ]]; then
  echo "Installing project in editable mode (-e .)" >&2
  "${PYTHON_BIN}" -m pip install -e .
fi

echo "Executing tox lint/type/test matrix" >&2
"${PYTHON_BIN}" -m tox -e lint,type,py313

echo "All local CI checks completed successfully." >&2
