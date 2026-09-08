#!/usr/bin/env bash
# Resolve an interpreter that actually runs Python 3, and put it in $PY.
#
# Source it, do not execute it:
#     . "$(dirname "$0")/../scripts/gm_py.sh"
#     "$PY" gm_bind_check.py --render ...
#
# Why this exists, so it is not rediscovered a fourth time
# -------------------------------------------------------
# The gates are written for `python3`. On Amanda's Windows machine there is no
# `python3`: the real interpreter is `python` (C:\Python314\python.exe), and the
# name `python3` is taken by a Microsoft Store alias stub in
# %LOCALAPPDATA%\Microsoft\WindowsApps that prints an install message and exits
# non-zero. On 2026-09-08 that turned the whole suite red, 87 of 96 tests, with
# every failure reading "Python was not found".
#
# The important part: `command -v python3` SUCCEEDS on that machine. The stub is
# on PATH and it is executable, so looking the name up finds it and every call
# then fails. A name check cannot tell the two apart. The only thing that can is
# running the candidate and seeing whether it answers, which is what this does.
#
# Order is python3 first, so a normal POSIX box is unaffected.

# Does this candidate actually run Python 3?
_gm_py_works() {
  [ -n "${1:-}" ] || return 1
  "$1" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)' \
    >/dev/null 2>&1
}

gm_resolve_python() {
  local cand resolved

  # An explicit PY from the caller wins, but it still has to work.
  if [ -n "${PY:-}" ]; then
    if _gm_py_works "$PY"; then
      return 0
    fi
    echo "gm_py.sh: PY is set to '$PY', which does not run Python 3.8 or newer." >&2
    return 1
  fi

  for cand in python3 python; do
    if _gm_py_works "$cand"; then
      PY="$cand"
      export PY
      return 0
    fi
  done

  # Windows py launcher. Ask it for the interpreter path so $PY stays one word.
  if command -v py >/dev/null 2>&1; then
    resolved="$(py -3 -c 'import sys; print(sys.executable)' 2>/dev/null)"
    if _gm_py_works "$resolved"; then
      PY="$resolved"
      export PY
      return 0
    fi
  fi

  echo "gm_py.sh: no working Python 3.8+ found. Tried: python3, python, py -3." >&2
  echo "          On Windows, 'python3' is usually the Microsoft Store stub and" >&2
  echo "          the real interpreter is 'python'. Set PY to it explicitly:" >&2
  echo "            PY=/c/Python314/python bash filing-system/tests/run-tests.sh" >&2
  return 1
}

gm_resolve_python
