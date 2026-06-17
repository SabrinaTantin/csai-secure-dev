#!/usr/bin/env bash
# Trouve un interpréteur Python >= 3.10 pour créer le venv du cours.
set -euo pipefail

candidates=(
  python3.14 python3.13 python3.12 python3.11 python3.10
  /usr/local/bin/python3.14
  /opt/homebrew/bin/python3.14
  /usr/local/Cellar/python@3.14/*/Frameworks/Python.framework/Versions/3.14/bin/python3.14
  /opt/homebrew/Cellar/python@3.14/*/Frameworks/Python.framework/Versions/3.14/bin/python3.14
  python3
)

for candidate in "${candidates[@]}"; do
  for path in $candidate; do
    if ! command -v "$path" >/dev/null 2>&1 && [ ! -x "$path" ]; then
      continue
    fi
    if "$path" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      echo "$path"
      exit 0
    fi
  done
done

echo "Python 3.10+ introuvable. Installez-le (ex. brew install python@3.14)." >&2
exit 1
