#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv sync --locked

output="$(make i18n 2>&1)" || {
    echo "$output"
    exit 1
}
echo "$output"

if grep -Eiq "Error|Warning" <<< "$output"; then
    echo "make i18n reported an error or warning"
    exit 1
fi

if grep -E "[0-9]+ added, [0-9]+ removed" <<< "$output" |
    grep -qv "0 added, 0 removed$"; then
    echo "Translations are not up to date"
    exit 1
fi
