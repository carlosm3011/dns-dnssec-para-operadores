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

SLIDE_MODULES     := 01-Introduccion 02-Registros 03-Zonas-BIND \
                     04-Firmando-con-BIND-y-KASP 05-Monitoreo-Troubleshooting \
                     06-Arquitectura-Hidden-Signer 07-DNSSEC-Avanzado
SLIDE_TEMPLATE    := _templates/lacnic46.pptx
SLIDE_SCRIPTS_DIR := scripts/slides
SLIDE_OUT_DIR     := _slides

.PHONY: help deps book slides clean release

help:
	@echo "Targets:"
	@echo "  make deps    Install what 'make book' and 'make slides' need:"
	@echo "               Quarto itself (via Homebrew), then TinyTeX (PDF/LaTeX)"
	@echo "               and chrome-headless-shell (Mermaid-to-PDF rendering)"
	@echo "               via 'quarto install', plus python-pptx (pip). macOS"
	@echo "               only; safe to re-run."
	@echo " "
	@echo "  make book    Render the book to PDF. Rebuilds only if a chapter"
	@echo "               .md file, _quarto.yml, or a mermaid hook script"
	@echo "               changed since the last build."
	@echo " "
	@echo "  make slides  Rebuild every module's .pptx from $(SLIDE_TEMPLATE) via"
	@echo "               scripts/slides/build_moduleNN.py, and copy the results"
	@echo "               into $(SLIDE_OUT_DIR)/. Requires python-pptx."
	@echo " "
	@echo "  make release Tag new version using (VERSION) variable. Pushes"
	@echo "               to origin. Current value: $(VERSION)"
	@echo " "
	@echo "  make clean   Remove the _book/ output, the .quarto/ cache, any"
	@echo "               stray .qmd files left by an interrupted render, and"
	@echo "               any stray template/-wip.pptx left by an interrupted"
	@echo "               'make slides'."
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
	@echo "==> Installing python-pptx (builds the slide decks)"
	@# --user keeps this out of Homebrew's own site-packages; --break-system-packages
	@# is required on Homebrew Python (PEP 668) and is safe combined with --user.
	python3 -m pip install --quiet --upgrade --user --break-system-packages python-pptx
	@echo "==> Verifying"
	quarto check

book: $(BOOK_PDF)

$(BOOK_PDF): $(MD_FILES) $(CONFIG) $(SCRIPTS)
	bash scripts/mermaid-pre-render.sh
	quarto render; status=$$?; bash scripts/mermaid-post-render.sh; exit $$status

slides:
	@python3 -c "import pptx" 2>/dev/null || { \
		echo "python-pptx not installed. Run 'make deps' or 'python3 -m pip install python-pptx'."; \
		exit 1; \
	}
	cp $(SLIDE_TEMPLATE) $(SLIDE_SCRIPTS_DIR)/lacnic46.pptx
	@for m in $(SLIDE_MODULES); do \
		num=$${m%%-*}; \
		echo "==> Building $$m.pptx"; \
		(cd $(SLIDE_SCRIPTS_DIR) && python3 build_module$$num.py) || { \
			rm -f $(SLIDE_SCRIPTS_DIR)/lacnic46.pptx; exit 1; \
		}; \
		mv "$(SLIDE_SCRIPTS_DIR)/$$m-wip.pptx" "$(SLIDE_OUT_DIR)/$$m.pptx"; \
	done
	rm -f $(SLIDE_SCRIPTS_DIR)/lacnic46.pptx
	@echo "==> Done: $(SLIDE_OUT_DIR)/*.pptx rebuilt"

release:
	-git commit -a -m "new release $(VERSION)"
	git push
	git tag $(VERSION)
	git push origin $(VERSION)

clean:
	-rm -rf _book .quarto
	-rm -f *.qmd
	-rm -f $(SLIDE_SCRIPTS_DIR)/lacnic46.pptx $(SLIDE_SCRIPTS_DIR)/*-wip.pptx
