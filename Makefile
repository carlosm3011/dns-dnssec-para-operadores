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
VERSION  := "v0.6.2"

.PHONY: help deps book clean release

help:
	@echo "Targets:"
	@echo "  make deps    Install what 'make book' needs: Quarto itself (via"
	@echo "               Homebrew), then TinyTeX (PDF/LaTeX) and"
	@echo "               chrome-headless-shell (Mermaid-to-PDF rendering)"
	@echo "               via 'quarto install'. macOS only; safe to re-run."
	@echo " "
	@echo "  make book    Render the book to PDF. Rebuilds only if a chapter"
	@echo "               .md file, _quarto.yml, or a mermaid hook script"
	@echo "               changed since the last build."
	@echo " "
	@echo "  make release Tag new version using (VERSION) variable. Pushes"
	@echo "               to origin. Current value: $(VERSION)"
	@echo " "
	@echo "  make clean   Remove the _book/ output, the .quarto/ cache, and"
	@echo "               any stray .qmd files left by an interrupted render."
	@echo " "
	@echo "  make help    Show this message (default target)."

deps:
	@command -v brew >/dev/null 2>&1 || { \
		echo "Homebrew not found. Install it from https://brew.sh, then re-run 'make deps'."; \
		exit 1; \
	}
	@echo "==> Installing Quarto (brew cask)"
	brew install --cask quarto
	@echo "==> Installing TinyTeX (LaTeX engine for PDF output)"
	quarto install tinytex --no-prompt
	@echo "==> Installing chrome-headless-shell (renders {mermaid} cells to PDF)"
	quarto install chrome-headless-shell --no-prompt
	@echo "==> Verifying"
	quarto check

book: $(BOOK_PDF)

$(BOOK_PDF): $(MD_FILES) $(CONFIG) $(SCRIPTS)
	bash scripts/mermaid-pre-render.sh
	quarto render; status=$$?; bash scripts/mermaid-post-render.sh; exit $$status

release:
	-git commit -a -m "new release $(VERSION)"
	git push 
	git tag $(VERSION)
	git push origin $(VERSION)

clean:
	-rm -rf _book .quarto
	-rm -f *.qmd
