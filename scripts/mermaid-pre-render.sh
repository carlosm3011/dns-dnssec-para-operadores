#!/usr/bin/env bash
# Run by `make book` before `quarto render` (NOT wired into _quarto.yml's
# pre-render hook: Quarto validates book chapters before running that
# hook, so it can't be used to generate them - see quarto-dev/quarto-cli#11567).
#
# For every source .md file, generate a disposable .qmd twin with
# Obsidian-style ```mermaid fences converted to Quarto's ```{mermaid}
# executable-cell syntax. Quarto requires the .qmd extension for any
# file containing executable cells, so the book's `chapters:` list
# points at these generated .qmd files rather than the .md originals.
# Removed by scripts/mermaid-post-render.sh once rendering finishes.
set -euo pipefail
cd "$(dirname "$0")/.."

for f in *.md; do
  [ "$f" = "CLAUDE.md" ] && continue
  base="${f%.md}"
  perl -pe 's/^```mermaid$/```{mermaid}/' "$f" > "${base}.qmd"
done
