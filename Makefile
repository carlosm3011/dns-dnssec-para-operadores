# Makefile for the DNS y DNSSEC para Operadores Quarto book.
#
# Chapters are authored as plain .md files (Obsidian-compatible). Quarto
# needs .qmd files for the {mermaid} executable cells that make diagrams
# render in PDF output, so this Makefile - not _quarto.yml - drives the
# scripts/mermaid-*.sh scripts that generate/remove disposable .qmd
# twins around the `quarto render` call. (A _quarto.yml pre-render hook
# can't do this: Quarto validates book chapters before pre-render runs,
# see quarto-dev/quarto-cli#11567. Always build via `make book`, not a
# bare `quarto render`.)

MD_FILES := $(filter-out CLAUDE.md,$(wildcard *.md))
CONFIG   := _quarto.yml
SCRIPTS  := scripts/mermaid-pre-render.sh scripts/mermaid-post-render.sh
BOOK_PDF := _book/DNS-y-DNSSEC-para-Operadores.pdf

.PHONY: help book clean

help:
	@echo "Targets:"
	@echo "  make book   Render the book to PDF. Rebuilds only if a chapter"
	@echo "              .md file, _quarto.yml, or a mermaid hook script"
	@echo "              changed since the last build."
	@echo "  make clean  Remove the _book/ output, the .quarto/ cache, and"
	@echo "              any stray .qmd files left by an interrupted render."
	@echo "  make help   Show this message (default target)."

book: $(BOOK_PDF)

$(BOOK_PDF): $(MD_FILES) $(CONFIG) $(SCRIPTS)
	bash scripts/mermaid-pre-render.sh
	quarto render; status=$$?; bash scripts/mermaid-post-render.sh; exit $$status

clean:
	rm -rf _book .quarto
	rm -f *.qmd
