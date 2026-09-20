#!/usr/bin/env bash
# Run by `make book` before `quarto render`. Generates scripts/title-page.tex
# from the tracked scripts/title-page.tex.in template, filling in:
#   - the current version (passed as $1, from the Makefile's VERSION
#     variable), replacing @@VERSION@@
#   - a release-history table built from `git tag`, replacing
#     @@VERSION_HISTORY@@
# so both reflect actual repo state instead of being hand-maintained.
set -euo pipefail
cd "$(dirname "$0")/.."

version="$1"
template="scripts/title-page.tex.in"
output="scripts/title-page.tex"

rows_file="$(mktemp)"
trap 'rm -f "$rows_file"' EXIT
git for-each-ref --sort=-creatordate \
  --format='%(refname:short) & %(creatordate:short) \\' refs/tags > "$rows_file"

sed -e "s/@@VERSION@@/$version/" \
    -e "/@@VERSION_HISTORY@@/r $rows_file" \
    -e "/@@VERSION_HISTORY@@/d" \
    "$template" > "$output"
